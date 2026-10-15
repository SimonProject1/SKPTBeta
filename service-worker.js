const RELEASE='2.6.1.3-Beta';
const CACHE_PREFIX='sk-pct-tools-';
const CACHE_EPOCH='v2-6-1-3-icons-r1';
const CORE_CACHE=`${CACHE_PREFIX}core-${CACHE_EPOCH}`;
const DOCUMENT_CACHE=`${CACHE_PREFIX}documents-${CACHE_EPOCH}`;
const CORE=[
  './',
  './analogsignal/',
  './assets/analogsignal-rechner.js',
  './assets/app-v2-6-1-3.js',
  './assets/pct-home-v2-6-1-3.css',
  './assets/pct-home-v2-6-1-3.js',
  './assets/navigation-icons/v2-6-1-3-app-analogsignal.png',
  './assets/navigation-icons/v2-6-1-3-app-eh-viewer.png',
  './assets/navigation-icons/v2-6-1-3-app-einheitendatenbank.png',
  './assets/navigation-icons/v2-6-1-3-app-einheitenrechner.png',
  './assets/navigation-icons/v2-6-1-3-app-pf-rechner.png',
  './assets/navigation-icons/v2-6-1-3-app-pt-rechner.png',
  './assets/navigation-icons/v2-6-1-3-app-siemens-rohwert.png',
  './assets/navigation-icons/v2-6-1-3-app-spannungsfall.png',
  './assets/navigation-icons/v2-6-1-3-app-werkstoffdatenbank.png',
  './assets/navigation-icons/v2-6-1-3-app-wissensdatenbank.png',
  './assets/navigation-icons/v2-6-1-3-manufacturer-air-torque.png',
  './assets/navigation-icons/v2-6-1-3-manufacturer-endress-hauser.png',
  './assets/navigation-icons/v2-6-1-3-manufacturer-siemens.png',
  './assets/navigation-icons/v2-6-1-3-manufacturer-sonstiges.png',
  './assets/navigation-icons/v2-6-1-3-manufacturer-vacon.png',
  './assets/navigation-icons/v2-6-1-3-nav-back.png',
  './assets/navigation-icons/v2-6-1-3-nav-home.png',
  './assets/pct-controls-v2-6-1-3.css',
  './assets/pct-controls-v2-6-1-3.js',
  './assets/pct-controls.svg',
  './assets/pct-frame.css',
  './assets/apple-touch-icon.png',
  './assets/core.css',
  './assets/design-system.css',
  './assets/einheitenrechner.js',
  './assets/favicon.png',
  './assets/icon-192.png',
  './assets/icon-512.png',
  './assets/icon-maskable-192.png',
  './assets/icon-maskable-512.png',
  './assets/knowledge-article.css',
  './assets/knowledge-compact.js',
  './assets/knowledge-cartoon.css',
  './assets/knowledge-overview.css',
  './assets/knowledge-overview.js',
  './assets/materials.css',
  './assets/materials.js',
  './assets/materials.json',
  './assets/pf-rechner.js',
  './assets/pt-rechner.js',
  './assets/rechner-unified.css',
  './assets/responsive.css',
  './assets/search-index-v2-6-1-3.json',
  './assets/siemens-analogwert-rechner.css',
  './assets/siemens-analogwert-rechner.js',
  './assets/unit-database-page.js',
  './assets/unit-database.css',
  './assets/unit-system.js',
  './assets/units.json',
  './einheitendatenbank/',
  './einheitenrechner/',
  './manifest-v2-6-1-3.webmanifest',
  './pf-rechner/',
  './pt-rechner/',
  './siemens-analogwert-rechner/',
  './spannungsfall-rechner/',
  './spannungsfall-rechner/calculator.js',
  './wissensdatenbank/',
  './wissensdatenbank/air-torque-antrieb-drehrichtung/',
  './wissensdatenbank/endress-hauser-promass-einbaulage/',
  './wissensdatenbank/siemens-sitrans-p320-sil-verriegelung/',
  './wissensdatenbank/siemens-sps-rohwert/',
  './werkstoffdatenbank/',
  './wissensdatenbank/vacon-frequenzumrichter-ist-sollwert-abweichung/',
  './wissensdatenbank/werkstoff-nachschlagewerk/'
];
const OPTIONAL_DOCUMENTS=[
  './WISSENSBEITRAGS-STANDARD.md',
  './SIEMENS-QUELLEN-UND-GRENZWERTE.md',
  './ICON-DESIGNRICHTLINIE.txt'
];

