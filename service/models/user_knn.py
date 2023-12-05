from collections import Counter
from copy import deepcopy

import numpy as np
import pandas as pd
import scipy as sp
from implicit.nearest_neighbours import ItemItemRecommender
from rectools.dataset import Dataset
from rectools.models import PopularModel


class UserKnn:
    def __init__(self, model: ItemItemRecommender, n_users: int = 50):
        self._n_users = n_users
        self._model = model
        self.is_fitted = False
        self._pop_model = PopularModel()

    def get_mappings(self, train: pd.DataFrame) -> None:
        self.users_inv_mapping = dict(enumerate(train["user_id"].unique()))
        self.users_mapping = {v: k for k, v in self.users_inv_mapping.items()}

        self.items_inv_mapping = dict(enumerate(train["item_id"].unique()))
        self.items_mapping = {v: k for k, v in self.items_inv_mapping.items()}

    def __str__(self):
        return f"User KNN with {self._model.__class__.__name__}"

    def get_matrix(
        self,
        df: pd.DataFrame,
        user_col: str = "user_id",
        item_col: str = "item_id",
        weight_col: str = None,
    ):
        if weight_col:
            weights = df[weight_col].astype(np.float32)
        else:
            weights = np.ones(len(df), dtype=np.float32)

        self.interaction_matrix = sp.sparse.coo_matrix(
            (weights, (df[item_col].map(self.items_mapping.get), df[user_col].map(self.users_mapping.get)))
        )

        self.watched = (
            df.groupby(user_col, as_index=False).agg({item_col: list}).rename(columns={user_col: "sim_user_id"})
        )

        return self.interaction_matrix

    def idf(self, n: int, x: float):
        return np.log((1 + n) / (1 + x) + 1)

    def _count_item_idf(self, df: pd.DataFrame):
        item_cnt = Counter(df["item_id"].values)
        item_idf = pd.DataFrame.from_dict(item_cnt, orient="index", columns=["doc_freq"]).reset_index()
        item_idf["idf"] = item_idf["doc_freq"].apply(lambda x: self.idf(self.n, x))
        self.item_idf = item_idf

    def fit(self, train: pd.DataFrame):
        self._user_knn = deepcopy(self._model)
        self.get_mappings(train=train)
        self.weights_matrix = self.get_matrix(df=train)

        self.n = train.shape[0]
        self._count_item_idf(train)

        self._user_knn.fit(self.weights_matrix)
        self._pop_model.fit(Dataset.construct(train))
        self._pop_items = [self.items_inv_mapping[p] for p in self._pop_model.popularity_list[0]]
        self.is_fitted = True

    def _generate_recs_mapper(self, model: ItemItemRecommender, n: int):
        def _recs_mapper(user):
            user_id = self.users_mapping[user]
            users, sim = model.similar_items(user_id, N=n)
            return [self.users_inv_mapping[user] for user in users], sim

        return _recs_mapper

    def _get_popular(self, num_reco: int):
        return self._pop_items[:num_reco]

    def predict(self, test: pd.DataFrame, n_recs: int = 10):
        if not self.is_fitted:
            raise ValueError("Please call fit before predict")

        mapper = self._generate_recs_mapper(model=self._user_knn, n=self._n_users)

        recs = pd.DataFrame({"user_id": test["user_id"].unique()})
        recs["sim_user_id"], recs["sim"] = zip(*recs["user_id"].map(mapper))
        recs = recs.set_index("user_id").apply(pd.Series.explode).reset_index()

        recs = (
            recs[~(recs["user_id"] == recs["sim_user_id"])]
            .merge(self.watched, on=["sim_user_id"], how="left")
            .explode("item_id")
            .sort_values(["user_id", "sim"], ascending=False)
            .drop_duplicates(["user_id", "item_id"], keep="first")
            .merge(self.item_idf, left_on="item_id", right_on="index", how="left")
        )

        recs["score"] = recs["sim"] * recs["idf"]
        recs = recs.sort_values(["user_id", "score"], ascending=False)
        recs["rank"] = recs.groupby("user_id").cumcount() + 1
        return recs[recs["rank"] <= n_recs][["user_id", "item_id", "score", "rank"]]

    def recommend(self, user_id: int, num_reco: int) -> list[int]:
        cold_recs = self._get_popular(num_reco)

        if user_id not in self.users_mapping:
            return cold_recs
        internal_user_id = self.users_mapping[user_id]
        rec_items = []
        for sim_user, sim in zip(*self._user_knn.similar_items(internal_user_id, N=num_reco)):
            if sim_user != internal_user_id:
                original_user_id = self.users_inv_mapping.get(sim_user)
                if items_watched_by_sim_user := self.watched.get(original_user_id):
                    rec_items.extend([(item, sim * self.item_idf[item]) for item in items_watched_by_sim_user])
        rec_items.sort(key=lambda x: x[1], reverse=False)

        recos = [item for item, _ in rec_items][::-1]

        if len(recos) < num_reco:
            return recos + list(set(cold_recs) - set(recos))[: num_reco - len(recos)]
        return recos[:num_reco]
