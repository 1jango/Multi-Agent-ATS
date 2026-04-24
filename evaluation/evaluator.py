import numpy as np


class ScreenerEvaluator:
    @staticmethod
    def calculate_metrics(ai_scores: list[int], human_scores: list[int]):
        """
        Computes Mean Absolute Error (MAE) and Root Mean Square Error (RMSE).
        MAE: Average distance between AI score and Human score.
        """
        ai = np.array(ai_scores)
        human = np.array(human_scores)

        mae = np.mean(np.abs(ai - human))
        rmse = np.sqrt(np.mean((ai - human) ** 2))

        return {
            "mean_absolute_error": round(float(mae), 2),
            "root_mean_square_error": round(float(rmse), 2),
            "status": "Excellent" if mae < 10 else "Needs Tuning"
        }