import pandas as pd
import numpy as np
from typing import Optional


class BaseModel:
    def __init__(self):
        self.avg = None

    def fit(self, X: Optional[pd.DataFrame], y: pd.Series):
        self.avg = y.mean()

    def predict(self, X: pd.DataFrame) -> np.ndarray:
        assert self.avg is not None, (
            "Fit the model before predicting values"
        )
        return np.full((len(X),), self.avg)