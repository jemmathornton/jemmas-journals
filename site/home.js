/* Jemma’s Journals home page: draws the page (moved out of index.html 22 Nov so the security policy can allow only the site’s own files). */
(function(){
  // The places. A new one is one more line here. "about" is a line from that app's own home page; null means a space for her words.
  // Pictures are parked for now (her call, 20 Nov): Sim World and Pokédex show a full map until she chooses.
  // all sites share one address: home at the root, each app under its folder name in Jemma’s Journals (her names, 21 Nov); online, or on her PC through tools/serve_all.py (port 8050); set HOME_DOMAIN if she buys her own
  var HOME_DOMAIN='', ONLINE=/github\.io$/.test(location.hostname) || (HOME_DOMAIN && location.hostname===HOME_DOMAIN) || (/^(localhost|127\.0\.0\.1)$/.test(location.hostname) && location.port==='8050');
  var PLACES=[
    {name:"Sim World", url:"/sim-world/", title:"My Sim World", pc:"#4E3182", pic:{img:"img/maps/sims-willow-creek.webp", map:true, alt:"Map of Willow Creek"},
     about:"Every world in the game, rebuilt one lot at a time. Wander the neighbourhoods, look around the homes and venues, and meet the households who live in them."},
    {name:"Library", url:"/library/", title:"My Library", pc:"#6E4524", pic:{wall:true, alt:"Covers of books from my shelves"},
     about:"Every book on the shelves at home, and everything you read."},
    {name:"Pokédex", url:"/pokedex/", title:"My Pokédex", pc:"#7E2530", pic:{img:"img/maps/region-johto-kanto.webp", map:true, alt:"Map of Johto and Kanto"},
     about:null},
    {name:"Travels", url:"/travels/", title:"My Travels", pc:"#1D7A69", pic:{img:"img/maps/travels-map.webp", map:true, alt:"Map of the places on my trips"},
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
  var WALL=''; for(var n=0;n<72;n++) WALL+='<img src="img/wall/'+String((n*7)%40).padStart(2,'0')+'.webp" alt="" loading="lazy" decoding="async">';
  function pic(p){
    if(p.demo) return '<span class="pic blank" style="--pc:'+p.pc+'"></span>';
    var q=p.pic;
    if(q.wall) return '<span class="pic" role="img" aria-label="'+esc(q.alt)+'"><span class="wall">'+WALL+'</span></span>';
    return '<span class="pic'+(q.map?' map':'')+'"><img class="bg" src="'+q.img+'" alt="'+esc(q.alt||'')+'" loading="lazy" decoding="async"></span>';
  }
  function aboutPlace(p){ return p.about ? '<p>'+esc(p.about)+'</p>' : '<p class="ph">A line or two about '+(p.demo?'it':esc(p.name))+', in your own words.<span class="ph-tag">Placeholder</span></p>'; }
  var CORNERS='<span class="c tl"></span><span class="c tr"></span><span class="c bl"></span><span class="c br"></span>';
  function h2(text,id){ return '<div class="h2"><h2'+(id?' id="'+id+'"':'')+'>'+text+'</h2><span class="rule"><i></i><b></b></span></div>'; }

  // state: more places (to show how it grows), light/dark (light unless the button is pressed). Her picks: the Improved version, with About this site.
  var more=0, root=document.documentElement, userMode=root.getAttribute('data-mode')==='dark'?'dark':'light';   // more: how many stand-in places to add (0–3); the mode was set by the family's mode.js
  location.hash.slice(1).split('--').forEach(function(w){ if(w==='more') more=3; var mm=/^more([123])$/.exec(w); if(mm) more=+mm[1]; if(w==='dark'||w==='light') userMode=w;
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
    var list=PLACES.concat(EXTRA.slice(0,more)), dark=userMode==='dark';
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
        +'<a class="snap" href="'+esc(p.url||'#')+'" data-open="'+esc(p.demo?'':p.name)+'" aria-label="Open '+esc(open)+'">'+CORNERS+pic(p)+'</a>'
        +'<h3>'+esc(p.title)+'</h3>'+aboutPlace(p)
        +'<a class="go" href="'+esc(p.url||'#')+'" data-open="'+esc(p.demo?'':p.name)+'">Open '+esc(open)+' '+ico('arrow-right')+'</a></article>';
    });
    h+='</div></div></main>'
      +'<div class="end" aria-hidden="true"><i></i><b></b><i></i></div>'
      +'<footer class="foot gut"><div class="wrap"><b>Jemma’s Journals</b>'+aboutSite()
      +'<div class="foot-links"><a class="totop" href="#top" data-jj-top>'+ico('arrow-up')+'Back to top</a>'+MODETEXT+'</div>'+'</div></footer>';
    var page=document.getElementById('page'); page.className='v2'+(firstRender?' i-enter':''); firstRender=false; page.innerHTML=h;
  }
  // title on scroll: show the slim bar once the banner has scrolled out of sight
  render();

  var toast=document.getElementById('toast'), t;
  function say(m){ toast.textContent=m; toast.hidden=false; clearTimeout(t); t=setTimeout(function(){ toast.hidden=true; },1800); }
  document.addEventListener('click',function(e){
    // Back to top and Dark mode: the family’s shared code (site/family/family.js)
    var a=e.target.closest('a[data-open]'); if(!a) return;
    if(ONLINE && a.getAttribute('href')!=='#') return;   // online, the links go to the apps
    e.preventDefault();
    say(a.dataset.open ? 'My '+a.dataset.open+' opens here once the sites are online' : 'A new place would go here');
  });
})();
