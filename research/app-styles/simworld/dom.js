const { chromium } = require('C:/Users/Jemma/Documents/SimTracker/node_modules/playwright');
const fs=require('fs'),path=require('path');const SITE='C:/Users/Jemma/Documents/SimTracker/site';
(async()=>{const b=await chromium.launch({channel:'msedge'});const c=await b.newContext({viewport:{width:1600,height:930},colorScheme:'light'});
await c.route('http://simworld.test/**',r=>{let p=decodeURIComponent(new URL(r.request().url()).pathname);const f=path.join(SITE,p);if(!fs.existsSync(f))return r.fulfill({status:404,body:''});const ext=path.extname(f);r.fulfill({status:200,body:fs.readFileSync(f),headers:{'content-type':{'.html':'text/html','.css':'text/css','.js':'text/javascript','.jpg':'image/jpeg','.png':'image/png','.woff2':'font/woff2','.svg':'image/svg+xml','.webp':'image/webp'}[ext]||'application/octet-stream'}})});
const p=await c.newPage();
for(let h of process.argv.slice(2)){let L=h.startsWith("L:");if(L)h=h.slice(2);await p.goto('http://simworld.test/index.html'+h);await p.waitForTimeout(500);if(L){console.log(await p.evaluate(()=>[...document.querySelectorAll("a.listing")].map(a=>a.getAttribute("href")).join(" ")));continue}
const out=await p.evaluate(()=>{function walk(e,d){if(d>7)return'';let s='  '.repeat(d)+e.tagName.toLowerCase()+(e.className&&typeof e.className=='string'?'.'+e.className.trim().replace(/\s+/g,'.'):'')+(e.children.length==0?' "'+(e.textContent||'').trim().slice(0,40)+'"':'')+'\n';let kids=[...e.children];let seen={};for(const k of kids){const key=k.tagName+k.className;seen[key]=(seen[key]||0)+1;if(seen[key]>2)continue;s+=walk(k,d+1)}return s}return walk(document.getElementById('view'),0)});
console.log('=====',h);console.log(out)}
await b.close()})();
