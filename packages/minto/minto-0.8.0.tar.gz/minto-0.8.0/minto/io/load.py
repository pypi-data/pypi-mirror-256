from __future__ import annotations

import json
import pathlib
from dataclasses import make_dataclass
from typing import TYPE_CHECKING, Literal

import jijmodeling as jm
import numpy as np
import pandas as pd

from minto.consts.default import DEFAULT_RESULT_DIR
from minto.experiment.experiment import Experiment
from minto.table.table import SchemaBasedTable


if TYPE_CHECKING:
    from minto.experiment.experiment import DatabaseSchema


def load(
    experiment_name: str,
    savedir: str | pathlib.Path = DEFAULT_RESULT_DIR,
) -> Experiment:
    """Load and return an artifact, experiment, or table from the given directory.

    Args:
        experiment_name (list[str] | None, optional): List of names of experiments to be loaded, if None, all experiments in `savedir` will be loaded. Defaults to None.
        savedir (str | pathlib.Path, optional): Directory of the experiment. Defaults to DEFAULT_RESULT_DIR.
    Raises:
        FileNotFoundError: If `name_or_dir` is not found in the `savedir` directory.
        ValueError: If `return_type` is not one of "Artifact", "Experiment", or "Table".

    Returns:
        Experiment | Artifact | Table: The loaded artifact, experiment, or table.
    """

    savedir = pathlib.Path(savedir)
    if not (savedir / experiment_name).exists():
        raise FileNotFoundError(f"{(savedir / experiment_name)} is not found.")

    exp = Experiment(experiment_name, savedir=savedir)

    database: DatabaseSchema = getattr(exp, "database")

    base_dir = savedir / experiment_name
    with open(base_dir / "dtypes.json", "r") as f:
        dtypes = json.load(f)

    keys: list[Literal["index", "solver", "parameter", "result"]] = [
        "index",
        "solver",
        "parameter",
        "result",
    ]
    for key in keys:
        if key == "index":
            with open(base_dir / "index.json", "r") as f:
                obj = json.load(f)
                run_ids = range(*obj["run_id_range"])
                index = pd.DataFrame(
                    {
                        "experiment_name": [obj["experiment_name"]] * len(run_ids),
                        "run_id": run_ids,
                    }
                )
            database["index"] = SchemaBasedTable.from_dataframe(index)
        else:
            with open(base_dir / f"{key}" / "info.json", "r") as f:
                obj = json.load(f)
                run_ids = np.repeat(
                    range(*obj["run_id_range"]), len(obj[f"{key}_names"])
                ).tolist()
                names = obj[f"{key}_names"] * obj["run_id_range"][1]
                info = pd.DataFrame(
                    {
                        "experiment_name": [obj["experiment_name"]]
                        * obj[f"{key}_id_range"][1],
                        "run_id": run_ids,
                        f"{key}_name": names,
                        f"{key}_id": range(*obj[f"{key}_id_range"]),
                    }
                )
                if key == "solver":
                    info["source"] = obj["source"] * obj[f"{key}_id_range"][1]
            database[key]["info"] = SchemaBasedTable.from_dataframe(info)

            content = pd.read_csv(base_dir / f"{key}" / "content.csv")

            if key in ("parameter", "result"):
                problems = {}
                for i, file in enumerate(
                    (exp.savedir / exp.name / f"{key}" / "problems").glob("*")
                ):
                    with open(file, "rb") as f:
                        content_id = int(file.name.split(".")[0])
                        problem = jm.from_protobuf(f.read())

                        problems[i] = {f"{key}_id": content_id, "content": problem}
                content = pd.concat([content, pd.DataFrame(problems).T]).reset_index(
                    drop=True
                )

                samplesets = {}
                for i, file in enumerate(
                    (exp.savedir / exp.name / f"{key}" / "samplesets").glob("*")
                ):
                    with open(file, "r") as f:
                        content_id = int(file.name.split(".")[0])
                        sampleset = jm.experimental.SampleSet.from_dict(json.load(f))
                        samplesets[i] = {f"{key}_id": content_id, "content": sampleset}
                content = pd.concat([content, pd.DataFrame(samplesets).T]).reset_index(
                    drop=True
                )

                dc_objs = {}
                for i, file in enumerate(
                    (exp.savedir / exp.name / f"{key}" / "dataclasses").glob("*")
                ):
                    with open(file, "r") as f:
                        content_id = int(file.name.split(".")[0])
                        json_obj = json.load(f)
                        dc_obj = make_dataclass(json_obj["name"], json_obj["type"])(
                            **json_obj["data"]
                        )

                        dc_objs[i] = {f"{key}_id": content_id, "content": dc_obj}
                content = pd.concat([content, pd.DataFrame(dc_objs).T]).reset_index(
                    drop=True
                )

            if content.empty:
                content = pd.DataFrame(columns=dtypes[key]["content"])
            content = content.astype(dtypes[key]["content"])
            content = content[content[f"{key}_id"].isin(info[f"{key}_id"])].sort_values(
                f"{key}_id"
            )
            database[key]["content"] = SchemaBasedTable.from_dataframe(content)
    return exp
