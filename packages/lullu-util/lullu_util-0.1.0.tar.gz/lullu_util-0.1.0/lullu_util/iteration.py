from typing import Iterable, Iterator, Any
import os
import inspect
import rich
import typer
from collections import defaultdict


app = typer.Typer()


def job_iterator(
    iterable: Iterable[Any],
    identifier: str = None,
    job_name: str = None,
    dry_run: bool = False,
) -> Iterator[Any]:
    """
    iterable을 순회하면서, identifier를 기준으로 이미 수행한 작업은 건너뛴다.
    identifier가 없는 경우, str(item)을 identifier로 사용한다.
    """
    self_name = job_iterator.__name__

    frame = inspect.currentframe().f_back
    caller_locals = frame.f_locals
    if not job_name:
        for var_name, var_value in caller_locals.items():
            if id(var_value) == id(iterable):
                job_name = var_name

    if not job_name:
        raise ValueError(f"job_name not found in {caller_locals}")

    if dry_run:
        rich.print(
            f"job_iterator({job_name}, identifier={identifier}, dry_run={dry_run})"
        )

    tmp_file_dir = f"/tmp/lullu_util/{self_name}/{job_name}/"
    os.makedirs(tmp_file_dir, exist_ok=True)

    for item in iterable:
        _id = None
        if identifier:
            if hasattr(item, identifier):
                _id = getattr(item, identifier)
            else:
                _id = item.get(identifier)
            if not _id:
                raise ValueError(f"identifier {identifier} not found in {item}")
        else:
            _id = str(item)
            if len(_id) > 100:
                raise ValueError(
                    f"string representation of {job_name} is too long. length: {len(_id)}"
                )

        tmp_file_path = f"{tmp_file_dir}{_id}.txt"
        if os.path.exists(tmp_file_path):
            with open(tmp_file_path, "r") as f:
                status = f.read()
                if status.strip() == "done":
                    continue
                else:
                    rich.print(f"continue processing {job_name} with {_id}")

        with open(tmp_file_path, "w") as f:
            f.write("processing")

        yield item

        with open(tmp_file_path, "w") as f:
            f.write("done")

    return job_name


@app.command()
def list():
    """
    List all job names with the count of their respective .txt files.
    """
    tmp_file_dir = f"/tmp/lullu_util/job_iterator/"
    if os.path.exists(tmp_file_dir):
        job_counts = defaultdict(int)
        for root, dirs, files in os.walk(tmp_file_dir):
            for _dir in dirs:
                job_dir = os.path.join(root, _dir)
                count = len(
                    [file for file in os.listdir(job_dir) if file.endswith(".txt")]
                )
                job_counts[_dir] += count
        for job, count in job_counts.items():
            rich.print(f"- {job}: {count}")
    else:
        rich.print("No jobs found.")


@app.command()
def clear(job_name: str):
    """
    Clear all jobs for a given job name.
    """
    tmp_file_dir = f"/tmp/lullu_util/job_iterator/{job_name}/"
    if os.path.exists(tmp_file_dir):
        for job in os.listdir(tmp_file_dir):
            os.remove(os.path.join(tmp_file_dir, job))
        print(f"Cleared all jobs for {job_name}.")
    else:
        print("No jobs to clear.")


if __name__ == "__main__":
    app()
