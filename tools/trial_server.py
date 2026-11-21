"""Serve one of Jemma's apps exactly as it is, with a trial style switch added on the way out.

Her app's files are only read, never changed: when the browser asks for the app's index.html,
this adds a stylesheet link and a small switch (bottom right) to the copy it sends. The trial
styles live in research/app-styles/<app>/ in this project.

Run (Python 3.13):  python -I tools/trial_server.py simworld
Then open http://localhost:8044/
"""
import http.server, json, os, sys, functools

HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT = os.path.dirname(HERE)
APPS = {
    # app: (her app's site folder, port, [(style file or "", label)])
    "simworld": (r"C:\Users\Jemma\Documents\SimTracker\site", 8044, [
        ("", "Now"),
        ("s1fa.css", "Town plan (your pick)"),
    ]),
}

SWITCH_JS = r"""
(function(){
  var OPTS = %(opts)s, KEY = 'jj-trial-%(app)s';
  var link = document.getElementById('jj-trial');
  // lot-type tags for the lot-type colours (re-run as the app changes page)
  function tagKinds(){
    document.querySelectorAll('a.listing').forEach(function(a){
      var t = ((a.querySelector('.type') || {}).textContent || '').toLowerCase(), k = 'other';
      if (/rental/.test(t)) k = 'rental';
      else if (/residential|starter|home/.test(t)) k = 'home';
      else if (/restaurant|bar|lounge|caf|diner|bakery|boba|nightclub|pub/.test(t)) k = 'food';
      else if (/retail|shop|store|thrift|market/.test(t)) k = 'shop';
      else if (/park|library|gym|museum|pool|community|spa|club|centre|center|cemetery|arts|marketplace|karaoke|festival|school|hall/.test(t)) k = 'community';
      if (a.dataset.kind !== k) a.dataset.kind = k;
    });
  }
  new MutationObserver(tagKinds).observe(document.body, {childList:true, subtree:true});
  tagKinds();
  var box = document.createElement('div');
  box.id = 'jj-trial-switch';
  box.setAttribute('role', 'group'); box.setAttribute('aria-label', 'Try a style');
  box.innerHTML = '<span>Try</span>' + OPTS.map(function(o, i){ return '<button type="button" data-i="' + i + '">' + o[1] + '</button>'; }).join('');
  document.body.appendChild(box);
  function pick(i){
    var o = OPTS[i] || OPTS[0];
    if (o[0]) { link.href = '/__trial/' + o[0]; link.disabled = false; } else { link.disabled = true; link.removeAttribute('href'); }
    box.querySelectorAll('button').forEach(function(b){ b.setAttribute('aria-pressed', +b.dataset.i === i ? 'true' : 'false'); });
    try { localStorage.setItem(KEY, String(i)); } catch(e) {}
  }
  box.addEventListener('click', function(e){ var b = e.target.closest('button'); if (b) pick(+b.dataset.i); });
  var saved = 1; try { var s = localStorage.getItem(KEY); if (s !== null) saved = +s; } catch(e) {}
  pick(saved);
})();
"""

SWITCH_CSS = """
#jj-trial-switch{position:fixed;z-index:2147483000;right:14px;bottom:14px;display:flex;flex-wrap:wrap;gap:4px;align-items:center;max-width:calc(100vw - 28px);
  padding:7px;border-radius:14px;background:#fff;color:#1A1F2C;border:1px solid #E1E4EA;box-shadow:0 10px 30px -8px rgba(0,0,0,.35);font:600 13px system-ui,"Segoe UI",sans-serif}
#jj-trial-switch span{font-size:10px;letter-spacing:.12em;text-transform:uppercase;color:#6B7280;padding:0 6px}
#jj-trial-switch button{font:inherit;border:0;background:none;padding:6px 11px;border-radius:99px;cursor:pointer;color:#1A1F2C}
#jj-trial-switch button:hover{background:#F1F2F5}
#jj-trial-switch button[aria-pressed="true"]{background:#1A1F2C;color:#fff}
"""


class Handler(http.server.SimpleHTTPRequestHandler):
    app = None

    def do_GET(self):
        site, port, opts = APPS[self.app]
        path = self.path.split("?")[0].split("#")[0]
        styles = os.path.join(PROJECT, "research", "app-styles", self.app)
        if path.startswith("/__trial/"):
            name = os.path.basename(path)
            if name == "switch.js":
                return self.send_text(SWITCH_JS % {"opts": json.dumps(opts, ensure_ascii=False), "app": self.app}, "application/javascript")
            if name == "switch.css":
                return self.send_text(SWITCH_CSS, "text/css")
            f = os.path.join(styles, name)
            if name.endswith(".css") and os.path.isfile(f):
                with open(f, "r", encoding="utf-8") as h:
                    return self.send_text(h.read(), "text/css")
            return self.send_error(404)
        if path in ("/", "/index.html"):
            with open(os.path.join(site, "index.html"), "r", encoding="utf-8") as h:
                html = h.read()
            html = html.replace("</head>", '<link rel="stylesheet" href="/__trial/switch.css"><link id="jj-trial" rel="stylesheet">\n</head>', 1)
            html = html.replace("</body>", '<script src="/__trial/switch.js"></script>\n</body>', 1)
            return self.send_text(html, "text/html")
        return super().do_GET()

    def send_text(self, text, ctype):
        body = text.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", ctype + "; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *a):
        pass


if __name__ == "__main__":
    app = sys.argv[1] if len(sys.argv) > 1 else "simworld"
    site, port, _ = APPS[app]
    Handler.app = app
    handler = functools.partial(Handler, directory=site)
    print(f"Trial styles for {app} on http://localhost:{port}/ (her files are only read)", flush=True)
    http.server.ThreadingHTTPServer(("127.0.0.1", port), handler).serve_forever()
