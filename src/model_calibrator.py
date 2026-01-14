import numpy as np

class ModelCalibrator:
    def __init__(self, model_class, param_names, param_ranges, param_steps, score_func, max_iter=100):
        self.model_class = model_class
        self.param_names = param_names
        self.param_ranges = param_ranges
        self.param_steps = param_steps
        self.score_func = score_func
        self.max_iter = max_iter

    def calibrate(self, fixed_params, tune_params_init, *score_args, **score_kwargs):
        best_params = tune_params_init.copy()
        best_score = self.evaluate({**fixed_params, **best_params}, *score_args, **score_kwargs)
        for _ in range(self.max_iter):
            improved = False
            for param in self.param_names:
                for direction in [-1, 1]:
                    candidate = best_params.copy()
                    step = self.param_steps[param]
                    min_val, max_val = self.param_ranges[param]
                    new_val = np.clip(candidate[param] + direction * step, min_val, max_val)
                    candidate[param] = new_val
                    score = self.evaluate({**fixed_params, **candidate}, *score_args, **score_kwargs)
                    if score < best_score:
                        best_score = score
                        best_params = candidate
                        improved = True
            if not improved:
                break
        return best_params, best_score

    def evaluate(self, params, *args, **kwargs):
        model = self.model_class(**params)
        return self.score_func(model, *args, **kwargs)

