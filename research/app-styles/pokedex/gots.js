const { chromium } = require('C:/Users/Jemma/Documents/SimTracker/node_modules/playwright');
const fs=require('fs'),path=require('path');
const SITE='C:/Users/Jemma/Documents/Pokedex/site', COLL='C:/Users/Jemma/Documents/Pokedex/data/collection/go.json';
(async()=>{
 const b=await chromium.launch({channel:'msedge'}); const ctx=await b.newContext({viewport:{width:1600,height:930}});
 await ctx.route('**/*',r=>{const u=new URL(r.request().url()); if(u.pathname==='/api/collection')return r.fulfill({contentType:'application/json',body:fs.readFileSync(COLL)}); let p=u.pathname==='/'?'/index.html':decodeURIComponent(u.pathname); const f=path.join(SITE,p); if(!fs.existsSync(f)||fs.statSync(f).isDirectory())return r.fulfill({status:404,body:''}); r.fulfill({body:fs.readFileSync(f)});});
 const p=await ctx.newPage(); await p.addInitScript(()=>localStorage.setItem('jemmas-pokedex-view',JSON.stringify({workShow:'all'})));
 for (const g of ['1','2','3','4','5','6','7','8','hisui','9']) {
  await p.goto('http://pokedex.localhost/#gen-'+g); await p.waitForTimeout(1200);
  console.log(g, await p.evaluate(()=>[...document.querySelectorAll('.grid .card')].slice(0,16).map(c=>c.classList.contains('got')?'X':'.').join('')));
 }
 await b.close();})();
