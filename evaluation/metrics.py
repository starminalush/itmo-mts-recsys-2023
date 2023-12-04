from copy import deepcopy
from time import time
from typing import Any, Iterator, Tuple, TypeAlias

import numpy as np
import pandas as pd
from rectools import Columns
from rectools.dataset import Interactions
from rectools.metrics import MAP, NDCG, MeanInvUserFreq, Precision, Recall, Serendipity, calc_metrics
from rectools.metrics.base import MetricAtK
from rectools.model_selection import Splitter, TimeRangeSplitter

ModelMetrics: TypeAlias = list[dict[str, Any]]
InteractionFold: TypeAlias = Tuple[np.ndarray, np.ndarray, dict[str, Any]]
InteractionFolds: TypeAlias = Iterator[InteractionFold]
_N_SPLITS = 3


def _get_default_metrics(k: int) -> dict[str, MetricAtK]:
    return {
        f"top@{k}_precision": Precision(k=k),
        f"top@{k}_recall": Recall(k=k),
        f"top@{k}_ndcg": NDCG(k=k),
        f"top@{k}_map": MAP(k=k),
        f"top@{k}_serendipity": Serendipity(k=k),
        f"top@{k}_mean_inv_user_freq": MeanInvUserFreq(k=k),
    }


def _get_default_splitter() -> Splitter:
    return TimeRangeSplitter(
        test_size="7D",
        n_splits=_N_SPLITS,
        filter_already_seen=True,
        filter_cold_items=True,
        filter_cold_users=True,
    )


def _split_dataset(splitter: Splitter, interactions: Interactions) -> InteractionFolds:
    return splitter.split(interactions, collect_fold_stats=True)


def _calculate_model_metrics(
    model, metrics: dict[str, MetricAtK], df_train: pd.DataFrame, df_test: pd.DataFrame, k_recos: int
) -> Tuple[dict[str, float], float]:
    start_train_time = time()
    model.fit(df_train)
    train_time = time() - start_train_time
    recos = model.predict(df_test)
    metric_values = calc_metrics(
        metrics,
        reco=recos,
        interactions=df_test,
        prev_interactions=df_train,
        catalog=df_train[Columns.Item].unique(),
    )
    return metric_values, train_time


def calculate_metrics(
    interactions: Interactions,
    metrics: dict[str, MetricAtK] | None,
    model,
    splitter: Splitter | None,
    k_recos: int,
) -> ModelMetrics:
    if not model:
        raise ValueError("Models should not be empty")
    if not interactions:
        raise ValueError("Interactions dataset should not be empty")
    if not metrics or len(metrics) == 0:
        metrics = {metric_name: metric for k in [1, 5, 10] for metric_name, metric in _get_default_metrics(k).items()}

    splitter = _get_default_splitter() if not splitter else splitter
    results = []

    for train_ids, test_ids, fold_info in _split_dataset(splitter=splitter, interactions=interactions):
        df_train = interactions.df.iloc[train_ids]
        df_test = interactions.df.iloc[test_ids][Columns.UserItem]
        metric_values, train_time = _calculate_model_metrics(
            model=deepcopy(model), metrics=metrics, df_train=df_train, df_test=df_test, k_recos=k_recos
        )
        fold_result = {"fold": fold_info["i_split"], "model": str(model), "train time (sec)": train_time}
        fold_result.update(metric_values)
        results.append(fold_result)
    return results
