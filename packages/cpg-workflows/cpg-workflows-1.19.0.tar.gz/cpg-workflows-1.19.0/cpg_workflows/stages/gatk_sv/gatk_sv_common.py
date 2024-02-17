"""
Common methods for all GATK-SV workflows
"""
import re
from enum import Enum
from functools import lru_cache
from os.path import join
from random import randint
from typing import Any

from analysis_runner.cromwell import (
    CromwellOutputType,
    run_cromwell_workflow_from_repo_and_get_outputs,
)
from cpg_utils import Path, to_path
from cpg_utils.config import ConfigError, get_config
from cpg_utils.hail_batch import Batch, command, image_path, reference_path
from hailtop.batch.job import Job

from cpg_workflows.batch import make_job_name
from cpg_workflows.workflow import Cohort, Dataset

GATK_SV_COMMIT = '6d6100082297898222dfb69fcf941d373d78eede'
SV_CALLERS = ['manta', 'wham', 'scramble']
_FASTA = None
PED_FAMILY_ID_REGEX = re.compile(r'(^[A-Za-z0-9_]+$)')


class CromwellJobSizes(Enum):
    """
    Enum for polling intervals
    """

    SMALL = 'small'
    MEDIUM = 'medium'
    LARGE = 'large'


@lru_cache(maxsize=1)
def create_polling_intervals() -> dict:
    """
    Set polling intervals for cromwell status
    these values are integers, indicating seconds
    for each job size, there is a min and max value
    analysis-runner implements a backoff-retrier when checking for
    success, with a minimum value, gradually reaching a max ceiling

    a config section containing overrides would look like

    [cromwell_polling_intervals.medium]
    min = 69
    max = 420
    """

    # create this dict with default values
    polling_interval_dict = {
        CromwellJobSizes.SMALL: {'min': 30, 'max': 140},
        CromwellJobSizes.MEDIUM: {'min': 40, 'max': 400},
        CromwellJobSizes.LARGE: {'min': 200, 'max': 2000},
    }

    # update if these exist in config
    for job_size in CromwellJobSizes:
        if job_size.value in get_config().get('cromwell_polling_intervals', {}):
            polling_interval_dict[job_size].update(
                get_config()['cromwell_polling_intervals'][job_size.value]
            )
    return polling_interval_dict


def _sv_batch_meta(
    output_path: str,  # pylint: disable=W0613:unused-argument
) -> dict[str, Any]:
    """
    Callable, add meta[type] to custom analysis object
    """
    return {'type': 'gatk-sv-batch-calls'}


def _sv_filtered_meta(
    output_path: str,  # pylint: disable=W0613:unused-argument
) -> dict[str, Any]:
    """
    Callable, add meta[type] to custom analysis object
    """
    return {'type': 'gatk-sv-filtered-calls'}


def _sv_individual_meta(
    output_path: str,  # pylint: disable=W0613:unused-argument
) -> dict[str, Any]:
    """
    Callable, add meta[type] to custom analysis object
    """
    return {'type': 'gatk-sv-sequence-group-calls'}


def get_fasta() -> Path:
    """
    find or return the fasta to use
    """
    global _FASTA
    if _FASTA is None:
        _FASTA = to_path(
            get_config()['workflow'].get('ref_fasta')
            or reference_path('broad/ref_fasta')
        )
    return _FASTA


def get_images(keys: list[str], allow_missing=False) -> dict[str, str]:
    """
    Dict of WDL inputs with docker image paths.

    Args:
        keys (list): all the images to get
        allow_missing (bool): if False, require all query keys to be found

    Returns:
        dict of image keys to image paths
        or AssertionError
    """

    if not allow_missing:
        image_keys = get_config()['images'].keys()
        query_keys = set(keys)
        if not query_keys.issubset(image_keys):
            raise KeyError(f'Unknown image keys: {query_keys - image_keys}')

    return {k: image_path(k) for k in get_config()['images'].keys() if k in keys}


def get_references(keys: list[str | dict[str, str]]) -> dict[str, str | list[str]]:
    """
    Dict of WDL inputs with reference file paths.
    """
    res: dict[str, str | list[str]] = {}
    for key in keys:
        # Keys can be maps (e.g. {'MakeCohortVcf.cytobands': 'cytoband'})
        if isinstance(key, dict):
            key, ref_d_key = list(key.items())[0]
        else:
            ref_d_key = key
        # e.g. GATKSVPipelineBatch.rmsk -> rmsk
        ref_d_key = ref_d_key.split('.')[-1]
        try:
            res[key] = str(reference_path(f'gatk_sv/{ref_d_key}'))
        except KeyError:
            res[key] = str(reference_path(f'broad/{ref_d_key}'))
        except ConfigError:
            res[key] = str(reference_path(f'broad/{ref_d_key}'))

    return res


