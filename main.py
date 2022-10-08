import sys
import requests
from urllib import parse

resource = sys.argv[1]
authorisation = 'Bearer %s' % (sys.argv[2])
issues_query = sys.argv[3]

sprint_query = '%s/activities?categories=CustomFieldCategory&fields=timestamp,target(text),added(name),removed(name)'

issues_request = '%s/api/issues?query=%s&fields=id' % (resource, issues_query)

issues_response = requests.get(
    issues_request,
    headers={
        'Authorization': authorisation,
        'Accept': 'application/json',
    }
)

def sprint_response(id):
    q = sprint_query % (id)
    request = '%s/api/issues/%s' % (resource, q)
    return requests.get(
        request,
        headers={
            'Authorization': authorisation,
            'Accept': 'application/json',
        }
    )

json_response = issues_response.json()

for s in json_response:
    id = (s["id"])
    res = sprint_response(id)
    print(res.json())
