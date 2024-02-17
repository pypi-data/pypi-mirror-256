import os
import py_rocket_launch_live_client as prllc
import py_rocket_launch_live_client.get.pads as pads
from dotenv import load_dotenv
import base64
load_dotenv('py-rocket-launch-live-client/.env')

def test_get_companies():
    encKey = os.getenv('API_KEY')
    assert encKey is not None, 'could not load API_KEY enviornment variable'
    key = base64.b64decode(encKey).decode('utf-8')
    result = prllc.companies.get(key)
    assert result.isOk == True,'result is not ok'

def test_get_companies_by_country():
    encKey = os.getenv('API_KEY')
    assert encKey is not None, 'could not load API_KEY enviornment variable'
    key = base64.b64decode(encKey).decode('utf-8')
    result = prllc.companies.get(key,country=prllc.countries.RU)
    assert result.isOk == True,'result is not ok'
    data = result.responseData
    for company in data['result']:
       assert company['country']['code'] == prllc.countries.RU,'filter by country returned a company from another country'
def test_get_companies_by_id():
    encKey = os.getenv('API_KEY')
    assert encKey is not None, 'could not load API_KEY enviornment variable'
    key = base64.b64decode(encKey).decode('utf-8')
    result = prllc.companies.get(key,id=91)
    assert result.isOk == True,'result is not ok'
    data = result.responseData
    assert len(data['result']) != 0,'no id match'
    assert data['result'][0]['id'] == 91,'returned result does not match id'
    assert len(data['result']) == 1,'more than one entry for id match'
def test_get_companies_by_partial_name():
    encKey = os.getenv('API_KEY')
    assert encKey is not None, 'could not load API_KEY enviornment variable'
    key = base64.b64decode(encKey).decode('utf-8')
    result = prllc.companies.get(key,name='BL Sp')
    assert result.isOk == True,'result is not ok'
    data = result.responseData
    assert len(data['result']) > 0, 'expected company was not found by name'
    for company in data['result']:
        assert 'BL Sp'.lower() in company['name'].lower()
def test_get_inactive_companies():
    encKey = os.getenv('API_KEY')
    assert encKey is not None, 'could not load API_KEY enviornment variable'
    key = base64.b64decode(encKey).decode('utf-8')
    result = prllc.companies.get(key,inactive=prllc.Truth.YES)
    assert result.isOk == True,'result is not ok'
    data = result.responseData
    assert len(data['result']) > 0, 'no inactive companies found'
    for company in data['result']:
        assert company['inactive'] == prllc.Truth.YES.value
def test_get_active_companies():
    encKey = os.getenv('API_KEY')
    assert encKey is not None, 'could not load API_KEY enviornment variable'
    key = base64.b64decode(encKey).decode('utf-8')
    result = prllc.companies.get(key,inactive=prllc.Truth.NO)
    assert result.isOk == True,'result is not ok'
    data = result.responseData
    assert len(data['result']) > 0, 'no active companies found'
    for company in data['result']:
        assert company['inactive'] == prllc.Truth.NO.value
    