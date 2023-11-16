import sys

TermsOfInterest=[['diet','intervention'],['diet', 'observation']]

f_in=sys.argv[1]
f_out=f_in.split('.')[0]+'_DietSelectedStudies.csv'


def searchTerm(t, TermsOfInterest):
    for p in TermsOfInterest:
        p1=p[0]
        p2=p[1]
        if p1 and p2 in t:
            return True
        else:
            return False
    

def getRelevantStudies(fin, TermsOfInterest):
    L=[]
    f=open(fin, 'r')
    firstLine=f.readline()
    L.append(firstLine)
    for line in f:
        l=line.strip().split(',')
        #print (l[0])
        try:
            abs=l[10]
            if searchTerm(abs, TermsOfInterest)==True:
                L.append(line)
        except IndexError:
            continue
    return L

RelevantStudies=getRelevantStudies(f_in, TermsOfInterest)
fout=open(f_out,'w')
fout.write(''.join(RelevantStudies))
fout.close()
