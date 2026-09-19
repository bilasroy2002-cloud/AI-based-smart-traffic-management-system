from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Iterable


@dataclass
class TrafficSnapshot:
    vehicle_count: int
    avg_speed_kmh: float
    occupancy: int
    queue_length_m: float
    weather_factor: float
    time_of_day: str


class CongestionPredictor:
    """Predict congestion intensity from live traffic sensor readings."""

    def predict(self, snapshot: TrafficSnapshot) -> Dict[str, Any]:
        vehicle_score = min(100.0, snapshot.vehicle_count / 12.0)
        speed_score = max(0.0, 100.0 - snapshot.avg_speed_kmh * 2.2)
        occupancy_score = float(snapshot.occupancy)
        queue_score = min(100.0, snapshot.queue_length_m / 2.5)
        weather_score = snapshot.weather_factor * 100.0

        time_bias = {
            "morning_peak": 10,
            "evening_peak": 18,
            "weekend": 8,
            "night": -5,
        }.get(snapshot.time_of_day, 0)

        score = (
            0.30 * vehicle_score
            + 0.25 * speed_score
            + 0.20 * occupancy_score
            + 0.15 * queue_score
            + 0.10 * weather_score
            + time_bias
        )
        score = max(0.0, min(100.0, score))

        if score >= 75:
            level = "high"
            action = "Adaptive signal priority and lane reallocation"
        elif score >= 45:
            level = "medium"
            action = "Monitor queue growth and smooth traffic waves"
        else:
            level = "low"
            action = "Standard cycle timing"

        return {
            "level": level,
            "score": round(score, 1),
            "recommended_action": action,
        }


class SignalOptimizer:
    """Generate signal timing percentages based on directional demand."""

    def optimize(self, demand: Dict[str, float]) -> Dict[str, int]:
        if not demand:
            return {}

        total = sum(demand.values())
        if total <= 0:
            return {key: 0 for key in demand}

        raw_percentages = {key: (value / total) * 100.0 for key, value in demand.items()}
        result = {key: int(value) for key, value in raw_percentages.items()}
        remaining = 100 - sum(result.values())

        ordered_keys = sorted(demand, key=lambda key: demand[key], reverse=True)
        index = 0
        while remaining != 0:
            key = ordered_keys[index % len(ordered_keys)]
            result[key] += 1 if remaining > 0 else -1
            remaining += -1 if remaining > 0 else 1
            index += 1

        return result


class TrafficManager:
    def __init__(self):
        self.predictor = CongestionPredictor()
        self.optimizer = SignalOptimizer()

    def evaluate(self, snapshot: TrafficSnapshot) -> Dict[str, Any]:
        prediction = self.predictor.predict(snapshot)
        return prediction

    def optimize_signal_plan(self, demand: Dict[str, float]) -> Dict[str, int]:
        return self.optimizer.optimize(demand)


if __name__ == "__main__":
    sample = TrafficSnapshot(
        vehicle_count=720,
        avg_speed_kmh=25,
        occupancy=68,
        queue_length_m=140,
        weather_factor=0.65,
        time_of_day="evening_peak",
    )

    manager = TrafficManager()
    print(manager.evaluate(sample))
    print(manager.optimize_signal_plan({"north_south": 0.84, "east_west": 0.46, "pedestrian": 0.18}))
