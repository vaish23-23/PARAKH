const fs=require('fs');eval(fs.readFileSync('ml.js','utf8')+';global.mlScore=mlScore');
const M=JSON.parse(fs.readFileSync('model.json','utf8')),T=JSON.parse(fs.readFileSync('parity_texts.json','utf8')),P=JSON.parse(fs.readFileSync('parity_py.json','utf8'));
let mx=0;T.forEach((t,i)=>{mx=Math.max(mx,Math.abs(mlScore(t,M).p-P[i]))});console.log('texts',T.length,'max |JS - Python| =',mx.toExponential(2));
