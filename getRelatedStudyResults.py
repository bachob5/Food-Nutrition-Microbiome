import sys
import requests as rq
import pandas as pd

''' This scrpt should be fixed to account for empty columns resulting in API error while retrieving the results from Mgnify'''

InFile=sys.argv[1]

def get_StudyId_Links(InFile):
    D_studyID_linkResults={}
    D_studyID_linkSamples={}
    D_studyID_linkPubblications={}
    D_studyID_linkAnalyses={}
    df=pd.read_csv(InFile)
    for ix, nm in enumerate(df['id']):
        D_studyID_linkResults[nm]=df['relationships.downloads.links.related'][ix]
        D_studyID_linkSamples[nm]=df['relationships.samples.links.related'][ix]
        D_studyID_linkPubblications[nm]=df['relationships.publications.links.related'][ix]
        D_studyID_linkAnalyses[nm]=df['relationships.analyses.links.related'][ix]
    return D_studyID_linkResults, D_studyID_linkSamples, D_studyID_linkPubblications, D_studyID_linkAnalyses

StudyID_links=get_StudyId_Links(InFile)
Ress=StudyID_links[0]
Samp=StudyID_links[1]
Pubb=StudyID_links[2]
Analyses=StudyID_links[3]


def GET_Analysis(Link2Analysis):
    res=rq.get(Link2Analysis)
    return res

def retrieveData(LINK):
    res=rq.get(LINK)
    res1=res.json()['data']
    return res1

def transformJson2csv(res_json):
    df=pd.json_normalize(res_json)
    return df


#Get analysis data information

for sID in Ress:
    Link2Results=Ress[sID]
    #print (sID, Link2Results, type(Link2Results))
    if str(Link2Results).startswith('https:'): #This checks whether it is a web link
        r=GET_Analysis(Link2Results)
        #Get results in json format
        d=r.json()
        AllData=d['links']
        #print (AllData)
        baseLink=AllData['first']
        ParsedLink=baseLink.split('&')
        #print (ParsedLink)
        NumPages=d['meta']['pagination']['pages']
        #print(NumPages)      
        AllLinks=[]
        if NumPages==1:
            AllLinks.append(ParsedLink[0])
        elif NumPages > 1:
            for n in range(NumPages):
                tmp=ParsedLink[1].split('=')
                tmp.pop()
                tmp.append(str(n+1))
                currPage='='.join(tmp)
                ParsedLink.remove(ParsedLink[1])
                ParsedLink.insert(1, currPage)
                newLink='&'.join(ParsedLink)
                AllLinks.append(newLink)
        #print (sID, AllLinks)
        f_out=sID+'_RelatedResults.csv'
        res_dfs=[]
        for ln in AllLinks:
            res_ln = retrieveData(ln)
            res_df=transformJson2csv(res_ln)
            res_dfs.append(res_df)
            res_all=pd.concat(res_dfs, ignore_index=True)
            res_all.to_csv(f_out)
