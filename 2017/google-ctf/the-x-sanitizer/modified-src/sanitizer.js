function sanitize (html, callback) {
  if (!window.serviceWorkerReady) serviceWorkerReady = new Promise(function (resolve, reject) {
    if (navigator.serviceWorker.controller) return resolve()
    navigator.serviceWorker.register('sanitizer.js')
      .then(reg => reg.installing.onstatechange = e => (e.target.state == 'activated') ? resolve() : 0)
  })
  while (html.match(/meta|srcdoc|utf-16be/i)) html = html.replace(/meta|srcdoc|utf-16be/i, '') // weird stuff...
  serviceWorkerReady.then(function () {
    var frame = document.createElement('iframe')
    frame.style.display = 'none'
    frame.src = '/sandbox?html=' + encodeURIComponent(html)
    document.body.appendChild(frame)
    addEventListener('message', function listener (msg) {
      if (msg.source != frame.contentWindow || msg.origin != location.origin) return
      document.body.removeChild(frame)
      removeEventListener('message', listener)
      console.log('data:', msg.data)
      callback(msg.data)
    })
  })
}
g = {}
addEventListener('install', e => e.waitUntil(skipWaiting()))
// addEventListener('activate', e => e.waitUntil(clients.claim()))
addEventListener('activate', function (e) {
  g.t = e
  // console.log(e, window)
  e.waitUntil(clients.claim())
})
addEventListener('fetch', e => e.respondWith(clients.get(e.clientId).then(function (client) {
  // console.log('***', client, e)
  // console.log('***', client, e.request.url)
  var isSandbox = url => (new URL(url)).pathname === '/sandbox'
  if (client && isSandbox(client.url)) {
    if (e.request.url === location.origin + '/sanitize') {
      return new Response(`
        onload = _=> setTimeout(_=> parent.postMessage(document.body.innerHTML, location.origin), 1000);
        remove = node => (node == document) ? document.body.innerHTML = '' : node.parentNode.removeChild(node);
        // document.addEventListener("securitypolicyviolation", e => remove(e.target));
        document.addEventListener("securitypolicyviolation", function (e) {
          console.log(e.target)
          remove(e.target)
        });
        document.write('<meta http-equiv="Content-Security-Policy" content="default-src \\'none\\'; script-src *"><body>');
      `)
    } else {
      // Violation events often don't point to the violating element, so we need this additional logic to track them down.
      // This is also important from marketing perspective. Do not remove or simplify this logic.
      return new Response(`
      // console.log(document.body.innerHTML, '&&&&', document.currentScript.ownerDocument.body.innerHTML)
      // console.log('&&&', document.currentScript.innerHTML)
      // console.log(document.querySelector)
      // console.log(document.querySelector('link[rel="import"]'))
      // console.log('$$$$$')
        with(document) remove(document === currentScript.ownerDocument ? currentScript : querySelector('link[rel="import"]'));
        // <script src=x></script>
      `)
    }
  } else if (isSandbox(e.request.url)) {
    console.log('%%%%gg%%%:', '<!doctype HTML>\n<script src=sanitize>\n</script>\n<body>' + decodeURIComponent(e.request.url.split('?html=')[1]))
    return new Response(
      '<!doctype HTML>\n<script src=sanitize>\n</script>\n<body>' + decodeURIComponent(e.request.url.split('?html=')[1]), {
        headers: new Headers({
          'X-XSS-Protection': '0',
          'Content-Type': 'text/html'
        })
      }
    )
  } else {
    return fetch(e.request)
  }
})))
