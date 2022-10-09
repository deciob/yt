import sys
import json
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

sprint_phases = ['Need Review', 'Ready To Dev', 'In Dev', 'Code Review', 'Ready To QA', 'In QA', 'Ready To Merge', 'Closed-Fixed', 'Closed-Not Fixed', 'Closed-Obsolete']

def match(r, k):
    return isinstance(r[k], list) and len(r[k]) == 1 and r[k][0]['name']

def filter_sprint_response(r):
    #breakpoint()
    key_added = match(r, 'added')
    key_removed = match(r, 'removed')
    return sprint_phases.count(key_added) > 0 and key_added != key_removed


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
json_object = []

for s in json_response:
    id = (s["id"])
    res = list(filter(filter_sprint_response, sprint_response(id).json()))

    if len(res) > 0:
        json_object.append(res)

print(json.dumps(json_object, indent=4))

with open("sprint.json", "w") as outfile:
    json.dump(json_object, outfile, indent=4)