async function addStrict(cacheName,urls){
  const cache=await caches.open(cacheName);
  await Promise.all(urls.map(async url=>{
    const request=new Request(url,{cache:'reload'});
    const response=await fetch(request);
    if(!response.ok)throw new Error(`Precache failed: ${url} (${response.status})`);
    await cache.put(request,response);
  }));
}
async function addOptional(cacheName,urls){
  const cache=await caches.open(cacheName);
  await Promise.allSettled(urls.map(async url=>{
    const request=new Request(url,{cache:'reload'});
    const response=await fetch(request);
    if(response.ok)await cache.put(request,response);
  }));
}
self.addEventListener('install',event=>{
  event.waitUntil((async()=>{
    await addStrict(CORE_CACHE,CORE);
    await addOptional(DOCUMENT_CACHE,OPTIONAL_DOCUMENTS);
    await self.skipWaiting();
  })());
});
self.addEventListener('activate',event=>{
  event.waitUntil((async()=>{
    const keep=new Set([CORE_CACHE,DOCUMENT_CACHE]);
    const keys=await caches.keys();
    await Promise.all(keys.filter(key=>key.startsWith(CACHE_PREFIX)&&!keep.has(key)).map(key=>caches.delete(key)));
    await self.clients.claim();
    const clients=await self.clients.matchAll({type:'window',includeUncontrolled:true});
    clients.forEach(client=>client.postMessage({type:'SK_PCT_RELEASE_READY',release:RELEASE,cache:CACHE_EPOCH}));
  })());
});
function canonicalNavigation(request){
  const url=new URL(request.url);
  url.search=''; url.hash='';
  if(url.pathname.endsWith('/index.html'))url.pathname=url.pathname.slice(0,-'index.html'.length);
  else if(!url.pathname.endsWith('/')&&!url.pathname.split('/').pop().includes('.'))url.pathname+='/';
  return new Request(url.href);
}
async function navigation(request){
  const cache=await caches.open(CORE_CACHE);
  try{
    const response=await fetch(request,{cache:'no-store'});
    if(response.ok)await cache.put(canonicalNavigation(request),response.clone());
    return response;
  }catch{
    return await cache.match(canonicalNavigation(request),{ignoreSearch:true})||await cache.match('./');
  }
}
function canonicalAsset(request){
  const url=new URL(request.url);
  url.search='';
  url.hash='';
  return new Request(url.href,{method:'GET',headers:request.headers,credentials:request.credentials,mode:request.mode});
}
function isReleaseCritical(request){
  const path=new URL(request.url).pathname;
  return path.includes('/assets/navigation-icons/v2-6-1-3-')||
    path.endsWith('/assets/app-v2-6-1-3.js')||
    path.endsWith('/assets/pct-controls-v2-6-1-3.js')||
    path.endsWith('/assets/pct-controls-v2-6-1-3.css')||
    path.endsWith('/assets/pct-home-v2-6-1-3.js')||
    path.endsWith('/assets/pct-home-v2-6-1-3.css')||
    path.endsWith('/assets/search-index-v2-6-1-3.json')||
    path.endsWith('/manifest-v2-6-1-3.webmanifest');
}
async function optionalDocument(request){
  const cache=await caches.open(DOCUMENT_CACHE);
  const key=canonicalAsset(request);
  const cached=await cache.match(key);
  if(cached)return cached;
  const response=await fetch(request,{cache:'no-store'});
  if(response.ok)await cache.put(key,response.clone());
  return response;
}
async function asset(request){
  const cache=await caches.open(CORE_CACHE);
  const key=canonicalAsset(request);
  if(isReleaseCritical(request)){
    try{
      const response=await fetch(request,{cache:'reload'});
      if(response.ok)await cache.put(key,response.clone());
      return response;
    }catch{
      return await cache.match(key)||Response.error();
    }
  }
  const cached=await cache.match(key);
  if(cached)return cached;
  const response=await fetch(request);
  if(response.ok)await cache.put(key,response.clone());
  return response;
}
self.addEventListener('message',event=>{
  if(event.data?.type==='SKIP_WAITING')self.skipWaiting();
});
self.addEventListener('fetch',event=>{
  const request=event.request;
  if(request.method!=='GET'||new URL(request.url).origin!==self.location.origin)return;
  const relative=new URL(request.url).pathname.replace(new URL(self.registration.scope).pathname,'');
  if(request.mode==='navigate')event.respondWith(navigation(request));
  else if(OPTIONAL_DOCUMENTS.some(item=>item.slice(2)===relative))event.respondWith(optionalDocument(request));
  else event.respondWith(asset(request));
});
