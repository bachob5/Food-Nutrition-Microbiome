#!/usr/bin/env python
# coding: utf-8

import sys
from datetime import datetime
from pathlib import Path
from tqdm import tqdm
import itertools
import json
import pandas as pd
import requests
import urllib3

base_url = "https://api.mg-rast.org/1"
# Often the SSL certificate is not working, change if the base_url can be reached without problems
VERIFY_SSL = False

biomes_list = [
    "human-associated habitat", "organism-associated habitat",
    "gut" "feces", "food", 
    #"plant associated", 
    #"plant-associated habitat",
    #"animal-associated habitat", 
]

env_packages = [
    "human-gut", "human-oral", "human-vaginal", "human-skin"
]

# Number of entries to download per *page+ as per API specs
limit = 1000
# Environmental search URL
env_package_url = "{base_url}/search?env_package={env_package}&limit={limit}"
# public_options = 1 # unused

# Keys used in the response body
total_count_key = "total_count"
project_key = "project_id"
# usato per prendere il prossimo set di dati 
next_url_key = "next"
project_url = "{base_url}/project/{project_id}?verbosity=full"
# 
sample_url = "{base_url}/sample/{sample_id}?verbosity=full"
# download metagenome URL
metag_url = "https://api.mg-rast.org/download/"

# pages will be stored in a list for convenience before parsing
pages = []
# get pages for each item in env_packages
for env_package in tqdm(env_packages):
    first_page_url = env_package_url.format(base_url=base_url, env_package=env_package, limit=limit)
    last_request = requests.get(first_page_url, verify=VERIFY_SSL)
    # each response will include the next page URL
    if last_request.ok:
        last_page = last_request.json()
        total_count = last_page[total_count_key]
        pages.append(last_page)
        # loop starts here to get all pags
        while True:
            try:
                next_url = last_page[next_url_key]
            except KeyError:
                print("Finished? Cannot find a new page URL")
                break
            last_request = requests.get(next_url, verify=VERIFY_SSL)
            if last_request.ok:
                last_page = last_request.json()
                pages.append(last_page)
            else:
                # if response is not 2xx breaks because no more pages are available
                break

# Chains data from all pages into one list
all_data = list(itertools.chain(*(page['data'] for page in pages)))
sorted(set(itertools.chain(*(x.keys() for x in all_data))))
sum(1 for x in all_data if x['public'])

# Save all data in a JSON file
with open('all_data.json', 'w') as f:
    json.dump(all_data, f) 

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
for data in tqdm(all_data):
    try:
        pubmed_ids = data[pubmed_key]
    except KeyError:
        continue
    project_id = data[project_key]
    
    for pubmed_id in pubmed_ids.split(', '):
        if pubmed_id in abstracts:
            abstracts[pubmed_id]['project_ids'].add(project_id)
            continue
        print(project_id, pubmed_id)
        pubmed_project_url = pubmed_url.format(pubmed_id=pubmed_id)
        pubmed_entry = requests.get(pubmed_project_url) 
        # the data returned is actually a web page, but with a <pre> tag for the text, so it still works
        abstract_text = extract_abstract(pubmed_entry.text.splitlines())
        abstracts[pubmed_id] = dict(abstract=abstract_text, project_ids=set([project_id]))

abstracts_ = {
    pubmed_id: {'abstract': d['abstract'], 'project_ids': list(d['project_ids'])}
    for pubmed_id, d in abstracts.items()
}
# Abstracts downloaded as JSON
with open('abstracts-mgrast-{}.json'.format(datetime.now().date()), 'w') as f:
    json.dump(abstracts_, f)
del abstracts_

try:
    projects_extra_metadata = json.load(open('project_metadata.json', 'r'))
except IOError:
    projects_extra_metadata = {}
failed_projects = set()

for project_data in tqdm(all_data):
    project_id = project_data[project_key]
    if (project_id in projects_extra_metadata) or (project_id in failed_projects):
        continue
    r = requests.get(project_url.format(base_url=base_url, project_id=project_id), verify=VERIFY_SSL)
    if r.ok:
        projects_extra_metadata[project_id] = r.json()
    else:
        print(project_id, "failed")
        failed_projects.add(project_id)
with open("project_metadata.json", 'w') as f:
    json.dump(projects_extra_metadata, f)

print(len(projects_extra_metadata), failed_projects)

# Makes a DataFrame to save as CSV file
df = pd.DataFrame(all_data)
df['abstract_pubmed'] = df.pubmed_id.map(lambda x: ' '.join(abstracts[x]['abstract']) if x in abstracts else None)
df['description'] = df.project_id.map(lambda x: projects_extra_metadata[x]['description'].replace('\r', ' ').replace('\n', ' ') if x in projects_extra_metadata else None)
df.to_csv('table-mgrast.csv')

continue_with_metagenomes = input("Continue downloading metagenomes metadata? (y/N)")

if continue_with_metagenomes.strip() != 'y':
    sys.exit(0)

# Saves the metagenome files into a project directory (one for each project, really slow)
for project_id in tqdm(df.project_id.unique()):
    metagenome_ids = df[df.project_id == project_id].metagenome_id.to_list()
    #print(project_id, len(metagenome_ids))
    outdir = Path('./' + project_id)
    outdir.mkdir(exist_ok=True)
    for metagenome_id in tqdm(metagenome_ids):
        outfile = outdir.joinpath(f'{metagenome_id}.json')
        if outfile.exists():
            continue
        m_url = metag_url + metagenome_id
        #print(m_url)
        r = requests.get(m_url, verify=VERIFY_SSL).json()
        with outfile.open(mode='w') as f:
            json.dump(r, f)

continue_with_results = input("Continue with downloading metagenome results? (y/N)")

if continue_with_results.strip() != 'y':
    sys.exit(0)

# Download Results for each metagenome (really slow)
start_dir = Path('.')
for path in tqdm(list(start_dir.glob('mgp*'))):
    if not path.is_dir():
        continue
    print(path)
    for fname in tqdm(list(path.glob('mgm*.json'))):
        if 'statistics' in fname.name:
            continue
        info = json.load(fname.open())
        try:
            info['data']
        except KeyError:
            print(fname)
            continue
        for data in info['data']:
            if data['data_type'] == 'statistics':
                url = data['url']
                file_name = path.joinpath(data['file_name'])
                if file_name.exists():
                    continue
                try:
                    r = requests.get(url, verify=verify_ssl)
                except urllib3.response.SocketTimeout as e:
                    print(fname, url, e)
                except requests.exceptions.ChunkedEncodingError as e:
                    print(fname, url, e)
                with file_name.open('wb') as f:
                    f.write(r.content)
        
