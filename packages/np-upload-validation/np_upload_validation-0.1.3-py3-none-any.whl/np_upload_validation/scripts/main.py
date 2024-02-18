import json
import logging
import os
import pathlib

import click
import dotenv
import fabric

from np_upload_validation import checksum, hpc, validation


@click.group()
@click.option("--debug/--no-debug", default=False)
def cli(debug: bool) -> None:
    click.echo(f"Debug mode is {'on' if debug else 'off'}")
    if debug:
        validation.logger.setLevel(logging.DEBUG)
        checksum.logger.setLevel(logging.DEBUG)
        hpc.logger.setLevel(logging.DEBUG)


@cli.command()
@click.argument(
    "session_id",
    type=str,
)
@click.option(
    "--chunk-size",
    type=int,
    default=1000,
)
@click.option(
    "--stdout",
    default=False,
)
@click.option(
    "--output_path",
    type=click.Path(
        exists=False,
        file_okay=True,
        dir_okay=False,
        writable=True,
    ),
    default="validation.json",
)
def validate_npc_session(
    session_id: str,
    stdout: bool,
    chunk_size: int,
    output_path: click.Path,
) -> None:
    result = validation.validate_npc_session(
        session_id,
        chunk_size,
    )
    report = json.dumps(
        [validation_result.model_dump() for validation_result in result],
        indent=4,
        sort_keys=True,
    )

    if stdout:
        click.echo(report)
    else:
        pathlib.Path(str(output_path)).write_text(report)


@cli.command()
@click.argument(
    "session_id",
    type=str,
)
@click.option(
    "--chunk-size",
    type=int,
    default=1000,
)
@click.option(
    "--memsize",
    type=int,
    default=20,
)
def validate_npc_session_hpc(session_id: str, chunk_size: int, memsize: int) -> None:
    dotenv.load_dotenv()
    username = os.environ["HPC_USERNAME"]
    with fabric.Connection(
        os.environ["HPC_HOST"],
        user=username,
        connect_kwargs={
            "password": os.environ["HPC_PASSWORD"],
        },
    ) as con:
        user_dir = f"/home/{username}"
        slurm_id, job_name = hpc.run_hpc_job(
            con,
            hpc.HPCJob(
                email_address=os.environ["HPC_EMAIL_ADDRESS"],
                entry_point=f"python -m np_upload_validation validate validate-npc-session {session_id} --chunk_size={chunk_size} --stdout",
                mem_size=memsize,
            ),
            f"{user_dir}/jobs",
            f"{user_dir}/job-logs",
            hpc.SIFContext(
                sif_loc_str=os.environ["HPC_SIF_PATH"],
                env_vars={
                    "CODE_OCEAN_API_TOKEN": os.environ["CODE_OCEAN_API_TOKEN"],
                    "CODE_OCEAN_DOMAIN": os.environ["CODE_OCEAN_DOMAIN"],
                    "AWS_ACCESS_KEY_ID": os.environ["AWS_ACCESS_KEY_ID"],
                    "AWS_SECRET_ACCESS_KEY": os.environ["AWS_ACCESS_KEY_ID"],
                    "AWS_DEFAULT_REGION": os.environ["AWS_ACCESS_KEY_ID"],
                },
            ),
            "npc_cleanup",
        )
        click.echo(f"Submitted job: {slurm_id} ({job_name})")


@cli.command()
@click.argument(
    "job_name",
    type=str,
)
def get_job_log(job_name: str) -> None:
    dotenv.load_dotenv()
    username = os.environ["HPC_USERNAME"]
    with fabric.Connection(
        os.environ["HPC_HOST"],
        user=username,
        connect_kwargs={
            "password": os.environ["HPC_PASSWORD"],
        },
    ) as con:
        user_dir = f"/home/{username}"
        log_content = hpc.get_remote_content(
            con,
            f"{user_dir}/job-logs/{job_name}.log",
        )
        click.echo(log_content)


# INTERNAL_JOB_LIMIT = 10
# @cli.command()
# @click.option(
#     '--stdout',
#     default=False,
# )
# @click.option(
#     '--output_path',
#     type=click.Path(
#         exists=False,
#         file_okay=True,
#         dir_okay=False,
#         writable=True,
#     ),
#     default="validation.json",
# )
# def validate_npc_session_hpc():
#     dotenv.load_dotenv()


if __name__ == "__main__":
    cli()