def add_gatk_sv_jobs(
    batch: Batch,
    dataset: Dataset,
    wfl_name: str,
    # "dict" is invariant (supports updating), "Mapping" is covariant (read-only)
    # we have to support inputs of type dict[str, str], so using Mapping here:
    input_dict: dict[str, Any],
    expected_out_dict: dict[str, Path | list[Path]],
    sequencing_group_id: str | None = None,
    driver_image: str | None = None,
    labels: dict[str, str] | None = None,
    job_size: CromwellJobSizes = CromwellJobSizes.MEDIUM,
) -> list[Job]:
    """
    Generic function to add a job that would run one GATK-SV workflow.
    """

    # create/retrieve dictionary of polling intervals for cromwell status
    polling_intervals = create_polling_intervals()

    # obtain upper and lower polling bounds for this job size
    polling_minimum = randint(
        polling_intervals[job_size]['min'], polling_intervals[job_size]['min'] * 2
    )
    polling_maximum = randint(
        polling_intervals[job_size]['max'], polling_intervals[job_size]['max'] * 2
    )

    # If a config section exists for this workflow, apply overrides
    if override := get_config()['resource_overrides'].get(wfl_name):
        input_dict |= override

    # Where Cromwell writes the output.
    # Will be different from paths in expected_out_dict:
    output_prefix = f'gatk_sv/output/{wfl_name}/{dataset.name}'
    if sequencing_group_id:
        output_prefix = join(output_prefix, sequencing_group_id)

    outputs_to_collect = dict()
    for key, value in expected_out_dict.items():
        if isinstance(value, list):
            outputs_to_collect[key] = CromwellOutputType.array_path(
                name=f'{wfl_name}.{key}', length=len(value)
            )
        else:
            outputs_to_collect[key] = CromwellOutputType.single_path(
                f'{wfl_name}.{key}'
            )

    driver_image = driver_image or image_path('cpg_workflows')

    # pre-process input_dict
    paths_as_strings: dict = {}
    for key, value in input_dict.items():
        if isinstance(value, Path):
            paths_as_strings[f'{wfl_name}.{key}'] = str(value)
        elif isinstance(value, (list, set)):
            paths_as_strings[f'{wfl_name}.{key}'] = [str(v) for v in value]
        else:
            paths_as_strings[f'{wfl_name}.{key}'] = value

    # sometimes we need to pass inputs on to a sub-workflow, rather than the top
    # level. See the config_overrides toml for an example of how to use this
    if 'sub_workflow_overrides' in get_config():
        if sub_wfl_inputs := get_config()['sub_workflow_overrides'].get(wfl_name):
            for sub_wf, sub_section in sub_wfl_inputs.items():
                for key, value in sub_section.items():
                    paths_as_strings[f'{sub_wf}.{key}'] = value

    job_prefix = make_job_name(
        wfl_name, sequencing_group=sequencing_group_id, dataset=dataset.name
    )

    # config toggle decides if outputs are copied out
    copy_outputs = get_config()['workflow'].get('copy_outputs', False)

    submit_j, output_dict = run_cromwell_workflow_from_repo_and_get_outputs(
        b=batch,
        job_prefix=job_prefix,
        dataset=get_config()['workflow']['dataset'],
        repo='gatk-sv',
        commit=GATK_SV_COMMIT,
        cwd='wdl',
        workflow=f'{wfl_name}.wdl',
        libs=['.'],
        output_prefix=output_prefix,
        input_dict=paths_as_strings,
        outputs_to_collect=outputs_to_collect,
        driver_image=driver_image,
        copy_outputs_to_gcp=copy_outputs,
        labels=labels,
        min_watch_poll_interval=polling_minimum,
        max_watch_poll_interval=polling_maximum,
    )

    copy_j = batch.new_job(f'{job_prefix}: copy outputs')
    copy_j.image(driver_image)
    cmds = []
    for key, resource in output_dict.items():
        out_path = expected_out_dict[key]
        if isinstance(resource, list):
            for source, dest in zip(resource, out_path):
                cmds.append(f'gsutil cp "$(cat {source})" "{dest}"')
        else:
            cmds.append(f'gsutil cp "$(cat {resource})" "{out_path}"')
    copy_j.command(command(cmds, setup_gcp=True))
    return [submit_j, copy_j]


