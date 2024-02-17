import os
from tkinter import N
import py_rocket_launch_live_client as prllc
import py_rocket_launch_live_client.get.pads as pads
from dotenv import load_dotenv
import base64
load_dotenv('py-rocket-launch-live-client/.env')


def test_get_pads():
    encKey = os.getenv('API_KEY')
    assert encKey is not None, 'could not load API_KEY enviornment variable'
    key = base64.b64decode(encKey).decode('utf-8')
    result = prllc.pads.get(key)
    assert result.isOk == True,'result is not ok'
    
def test_get_pads_by_state():
    encKey = os.getenv('API_KEY')
    assert encKey is not None, 'could not load API_KEY enviornment variable'
    key = base64.b64decode(encKey).decode('utf-8')
    result = prllc.pads.get(key,state=prllc.us_states.CA)
    assert result.isOk == True,'result is not ok'
    data = result.responseData
    for pad in data['result']:
            assert pad['location']['state']['abbr']=='CA','filter by state resturned a pad from another state'
def test_get_pads_by_country():
    encKey = os.getenv('API_KEY')
    assert encKey is not None, 'could not load API_KEY enviornment variable'
    key = base64.b64decode(encKey).decode('utf-8')
    result = prllc.pads.get(key,country=prllc.countries.RU)
    assert result.isOk == True,'result is not ok'
    data = result.responseData
    for pad in data['result']:
       assert pad['location']['country']['code'] == prllc.countries.RU,'filter by country returned a pad from another country'
def test_get_pads_by_id():
    encKey = os.getenv('API_KEY')
    assert encKey is not None, 'could not load API_KEY enviornment variable'
    key = base64.b64decode(encKey).decode('utf-8')
    result = prllc.pads.get(key,id=87)
    assert result.isOk == True,'result is not ok'
    data = result.responseData
    
    assert len(data['result']) != 0,'no id match'
    assert data['result'][0]['id'] == 87,'returned result does not match id'
    assert len(data['result']) == 1,'more than one entry for id match'
def test_get_pads_by_partial_name():
    encKey = os.getenv('API_KEY')
    assert encKey is not None, 'could not load API_KEY enviornment variable'
    key = base64.b64decode(encKey).decode('utf-8')
    result = prllc.pads.get(key,name='osmic g')
    assert result.isOk == True,'result is not ok'
    data = result.responseData
    assert len(data['result']) > 0, 'expected pad was not found by name'
    for pad in data['result']:
        assert 'osmic g'.lower() in pad['name'].lower()