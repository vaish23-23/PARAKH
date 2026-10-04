# Step before train.py: scores every text with the app's rule engine (index.html) and saves all_rules.json
import csv,json,subprocess,sys
sys.path.insert(0,'.');from ood import OOD
rows=list(csv.DictReader(open('dataset.csv',encoding='utf-8')))
json.dump([r['text'] for r in rows]+[t for t,_ in OOD],open('all_texts.json','w'))
subprocess.run(['node','rules_risk.js','all_texts.json','all_rules.json'],check=True)
print('ok')
