from __future__ import annotations

import inspect
import pathlib
import types
import uuid
from typing import Any, Callable, Literal, Optional, TypedDict

import jijmodeling as jm
import pandas as pd
from jijzept.response import JijModelingResponse
from pandas import DataFrame

from minto.consts.default import DEFAULT_RESULT_DIR
from minto.records.records import (
    Index,
    ParameterContent,
    ParameterInfo,
    ResultContent,
    ResultInfo,
    SolverContent,
    SolverInfo,
)
from minto.records.sampleset_expansion import expand_sampleset
from minto.table.table import SchemaBasedTable


class DatabaseComponentSchema(TypedDict):
    info: SchemaBasedTable
    content: SchemaBasedTable


class DatabaseSchema(TypedDict):
    index: SchemaBasedTable
    solver: DatabaseComponentSchema
    parameter: DatabaseComponentSchema
    result: DatabaseComponentSchema


class Experiment:
    def __init__(
        self,
        name: Optional[str] = None,
        savedir: str | pathlib.Path = DEFAULT_RESULT_DIR,
    ):
        self.name = name or str(uuid.uuid4())
        self.savedir = pathlib.Path(savedir)

        database: DatabaseSchema = {
            "index": SchemaBasedTable(Index.dtypes),
            "solver": {
                "info": SchemaBasedTable(SolverInfo.dtypes),
                "content": SchemaBasedTable(SolverContent.dtypes),
            },
            "parameter": {
                "info": SchemaBasedTable(ParameterInfo.dtypes),
                "content": SchemaBasedTable(ParameterContent.dtypes),
            },
            "result": {
                "info": SchemaBasedTable(ResultInfo.dtypes),
                "content": SchemaBasedTable(ResultContent.dtypes),
            },
        }
        object.__setattr__(self, "database", database)

    def __enter__(self) -> Experiment:
        """Set up Experiment.
        Automatically makes a directory for saving the experiment, if it doesn't exist.
        """
        _mkdir(self)

        return self

    def __exit__(self, exception_type, exception_value, traceback) -> None:
        """Saves the experiment if autosave is True."""
        pass

    def run(self) -> Experiment:
        """Run the experiment."""
        database: DatabaseSchema = getattr(self, "database")

        if database["index"].empty():
            run_id = 0
        else:
            run_id = database["index"][-1].series()["run_id"] + 1
        database["index"].insert(
            Index(
                experiment_name=self.name,
                run_id=run_id,
                # TODO: New attribute will be added.
                # date=datetime.datetime.now()
            )
        )
        return self

    def table(
        self,
        key: Literal["solver", "parameter", "result"] | None = None,
        enable_sampleset_expansion: bool = True,
    ) -> pd.DataFrame:
        """Merge the experiment table and return it as a DataFrame.

        Returns:
            pd.DataFrame: The merged table.
        """
        database: DatabaseSchema = getattr(self, "database")

        solver_df = _get_component_dataframe(self, "solver")
        if key == "solver":
            return solver_df
        parameter_df = _get_component_dataframe(self, "parameter")
        if key == "parameter":
            return parameter_df
        result_df = _get_component_dataframe(self, "result")
        if key == "result":
            return result_df

        df = database["index"].dataframe()
        # Merge solver
        if not solver_df.empty:
            df = df.merge(
                _pivot(solver_df, columns="solver_name", values="source"),
                on=["experiment_name", "run_id"],
                how="outer",
            )

        # Merge parameter
        if not parameter_df.empty:
            df = df.merge(
                _pivot(parameter_df, columns="parameter_name", values="content"),
                on=["experiment_name", "run_id"],
                how="outer",
            )

        # Merge result
        if not result_df.empty:
            df = df.merge(
                _pivot(result_df, columns="result_name", values="content"),
                on=["experiment_name", "run_id"],
                how="outer",
            )

        # Expand sampleset
        if enable_sampleset_expansion:
            sampleset_df = expand_sampleset(database["result"]["content"].dataframe())
            if not sampleset_df.empty:
                sampleset_df = pd.merge(
                    database["result"]["info"].dataframe()[
                        ["experiment_name", "run_id", "result_id"]
                    ],
                    sampleset_df,
                    on="result_id",
                    how="inner",
                ).drop(columns="result_id")

                result_names = [
                    name
                    for name in result_df["result_name"].unique()
                    if isinstance(
                        result_df[result_df["result_name"] == name]["content"].iloc[0],
                        (jm.experimental.SampleSet, jm.SampleSet, JijModelingResponse),
                    )
                ]

                df = df.merge(sampleset_df, on=["experiment_name", "run_id"]).drop(
                    columns=result_names
                )
        return df

    def log_solver(self, name: str, solver: Callable[..., Any]) -> None:
        database: DatabaseSchema = getattr(self, "database")

        run_id = int(database["index"][-1].series()["run_id"])
        solver_id = len(database["solver"]["info"])

        if isinstance(solver, types.FunctionType):
            source = inspect.getfile(solver)
        else:
            if _is_running_in_notebook():
                source = "Dynamically generated in Jupyter Notebook"
            else:
                if isinstance(solver, types.MethodType):
                    source = inspect.getfile(solver)
                else:
                    source = inspect.getfile(solver.__class__)

        info = SolverInfo(
            experiment_name=self.name,
            run_id=run_id,
            solver_name=name,
            source=source,
            solver_id=solver_id,
        )
        content = SolverContent(solver_id=solver_id, content=solver)

        database["solver"]["info"].insert(info)
        database["solver"]["content"].insert(content)

    def log_solvers(self, solvers: dict[str, Callable[..., Any]]) -> None:
        for name, solver in solvers.items():
            self.log_solver(name, solver)

    def log_parameter(self, name: str, parameter: Any) -> None:
        """Log a parameter to the experiment.

        Args:
            parameter (Parameter): The parameter to be logged.
        """
        database: DatabaseSchema = getattr(self, "database")

        run_id = int(database["index"][-1].series()["run_id"])
        parameter_id = len(database["parameter"]["info"])

        info = ParameterInfo(
            experiment_name=self.name,
            run_id=run_id,
            parameter_name=name,
            parameter_id=parameter_id,
        )
        content = ParameterContent(parameter_id=parameter_id, content=parameter)

        database["parameter"]["info"].insert(info)
        database["parameter"]["content"].insert(content)

    def log_parameters(self, parameters: dict[str, Any]) -> None:
        for name, parameter in parameters.items():
            self.log_parameter(name, parameter)

    def log_result(self, name: str, result: Any) -> None:
        database: DatabaseSchema = getattr(self, "database")

        run_id = int(database["index"][-1].series()["run_id"])
        result_id = len(database["result"]["info"])

        info = ResultInfo(
            experiment_name=self.name,
            run_id=run_id,
            result_name=name,
            result_id=result_id,
        )
        content = ResultContent(result_id=result_id, content=result)

        database["result"]["info"].insert(info)
        database["result"]["content"].insert(content)

    def log_results(self, results: dict[str, Any]) -> None:
        for name, result in results.items():
            self.log_result(name, result)

    def save(self) -> None:
        """Save the experiment to a file."""
        from minto.io.save import save

        save(self)


