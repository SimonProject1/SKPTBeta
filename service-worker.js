const RELEASE='2.6.5.2-Beta';
const CACHE_PREFIX='sk-pct-tools-';
const CACHE_EPOCH='v2-6-5-2-core-r1';
const CACHE_NAME=`${CACHE_PREFIX}${CACHE_EPOCH}`;

// Ausschließlich aktive Laufzeitressourcen. Dokumentation, Tests, Generatoren und
// ersetzte Versionsdateien gehören bewusst nicht in den Offline-Cache.
const CORE=[
  './',
  './analogsignal/',
  './einheitendatenbank/',
  './einheitenrechner/',
  './pf-rechner/',
  './pt-rechner/',
  './siemens-analogwert-rechner/',
  './spannungsfall-rechner/',
  './werkstoffdatenbank/',
  './wissensdatenbank/',
  './wissensdatenbank/air-torque-antrieb-drehrichtung/',
  './wissensdatenbank/endress-hauser-promass-einbaulage/',
  './wissensdatenbank/siemens-sitrans-p320-sil-verriegelung/',
  './wissensdatenbank/siemens-sps-rohwert/',
  './wissensdatenbank/vacon-frequenzumrichter-ist-sollwert-abweichung/',
  './wissensdatenbank/werkstoff-nachschlagewerk/',
  './manifest-v2-6-5-2.webmanifest',
  './assets/app-v2-6-5-2.css',
  './assets/app-v2-6-5-2.js',
  './assets/analogsignal-rechner.js',
  './assets/einheitenrechner.js',
  './assets/knowledge-compact.js',
  './assets/knowledge-overview.js',
  './assets/materials.js',
  './assets/pf-rechner.js',
  './assets/pt-rechner.js',
  './assets/siemens-analogwert-rechner.js',
  './assets/unit-database-page.js',
  './assets/unit-system.js',
  './spannungsfall-rechner/calculator.js',
  './assets/materials.json',
  './assets/units.json',
  './assets/search-index-v2-6-5-2.json',
  './assets/pct-controls.svg',
  './assets/logo-sk-pct-tools.png',
  './assets/header-logo-simple.png',
  './assets/release-module-v2-6-5-2.png',
  './assets/favicon.png',
  './assets/apple-touch-icon.png',
  './assets/icon-192.png',
  './assets/icon-512.png',
  './assets/icon-maskable-192.png',
  './assets/icon-maskable-512.png',
  './assets/navigation-icons/v2-6-5-2-app-analogsignal.png',
  './assets/navigation-icons/v2-6-5-2-app-eh-viewer.png',
  './assets/navigation-icons/v2-6-5-2-app-einheitendatenbank.png',
  './assets/navigation-icons/v2-6-5-2-app-einheitenrechner.png',
  './assets/navigation-icons/v2-6-5-2-app-pf-rechner.png',
  './assets/navigation-icons/v2-6-5-2-app-pt-rechner.png',
  './assets/navigation-icons/v2-6-5-2-app-siemens-rohwert.png',
  './assets/navigation-icons/v2-6-5-2-app-spannungsfall.png',
  './assets/navigation-icons/v2-6-5-2-app-werkstoffdatenbank.png',
  './assets/navigation-icons/v2-6-5-2-app-wissensdatenbank.png',
  './assets/navigation-icons/v2-6-5-2-knowledge-air-torque-antrieb-drehrichtung.png',
  './assets/navigation-icons/v2-6-5-2-knowledge-endress-hauser-promass-einbaulage.png',
  './assets/navigation-icons/v2-6-5-2-knowledge-siemens-sitrans-p320-sil-verriegelung.png',
  './assets/navigation-icons/v2-6-5-2-knowledge-siemens-sps-rohwert.png',
  './assets/navigation-icons/v2-6-5-2-knowledge-vacon-frequenzumrichter-ist-sollwert-abweichung.png',
  './assets/navigation-icons/v2-6-5-2-manufacturer-air-torque.png',
  './assets/navigation-icons/v2-6-5-2-manufacturer-endress-hauser.png',
  './assets/navigation-icons/v2-6-5-2-manufacturer-siemens.png',
  './assets/navigation-icons/v2-6-5-2-manufacturer-sonstiges.png',
  './assets/navigation-icons/v2-6-5-2-manufacturer-vacon.png',
  './assets/navigation-icons/v2-6-5-2-nav-back.png',
  './assets/navigation-icons/v2-6-5-2-nav-home.png',
  './assets/navigation-icons/v2-6-5-2-nav-search.png',
  './assets/navigation-icons/v2-6-5-2-nav-favorite.png'
];

const canonicalRequest=request=>{
  const url=new URL(request.url);
  url.search='';
  url.hash='';
  if(request.mode==='navigate'){
    if(url.pathname.endsWith('/index.html'))url.pathname=url.pathname.slice(0,-'index.html'.length);
    else if(!url.pathname.endsWith('/')&&!url.pathname.split('/').pop().includes('.'))url.pathname+='/';
  }
  return new Request(url.href,{method:'GET',credentials:request.credentials,mode:request.mode==='navigate'?'same-origin':request.mode});
};

async function precache(){
  const cache=await caches.open(CACHE_NAME);
  await Promise.all(CORE.map(async url=>{
    const request=new Request(url,{cache:'reload'});
    const response=await fetch(request);
    if(!response.ok)throw new Error(`Precache fehlgeschlagen: ${url} (${response.status})`);
    await cache.put(canonicalRequest(request),response);
  }));
}

self.addEventListener('install',event=>event.waitUntil(precache().then(()=>self.skipWaiting())));

self.addEventListener('activate',event=>event.waitUntil((async()=>{
  const keys=await caches.keys();
  await Promise.all(keys.filter(key=>key.startsWith(CACHE_PREFIX)&&key!==CACHE_NAME).map(key=>caches.delete(key)));
  await self.clients.claim();
  const clients=await self.clients.matchAll({type:'window',includeUncontrolled:true});
  clients.forEach(client=>client.postMessage({type:'SK_PCT_RELEASE_READY',release:RELEASE,cache:CACHE_EPOCH}));
})()));

async function navigate(request){
  const cache=await caches.open(CACHE_NAME);
  const key=canonicalRequest(request);
  try{
    const response=await fetch(request,{cache:'no-store'});
    if(response.ok)await cache.put(key,response.clone());
    return response;
  }catch{
    const home=new Request(new URL('./',self.registration.scope).href);
    return await cache.match(key)||await cache.match(canonicalRequest(home));
  }
}

async function asset(request){
  const cache=await caches.open(CACHE_NAME);
  const key=canonicalRequest(request);
  const cached=await cache.match(key);
  if(cached)return cached;
  const response=await fetch(request);
  if(response.ok)await cache.put(key,response.clone());
  return response;
}

self.addEventListener('message',event=>{if(event.data?.type==='SKIP_WAITING')self.skipWaiting()});
self.addEventListener('fetch',event=>{
  const request=event.request;
  if(request.method!=='GET'||new URL(request.url).origin!==self.location.origin)return;
  event.respondWith(request.mode==='navigate'?navigate(request):asset(request));
});
