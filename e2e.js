// End-to-end check of the page's own logic: extract engine+model, score the unseen set exactly as the UI does.
const fs=require('fs');const h=fs.readFileSync('../index.html','utf8');
const a=h.indexOf('var MODEL='),b=h.indexOf('var L=');const c=h.indexOf('/* each rule'),d=h.indexOf('function marked');
const f=new Function(h.slice(a,b)+h.slice(c,d)+';return {analyze,mlScore,MODEL};')();
const tests=[["Join our VIP Telegram group t.me/profitking99 for sure shot intraday tips. 300% return in 1 month guaranteed. Pay Rs 2999 registration fee on UPI 98xxxx@paytm",1],["Your monthly SIP of Rs 2000 will be processed on the 5th. Please keep balance in your account.",0],["सेबी रजिस्टर्ड एक्सपर्ट! रोज 5% मुनाफ़ा पक्का। आज ही WhatsApp ग्रुप जॉइन करें और ऐप डाउनलोड करें: zerodha-pro.in/app.apk",1],["OTP for your transaction is 482913. Do not share it with anyone.",0]];
tests.forEach(([t,l])=>{const r=f.analyze(t).risk,m=f.mlScore(t,f.MODEL).p,s=.9*m+.1*r;console.log(l,'final=%s model=%s rules=%s',s.toFixed(2),m.toFixed(2),r.toFixed(2),'|',t.slice(0,40))});
