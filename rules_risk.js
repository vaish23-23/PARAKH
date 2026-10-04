// Runs the exact rule engine embedded in satark.html over a list of texts. usage: node rules_risk.js in.json out.json
const fs=require('fs');const h=fs.readFileSync('../index.html','utf8');
const a=h.indexOf('/* each rule'),b=h.indexOf('function marked');
const eng=new Function(h.slice(a,b)+';return analyze;')();
const xs=JSON.parse(fs.readFileSync(process.argv[2],'utf8'));
fs.writeFileSync(process.argv[3],JSON.stringify(xs.map(x=>eng(x).risk)));
