import requests
import json

baseurl = 'http://localhost:5000/'

def post(url, payload=None, headers={'Content-Type': 'application/json'}):
    return  requests.post(baseurl + url, headers=headers, data=json.dumps(payload,indent=4)) 

def get(url):
    return requests.get(baseurl + url)

def test_invalid_login():
    resp = get("login")
    assert resp.status_code == 400

def test_server_login():
    resp = get("login?name=feri")
    assert resp.status_code == 200

