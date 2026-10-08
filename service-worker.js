const RELEASE='2.1.1.0-Beta';
const CACHE_PREFIX='sk-plt-tools-';
const CACHE=`${CACHE_PREFIX}v${RELEASE}`;
const CORE=[
  // precache:start
  "./",
  "./SIEMENS-QUELLEN-UND-GRENZWERTE.md",
  "./VDE0100-600-MESSWERTPRUEFER.md",
  "./analogsignal/",
  "./analogsignal/index.html",
  "./assets/airttorque-wissen.css",
  "./assets/app.js",
  "./assets/apple-touch-icon.png",
  "./assets/core.css",
  "./assets/favicon.png",
  "./assets/icon-192.png",
  "./assets/icon-512.png",
  "./assets/logo-horizontal.png",
  "./assets/logo-layout.css",
  "./assets/logo.png",
  "./assets/materials.css",
  "./assets/materials.js",
  "./assets/materials.json",
  "./assets/navigation-tree.json",
  "./assets/search-index.json",
  "./assets/siemens-analogwert-rechner.css",
  "./assets/siemens-analogwert-rechner.js",
  "./assets/siemens-sitrans-wissen.css",
  "./assets/vacon-wissen.css",
  "./assets/vde0100-600-engine.js",
  "./assets/vde0100-600-input-schema.json",
  "./assets/vde0100-600-rules.json",
  "./einheitenrechner/",
  "./einheitenrechner/index.html",
  "./index.html",
  "./manifest.webmanifest",
  "./messstellen-doku/",
  "./messstellen-doku/index.html",
  "./pf-rechner/",
  "./pf-rechner/index.html",
  "./plausibilitaetspruefung-vde0100-600/",
  "./plausibilitaetspruefung-vde0100-600/checker.css",
  "./plausibilitaetspruefung-vde0100-600/checker.js",
  "./plausibilitaetspruefung-vde0100-600/index.html",
  "./pt-rechner/",
  "./pt-rechner/index.html",
  "./servicewerte/",
  "./servicewerte/index.html",
  "./siemens-analogwert-rechner/",
  "./siemens-analogwert-rechner/index.html",
  "./spannungsfall-rechner/",
  "./spannungsfall-rechner/calculator.css",
  "./spannungsfall-rechner/calculator.js",
  "./spannungsfall-rechner/index.html",
  "./vendor/pdfjs/LICENSE",
  "./vendor/pdfjs/pdf.min.mjs",
  "./vendor/pdfjs/pdf.worker.min.mjs",
  "./wissensdatenbank/",
  "./wissensdatenbank/air-torque-antrieb-drehrichtung/",
  "./wissensdatenbank/air-torque-antrieb-drehrichtung/index.html",
  "./wissensdatenbank/index.html",
  "./wissensdatenbank/siemens-sitrans-p320-sil-verriegelung/",
  "./wissensdatenbank/siemens-sitrans-p320-sil-verriegelung/index.html",
  "./wissensdatenbank/siemens-sps-rohwert/",
  "./wissensdatenbank/siemens-sps-rohwert/index.html",
  "./wissensdatenbank/vacon-frequenzumrichter-ist-sollwert-abweichung/",
  "./wissensdatenbank/vacon-frequenzumrichter-ist-sollwert-abweichung/index.html",
  "./wissensdatenbank/vorlagen/Wissensdatenbank_Beitragsvorlage.docx",
  "./wissensdatenbank/vorlagen/Wissensdatenbank_Beitragsvorlage.pdf",
  "./wissensdatenbank/werkstoff-nachschlagewerk/",
  "./wissensdatenbank/werkstoff-nachschlagewerk/index.html"
  // precache:end
];

self.addEventListener('install',event=>{
  event.waitUntil((async()=>{
    const cache=await caches.open(CACHE);
    await Promise.all(CORE.map(async url=>{
      const request=new Request(url,{cache:'reload'});
      const response=await fetch(request);
      if(!response.ok)throw new Error(`Precache failed: ${url} (${response.status})`);
      await cache.put(request,response);
    }));
    await self.skipWaiting();
  })());
});

self.addEventListener('activate',event=>{
  event.waitUntil((async()=>{
    const keys=await caches.keys();
    await Promise.all(keys.filter(key=>key.startsWith(CACHE_PREFIX)&&key!==CACHE).map(key=>caches.delete(key)));
    await self.clients.claim();
  })());
});

async function navigation(request){
  const cache=await caches.open(CACHE);
  try{
    const response=await fetch(request,{cache:'no-store'});
    if(response.ok)await cache.put(request,response.clone());
    return response;
  }catch{
    const exact=await cache.match(request,{ignoreSearch:true});
    if(exact)return exact;
    const url=new URL(request.url);
    const indexRequest=new Request(url.pathname.endsWith('/')?new URL('index.html',url).href:url.href);
    return await cache.match(indexRequest,{ignoreSearch:true})||await cache.match('./index.html');
  }
}

async function asset(request){
  const cache=await caches.open(CACHE);
  const cached=await cache.match(request,{ignoreSearch:true});
  if(cached)return cached;
  const response=await fetch(request);
  if(response.ok)await cache.put(request,response.clone());
  return response;
}

self.addEventListener('fetch',event=>{
  const request=event.request;
  if(request.method!=='GET'||new URL(request.url).origin!==self.location.origin)return;
  event.respondWith(request.mode==='navigate'?navigation(request):asset(request));
});
