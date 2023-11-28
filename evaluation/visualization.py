from typing import Any

import pandas as pd
from rectools.dataset import Dataset, Interactions
from rectools.models.base import ModelBase


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


def visualize_training_result(
    model: ModelBase,
    dataset: Dataset,
    user_ids: list[int],
    item_data: dict[str, str],
    k_recos: int,
    interactions: Interactions,
    history_size_per_user: int = 10,
) -> pd.DataFrame:
    df = dataset.interactions.df
    recos = model.recommend(users=user_ids, k=k_recos, dataset=dataset, filter_viewed=True)
    recos["type"] = "reco"
    recos.drop("score", axis=1, inplace=True)
    history = (
        df[df["user_id"].isin(user_ids)]
        .sort_values(["user_id", "datetime"], ascending=[True, False])
        .groupby("user_id")
        .head(history_size_per_user)
    )
    history["rank"] = history.sort_values("datetime").groupby(["user_id"]).datetime.rank().astype("int")
    history["type"] = "history"
    history.drop(["datetime", "weight"], axis=1, inplace=True)

    report = pd.concat([recos, history])
    count_views = interactions.df.groupby("item_id").count()["user_id"]
    report = report.merge(item_data, how="inner", on="item_id")
    count_views.name = "count_views"
    report = report.merge(count_views, how="inner", on="item_id")

    report.sort_values(["user_id", "type"], inplace=True)
    report.set_index(["user_id", "type"], inplace=True)
    report = report.style.set_table_styles([{"selector": "th", "props": [("text-align", "center")]}])
    return report
