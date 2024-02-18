from __future__ import annotations

import pandas as pd
import numpy as np
import sys
sys.path.append('..')
from iblm.ibl import IBLModel

from typing import TYPE_CHECKING

class IBLBaggingModel(IBLModel):
    def __init__(
        self,
        model_name: str,
        objective: str,
        # common
        api_type: str = "openai",
        # openai & azure
        api_key: str | None = None,
        max_retries: int = 5,
        timeout: int = 120,
        organization: str | None = None,
        # azure
        api_version: str | None = None,
        azure_endpoint: str | None = None,
        num_model: int = 10,
        top_n: int = 5,
        num_sampling: int = 100
    ) -> None:

        super().__init__(
            model_name,
            objective,
            # common
            api_type,
            # openai & azure
            api_key,
            max_retries,
            timeout,
            organization,
            # azure
            api_version,
            azure_endpoint
            )

        # bagging specific
        self.num_model = num_model
        self.num_sampling = num_sampling
        self.top_n = top_n
        self.bagging_code_model = None
        self.code_models = {}


    def fit(
        self,
        X: pd.DataFrame,
        y: np.array,
        temperature: float = 0,
        seed: int | None = None,
        prompt_template: str | None = None,
        prompt_args: dict | None = None,
        try_code: bool = True,
        ):

        # データのサンプリング
        np.random.seed(0)
        X.reset_index(drop=True, inplace=True)

        index_patterns = []
        for _ in range(self.num_model):
            random_sample_size = np.random.randint(400, 601)
            print(random_sample_size)
            sampled_indices = np.random.choice(X.index, random_sample_size, replace=False)
            index_patterns.append(sampled_indices)


        # モデルの学習
        for i, indices in enumerate(index_patterns, start=1):
            X_sampled = X.loc[indices]
            y_sampled = y[indices]
            key = f"model_{i}"
            self.code_model = super().fit(
                X_sampled,
                y_sampled,
                temperature,
                seed,
                prompt_template,
                prompt_args,
                try_code
                )
            y_pred = super().predict(X_sampled)
            metric_dict = super().evaluate(y_sampled, y_pred)
            self.code_models[key] = {'code_model': self.code_model, "metric_dict": metric_dict}

        return self.code_models

    def predict(self, X: pd.DataFrame) -> np.array:
        # 予測
        y_preds = []
        for key in self.code_models.keys():
            self.code_model = self.code_models[key]['code_model']
            y_pred = super().predict(X)
            y_preds.append(y_pred)
        return np.mean(y_preds, axis=0)