def _mkdir(experiment: Experiment) -> None:
    for key in ["solver", "parameter", "result"]:
        d = experiment.savedir / experiment.name / key
        d.mkdir(parents=True, exist_ok=True)

        if key in ["parameter", "result"]:
            problem_dir = d / "problems"
            problem_dir.mkdir(parents=True, exist_ok=True)

            sampleset_dir = d / "samplesets"
            sampleset_dir.mkdir(parents=True, exist_ok=True)

            dataclass_dir = d / "dataclasses"
            dataclass_dir.mkdir(parents=True, exist_ok=True)


def _get_component_dataframe(
    experiment: Experiment, key: Literal["solver", "parameter", "result"]
) -> DataFrame:
    database: DatabaseSchema = getattr(experiment, "database")

    return pd.merge(
        database[key]["info"].dataframe(),
        database[key]["content"].dataframe(),
        on=f"{key}_id",
    )


def _pivot(df: DataFrame, columns: str | list[str], values: str) -> DataFrame:
    return df.pivot_table(
        index=["experiment_name", "run_id"],
        columns=columns,
        values=values,
        aggfunc=lambda x: x,
        dropna=False,
    ).reset_index()


def _is_running_in_notebook():
    try:
        ipython = get_ipython()
        # Jupyter Notebook or JupyterLab
        if "IPKernelApp" in ipython.config:
            return True
    except NameError:
        return False
