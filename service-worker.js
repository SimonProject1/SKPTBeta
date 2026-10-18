const RELEASE='2.6.6.1-Beta';
const CACHE_PREFIX='sk-pct-tools-';
const CACHE_EPOCH='v2-6-6-1-core-r1';
const CACHE_NAME=`${CACHE_PREFIX}${CACHE_EPOCH}`;

// Vollständiger Offline-Core: alle Laufzeitseiten, Daten, aktiven Icons und Markenassets.
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
  './manifest-v2-6-6-1.webmanifest',
  './assets/app-v2-6-6-1.css',
  './assets/app-v2-6-6-1.js',
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
  './assets/search-index-v2-6-6-1.json',
  './assets/pct-controls.svg',
  './SIEMENS-QUELLEN-UND-GRENZWERTE.md',
  './assets/logo-sk-pct-tools.png',
  './assets/header-logo-simple.png',
  './assets/release-module-v2-6-6-1.png',
  './assets/favicon.png',
  './assets/apple-touch-icon.png',
  './assets/icon-192.png',
  './assets/icon-512.png',
  './assets/icon-maskable-192.png',
  './assets/icon-maskable-512.png',
  ...[
    'app-analogsignal','app-eh-viewer','app-einheitendatenbank','app-einheitenrechner','app-pf-rechner','app-pt-rechner','app-siemens-rohwert','app-spannungsfall','app-werkstoffdatenbank','app-wissensdatenbank',
    'manufacturer-air-torque','manufacturer-endress-hauser','manufacturer-siemens','manufacturer-sonstiges','manufacturer-vacon',
    'device-air-torque-pneumatic-actuator','device-endress-hauser-promass','device-siemens-sitrans-p320','device-siemens-sps-analogkarte','device-vacon-frequenzumrichter',
    'knowledge-air-torque-antrieb-drehrichtung','knowledge-endress-hauser-promass-einbaulage','knowledge-siemens-sitrans-p320-sil-verriegelung','knowledge-siemens-sps-rohwert','knowledge-vacon-frequenzumrichter-ist-sollwert-abweichung',
    'material-1-4301','material-1-4401','material-1-4404','material-1-4408','material-1-4409','material-1-4435','material-1-4539','material-1-4571','material-2-4602','material-2-4605',
    'nav-back','nav-home','nav-search','nav-favorite'
  ].map(name=>`./assets/navigation-icons/v2-6-6-1-${name}.png`)
];

const canonicalRequest=request=>{
  const url=new URL(request.url);url.search='';url.hash='';
  if(request.mode==='navigate'){
    if(url.pathname.endsWith('/index.html'))url.pathname=url.pathname.slice(0,-'index.html'.length);
    else if(!url.pathname.endsWith('/')&&!url.pathname.split('/').pop().includes('.'))url.pathname+='/';
  }
  return new Request(url.href,{method:'GET',credentials:request.credentials,mode:request.mode==='navigate'?'same-origin':request.mode});
};
async function precache(){const cache=await caches.open(CACHE_NAME);await Promise.all(CORE.map(async url=>{const request=new Request(url,{cache:'reload'}),response=await fetch(request);if(!response.ok)throw new Error(`Precache fehlgeschlagen: ${url} (${response.status})`);await cache.put(canonicalRequest(request),response)}))}
self.addEventListener('install',event=>event.waitUntil(precache().then(()=>self.skipWaiting())));
self.addEventListener('activate',event=>event.waitUntil((async()=>{const keys=await caches.keys();await Promise.all(keys.filter(key=>key.startsWith(CACHE_PREFIX)&&key!==CACHE_NAME).map(key=>caches.delete(key)));await self.clients.claim();const clients=await self.clients.matchAll({type:'window',includeUncontrolled:true});clients.forEach(client=>client.postMessage({type:'SK_PCT_RELEASE_READY',release:RELEASE,cache:CACHE_EPOCH}))})()));
async function navigate(request){const cache=await caches.open(CACHE_NAME),key=canonicalRequest(request);try{const response=await fetch(request,{cache:'no-store'});if(response.ok)await cache.put(key,response.clone());return response}catch{return await cache.match(key)||await cache.match(canonicalRequest(new Request(new URL('./',self.registration.scope).href)))}}
async function asset(request){const cache=await caches.open(CACHE_NAME),key=canonicalRequest(request),cached=await cache.match(key);if(cached)return cached;const response=await fetch(request);if(response.ok)await cache.put(key,response.clone());return response}
self.addEventListener('message',event=>{if(event.data?.type==='SKIP_WAITING')self.skipWaiting()});
self.addEventListener('fetch',event=>{const request=event.request;if(request.method!=='GET'||new URL(request.url).origin!==self.location.origin)return;event.respondWith(request.mode==='navigate'?navigate(request):asset(request))});
