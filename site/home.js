/* Jemma’s Journals home page: draws the page (moved out of index.html 22 Nov so the security policy can allow only the site’s own files). */
(function(){
  // The places. A new one is one more line here. "about" is a line from that app's own home page; null means a space for her words.
  // Pictures are parked for now (her call, 20 Nov): Sim World and Pokédex show a full map until she chooses.
  // all sites share one address: home at the root, each app under its folder name (her names, 21 Nov). The links work wherever the family is served:
  // her PC (tools/serve_all.py, 8050), the online-style copy (tools/build_site.py --serve, 8060) and online, at any address. Only where the apps
  // really aren't there (the page opened as a file, or the phone copy as a Claude artifact: claude.ai, claudeusercontent.com or a sandboxed frame) does a link say so instead (round 5 review).
  var NO_APPS=!/^https?:$/.test(location.protocol) || /(^|\.)(claude\.ai|claudeusercontent\.com)$/.test(location.hostname);
  var PLACES=[
    {name:"Sim World", url:"/sim-world/", frame:"img/home/frame-sim-world.webp", title:"My Sim World", pc:"#4E3182", pic:{img:"img/maps/sims-willow-creek.webp", map:true, alt:"Map of Willow Creek"},
     about:"Every world in the game, rebuilt one lot at a time. Wander the neighbourhoods, look around the homes and venues, and meet the households who live in them."},
    {name:"Library", url:"/library/", title:"My Library", pc:"#6E4524", pic:{wall:true, alt:"Covers of books from my shelves"},
     about:"Every book on the shelves at home, and everything you read."},
    {name:"Pokédex", url:"/pokedex/", frame:"img/home/frame-pokedex.webp", title:"My Pokédex", pc:"#7E2530", pic:{img:"img/maps/region-johto-kanto.webp", map:true, alt:"Map of Johto and Kanto"},
     about:null},
    {name:"Travels", url:"/travels/", frame:"img/home/frame-travels.webp", title:"My Travels", pc:"#1D7A69", pic:{img:"img/maps/travels-map.webp", map:true, alt:"Map of the places on my trips"},
     about:null}   // added 21 Nov (her yes); the picture is Travels' own map in its chosen Old Atlas look
  ];
  // Only for "More places": stand-ins to show how it grows. Not real places.
  var EXTRA=[{name:"New place",title:"New place",pc:"#35606F",demo:true},{name:"New place",title:"New place",pc:"#8A6A3A",demo:true},{name:"New place",title:"New place",pc:"#5A5F73",demo:true}];
  var ICON={
    "arrow-right":'<path d="M5 12h14"/><path d="m12 5 7 7-7 7"/>',
    "arrow-up":'<path d="m5 12 7-7 7 7"/><path d="M12 19V5"/>',
    "plus":'<path d="M5 12h14"/><path d="M12 5v14"/>',
    "image":'<rect width="18" height="18" x="3" y="3" rx="2" ry="2"/><circle cx="9" cy="9" r="2"/><path d="m21 15-3.086-3.086a2 2 0 0 0-2.828 0L6 21"/>',
    "sun":'<circle cx="12" cy="12" r="4"/><path d="M12 2v2"/><path d="M12 20v2"/><path d="m4.93 4.93 1.41 1.41"/><path d="m17.66 17.66 1.41 1.41"/><path d="M2 12h2"/><path d="M20 12h2"/><path d="m6.34 17.66-1.41 1.41"/><path d="m19.07 4.93-1.41 1.41"/>',
    "moon":'<path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"/>'
  };
  function ico(n){ return '<svg class="i" viewBox="0 0 24 24" aria-hidden="true">'+ICON[n]+'</svg>'; }
  function esc(s){ return String(s).replace(/[&<>"]/g,function(c){return {"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c];}); }
  var WALL=''; for(var n=0;n<72;n++) WALL+='<img draggable="false" src="img/wall/'+String((n*7)%40).padStart(2,'0')+'.webp" alt="" loading="lazy" decoding="async">';
  // TRY SWITCH (temporary, 22 Nov: the photo corners and the mat behind each picture; remove with the TRY SWITCH CSS once she has picked)
  var CORNER_OPTS=[['now','As now'],['gold','Gold'],['cream','Cream'],['clear','Clear'],['frosted','Frosted'],['smoky','Smoky'],['brackets','Brackets'],['none','None']];
  var MAT_OPTS=[['flat','Flat'],['soft','Soft'],['deep','Deep']];
  var corners='now', mat='flat', tryHidden=false;
  function okCorner(v){ return CORNER_OPTS.some(function(o){ return o[0]===v; }); }
  function okMat(v){ return MAT_OPTS.some(function(o){ return o[0]===v; }); }
  try { var saved=JSON.parse(localStorage.getItem('jj-home-try')||'{}'); if(okCorner(saved.corners)) corners=saved.corners; if(okMat(saved.mat)) mat=saved.mat; tryHidden=!!saved.hidden; } catch(e){}
  function saveTry(){ try { localStorage.setItem('jj-home-try', JSON.stringify({corners:corners,mat:mat,hidden:tryHidden})); } catch(e){} }
  // every picture the same landscape plate, 2:1 (her pick, 22 Nov): maps cropped to that shape (img/home/frame-*), the Library's wall fills it
  function pic(p){
    if(p.demo||!p.pic) return '<span class="pic blank" style="--pc:'+p.pc+'"></span>';   // no picture yet (a new site from tools/new_site.py): the striped stand-in
    var q=p.pic;
    if(q.wall) return '<span class="pic" role="img" aria-label="'+esc(q.alt)+'"><span class="wall">'+WALL+'</span></span>';
    return '<span class="pic fill"><img class="bg" draggable="false" src="'+(p.frame||q.img)+'" alt="'+esc(q.alt||'')+'" loading="lazy" decoding="async"></span>';
  }
  function aboutPlace(p){ return p.about ? '<p>'+esc(p.about)+'</p>' : '<p class="ph">A line or two about '+(p.demo?'it':esc(p.name))+', in your own words.<span class="ph-tag">Placeholder</span></p>'; }
  var CORNERS='<span class="c tl"></span><span class="c tr"></span><span class="c bl"></span><span class="c br"></span>';
  function h2(text,id){ return '<div class="h2"><h2'+(id?' id="'+id+'"':'')+'>'+text+'</h2><span class="rule"><i></i><b></b></span></div>'; }

  // state: more places (to show how it grows), light/dark (light unless the button is pressed). Her picks: the Improved version, with About this site.
  var more=0, root=document.documentElement, userMode=root.getAttribute('data-mode')==='dark'?'dark':'light';   // more: how many stand-in places to add (0–3); the mode was set by the family's mode.js
  location.hash.slice(1).split('--').forEach(function(w){ if(w==='more') more=3; var mm=/^more([123])$/.exec(w); if(mm) more=+mm[1]; if(w==='dark'||w==='light') userMode=w;
    if(/^corners-/.test(w) && okCorner(w.slice(8))) corners=w.slice(8);   // e.g. #corners-gold in the address (for checking; not saved)
    if(/^mat-/.test(w) && okMat(w.slice(4))) mat=w.slice(4);   // e.g. #mat-soft
    });

  // About this site: two quiet lines (her pick, 20 Nov: option 2, each credit starting with a capital)
  var DOT='<span class="dot" aria-hidden="true"> ·</span>';   // the no-break space sits inside the dot, so a “·” never starts a line and on phones (dots hidden) no empty line is left
  function aboutSite(){
    return '<div class="about-site two"><p data-jj-line1>No cookies, no tracking, no ads. Made with HTML, CSS, JavaScript and Python, kept on GitHub.</p>'
      +'<p data-jj-credits>'+['World maps by 20th Century Plumbob','Region maps from the Pokémon games','Country shapes from Natural Earth','Book covers from their publishers','Fonts: Instrument Serif and Manrope','Icons by Lucide'].map(function(t){ return '<span class="cr">'+t+'</span>'; }).join(DOT+' ')+'</p></div>';
  }
  root.setAttribute('data-mode', userMode);   // #dark / #light in the address (for checking); the theme colour and tab icon follow through family.js (round 4: this page's own copy left the bar colour stuck)

  var firstRender=true;   // the gentle entrance plays once, when the page first opens
  function render(){
    var list=PLACES.concat(EXTRA.slice(0,more)), dark=root.getAttribute('data-mode')==='dark';
    var MODETEXT='<button type="button" class="mode-text" data-jj-mode aria-pressed="'+dark+'">'+ico(dark?'sun':'moon')+(dark?'Light mode':'Dark mode')+'</button>';
    var h='<a class="skip" href="#contents">Skip to contents</a>'
      +'<header class="cover gut" id="top" tabindex="-1"><span class="cn tl"></span><span class="cn tr"></span><span class="cn bl"></span><span class="cn br"></span>'
      +'<div class="wrap"><h1>Jemma’s <em>Journals</em></h1></div>'
      +'</header>'
      +'<main class="gut"><div class="wrap">';
    var INTRO='<p class="ph">An introduction to the site goes here, in your own words: what these journals are and what you’ll find in them.<span class="ph-tag">Placeholder</span></p>';
    h+='<section class="intro" aria-labelledby="intro"><div>'+h2('Introduction','intro')+INTRO+'</div></section>'   // Introduction to the site, words only (her picks, 20 Nov)
      +'<div class="sec">'+h2('Contents','contents')+'</div>'
      +'<div class="cards">';
    list.forEach(function(p){
      var open=p.demo?'it':p.title;   // "Open My Sim World" (her ask, 20 Nov: the link should say My like the heading)
      h+='<article class="card" style="--pc:'+p.pc+'">'
        +'<div class="snap">'+CORNERS+pic(p)+'</div>'   // the picture is not a link (her decision, 22 Nov): only "Open …" opens a site
        +'<div class="txt"><h3>'+esc(p.title)+'</h3>'+aboutPlace(p)+'</div>'
        +'<a class="go" href="'+esc(p.url||'#')+'" data-open="'+esc(p.demo?'':p.name)+'">Open '+esc(open)+' '+ico('arrow-right')+'</a></article>';
    });
    h+='</div></div></main>'
      +'<div class="end" aria-hidden="true"><i></i><b></b><i></i></div>'
      +'<footer class="foot gut"><div class="wrap"><b>Jemma’s Journals</b>'+aboutSite()
      +'<div class="foot-links"><a class="totop" href="#top" data-jj-top>'+ico('arrow-up')+'Back to top</a>'+MODETEXT+'</div>'+'</div></footer>';
    var page=document.getElementById('page'); page.className='v2 corners-'+corners+' mat-'+mat+(firstRender?' i-enter':''); firstRender=false; page.innerHTML=h;
  }
  render();

  // the Try switch itself (temporary: bottom right, only while she chooses)
  var box=document.createElement('div'); box.className='trybox'; box.setAttribute('role','group'); box.setAttribute('aria-label','Try');
  function drawTry(){
    var h='<div class="try-head"><b>Try</b><button type="button" class="try-hide" aria-expanded="'+!tryHidden+'">'+(tryHidden?'Show':'Hide')+'</button></div>';
    if(!tryHidden) h+='<div class="try-row"><span>Corners</span>'+CORNER_OPTS.map(function(o){ return '<button type="button" data-try="corners" data-val="'+o[0]+'" aria-pressed="'+(corners===o[0])+'">'+o[1]+'</button>'; }).join('')+'</div>'
      +'<div class="try-row"><span>Mat</span>'+MAT_OPTS.map(function(o){ return '<button type="button" data-try="mat" data-val="'+o[0]+'" aria-pressed="'+(mat===o[0])+'">'+o[1]+'</button>'; }).join('')+'</div>';
    box.innerHTML=h; box.classList.toggle('folded',tryHidden);
  }
  drawTry(); document.body.appendChild(box);
  box.addEventListener('click',function(e){
    var b=e.target.closest('button'); if(!b) return;
    if(b.classList.contains('try-hide')){ tryHidden=!tryHidden; saveTry(); drawTry(); box.querySelector('.try-hide').focus(); return; }
    var k=b.getAttribute('data-try'), v=b.getAttribute('data-val'), pg=document.getElementById('page');
    if(k==='corners' && okCorner(v)){ corners=v; pg.className=pg.className.replace(/corners-\w+/,'corners-'+v); }
    else if(k==='mat' && okMat(v)){ mat=v; pg.className=pg.className.replace(/mat-\w+/,'mat-'+v); }
    else return;
    saveTry(); drawTry();
    var again=box.querySelector('[data-try="'+k+'"][data-val="'+v+'"]'); if(again) again.focus();
  });

  var toast=document.getElementById('toast'), t;
  function say(m){ toast.textContent=m; toast.hidden=false; clearTimeout(t); t=setTimeout(function(){ toast.hidden=true; },1800); }
  document.addEventListener('click',function(e){
    // Back to top and Dark mode: the family’s shared code (site/family/family.js)
    var a=e.target.closest('a[data-open]'); if(!a) return;
    if(!NO_APPS && a.getAttribute('href')!=='#') return;   // the links go to the apps
    e.preventDefault();
    say(a.dataset.open ? 'My '+a.dataset.open+' opens here once the sites are online' : 'A new place would go here');
  });
})();