def get_ref_panel(keys: list[str] | None = None) -> dict:
    return {
        k: v
        for k, v in {
            'ref_panel_samples': get_config()['sv_ref_panel']['ref_panel_samples'],
            'ref_panel_bincov_matrix': str(
                reference_path('broad/ref_panel_bincov_matrix')
            ),
            'contig_ploidy_model_tar': str(
                reference_path('gatk_sv/contig_ploidy_model_tar')
            ),
            'gcnv_model_tars': [
                str(reference_path('gatk_sv/model_tar_tmpl')).format(shard=i)
                for i in range(get_config()['sv_ref_panel']['model_tar_cnt'])
            ],
            'ref_panel_PE_files': [
                str(reference_path('gatk_sv/ref_panel_PE_file_tmpl')).format(sample=s)
                for s in get_config()['sv_ref_panel']['ref_panel_samples']
            ],
            'ref_panel_SR_files': [
                str(reference_path('gatk_sv/ref_panel_SR_file_tmpl')).format(sample=s)
                for s in get_config()['sv_ref_panel']['ref_panel_samples']
            ],
            'ref_panel_SD_files': [
                str(reference_path('gatk_sv/ref_panel_SD_file_tmpl')).format(sample=s)
                for s in get_config()['sv_ref_panel']['ref_panel_samples']
            ],
        }.items()
        if not keys or k in keys
    }


def clean_ped_family_ids(ped_line: str) -> str:
    """
    Takes each line in the pedigree and cleans it up
    If the family ID already conforms to expectations, no action
    If the family ID fails, replace all non-alphanumeric/non-underscore
    characters with underscores

    >>> clean_ped_family_ids('family1\tchild1\t0\t0\t1\t0\\n')
    'family1\tchild1\t0\t0\t1\t0\\n'
    >>> clean_ped_family_ids('family-1-dirty\tchild1\t0\t0\t1\t0\\n')
    'family-1-dirty\tchild1\t0\t0\t1\t0\\n'

    Args:
        ped_line (str): line from the pedigree file, unsplit

    Returns:
        the same line with a transformed family id
    """

    split_line = ped_line.rstrip().split('\t')

    if re.match(PED_FAMILY_ID_REGEX, split_line[0]):
        return ped_line

    # if the family id is not valid, replace failing characters with underscores
    split_line[0] = re.sub(r'[^A-Za-z0-9_]', '_', split_line[0])

    # return the rebuilt string, with a newline at the end
    return '\t'.join(split_line) + '\n'


def make_combined_ped(cohort: Cohort, prefix: Path) -> Path:
    """
    Create cohort + ref panel PED.
    Concatenating all samples across all datasets with ref panel

    See #578 - there are restrictions on valid characters in PED file
    """
    combined_ped_path = prefix / 'ped_with_ref_panel.ped'
    conf_ped_path = get_references(['ped_file'])['ped_file']
    with combined_ped_path.open('w') as out:
        with cohort.write_ped_file().open() as f:
            # layer of family ID cleaning
            for line in f:
                out.write(clean_ped_family_ids(line))
        # The ref panel PED doesn't have any header, so can safely concatenate:
        with to_path(conf_ped_path).open() as f:
            out.write(f.read())
    return combined_ped_path


def queue_annotate_sv_jobs(
    batch,
    cohort,
    cohort_prefix: Path,
    input_vcf: Path,
    outputs: dict,
    labels: dict[str, str] | None = None,
) -> list[Job] | Job | None:
    """
    Helper function to queue jobs for SV annotation
    Enables common access to the same Annotation WDL for CNV & SV
    """
    input_dict: dict[str, Any] = {
        'vcf': input_vcf,
        'prefix': cohort.name,
        'ped_file': make_combined_ped(cohort, cohort_prefix),
        'sv_per_shard': 5000,
        'population': get_config()['references']['gatk_sv'].get(
            'external_af_population'
        ),
        'ref_prefix': get_config()['references']['gatk_sv'].get(
            'external_af_ref_bed_prefix'
        ),
        'use_hail': False,
    }

    input_dict |= get_references(
        [
            'noncoding_bed',
            'protein_coding_gtf',
            {'ref_bed': 'external_af_ref_bed'},
            {'contig_list': 'primary_contigs_list'},
        ]
    )

    # images!
    input_dict |= get_images(
        [
            'sv_pipeline_docker',
            'sv_base_mini_docker',
            'gatk_docker',
        ]
    )
    jobs = add_gatk_sv_jobs(
        batch=batch,
        dataset=cohort.analysis_dataset,
        wfl_name='AnnotateVcf',
        input_dict=input_dict,
        expected_out_dict=outputs,
        labels=labels,
    )
    return jobs
