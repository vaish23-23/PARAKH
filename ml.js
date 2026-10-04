function mlScore(text,M){
  var ws=text.toLowerCase().replace(/\s+/g,' ').trim().split(' ').filter(Boolean),tf={},occ=[],i,n,w,off,g,e;
  function add(g,wi){if(M.v[g]){tf[g]=(tf[g]||0)+1;occ.push([g,wi])}}
  for(i=0;i<ws.length;i++){w=' '+ws[i]+' ';for(n=2;n<=5;n++){off=0;add(w.substr(0,n),i);while(off+n<w.length){off++;add(w.substr(off,n),i)}if(off==0)break}}
  var x={},nm=0;for(g in tf){x[g]=(1+Math.log(tf[g]))*M.v[g][0];nm+=x[g]*x[g]}nm=Math.sqrt(nm)||1;
  var z=M.b,wc=ws.map(function(){return 0});
  occ.forEach(function(o){var c=x[o[0]]*M.v[o[0]][1]/nm/tf[o[0]];z+=c;wc[o[1]]+=c});
  return{p:1/(1+Math.exp(-z)),words:ws,wc:wc};
}
