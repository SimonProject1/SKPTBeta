#!/usr/bin/env node
'use strict';
const fs=require('fs'),vm=require('vm'),path=require('path');
const ROOT=path.resolve(__dirname,'..'),VERSION='2.1.7.1-Beta';
const read=file=>fs.readFileSync(path.join(ROOT,file),'utf8');
const json=file=>JSON.parse(read(file));
function ok(condition,label){if(!condition)throw new Error(label);console.log(`OK ${label}`)}
function equal(actual,expected,label){if(actual!==expected)throw new Error(`${label}: erwartet ${expected}, erhalten ${actual}`);console.log(`OK ${label}: ${actual}`)}
function close(actual,expected,tolerance,label){if(Math.abs(actual-expected)>tolerance)throw new Error(`${label}: erwartet ${expected} ± ${tolerance}, erhalten ${actual}`);console.log(`OK ${label}: ${actual}`)}

const data=json('assets/units.json');
equal(data.release,VERSION,'Einheitendatenbank Release');
equal(data.categories.length,19,'Einheitendatenbank Kategorien');
equal(data.categories.reduce((sum,entry)=>sum+entry.units.length,0),115,'Einheitendatenbank Einheiten');
const category=id=>data.categories.find(item=>item.id===id);
const unit=(categoryId,unitId)=>category(categoryId).units.find(item=>item.id===unitId);
const toBase=(value,categoryId,unitId)=>value*unit(categoryId,unitId).toBase.factor+(unit(categoryId,unitId).toBase.offset||0);
const fromBase=(value,categoryId,unitId)=>(value-(unit(categoryId,unitId).toBase.offset||0))/unit(categoryId,unitId).toBase.factor;
const convert=(value,categoryId,from,to)=>fromBase(toBase(value,categoryId,from),categoryId,to);
for(const entry of data.categories){ok(entry.units.some(item=>item.id===entry.defaultUnit),`${entry.name}: feste Standardeinheit vorhanden`);for(const item of entry.units){for(const value of [-273.15,-1,0,1,123.456]){const roundTrip=convert(convert(value,entry.id,item.id,entry.defaultUnit),entry.id,entry.defaultUnit,item.id);close(roundTrip,value,Math.max(1e-9,Math.abs(value)*1e-10),`${entry.id}/${item.id}: Roundtrip ${value}`)}}}
const requiredDefaults={pressure:'bar',temperature:'celsius',volumeFlow:'cubic_metre_hour',length:'metre',voltage:'volt',current:'ampere',resistance:'ohm'};
for(const [id,expected] of Object.entries(requiredDefaults))equal(category(id).defaultUnit,expected,`${id}: geforderte Grundeinheit`);
for(const test of data.validationCases)close(convert(test.input,test.category,test.from,test.to),test.expected,1e-10,`Referenzfall ${test.category} ${test.from}→${test.to}`);
close(convert(32,'temperature','fahrenheit','celsius'),0,1e-12,'Offset 32 °F = 0 °C');
close(convert(-40,'temperature','celsius','fahrenheit'),-40,1e-12,'Offset −40 °C = −40 °F');

const unitRuntime=read('assets/unit-system.js');
ok(unitRuntime.includes("const STORAGE_KEY='skPltUnitFavoritesV1'"),'Einheitenfavoriten eigener Local-Storage-Schlüssel');
ok(unitRuntime.includes('localStorage.setItem(STORAGE_KEY'),'Einheitenfavoriten persistent gespeichert');
ok(unitRuntime.includes("standard.label='Standardeinheit'")&&unitRuntime.includes("favoriteGroup.label='Favoriten'"),'Einheitliches Dropdown gruppiert Standard und Favoriten');
ok(unitRuntime.includes("new CustomEvent('sk:unit-change'")&&unitRuntime.includes('convertTargets'),'Automatische Wertumrechnung bei Einheitenwechsel');

const calculatorPages=['analogsignal/index.html','einheitenrechner/index.html','pf-rechner/index.html','pt-rechner/index.html','spannungsfall-rechner/index.html','siemens-analogwert-rechner/index.html'];
for(const file of calculatorPages){const html=read(file),inputs=[...html.matchAll(/<input\b[^>]*\btype="number"[^>]*>/g)].map(match=>match[0]);ok(inputs.length>0,`${file}: Zahlenfelder vorhanden`);ok(inputs.every(input=>/\binputmode="(?:decimal|numeric)"/.test(input)),`${file}: mobile Zahlentastatur für alle Zahlenfelder`);ok(html.includes('unit-system.js'),`${file}: zentrale Einheitendatenbank eingebunden`);equal((html.match(/class="sk-unit-database-cta"/g)||[]).length,1,`${file}: genau ein Datenbank-Sprung am Seitenende`);ok(html.includes('class="sk-unit-database-button" href="../einheitendatenbank/"'),`${file}: Datenbank-Sprung zeigt auf die Einheitendatenbank`);ok(html.lastIndexOf('sk-unit-database-cta')<html.lastIndexOf('</main>'),`${file}: Datenbank-Sprung innerhalb des Hauptinhalts`)}
for(const file of ['assets/analogsignal-rechner.js','assets/einheitenrechner.js','assets/pf-rechner.js','assets/pt-rechner.js','spannungsfall-rechner/calculator.js','assets/siemens-unit-integration.js'])ok(read(file).includes('SK_UNITS'),`${file}: zentrale Umrechnungs-API verwendet`);

