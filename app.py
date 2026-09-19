from __future__ import annotations

from flask import Flask, jsonify, render_template_string, request

from traffic_system import TrafficManager, TrafficSnapshot

app = Flask(__name__)
manager = TrafficManager()

HTML_TEMPLATE = """
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>AI Traffic Control Center</title>
    <style>
        :root {
            --bg: #07111f;
            --bg-soft: #0f172a;
            --panel: rgba(15, 23, 42, 0.8);
            --text: #e2e8f0;
            --muted: #94a3b8;
            --green: #22c55e;
            --blue: #3b82f6;
            --amber: #f59e0b;
            --red: #ef4444;
            --line: #334155;
        }
        * { box-sizing: border-box; }
        body {
            margin: 0;
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, var(--bg), #172554);
            color: var(--text);
        }
        .container {
            max-width: 1200px;
            margin: 30px auto;
            padding: 20px;
        }
        .hero {
            display: flex; justify-content: space-between; align-items: center;
            margin-bottom: 24px; background: rgba(15, 23, 42, 0.75);
            border: 1px solid var(--line); border-radius: 16px; padding: 22px 24px;
        }
        .hero h1 { margin: 0 0 8px; font-size: 36px; }
        .hero p { margin: 0; color: var(--muted); }
        .badge {
            background: linear-gradient(135deg, var(--green), var(--blue));
            color: white; font-weight: bold; padding: 10px 16px; border-radius: 999px;
        }
        .grid {
            display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 18px;
        }
        .panel {
            background: var(--panel); border: 1px solid var(--line); border-radius: 16px;
            padding: 18px; box-shadow: 0 10px 28px rgba(0,0,0,0.2);
        }
        .metric-label { color: var(--muted); font-size: 13px; text-transform: uppercase; }
        .metric-value {
            display: block; margin-top: 12px; font-size: 30px; font-weight: bold;
        }
        .row { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 14px; }
        form { display: grid; gap: 16px; margin-top: 10px; }
        label {
            display: flex; flex-direction: column; gap: 6px; font-size: 13px; color: var(--muted);
        }
        input, select, button {
            width: 100%; padding: 11px 12px; border-radius: 10px; border: 1px solid var(--line);
            background: #0b1220; color: var(--text); font-size: 14px;
        }
        button {
            background: linear-gradient(90deg, var(--green), var(--blue)); border: none; cursor: pointer;
            font-weight: bold; transition: transform 0.18s ease;
        }
        button:hover { transform: translateY(-1px); }
        .result-box {
            display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 18px;
            margin-top: 20px;
        }
        .signal-bar {
            display: flex; height: 20px; border-radius: 999px; overflow: hidden; margin-top: 14px;
        }
        .bar-north { background: var(--green); }
        .bar-east { background: var(--blue); }
        .bar-ped { background: var(--amber); }
        .chart {
            margin-top: 20px; display: grid; grid-template-columns: repeat(5, 1fr); align-items: end; gap: 10px; height: 120px;
        }
        .bar {
            background: linear-gradient(180deg, #3b82f6, #22c55e); border-radius: 8px 8px 0 0;
            min-height: 12px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="hero">
            <div>
                <h1>AI Traffic Control Center</h1>
                <p>Adaptive traffic signal optimization and congestion forecasting for smart cities</p>
            </div>
            <div class="badge" id="status-badge">SYSTEM ONLINE</div>
        </div>

        <div class="grid">
            <div class="panel">
                <div class="metric-label">Congestion Level</div>
                <span class="metric-value" id="level">--</span>
            </div>
            <div class="panel">
                <div class="metric-label">Risk Score</div>
                <span class="metric-value" id="score">--</span>
            </div>
            <div class="panel">
                <div class="metric-label">Corridor Load</div>
                <span class="metric-value" id="corridor">--</span>
            </div>
            <div class="panel">
                <div class="metric-label">System Status</div>
                <span class="metric-value" id="system-status">--</span>
            </div>
        </div>

        <div class="panel" style="margin-top: 24px;">
            <h2>Traffic Inputs</h2>
            <form id="traffic-form">
                <div class="row">
                    <label>Vehicle count <input name="vehicle_count" type="number" value="900"></label>
                    <label>Average speed (km/h) <input name="avg_speed" type="number" step="0.1" value="18"></label>
                    <label>Occupancy (%) <input name="occupancy" type="number" value="78"></label>
                </div>
                <div class="row">
                    <label>Queue length (m) <input name="queue_length" type="number" step="0.1" value="180"></label>
                    <label>Weather factor <input name="weather" type="number" step="0.1" value="0.8"></label>
                    <label>Time of day
                        <select name="time_of_day">
                            <option value="morning_peak">Morning peak</option>
                            <option value="evening_peak" selected>Evening peak</option>
                            <option value="weekend">Weekend</option>
                            <option value="night">Night</option>
                        </select>
                    </label>
                </div>
                <button type="submit">Analyze traffic</button>
            </form>
        </div>

        <div class="result-box">
            <div class="panel">
                <h2>Recommended Action</h2>
                <p id="action">--</p>
                <div class="chart">
                    <div class="bar" style="height: 65%"></div>
                    <div class="bar" style="height: 80%"></div>
                    <div class="bar" style="height: 92%"></div>
                    <div class="bar" style="height: 76%"></div>
                    <div class="bar" style="height: 88%"></div>
                </div>
            </div>

            <div class="panel">
                <h2>Signal Plan</h2>
                <div id="signal-plan">
                    <div>North-South: --%</div>
                    <div>East-West: --%</div>
                    <div>Pedestrian: --%</div>
                </div>
                <div class="signal-bar">
                    <div class="bar-north" id="bar-north" style="width: 0%"></div>
                    <div class="bar-east" id="bar-east" style="width: 0%"></div>
                    <div class="bar-ped" id="bar-ped" style="width: 0%"></div>
                </div>
            </div>
        </div>
    </div>

    <script>
        const form = document.getElementById('traffic-form');
        const setInfo = (payload) => {
            document.getElementById('level').textContent = payload.prediction.level.toUpperCase();
            document.getElementById('score').textContent = payload.prediction.score + '/100';
            document.getElementById('corridor').textContent = payload.corridor_load + '%';
            document.getElementById('system-status').textContent = payload.system_status;
            document.getElementById('action').textContent = payload.prediction.recommended_action;
            document.getElementById('status-badge').textContent = payload.system_status.toUpperCase();

            const plan = payload.signal_plan;
            document.getElementById('signal-plan').innerHTML = `
                <div>North-South: ${plan.north_south}%</div>
                <div>East-West: ${plan.east_west}%</div>
                <div>Pedestrian: ${plan.pedestrian}%</div>
            `;

            document.getElementById('bar-north').style.width = plan.north_south + '%';
            document.getElementById('bar-east').style.width = plan.east_west + '%';
            document.getElementById('bar-ped').style.width = plan.pedestrian + '%';
        };

        const updateFromForm = async (event) => {
            event.preventDefault();
            const formData = new FormData(form);
            const params = new URLSearchParams(formData);
            const response = await fetch('/api/traffic?' + params.toString());
            const payload = await response.json();
            setInfo(payload);
        };

        form.addEventListener('submit', updateFromForm);
        updateFromForm({ preventDefault: () => {} });
    </script>
</body>
</html>
"""


@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)


@app.route('/api/traffic')
def traffic_api():
    snapshot = TrafficSnapshot(
        vehicle_count=int(request.args.get('vehicle_count', 900)),
        avg_speed_kmh=float(request.args.get('avg_speed', 18.0)),
        occupancy=int(request.args.get('occupancy', 78)),
        queue_length_m=float(request.args.get('queue_length', 180.0)),
        weather_factor=float(request.args.get('weather', 0.8)),
        time_of_day=request.args.get('time_of_day', 'evening_peak'),
    )

    prediction = manager.evaluate(snapshot)
    signal_plan = manager.optimize_signal_plan(
        {
            'north_south': 0.85,
            'east_west': 0.42,
            'pedestrian': 0.15,
        }
    )

    corridor_load = min(100, int(round((snapshot.vehicle_count / 1200) * 100 + snapshot.occupancy * 0.25)))
    if prediction['level'] == 'high':
        system_status = 'critical'
    elif prediction['level'] == 'medium':
        system_status = 'active'
    else:
        system_status = 'stable'

    return jsonify(
        {
            'prediction': prediction,
            'signal_plan': signal_plan,
            'system_status': system_status,
            'corridor_load': corridor_load,
        }
    )


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
