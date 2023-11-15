import json 
import requests as rq
import pandas as pd
import collections


def GET_Studies():
    res=rq.get("https://www.ebi.ac.uk/metagenomics/api/v1/studies?page_size=1000&lineage=root%3AHost-associated%3AHuman")
    return res

def retrieveData(LINK):
    res=rq.get(LINK)
    res1=res.json()['data']
    return res1

def transformJson2csv(res_json):
    df=pd.json_normalize(res_json)
    return df


#Get all data information
r=GET_Studies()

#Get results in json format
d=r.json()

#Format new links to retrieve all available data
AllData=d['links']
baseLink=AllData['first']
ParsedLink=baseLink.split('&')
NumPages=d['meta']['pagination']['pages']

AllLinks=[]
for n in range(NumPages):
    tmp=ParsedLink[1].split('=')
    tmp.pop()
    tmp.append(str(n+1))
    currPage='='.join(tmp)
    ParsedLink.remove(ParsedLink[1])
    ParsedLink.insert(1, currPage)
    newLink='&'.join(ParsedLink)
    AllLinks.append(newLink)

print (AllLinks)


#Merge all results

res_dfs=[]
for ln in AllLinks:
    res_ln = retrieveData(ln)
    res_df=transformJson2csv(res_ln)
    res_dfs.append(res_df)

res_all=pd.concat(res_dfs, ignore_index=True)
res_all.to_csv('Mgnify_HumanAssociatedBiomes.csv')
