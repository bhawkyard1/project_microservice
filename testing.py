import requests

test_data = {"name": "foo", "path": "/foo/bar/baz"}
requests.request("POST", "http://localhost:5000/project", json=test_data)

print(requests.request("GET", "http://localhost:5000/project"))