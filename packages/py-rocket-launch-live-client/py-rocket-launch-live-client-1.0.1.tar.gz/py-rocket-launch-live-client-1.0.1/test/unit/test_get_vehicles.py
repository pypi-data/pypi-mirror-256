import os
from tkinter import N
import py_rocket_launch_live_client as prllc
import py_rocket_launch_live_client.get.pads as pads
from dotenv import load_dotenv
import base64
load_dotenv('py-rocket-launch-live-client/.env')

def test_get_vehicles():
    encKey = os.getenv('API_KEY')
    assert encKey is not None, 'could not load API_KEY enviornment variable'
    key = base64.b64decode(encKey).decode('utf-8')
    result = prllc.vehicles.get(key)
    assert result.isOk == True,'result is not ok'
def test_get_vehicles_by_id():
    encKey = os.getenv('API_KEY')
    assert encKey is not None, 'could not load API_KEY enviornment variable'
    key = base64.b64decode(encKey).decode('utf-8')
    result = prllc.vehicles.get(key,id=65)
    assert result.isOk == True,'result is not ok'
    data = result.responseData
    assert len(data['result']) != 0,'no id match'
    assert data['result'][0]['id'] == 65,'returned result does not match id'
    assert len(data['result']) == 1,'more than one entry for id match'
def test_get_vehicles_by_partial_name():
    encKey = os.getenv('API_KEY')
    assert encKey is not None, 'could not load API_KEY enviornment variable'
    key = base64.b64decode(encKey).decode('utf-8')
    result = prllc.vehicles.get(key,name='t Test Bo')
    assert result.isOk == True,'result is not ok'
    data = result.responseData
    assert len(data['result']) > 0, 'expected vehicle was not found by name'
    for vehicle in data['result']:
        assert 't Test Bo'.lower() in vehicle['name'].lower()
