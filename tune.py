import csv,json,numpy as np,sys
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score,f1_score,accuracy_score
exec(open('train.py').read().split("def mk")[0])
sc=sorted(set(T[y==1]));lg=sorted(set(T[y==0]));sp=[]
for i,s in enumerate(sc):
    hold=(T==s)|(T==lg[i%len(lg)]);sp.append((np.where(~hold)[0],np.where(hold)[0]))
def lofo(ng,C,mf):
    P=np.zeros(N)
    for tr,te in sp:
        v=TfidfVectorizer(analyzer='char_wb',ngram_range=ng,sublinear_tf=True,min_df=3,max_features=mf);m=LogisticRegression(C=C,max_iter=3000)
        m.fit(v.fit_transform([X[i] for i in tr]),y[tr]);P[te]=m.predict_proba(v.transform([X[i] for i in te]))[:,1]
    idx=np.concatenate([te for _,te in sp]);return P,idx
best=None
for ng in[(2,5),(3,6),(1,4)]:
    for C in[0.5,2,8]:
        P,idx=lofo(ng,C,6000);a=roc_auc_score(y[idx],P[idx]);f=f1_score(y[idx],P[idx]>=.5);print(ng,C,'auc=%.4f f1=%.4f'%(a,f))
        if best is None or a+f>best[0]:best=(a+f,ng,C,P,idx)
_,ng,C,P,idx=best;print('chosen',ng,C)
for a in[1,.9,.8,.7,.6]:
    s=a*P+(1-a)*rN;print('blend alpha=%.1f'%a,'acc=%.3f f1=%.3f auc=%.3f'%(accuracy_score(y[idx],s[idx]>=.5),f1_score(y[idx],s[idx]>=.5),roc_auc_score(y[idx],s[idx])))
