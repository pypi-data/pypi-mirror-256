import os
from tkinter import N
import py_rocket_launch_live_client as prllc
import py_rocket_launch_live_client.get.pads as pads
from dotenv import load_dotenv
import base64
load_dotenv('py-rocket-launch-live-client/.env')

def test_get_launches():
    encKey = os.getenv('API_KEY')
    assert encKey is not None, 'could not load API_KEY enviornment variable'
    key = base64.b64decode(encKey).decode('utf-8')
    result = prllc.launches.get(key,limit=1)
    #print("\n",result.text)
    assert result.isOk == True,'result is not ok'
def test_get_launches_limit_max_25():
    encKey = os.getenv('API_KEY')
    assert encKey is not None, 'could not load API_KEY enviornment variable'
    key = base64.b64decode(encKey).decode('utf-8')
    result = prllc.launches.get(key,limit=120)
    assert result.isOk == True,'result is not ok'
    data = result.responseData
    assert data['count'] == 25
def test_get_launches_by_company():
    encKey = os.getenv('API_KEY')
    assert encKey is not None, 'could not load API_KEY enviornment variable'
    key = base64.b64decode(encKey).decode('utf-8')
    result = prllc.launches.get(key,provider_id=1)
    assert result.isOk == True,'result is not ok'
    data = result.responseData
    for launch in data['result']:
        assert launch['provider']['id'] == 1
def test_get_launches_by_location():
    encKey = os.getenv('API_KEY')
    assert encKey is not None, 'could not load API_KEY enviornment variable'
    key = base64.b64decode(encKey).decode('utf-8')
    result = prllc.launches.get(key,location_id=61)
    assert result.isOk == True,'result is not ok'
    data = result.responseData
    for launch in data['result']:
        assert launch['pad']['location']['id'] == 61
def test_get_launches_by_pad():
    encKey = os.getenv('API_KEY')
    assert encKey is not None, 'could not load API_KEY enviornment variable'
    key = base64.b64decode(encKey).decode('utf-8')
    result = prllc.launches.get(key,pad_id=2)
    assert result.isOk == True,'result is not ok'
    data = result.responseData
    for launch in data['result']:
        assert launch['pad']['id'] == 2
def test_get_launches_by_tag():
    encKey = os.getenv('API_KEY')
    assert encKey is not None, 'could not load API_KEY enviornment variable'
    key = base64.b64decode(encKey).decode('utf-8')
    result = prllc.launches.get(key,tag_id=105)
    assert result.isOk == True,'result is not ok'
    data = result.responseData
    for launch in data['result']:
        hasTag = False
        for tag in launch['tags']:
            if tag['id'] == 105:
                hasTag = True
                break
        assert hasTag == True
def test_get_launches_by_vehicle():
    encKey = os.getenv('API_KEY')
    assert encKey is not None, 'could not load API_KEY enviornment variable'
    key = base64.b64decode(encKey).decode('utf-8')
    result = prllc.launches.get(key,vehicle_id=1)
    assert result.isOk == True,'result is not ok'
    data = result.responseData
    for launch in data['result']:
        assert launch['vehicle']['id'] == 1
def test_get_launches_by_state():
    encKey = os.getenv('API_KEY')
    assert encKey is not None, 'could not load API_KEY enviornment variable'
    key = base64.b64decode(encKey).decode('utf-8')
    result = prllc.launches.get(key,state_abbr=prllc.us_states.CA)
    assert result.isOk == True,'result is not ok'
    data = result.responseData
    for launch in data['result']:
        assert launch['pad']['location']['state'] == prllc.us_states.CA
def test_get_launches_by_slug():
    encKey = os.getenv('API_KEY')
    assert encKey is not None, 'could not load API_KEY enviornment variable'
    key = base64.b64decode(encKey).decode('utf-8')
    result = prllc.launches.get(key,slug='starlink-6-38')
    assert result.isOk == True,'result is not ok'
    data = result.responseData
    assert len(data['result']) > 0,'no results found for slug'
    for launch in data['result']:
       assert launch['slug'] == 'starlink-6-38'
def test_get_launches_by_date_range():
    encKey = os.getenv('API_KEY')
    assert encKey is not None, 'could not load API_KEY enviornment variable'
    key = base64.b64decode(encKey).decode('utf-8')
    result = prllc.launches.get(key,after_date='2012-12-31',before_date='2014-01-01')
    assert result.isOk == True,'result is not ok'
    data = result.responseData
    assert len(data['result']) > 0
    for launch in data['result']:
        year = int(launch['date_str'][-4:])
        assert year == 2013           
def test_get_launches_by_cospar_id():
    encKey = os.getenv('API_KEY')
    assert encKey is not None, 'could not load API_KEY enviornment variable'
    key = base64.b64decode(encKey).decode('utf-8')
    result = prllc.launches.get(key,cospar_id='2013-001')
    assert result.isOk == True,'result is not ok'
    data = result.responseData
    assert len(data['result']) > 0
    assert len(data['result']) == 1
    assert data['result'][0]['cospar_id'] == '2013-001'
