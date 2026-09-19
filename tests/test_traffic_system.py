from traffic_system import CongestionPredictor, SignalOptimizer, TrafficSnapshot


def test_predicts_high_congestion_for_heavy_conditions():
    predictor = CongestionPredictor()
    snapshot = TrafficSnapshot(
        vehicle_count=900,
        avg_speed_kmh=18,
        occupancy=78,
        queue_length_m=180,
        weather_factor=0.8,
        time_of_day='evening_peak',
    )

    result = predictor.predict(snapshot)

    assert result["level"] == "high"
    assert result["score"] >= 75


def test_signal_timing_prioritizes_busiest_direction():
    optimizer = SignalOptimizer()
    demand = {
        "north_south": 0.85,
        "east_west": 0.42,
        "pedestrian": 0.15,
    }

    plan = optimizer.optimize(demand)

    assert plan["north_south"] > plan["east_west"]
    assert sum(plan.values()) == 100
