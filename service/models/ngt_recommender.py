"""Класс, позволяюший выполнять приближенный поиск соседей для юзера с помощью NGT.
Примечание: все методы в этом классе, кроме fit и _get_similar взяты из класса rectools.UserToItemANNRecommender.
Не стала наследоваться от него, потому что он уже работает с nswlib, и это логически выглядело странно.
"""  # noqa: W505

import itertools
from typing import Any, Hashable, Sequence, Set

import ngtpy
import numpy as np
from rectools import ExternalId, ExternalIds, InternalIds
from rectools.dataset import IdMap


class UserToItemNGTRecommender:
    def __init__(
        self,
        user_vectors: np.ndarray,
        item_vectors: np.ndarray,
        user_id_map: IdMap | dict[str, str],
        item_id_map: IdMap | dict[str, str],
    ):
        self._user_vectors = user_vectors
        self._item_vectors = item_vectors
        if isinstance(item_id_map, dict):
            self._item_id_map = IdMap.from_dict(item_id_map)
        else:
            self._item_id_map = item_id_map
        if isinstance(user_id_map, dict):
            self._user_id_map = IdMap.from_dict(user_id_map)
        else:
            self._user_id_map = user_id_map

        if self._user_vectors.shape[1] != self._item_vectors.shape[1]:
            raise ValueError(
                f"""Vectors shape mismatch:
                                 user vectors dim={self._user_vectors.shape[1]} !=
                                 item vectors dim={self._item_vectors.shape[1]}"""
            )
        ngtpy.create(path="user2item", dimension=len(self._item_vectors[0]), distance_type="Cosine")
        self._index = ngtpy.Index(b"user2item")

    def fit(self) -> None:
        self._index.batch_insert(self._item_vectors, num_threads=24, debug=False)
        self._index.save()

    def _map_to_external_id(self, item_arrays: Sequence[InternalIds]) -> Sequence[ExternalIds]:
        return [self._item_id_map.convert_to_external(item_array) for item_array in item_arrays]

    @staticmethod
    def _truncate_item_list(
        top_n: int,
        item_arrays: Sequence[InternalIds],
        available_items: Sequence[InternalIds] | None = None,
        self_indices: Sequence[InternalIds] | None = None,
    ) -> Sequence[InternalIds]:
        out = []
        if available_items is not None:
            for item_array, available_list in zip(item_arrays, available_items):
                available_set: Set[int] = (
                    set(available_list) if self_indices is None else set(available_list).difference(set(self_indices))
                )
                truncated_item_list = list(itertools.islice((rec for rec in item_array if rec in available_set), top_n))
                out.append(truncated_item_list)
            return out

        for idx, item_array in enumerate(item_arrays):
            set_self_indices = {self_indices[idx]} if self_indices is not None else {}
            truncated_item_list = list(
                itertools.islice((rec for rec in item_array if rec not in set_self_indices), top_n)
            )
            out.append(truncated_item_list)

        return out

    def _get_item_list_from_index(
        self, user_ids: InternalIds, top_n: int, item_ids: Sequence[InternalIds] | None = None
    ) -> Sequence[Sequence[Hashable] | np.ndarray]:
        user_vectors = self._user_vectors[user_ids, :]
        available_items = item_ids
        ids = self._get_similar(query=user_vectors, top_n=top_n)
        return self._map_to_external_id(
            self._truncate_item_list(top_n, item_arrays=ids, available_items=available_items)
        )

    def _get_similar(self, query, top_n: int) -> Sequence[Sequence[int]]:
        result = self._index.search(query, top_n)
        return [[out[0] for out in result]]

    def get_item_list_for_user(
        self, user_id: ExternalId, top_n: int = 10, item_ids: ExternalIds | None = None
    ) -> Sequence[Hashable] | np.ndarray[Any, Any]:
        user_id_ = self._user_id_map.convert_to_internal([user_id])
        item_ids_ = None
        if item_ids is not None:
            item_ids_ = [self._item_id_map.convert_to_internal(item_ids)]
        return self._get_item_list_from_index(user_id_, top_n, item_ids_)[0]
