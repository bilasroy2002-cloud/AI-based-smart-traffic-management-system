from app import app


def test_home_page_renders():
    client = app.test_client()
    response = client.get('/')
    assert response.status_code == 200
    assert b'AI Traffic Control Center' in response.data


def test_api_returns_prediction_and_signal_plan():
    client = app.test_client()
    response = client.get('/api/traffic?vehicle_count=900&avg_speed=18&occupancy=78&queue_length=180&weather=0.8&time_of_day=evening_peak')

    assert response.status_code == 200
    payload = response.get_json()
    assert payload['prediction']['level'] in {'low', 'medium', 'high'}
    assert 'north_south' in payload['signal_plan']
    assert 'east_west' in payload['signal_plan']
    assert 'system_status' in payload
    assert 'corridor_load' in payload