close(4+(50-0)/(100-0)*(20-4),12,1e-12,'Analogsignal 0…100 → 4…20 mA');
close((20-4)/(100-0),0.16,1e-12,'P+F K-Faktor');
function resistance(t,r0){const A=3.9083e-3,B=-5.775e-7,C=-4.183e-12;return t>=0?r0*(1+A*t+B*t*t):r0*(1+A*t+B*t*t+C*(t-100)*t*t*t)}
close(resistance(0,100),100,1e-12,'Pt100 bei 0 °C');close(resistance(100,100),138.5055,1e-6,'Pt100 bei 100 °C');
const drop=Math.sqrt(3)*35*16/(56*2.5);close(drop,6.928203230275509,1e-12,'Spannungsfall Referenzrechnung');

{
 const context={console,Math,Number,Object,Array,String,Intl,Error,globalThis:null};context.globalThis=context;vm.createContext(context);vm.runInContext(read('assets/siemens-analogwert-rechner.js'),context,{filename:'siemens-analogwert-rechner.js'});const api=context.SK_SIEMENS_ANALOG,result=api.calculate('4-20mA','raw',13824,'et200sp_st',{min:-50,max:150,unit:'°C'});equal(result.raw,13824,'Siemens Rohwert');close(result.signal,12,1e-12,'Siemens Signal');close(result.physical,50,1e-12,'Siemens physikalischer Wert');equal(api.statusForRaw(32512,'et200sp_st','4-20mA'),'overflow','Siemens Überlaufgrenze');equal(api.toggleSignValue(12),-12,'Siemens ±-Vorzeichenwechsel');
}

const pages=[...function*(){function* walk(dir=''){for(const name of fs.readdirSync(path.join(ROOT,dir))){const rel=path.join(dir,name),full=path.join(ROOT,rel),stat=fs.statSync(full);if(stat.isDirectory()&&!['tools','test-artifacts','shared'].includes(name))yield* walk(rel);else if(name==='index.html')yield rel.replaceAll('\\','/')}}yield* walk()}()];
equal(pages.length,16,'HTML-Seiten einschließlich Einheitendatenbank');
for(const file of pages)ok(read(file).includes(`data-sk-version="${VERSION}"`),`${file}: Version konsistent`);
const databaseHtml=read('einheitendatenbank/index.html');ok(databaseHtml.includes('id="unitSearch"')&&databaseHtml.includes('id="unitCategoryFilter"'),'Einheitendatenbank Suche und Kategorienfilter');
const nav=json('assets/navigation-tree.json');ok(nav.groups.some(group=>group.items.some(item=>item.url==='einheitendatenbank/')),'Navigation enthält Einheitendatenbank');
const search=json('assets/search-index.json');ok(search.some(item=>item.url==='einheitendatenbank/'&&item.keywords.includes('Viskosität')),'Suchindex enthält Einheitendatenbank und Kategorien');
const sw=read('service-worker.js');for(const item of ['./assets/units.json','./assets/unit-system.js','./einheitendatenbank/','./einheitendatenbank/index.html'])ok(sw.includes(`"${item}"`),`Offline-Precache enthält ${item}`);
const manifest=json('manifest.webmanifest');equal(manifest.version,VERSION,'Manifest-Version');equal(manifest.id,`./?app=sk-plt-tools-${VERSION.toLowerCase()}`,'Manifest-App-ID');
const start=read('index.html');equal((start.match(/<a\b[^>]*class="[^"]*\bcard\b[^"]*"/g)||[]).length,10,'Startseite Werkzeugkacheln');ok(start.includes('href="einheitendatenbank/"'),'Startseite Einheitendatenbank-Kachel');
const core=read('assets/core.css'),responsive=read('assets/responsive.css'),app=read('assets/app.js');ok(responsive.includes('safe-area-inset-bottom')&&responsive.includes('safe-area-inset-top'),'iPhone Safe Areas erhalten');ok(core.includes('.sk-favorites-trigger')&&core.includes('.sk-tree-trigger'),'Mobile untere Bedienzone erhalten');ok(core.includes('.sk-unit-database-cta')&&core.includes('.sk-unit-database-button'),'Einheitendatenbank-Sprung zentral gestaltet');ok(app.includes("button.textContent='±'")||read('assets/siemens-analogwert-rechner.js').includes('toggleSignValue'),'±-Vorzeichenwechsel erhalten');
console.log('OK: Einheitendatenbank, Favoriten, Umrechnungen, Rechner und PWA-Integration funktional geprüft.');
