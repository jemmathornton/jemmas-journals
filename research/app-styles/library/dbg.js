const { chromium } = require('C:/Users/Jemma/Documents/SimTracker/node_modules/playwright');
const fs=require('fs'),path=require('path');
(async()=>{const b=await chromium.launch({channel:'msedge'});const p=await b.newPage({viewport:{width:1600,height:930}});
await p.route('**/*',r=>{const u=new URL(r.request().url());if(u.host!=='library.test')return r.continue();let f=path.join('C:/Users/Jemma/Documents/HomeLibrary/site',decodeURIComponent(u.pathname));r.fulfill({body:fs.readFileSync(f),contentType:f.endsWith('.js')?'application/javascript':f.endsWith('.css')?'text/css':'text/html'})});
await p.goto('http://library.test/index.html'+process.argv[2],{waitUntil:'networkidle'});
await p.addStyleTag({content:fs.readFileSync(process.argv[3],'utf8')});
console.log(await p.evaluate(sel=>[...document.querySelectorAll(sel)].slice(0,3).map(e=>{const c=getComputedStyle(e);return e.className+' '+JSON.stringify(e.getBoundingClientRect())+' pad '+c.padding+' ar '+c.aspectRatio+' h '+c.height+' style '+e.getAttribute('style')}),process.argv[4]));
await b.close();})();
