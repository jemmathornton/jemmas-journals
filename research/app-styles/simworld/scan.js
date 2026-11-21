const { chromium } = require('C:/Users/Jemma/Documents/SimTracker/node_modules/playwright');
const fs=require('fs'),path=require('path');const SITE='C:/Users/Jemma/Documents/SimTracker/site';
(async()=>{const b=await chromium.launch({channel:'msedge'});const c=await b.newContext({viewport:{width:1600,height:930}});
await c.route('http://simworld.test/**',r=>{let p=decodeURIComponent(new URL(r.request().url()).pathname);const f=path.join(SITE,p);if(!fs.existsSync(f))return r.fulfill({status:404,body:''});r.fulfill({status:200,body:fs.readFileSync(f),headers:{'content-type':{'.html':'text/html','.css':'text/css','.js':'text/javascript'}[path.extname(f)]||'application/octet-stream'}})});
const p=await c.newPage();await p.goto('http://simworld.test/index.html#home');await p.waitForTimeout(400);
const worlds=await p.evaluate(()=>[...document.querySelectorAll('a.wt')].map(a=>a.getAttribute('href')));
for(const w of worlds){await p.goto('http://simworld.test/index.html'+w);await p.waitForTimeout(250);
const hoods=await p.evaluate(()=>[...document.querySelectorAll('a.listing')].map(a=>a.getAttribute('href')));
for(const h of hoods){await p.goto('http://simworld.test/index.html'+h);await p.waitForTimeout(200);
const r=await p.evaluate(()=>{const L=[...document.querySelectorAll('a.listing')];return [L.length,L.filter(a=>a.querySelector('.photo img, .photo[style*="url"]')).length]});
if(r[1]>=3)console.log(h,r)}}
await b.close()})();
