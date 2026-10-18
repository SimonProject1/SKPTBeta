const RELEASE='3.1.0.0-Beta';
const CACHE_PREFIX='sk-pct-tools-';
const CACHE_EPOCH='v3-1-0-0-beta-core-r1';
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
  './wissensdatenbank/endress-hauser-micropilot-grundlagen-radar-fuellstandmessung/',
  './wissensdatenbank/endress-hauser-micropilot-reflexion-dk-wert/',
  './wissensdatenbank/endress-hauser-micropilot-pulse-radar-time-of-flight/',
  './wissensdatenbank/endress-hauser-micropilot-fmcw-radar-80-ghz/',
  './wissensdatenbank/endress-hauser-micropilot-frequenz-abstrahlwinkel/',
  './wissensdatenbank/endress-hauser-micropilot-produktuebersicht-geraeteauswahl/',
  './wissensdatenbank/endress-hauser-micropilot-einbauposition-antennenausrichtung/',
  './wissensdatenbank/endress-hauser-micropilot-stutzen-antenne-prozessanschluss/',
  './wissensdatenbank/endress-hauser-micropilot-sonderfaelle-einbau/',
  './wissensdatenbank/endress-hauser-micropilot-gehaeuse-anzeigemodul-ausrichten/',
  './wissensdatenbank/endress-hauser-micropilot-elektrischer-anschluss-bedienzugaenge/',
  './wissensdatenbank/endress-hauser-micropilot-grundabgleich-inbetriebnahme/',
  './wissensdatenbank/endress-hauser-micropilot-huellkurve-verstehen-auswerten/',
  './wissensdatenbank/endress-hauser-micropilot-fehler-falscher-hoher-fuellstand-stoerechoausblendung/',
  './wissensdatenbank/endress-hauser-micropilot-fehler-null-prozent-fuellstandsignal-ausgeblendet/',
  './wissensdatenbank/endress-hauser-micropilot-fehler-unplausible-distanz-stutzen-stoersignal/',
  './wissensdatenbank/endress-hauser-micropilot-fehler-ueber-hundert-prozent-ansatz-antenne/',
  './wissensdatenbank/endress-hauser-micropilot-fehler-kein-mediumsignal-medium-in-antenne/',
  './wissensdatenbank/endress-hauser-micropilot-fehler-f941-echo-verloren-tankbodenbereich/',
  './wissensdatenbank/endress-hauser-levelflex-grundlagen-gefuertes-radar-einsatz/',
  './wissensdatenbank/endress-hauser-levelflex-mikrowellen-dk-time-of-flight/',
  './wissensdatenbank/endress-hauser-levelflex-signalauswertung-huellkurve-ausblendung-differenzkurve/',
  './wissensdatenbank/endress-hauser-levelflex-sondenendsignal-eop-positive-negative-signale/',
  './wissensdatenbank/endress-hauser-levelflex-produktuebersicht-geraeteauswahl-fmp50-fmp57/',
  './wissensdatenbank/endress-hauser-levelflex-montageabstaende-seil-stabsonden/',
  './wissensdatenbank/endress-hauser-levelflex-fixierung-durchhang-abstuetzung-sonden/',
  './wissensdatenbank/endress-hauser-levelflex-stutzenabmessungen-behaelterisolation/',
  './wissensdatenbank/endress-hauser-levelflex-bypass-schwallrohr/',
  './wissensdatenbank/endress-hauser-levelflex-nichtmetallische-kunststoff-glasbehaelter/',
  './wissensdatenbank/endress-hauser-levelflex-gehaeuse-elektrischer-anschluss-bedienzugaenge/',
  './wissensdatenbank/endress-hauser-levelflex-grundabgleich-sondenlaenge-leertank-ausblendung/',
  './wissensdatenbank/endress-hauser-levelflex-mediumseigenschaft-dk-echoschwelle/',
  './wissensdatenbank/endress-hauser-levelflex-sondeneinstellungen-eop-erdung-kunststoffring/',
  './wissensdatenbank/endress-hauser-levelflex-prozesseigenschaften-echoverfolgung-blockdistanz-wartung-diagnose/',
  './wissensdatenbank/endress-hauser-levelflex-fehler-leerer-tank-25-prozent-fehlende-ausblendung/',
  './wissensdatenbank/endress-hauser-levelflex-fehler-oelfuellstand-nicht-erkannt-falscher-dk/',
  './wissensdatenbank/endress-hauser-levelflex-fehler-sondenbruch-falsche-sondenlaenge/',
  './wissensdatenbank/endress-hauser-levelflex-fehler-leerer-tank-75-prozent-kondensat-sondenanfang/',
  './manifest-v3-1-0-0-beta.webmanifest',
  './assets/app-v3-1-0-0-beta.css',
  './assets/app-v3-1-0-0-beta.js',
  './assets/analogsignal-rechner.js',
  './assets/einheitenrechner.js',
  './assets/knowledge-article.js',
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
  './assets/search-index-v3-1-0-0-beta.json',
  './assets/pct-controls.svg',
  './SIEMENS-QUELLEN-UND-GRENZWERTE.md',
  './assets/header-logo-simple.png',
  './assets/release-module-v3-1-0-0-beta.png',
  './assets/favicon-16.png',
  './assets/favicon-32.png',
  './assets/favicon.png',
  './assets/favicon.ico',
  './assets/apple-touch-icon.png',
  './assets/icon-192.png',
  './assets/icon-512.png',
  './assets/icon-maskable-192.png',
  './assets/icon-maskable-512.png',
  ...[
    'app-analogsignal','app-eh-viewer','app-einheitendatenbank','app-einheitenrechner','app-pf-rechner','app-pt-rechner','app-siemens-rohwert','app-spannungsfall','app-werkstoffdatenbank','app-wissensdatenbank',
    'manufacturer-air-torque','manufacturer-endress-hauser','manufacturer-siemens','manufacturer-sonstiges','manufacturer-vacon',
    'device-air-torque-pneumatic-actuator','device-endress-hauser-promass','device-endress-hauser-micropilot','device-endress-hauser-levelflex','knowledge-eh-levelflex-basic','knowledge-eh-levelflex-tof','knowledge-eh-levelflex-signal','knowledge-eh-levelflex-eop','knowledge-eh-levelflex-products','knowledge-eh-levelflex-distance','knowledge-eh-levelflex-fix','knowledge-eh-levelflex-nozzle','knowledge-eh-levelflex-bypass','knowledge-eh-levelflex-plastic','knowledge-eh-levelflex-access','knowledge-eh-levelflex-commission','knowledge-eh-levelflex-dk','knowledge-eh-levelflex-settings','knowledge-eh-levelflex-process','knowledge-eh-levelflex-fault-25','knowledge-eh-levelflex-fault-oil','knowledge-eh-levelflex-fault-break','knowledge-eh-levelflex-fault-75','knowledge-eh-micropilot-radar-grundlagen','knowledge-eh-micropilot-dk-reflexion','knowledge-eh-micropilot-pulse-tof','knowledge-eh-micropilot-fmcw-80ghz','knowledge-eh-micropilot-frequency-beam','knowledge-eh-micropilot-product-selection','knowledge-eh-micropilot-install-alignment','knowledge-eh-micropilot-nozzle-antenna','knowledge-eh-micropilot-special-install','knowledge-eh-micropilot-housing-display','knowledge-eh-micropilot-electrical-access','knowledge-eh-micropilot-commissioning','knowledge-eh-micropilot-envelope-curve','knowledge-eh-micropilot-fault-high-level','knowledge-eh-micropilot-fault-zero-level','knowledge-eh-micropilot-fault-nozzle','knowledge-eh-micropilot-fault-buildup','knowledge-eh-micropilot-fault-medium-antenna','knowledge-eh-micropilot-fault-f941','device-siemens-sitrans-p320','device-siemens-sps-analogkarte','device-vacon-frequenzumrichter',
    'knowledge-air-torque-antrieb-drehrichtung','knowledge-endress-hauser-promass-einbaulage','knowledge-siemens-sitrans-p320-sil-verriegelung','knowledge-siemens-sps-rohwert','knowledge-vacon-frequenzumrichter-ist-sollwert-abweichung',
    'material-1-4301','material-1-4401','material-1-4404','material-1-4408','material-1-4409','material-1-4435','material-1-4539','material-1-4571','material-2-4602','material-2-4605',
    'nav-back','nav-home','nav-search','nav-favorite'
  ].map(name=>`./assets/navigation-icons/v3-1-0-0-beta-${name}.png`)
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
