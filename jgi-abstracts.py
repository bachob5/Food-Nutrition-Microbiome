#!/usr/bin/env python

# the script needs an ACCESS_TOKEN passed as *first* argument and a series of
# GOLD IDs. Accepted are Project and Study IDs
# Refer to jgi-request-example.sh for information
import requests
from tqdm import tqdm
import sys
from pathlib import Path
import json
from datetime import datetime

ACCESS_TOKEN = sys.argv[1]
GOLD_IDS = [x.strip() for x in sys.argv[2:]]

PROJECT_PREFIX = 'Gp'
PROJECT_Q = "projectGoldId"
STUDY_PREFIX = 'Gs'
STUDY_Q = 'studyGoldId'

JGI_URL = 'https://gold-ws.jgi.doe.gov/api/v1/analysis_projects?{query_type}={query_id}'
HEADERS = {"Authorization": "Bearer {}".format(ACCESS_TOKEN)}

pubmed_ids = {}

for query_id in tqdm(GOLD_IDS):
    if query_id.startswith(PROJECT_PREFIX):
        query_type = PROJECT_Q
    elif query_id.startswith(STUDY_PREFIX):
        query_type = STUDY_Q
    else:
        print("Cannot use this ID:", query_id, file=sys.stderr)
        continue
    req_url = JGI_URL.format(query_type=query_type, query_id=query_id)
    # print(req_url)
    r = requests.get(req_url, headers=HEADERS)
    if not r.ok:
        print(query_id, r.status_code, file=sys.stderr)
        continue
    body = r.json()
    for item in body:
        try:
            publications = item['publications']
        except KeyError:
            print("No publications for:", query_id, file=sys.stderr)
            continue
        for publication in publications:
            # print(query_id, publication)
            try:
                pubmed_ids[query_id].add(publication['pubmedId'])
            except KeyError:
                pubmed_ids[query_ud] = set([publication['pubmedId']])

print("Found", len(pubmed_ids), "studies with associated Pubmed IDs")

# Extract abstracts when available
pubmed_url = 'https://pubmed.ncbi.nlm.nih.gov/{pubmed_id}/?format=pubmed'
pubmed_key = 'pubmed_id'

def extract_abstract(pubmed_entry):
    abstract_lines = []
    start_abstract = False
    for line in pubmed_entry:
        #print(line)
        if line.startswith('AB '):
            start_abstract = True
            abstract_lines.append(line.split('-', 1)[1].strip())
            continue
        if start_abstract and line.startswith(' '):
            abstract_lines.append(line.strip(' '))
            continue
        if start_abstract and (not line.startswith(' ')):
            break
    return abstract_lines

abstracts = {}
for gold_id, abstract_ids in tqdm(pubmed_ids.items()):
    
    for pubmed_id in abstract_ids:
        if pubmed_id in abstracts:
            abstracts[pubmed_id]['gold_ids'].add(gold_id)
            continue
        print(gold_id, pubmed_id)
        pubmed_project_url = pubmed_url.format(pubmed_id=pubmed_id)
        pubmed_entry = requests.get(pubmed_project_url) 
        # the data returned is actually a web page, but with a <pre> tag for the text, so it still works
        abstract_text = extract_abstract(pubmed_entry.text.splitlines())
        abstracts[pubmed_id] = dict(abstract=abstract_text, gold_ids=set([gold_id]))

abstracts_ = {
    pubmed_id: {'abstract': d['abstract'], 'project_ids': list(d['project_ids'])}
    for pubmed_id, d in abstracts.items()
}

with open('abstracts-jgi-{}.json'.format(datetime.now().date()), 'w') as f:
    json.dump(abstracts_, f)
del abstracts_
