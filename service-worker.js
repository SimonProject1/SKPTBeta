const RELEASE='2.5.0.4-Beta';
const CACHE_PREFIX='sk-pct-tools-';
const CORE_CACHE=`${CACHE_PREFIX}core-v${RELEASE}`;
const DOCUMENT_CACHE=`${CACHE_PREFIX}documents-v${RELEASE}`;
const CORE=[
  './',
  './analogsignal/',
  './assets/analogsignal-rechner.js',
  './assets/app.js',
  './assets/pct-home.css',
  './assets/pct-home.js',
  './assets/pct-home-icons.svg',
  './assets/pct-controls.css',
  './assets/pct-controls.js',
  './assets/pct-controls.svg',
  './assets/apple-touch-icon.png',
  './assets/core.css',
  './assets/einheitenrechner.js',
  './assets/favicon.png',
  './assets/icon-192.png',
  './assets/icon-512.png',
  './assets/icon-maskable-192.png',
  './assets/icon-maskable-512.png',
  './assets/knowledge-article.css',
  './assets/knowledge-cartoon.css',
  './assets/knowledge-manufacturer-logos.svg',
  './assets/knowledge-overview.css',
  './assets/knowledge-overview.js',
  './assets/logo.webp',
  './assets/materials.css',
  './assets/materials.js',
  './assets/materials.json',
  './assets/pf-rechner.js',
  './assets/pt-rechner.js',
  './assets/rechner-unified.css',
  './assets/responsive.css',
  './assets/search-index.json',
  './assets/siemens-analogwert-rechner.css',
  './assets/siemens-analogwert-rechner.js',
  './assets/unit-database-page.js',
  './assets/unit-database.css',
  './assets/unit-system.js',
  './assets/units.json',
  './einheitendatenbank/',
  './einheitenrechner/',
  './manifest.webmanifest',
  './messstellen-doku/',
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
  './wissensdatenbank/vorlagen/Wissensdatenbank_Beitragsvorlage.pdf'
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
    await Promise.all(keys.filter(key=>key.startsWith('sk-')&&key.includes('-tools-')&&!keep.has(key)).map(key=>caches.delete(key)));
    await self.clients.claim();
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
async function optionalDocument(request){
  const cache=await caches.open(DOCUMENT_CACHE);
  const cached=await cache.match(request,{ignoreSearch:true});
  if(cached)return cached;
  const response=await fetch(request);
  if(response.ok)await cache.put(request,response.clone());
  return response;
}
async function asset(request){
  const cache=await caches.open(CORE_CACHE);
  const cached=await cache.match(request,{ignoreSearch:true});
  if(cached)return cached;
  const response=await fetch(request);
  if(response.ok)await cache.put(request,response.clone());
  return response;
}
self.addEventListener('fetch',event=>{
  const request=event.request;
  if(request.method!=='GET'||new URL(request.url).origin!==self.location.origin)return;
  const relative=new URL(request.url).pathname.replace(new URL(self.registration.scope).pathname,'');
  if(request.mode==='navigate')event.respondWith(navigation(request));
  else if(OPTIONAL_DOCUMENTS.some(item=>item.slice(2)===relative))event.respondWith(optionalDocument(request));
  else event.respondWith(asset(request));
});
