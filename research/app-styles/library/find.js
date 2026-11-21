const { chromium } = require('C:/Users/Jemma/Documents/SimTracker/node_modules/playwright');
const fs=require('fs'),path=require('path');
(async()=>{const b=await chromium.launch({channel:'msedge'});const p=await b.newPage();
await p.route('**/*',r=>{const u=new URL(r.request().url());if(u.host!=='library.test')return r.continue();let f=path.join('C:/Users/Jemma/Documents/HomeLibrary/site',decodeURIComponent(u.pathname));r.fulfill({body:fs.readFileSync(f),contentType:f.endsWith('.js')?'application/javascript':'text/html'})});
await p.goto('http://library.test/index.html');
console.log(await p.evaluate(()=>Object.values(bookIndex).filter(b=>/Circe|Hope Street|Claudine|Poet Empress/.test(b.t)).map(b=>b.id+' '+b.t+' '+Object.keys(b).join(','))));
await b.close();})();
