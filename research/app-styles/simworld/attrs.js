const { chromium } = require('C:/Users/Jemma/Documents/SimTracker/node_modules/playwright');
const fs=require('fs'),path=require('path');const SITE='C:/Users/Jemma/Documents/SimTracker/site';
(async()=>{const b=await chromium.launch({channel:'msedge'});const c=await b.newContext({viewport:{width:1600,height:930}});
await c.route('http://simworld.test/**',r=>{let p=decodeURIComponent(new URL(r.request().url()).pathname);const f=path.join(SITE,p);if(!fs.existsSync(f))return r.fulfill({status:404,body:''});r.fulfill({status:200,body:fs.readFileSync(f),headers:{'content-type':{'.html':'text/html','.css':'text/css','.js':'text/javascript'}[path.extname(f)]||'application/octet-stream'}})});
const p=await c.newPage();
for(const h of ['#home','#n-willow-creek-foundry-cove']){await p.goto('http://simworld.test/index.html'+h);await p.waitForTimeout(400);
console.log(h, await p.evaluate(()=>[...document.querySelectorAll('[style]')].slice(0,14).map(e=>e.tagName+'.'+e.className+' => '+e.getAttribute('style').slice(0,160)).join('\n')))}
await b.close()})();
