import csv,json,numpy as np,sys
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import accuracy_score,precision_score,recall_score,f1_score,roc_auc_score,brier_score_loss,confusion_matrix
sys.path.insert(0,'.');from ood import OOD
R=list(csv.DictReader(open('dataset.csv',encoding='utf-8')));N=len(R)
X=[r['text'] for r in R];y=np.array([int(r['label']) for r in R]);T=np.array([r['type'] for r in R])
rules=np.array(json.load(open('all_rules.json')));rN,rO=rules[:N],rules[N:]
Xo=[t for t,_ in OOD];yo=np.array([l for _,l in OOD])
def mk(kind):
    v=TfidfVectorizer(analyzer='char_wb',ngram_range=(2,5),sublinear_tf=True,min_df=3,max_features=6000) if kind=='char' else TfidfVectorizer(analyzer='word',ngram_range=(1,2),sublinear_tf=True,min_df=2,token_pattern=r'(?u)\b\w+\b')
    return v,LogisticRegression(C=0.5,max_iter=3000)
def fitpred(kind,tr,Xte):
    v,m=mk(kind);m.fit(v.fit_transform([X[i] for i in tr]),y[tr]);return m.predict_proba(v.transform(Xte))[:,1]
hyb=lambda p,r:0.9*p+0.1*r
def met(yt,s):
    p=(s>=.5).astype(int);return dict(acc=accuracy_score(yt,p),prec=precision_score(yt,p),rec=recall_score(yt,p),f1=f1_score(yt,p),auc=roc_auc_score(yt,s),brier=brier_score_loss(yt,np.clip(s,0,1)))
res={}
def run(name,splits):
    S={k:np.zeros(N) for k in['rules','word','char','hybrid']};S['rules']=rN.copy()
    for tr,te in splits:
        for k in['word','char']:S[k][te]=fitpred(k,tr,[X[i] for i in te])
    S['hybrid']=hyb(S['char'],rN)
    idx=np.concatenate([te for _,te in splits]);res[name]={k:met(y[idx],S[k][idx]) for k in S}
skf=list(StratifiedKFold(5,shuffle=True,random_state=1).split(X,y))
run('Random 5-fold CV',skf)
sc=sorted(set(T[y==1]));lg=sorted(set(T[y==0]));sp=[]
for i,s in enumerate(sc):  # hold out one whole scam family + one whole genuine family
    hold=(T==s)|(T==lg[i%len(lg)]);sp.append((np.where(~hold)[0],np.where(hold)[0]))
run('Leave-one-family-out',sp)
al=np.arange(N);S2={'rules':rO,'word':fitpred('word',al,Xo),'char':fitpred('char',al,Xo)};S2['hybrid']=hyb(S2['char'],rO)
res['Hand-written unseen set (n=%d)'%len(Xo)]={k:met(yo,S2[k]) for k in S2}
for n,d in res.items():
    print('\n',n)
    for k,m in d.items():print('  %-7s'%k,' '.join('%s=%.3f'%(a,b) for a,b in m.items()))
print('\nOOD confusion (hybrid):',confusion_matrix(yo,(S2['hybrid']>=.5).astype(int)).tolist())
print('OOD errors (hybrid):')
for i,(t,l) in enumerate(OOD):
    if int(S2['hybrid'][i]>=.5)!=l:print('  true=%d ml=%.2f rules=%.2f | %s'%(l,S2['char'][i],rO[i],t[:80]))
json.dump(res,open('metrics.json','w'),indent=1)
v,m=mk('char');m.fit(v.fit_transform(X),y);voc=v.vocabulary_;idf=v.idf_;co=m.coef_[0]
M={'b':round(float(m.intercept_[0]),5),'v':{g:[round(float(idf[i]),3),round(float(co[i]),3)] for g,i in voc.items()}}
json.dump(M,open('model.json','w'),ensure_ascii=False,separators=(',',':'))
top=sorted(voc,key=lambda g:co[voc[g]]);print('\nTop scam n-grams:',[g for g in top[-14:]][::-1]);print('Top genuine n-grams:',top[:10])
json.dump([X[i] for i in range(0,N,37)]+Xo,open('parity_texts.json','w'));
pt=[X[i] for i in range(0,N,37)]+Xo;json.dump([float(p) for p in m.predict_proba(v.transform(pt))[:,1]],open('parity_py.json','w'))
# threshold sweep (choose on leave-family-out only, then report unseen set once)
P=np.zeros(N)
for tr,te in sp:P[te]=fitpred('char',tr,[X[i] for i in te])
idx=np.concatenate([te for _,te in sp]);H=0.9*P+0.1*rN
print('\nThreshold sweep  thr: LOFO(prec,rec,f1) | unseen(prec,rec,f1)')
for t in[.3,.35,.4,.45,.5]:
    a=(H[idx]>=t).astype(int);b=(S2['hybrid']>=t).astype(int)
    print(' %.2f: %.3f %.3f %.3f | %.3f %.3f %.3f'%(t,precision_score(y[idx],a),recall_score(y[idx],a),f1_score(y[idx],a),precision_score(yo,b),recall_score(yo,b),f1_score(yo,b)))
