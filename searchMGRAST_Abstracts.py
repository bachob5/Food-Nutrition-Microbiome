import sys

TermsOfInterest=[['diet','intervention'],['diet', 'observation'], ['obesity', 'diet'], ['nutrient', 'autism'], ['probiotics','gut'], ['diet', 'gut'], ['gut', 'prebiotic']]

f_in=sys.argv[1]
f_out=f_in.split('.')[0]+'_DietSelectedStudies.csv'


def searchTerm(t, TermsOfInterest):
    i=0
    for p in TermsOfInterest:
        p1=p[0]
        p2=p[1]
        if p1 and p2 in t:
            i+=1
    if i > 0:
        return True
    else:
        return False
    

def getRelevantStudies(fin, TermsOfInterest):
    L=[]
    D_MixsCompliant={}
    f=open(fin, 'r')
    firstLine_temp=f.readline()
    firstLine=firstLine_temp.strip().split('\t')
    #print (firstLine)
    MixComplIndex=firstLine.index('mixs_compliant')
    projectNameIndex=firstLine.index('project_name')
    absIndex=firstLine.index('abstract_pubmed')
    DesIndex=firstLine.index('description')
    ProjectIdIndex=firstLine.index('project_id')
    #MixComplIndex=firstLine.index('mixs_compliant')
    print (projectNameIndex, absIndex, DesIndex, MixComplIndex)
    L.append(firstLine_temp)
    for line in f:
        l=line.strip().split('\t')
        D_MixsCompliant.setdefault(l[MixComplIndex+1],[]).append(l[ProjectIdIndex + 1])
        #print (l[0])
        try:
            abs=l[absIndex+1] + ' ' +l[DesIndex+1] + ' ' + l[projectNameIndex+1]
            #if l[ProjectIdIndex+1] == 'mgp84098':
                #print(abs)
            if searchTerm(abs, TermsOfInterest)==True:
                #print (line)
                L.append(line)
        except IndexError:
            continue
    #print (len(L))
    #print (L)
    L_ProjectIds=[]
    for i in L[1:]:
        L_temp=i.strip().split('\t')
        L_ProjectIds.append(L_temp[ProjectIdIndex+1])
    print(len(list(set(L_ProjectIds))) ,list(set(L_ProjectIds)))
    for j in D_MixsCompliant:
        print(j, len(set(D_MixsCompliant[j])))
    #print (D_MixsCompliant['0.977'])
    return L

RelevantStudies=getRelevantStudies(f_in, TermsOfInterest)
#print (RelevantStudies)
fout=open(f_out,'w')
fout.write(''.join(RelevantStudies))
fout.close()

''' 
MG-RAST total studies: 299 of which Mixs compliance: TRUE 281, FALSE 18
MG-RAST data related to diet resulted from text mining: 70 (124 - 54). 
the 54 because we have redundant description abstarcts and study names which were labeled with different projectIds 
'''