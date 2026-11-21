const { chromium } = require('C:/Users/Jemma/Documents/SimTracker/node_modules/playwright');
const fs=require('fs'),path=require('path');
(async()=>{const b=await chromium.launch({channel:'msedge'});const p=await b.newPage();
await p.route('**/*',r=>{const u=new URL(r.request().url());if(u.host!=='library.test')return r.continue();let f=path.join('C:/Users/Jemma/Documents/HomeLibrary/site',decodeURIComponent(u.pathname));r.fulfill({body:fs.readFileSync(f),contentType:f.endsWith('.js')?'application/javascript':'text/html'})});
for (const h of ['#home','#b-yw7av9br71']){
await p.goto('http://library.test/index.html'+h);
console.log('=====',h);
console.log(await p.evaluate(()=>{const walk=(e,d)=>{if(d>7)return '';let s='  '.repeat(d)+e.tagName.toLowerCase()+(e.className&&typeof e.className==='string'?'.'+e.className.split(' ').join('.'):'')+(e.children.length===0?' "'+e.textContent.slice(0,30)+'"':'')+'\n';let kids=[...e.children];const seen=new Set();for(const k of kids){const sig=k.tagName+k.className;if(seen.has(sig)&&kids.length>3)continue;seen.add(sig);s+=walk(k,d+1);}return s;};return walk(document.getElementById('view'),0)+walk(document.getElementById('side'),0)}));}
await b.close();})();
