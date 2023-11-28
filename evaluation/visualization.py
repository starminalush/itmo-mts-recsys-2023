from typing import Any

import pandas as pd


def visualize_metrics(report: dict[str, Any]) -> pd.DataFrame:
    df = pd.DataFrame(report).drop(columns="fold").groupby(["model"], sort=False).agg(["mean"])
    df.columns = df.columns.droplevel(level=1)
    df_report = df.drop(columns=["train time (sec)"])

    df_report.columns = pd.MultiIndex.from_tuples(
        list(df_report.columns.str.extract(r"(top@\d+)_(\w+)", expand=True).itertuples(index=False))
    )
    df_report.columns = df_report.sort_index(axis=1, level=[0, 1], ascending=[True, True]).columns
    df_report["train time (sec)"] = df["train time (sec)"]
    mean_metric_subset = list(df_report.columns)
    df_report = (
        df_report.style.set_table_styles(
            [
                {"selector": "thead th", "props": [("text-align", "center")]},
            ]
        )
        .highlight_min(subset=mean_metric_subset, color="lightcoral", axis=0)
        .highlight_max(subset=mean_metric_subset, color="lightgreen", axis=0)
    )
    return df_report


def visualize_training_result():
    pass
