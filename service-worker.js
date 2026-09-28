const RELEASE='2.0.3.3-Beta.1';
const CACHE_PREFIX='sk-plt-tools-beta-';
const CACHE=`${CACHE_PREFIX}v${RELEASE}`;
const CORE=[
  './','./index.html','./manifest.webmanifest',
  './assets/styles.css','./assets/design.css','./assets/app.js',
  './assets/favorites.css','./assets/favorites.js',
  './assets/start-filter.css','./assets/start-filter.js',
  './assets/sort-tools.css','./assets/sort-tools.js',
  './assets/navigation-tree.css','./assets/navigation-tree.js','./assets/navigation-tree.json',
  './assets/search-index.json','./assets/materials.css','./assets/materials.js','./assets/materials.json',
  './assets/airttorque-wissen.css','./assets/logo-layout.css','./assets/siemens-sitrans-wissen.css','./assets/vacon-wissen.css','./assets/vde0100-600-rules.json',
  './assets/siemens-analogwert-rechner.css','./assets/siemens-analogwert-rechner.js',
  './assets/icon-192.png','./assets/icon-512.png','./assets/logo.png','./assets/logo-horizontal.png','./assets/apple-touch-icon.png','./assets/favicon.png',
  './analogsignal/','./analogsignal/index.html',
  './siemens-analogwert-rechner/','./siemens-analogwert-rechner/index.html',
  './einheitenrechner/','./einheitenrechner/index.html',
  './messstellen-doku/','./messstellen-doku/index.html',
  './pf-rechner/','./pf-rechner/index.html',
  './pt-rechner/','./pt-rechner/index.html',
  './servicewerte/','./servicewerte/index.html',
  './spannungsfall-rechner/','./spannungsfall-rechner/index.html','./spannungsfall-rechner/calculator.css','./spannungsfall-rechner/calculator.js',
  './plausibilitaetspruefung-vde0100-600/','./plausibilitaetspruefung-vde0100-600/index.html','./plausibilitaetspruefung-vde0100-600/checker.css','./plausibilitaetspruefung-vde0100-600/checker.js','./plausibilitaetspruefung-vde0100-600/logo-fallback.js',
  './wissensdatenbank/','./wissensdatenbank/index.html',
  './wissensdatenbank/air-torque-antrieb-drehrichtung/','./wissensdatenbank/air-torque-antrieb-drehrichtung/index.html',
  './wissensdatenbank/siemens-sitrans-p320-sil-verriegelung/','./wissensdatenbank/siemens-sitrans-p320-sil-verriegelung/index.html',
  './wissensdatenbank/vacon-frequenzumrichter-ist-sollwert-abweichung/','./wissensdatenbank/vacon-frequenzumrichter-ist-sollwert-abweichung/index.html',
  './wissensdatenbank/werkstoff-nachschlagewerk/','./wissensdatenbank/werkstoff-nachschlagewerk/index.html',
  './wissensdatenbank/vorlagen/Wissensdatenbank_Beitragsvorlage.pdf'
];
self.addEventListener('install',event=>{event.waitUntil((async()=>{const cache=await caches.open(CACHE);await Promise.all(CORE.map(async url=>{const request=new Request(url,{cache:'reload'});const response=await fetch(request);if(!response.ok)throw new Error(`Precache failed: ${url} (${response.status})`);await cache.put(request,response)}));await self.skipWaiting()})())});
self.addEventListener('activate',event=>{event.waitUntil((async()=>{const keys=await caches.keys();await Promise.all(keys.filter(key=>key.startsWith(CACHE_PREFIX)&&key!==CACHE).map(key=>caches.delete(key)));await self.clients.claim()})())});
async function navigation(request){const cache=await caches.open(CACHE);try{const response=await fetch(request,{cache:'no-store'});if(response.ok)await cache.put(request,response.clone());return response}catch{const exact=await cache.match(request);if(exact)return exact;const url=new URL(request.url);const indexRequest=new Request(url.pathname.endsWith('/')?new URL('index.html',url).href:url.href);return await cache.match(indexRequest)||await cache.match('./index.html')}}
async function asset(request){const cache=await caches.open(CACHE);const cached=await cache.match(request,{ignoreSearch:true});if(cached)return cached;const response=await fetch(request);if(response.ok)await cache.put(request,response.clone());return response}
self.addEventListener('fetch',event=>{const request=event.request;if(request.method!=='GET')return;if(new URL(request.url).origin!==self.location.origin)return;event.respondWith(request.mode==='navigate'?navigation(request):asset(request))});
