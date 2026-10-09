#!/usr/bin/env node
'use strict';
const fs=require('fs');const vm=require('vm');const path=require('path');
const ROOT=path.resolve(__dirname,'..');
function baseContext(){
  const context={console,URL,Number,Intl,Math,JSON,Array,String,RegExp,Object,Error,setTimeout:()=>0,clearTimeout:()=>{},location:{href:'http://localhost/',pathname:'/'},navigator:{},Event:function(type,options){this.type=type;Object.assign(this,options||{})}};
  context.window=context;
  context.document={currentScript:{src:'http://localhost/assets/app.js'},readyState:'loading',addEventListener:()=>{},querySelectorAll:()=>[],getElementById:()=>null,body:{dataset:{}}};
  vm.createContext(context);vm.runInContext(fs.readFileSync(path.join(ROOT,'assets/app.js'),'utf8'),context,{filename:'assets/app.js'});return context;
}
function inlineScript(file,needle){const html=fs.readFileSync(path.join(ROOT,file),'utf8'),scripts=[...html.matchAll(/<script(?:\s[^>]*)?>([\s\S]*?)<\/script>/gi)].map(match=>match[1]);const found=scripts.find(text=>text.includes(needle));if(!found)throw new Error(`Inline-Skript nicht gefunden: ${file}`);return found}
function assertEqual(actual,expected,label){if(actual!==expected)throw new Error(`${label}: erwartet ${expected}, erhalten ${actual}`);console.log(`OK ${label}: ${actual}`)}
function assertClose(actual,expected,tolerance,label){if(Math.abs(actual-expected)>tolerance)throw new Error(`${label}: erwartet ${expected} ± ${tolerance}, erhalten ${actual}`);console.log(`OK ${label}: ${actual}`)}
function assertThrows(callback,needle,label){let message='';try{callback()}catch(error){message=error.message}if(!message.includes(needle))throw new Error(`${label}: erwartete Fehlermeldung mit ${needle}, erhalten ${message||'keine Fehlermeldung'}`);console.log(`OK ${label}: ${message}`)}
function runInline(file,needle,values,assertions,setup){const context=baseContext();Object.assign(context,values);if(setup)setup(context);vm.runInContext(inlineScript(file,needle),context,{filename:file});for(const [key,expected] of Object.entries(assertions))assertEqual(context[key].textContent,expected,`${file} ${key}`)}
runInline('analogsignal/index.html','function calc()',{
 p0:{value:'0'},p1:{value:'100'},s0:{value:'4'},s1:{value:'20'},dir:{value:'ps'},x:{value:'50'},out:{textContent:''},pct:{textContent:''}
},{out:'12,000 mA',pct:'50,0 %'});
runInline('pf-rechner/index.html','function calc()',{
 x1:{value:'0'},y1:{value:'4'},x2:{value:'100'},y2:{value:'20'},k:{textContent:''},n:{textContent:''}
},{k:'0,160000',n:'4,000000'});
runInline('pt-rechner/index.html','function r(t,r0)',{
 sensor:{value:'100'},dir:{value:'tr'},x:{value:'0'},out:{textContent:''}
},{out:'100,000 Ω'});
{
 const context=baseContext();
 function select(){let options=[];let index=0;const object={oninput:null,onchange:null};Object.defineProperty(object,'innerHTML',{set(value){options=[...String(value).matchAll(/<option>(.*?)<\/option>/g)].map(match=>match[1]);index=0}});Object.defineProperty(object,'selectedIndex',{set(value){index=value}});Object.defineProperty(object,'value',{get(){return options[index]||''},set(value){const found=options.indexOf(value);if(found>=0)index=found}});return object}
 Object.assign(context,{cat:{value:'Druck'},from:select(),to:select(),x:{value:'1'},out:{textContent:''}});
 vm.runInContext(inlineScript('einheitenrechner/index.html','const U='),context,{filename:'einheitenrechner/index.html'});
 assertEqual(context.out.textContent,'1.000,000 mbar','Einheitenrechner 1 bar in mbar');
}
{
 const elements={system:{value:'three'},voltagePreset:{value:'400'},customVoltage:{value:'500'},customVoltageLabel:{hidden:true},current:{value:'16',addEventListener:()=>{}},length:{value:'35',addEventListener:()=>{}},area:{value:'2.5'},material:{value:'56'},cosphi:{value:'1.00',addEventListener:()=>{}},limit:{value:'6.0',addEventListener:()=>{}},calculate:{},reset:{},result:{hidden:true,scrollIntoView:()=>{}},statusBadge:{className:'',textContent:''},dropV:{textContent:''},dropPercent:{textContent:''},loadVoltage:{textContent:''},permittedV:{textContent:''},reserve:{textContent:''},protocolV:{textContent:''},protocolPercent:{textContent:''},formula:{textContent:''}};
 const context={console,Math,Number,Intl,Array,String,document:{readyState:'complete',getElementById:id=>elements[id],querySelectorAll:selector=>selector==='input'?[elements.current,elements.length,elements.cosphi,elements.limit]:[]},alert:message=>{throw new Error(message)}};vm.createContext(context);vm.runInContext(fs.readFileSync(path.join(ROOT,'spannungsfall-rechner/calculator.js'),'utf8'),context,{filename:'calculator.js'});elements.calculate.onclick();
 assertEqual(elements.dropV.textContent,'6,93 V','Spannungsfall ΔU');assertEqual(elements.dropPercent.textContent,'1,73 %','Spannungsfall Prozent');assertEqual(elements.loadVoltage.textContent,'393,07 V','Spannungsfall Lastspannung');assertEqual(elements.reserve.textContent,'+17,07 V','Spannungsfall Reserve');
}
{
  const context={console,window:{}};
  vm.createContext(context);
  vm.runInContext(fs.readFileSync(path.join(ROOT,'assets/materials.js'),'utf8'),context,{filename:'assets/materials.js'});
  const api=context.window.SK_MATERIALS;
  if(!api)throw new Error('Werkstoff-Suchfunktionen wurden nicht exportiert.');
  const data=JSON.parse(fs.readFileSync(path.join(ROOT,'assets/materials.json'),'utf8'));
  const ids=(query,group='all')=>api.filterMaterials(data.materials,query,group).map(item=>item.id).sort().join(',');
  assertEqual(ids('316L'),'1-4404,1-4409,1-4435','Werkstoffsuche 316L Mehrfachtreffer');
  assertEqual(ids('1.4404'),'1-4404','Werkstoffsuche 1.4404');
  assertEqual(ids('14404'),'1-4404','Werkstoffsuche 14404 ohne Punkt');
  assertEqual(ids('CF8M'),'1-4408','Werkstoffsuche CF8M');
  assertEqual(ids('316L','cast-stainless'),'1-4409','Werkstofffilter 316L Stahlguss');
  assertEqual(ids('Alloy 59'),'2-4605','Werkstoffsuche Alloy 59');
}
{
  const html=fs.readFileSync(path.join(ROOT,'wissensdatenbank/index.html'),'utf8');
  const tiles=[...html.matchAll(/<a class="([^"]*\bknowledge-entry\b[^"]*)"[^>]*href="([^"]+)"/g)].map(match=>({classes:match[1].split(/\s+/),href:match[2]}));
  assertEqual(tiles.length,5,'Wissensdatenbank Anzahl Wissenskacheln');
  const expected=['air-torque-antrieb-drehrichtung/','siemens-sitrans-p320-sil-verriegelung/','siemens-sps-rohwert/','vacon-frequenzumrichter-ist-sollwert-abweichung/','werkstoff-nachschlagewerk/'];
  assertEqual(tiles.map(tile=>tile.href).sort().join(','),expected.join(','),'Wissensdatenbank erwartete Kachelziele');
  assertEqual(tiles.every(tile=>tile.classes.includes('tool-card')),true,'Wissensdatenbank alle Kacheln favoritenfähig');
   const article=fs.readFileSync(path.join(ROOT,'wissensdatenbank/siemens-sps-rohwert/index.html'),'utf8');
   assertEqual(article.includes('4 mA  =     0')&&article.includes('12 mA = 13824'),true,'Rohwertartikel 4–20-mA-Parametrierung');
   assertEqual(article.includes('4 mA  =  5530')&&article.includes('12 mA = 16589'),true,'Rohwertartikel 0–20-mA-Bezugsweise getrennt');
   assertEqual(article.includes('Rohwert = 13824'),true,'Rohwertartikel Praxisbeispiel konsistent');
  const favorites=fs.readFileSync(path.join(ROOT,'assets/app.js'),'utf8');
  assertEqual(favorites.includes("const KEY='skPltToolsFavoritesV2'"),true,'Favoriten bestehender Speicherschlüssel');
  assertEqual(favorites.includes('localStorage.setItem(KEY'),true,'Favoriten persistente Speicherung');
  assertEqual(favorites.includes('event.preventDefault()')&&favorites.includes('event.stopPropagation()'),true,'Favoriten Sternklick ohne Kachelnavigation');
}
{
  const html=fs.readFileSync(path.join(ROOT,'wissensdatenbank/werkstoff-nachschlagewerk/index.html'),'utf8');
  const breadcrumb=html.match(/<nav aria-label="Brotkrümelnavigation" class="knowledge-breadcrumb">([\s\S]*?)<\/nav>/i);
  assertEqual(Boolean(breadcrumb),true,'Werkstoffseite Brotkrümelnavigation vorhanden');
  const links=[...breadcrumb[1].matchAll(/<a href="([^"]+)">([^<]+)<\/a>/g)].map(match=>`${match[2]}:${match[1]}`).join(',');
  assertEqual(links,'Startseite:../../,Wissensdatenbank:../','Werkstoffseite Breadcrumb-Linkziele');
  const labels=breadcrumb[1].replace(/<[^>]+>/g,' ').replace(/\s+/g,' ').trim();
  assertEqual(labels,'Startseite › Wissensdatenbank › Werkstoff-Nachschlagewerk','Werkstoffseite Breadcrumb-Beschriftung');
}
{
  const vacon=fs.readFileSync(path.join(ROOT,'wissensdatenbank/vacon-frequenzumrichter-ist-sollwert-abweichung/index.html'),'utf8');
  assertEqual(vacon.includes('Parameter 2.2.3.7'),true,'Vacon Parameterhinweis vorhanden');
  assertEqual(vacon.includes('maximale Frequenz'),true,'Vacon Soll-Einstellung vorhanden');
}
{
  const context={console,Math,Number,Object,Array,String,Intl,Error,globalThis:null};context.globalThis=context;vm.createContext(context);
  vm.runInContext(fs.readFileSync(path.join(ROOT,'assets/siemens-analogwert-rechner.js'),'utf8'),context,{filename:'siemens-analogwert-rechner.js'});
  const api=context.SK_SIEMENS_ANALOG,calc=api.calculate;
   const temperature={min:-50,max:150,unit:'°C'};
   let result=calc('4-20mA','raw',13824,'et200sp_st',temperature);
  assertEqual(result.raw,13824,'Siemens 4–20 mA Rohwert');assertEqual(result.signal,12,'Siemens 4–20 mA Signal');assertEqual(result.percent,50,'Siemens 4–20 mA Nennbereichsanteil');assertEqual(result.status,'nominal','Siemens ET 200SP Nennbereich');
   assertEqual(result.physical,50,'Siemens negativer Temperatur-Messbereich aus Rohwert');assertEqual(result.physicalRange.unit,'°C','Siemens frei gewählte Temperatureinheit');
   result=calc('4-20mA','signal',8,'et200sp_st',temperature);assertEqual(result.raw,6912,'Siemens Signal zu Rohwert mit Messbereich');assertEqual(result.percent,25,'Siemens Signal zu Prozent');assertEqual(result.physical,0,'Siemens Signal zu physikalischem Istwert');
   result=calc('4-20mA','physical',0,'et200sp_st',temperature);assertEqual(result.raw,6912,'Siemens physikalischer Istwert zu Rohwert');assertEqual(result.signal,8,'Siemens physikalischer Istwert zu Signal');assertEqual(result.percent,25,'Siemens physikalischer Istwert zu Prozent');
   result=calc('4-20mA','raw',27648,'et200sp_st',{min:-1,max:9,unit:'bar'});assertEqual(result.physical,9,'Siemens frei gewählte Druckeinheit und Messbereich');assertEqual(result.physicalRange.unit,'bar','Siemens frei gewählte Druckeinheit');
   result=calc('4-20mA','raw',-4864,'et200sp_st',temperature);assertEqual(result.status,'underrange','Siemens Unterbereich mit physikalischer Extrapolation');assertClose(result.physical,-85.1851851852,1e-9,'Siemens physikalischer Unterbereich');
   result=calc('4-20mA','raw',27649,'et200sp_st',temperature);assertEqual(result.status,'overrange','Siemens Überbereich mit physikalischer Extrapolation');assertClose(result.physical,150.0072337963,1e-9,'Siemens physikalischer Überbereich');
   assertThrows(()=>calc('4-20mA','physical',10,'et200sp_st',{min:10,max:10,unit:'°C'}),'größer als das Minimum','Siemens identische Messbereichsgrenzen abgewiesen');
   assertThrows(()=>calc('4-20mA','raw',0,'et200sp_st',{min:0,max:100,unit:'  '}),'Einheit','Siemens leere Einheit abgewiesen');
  result=calc('0-20mA','signal',20,'et200sp_st');
  assertEqual(result.raw,27648,'Siemens 0–20 mA Signal zu Rohwert');assertEqual(result.signal,20,'Siemens 0–20 mA Rückrechnung');
  result=calc('2-10V','raw',20736,'generic_scale');assertEqual(result.signal,8,'Siemens generische 2–10 V Skalierung');assertEqual(result.status,'scaleOnly','Generische Skalierung ohne Diagnosegrenzen');
  assertEqual(Object.keys(api.PROFILES).length,5,'Siemens fünf Karten-/Skalierungsprofile');
  assertEqual(api.statusForRaw(-4865,'et200sp_st','4-20mA'),'underflow','ET 200SP Unterlauf beginnt bei −4.865');
  assertEqual(api.statusForRaw(-4864,'et200sp_st','4-20mA'),'underrange','ET 200SP Untersteuerung beginnt bei −4.864');
  assertEqual(api.statusForRaw(32511,'et200sp_st','4-20mA'),'overrange','ET 200SP Übersteuerung bis 32.511');
  assertEqual(api.statusForRaw(32512,'et200sp_st','4-20mA'),'overflow','ET 200SP Überlauf beginnt bei 32.512');
  assertEqual(api.statusForRaw(-691,'et200spha_on','4-20mA'),'underflow','ET 200SP HA NE43 Unterlauf ab −691');
  assertEqual(api.statusForRaw(-690,'et200spha_on','4-20mA'),'underrange','ET 200SP HA NE43 untere Hysterese');
  assertEqual(api.statusForRaw(29375,'et200spha_on','4-20mA'),'overrange','ET 200SP HA NE43 obere Hysterese');
  assertEqual(api.statusForRaw(29376,'et200spha_on','4-20mA'),'overflow','ET 200SP HA NE43 Überlauf ab 29.376');
  assertEqual(api.profileScale('4-20mA','et200sp_st','raw').join(','),'-32768,-4865,0,27648,32512,32767','Siemens Rohwertskala mit sechs Profilgrenzen');
  const b=api.boundaries('et200sp_st','4-20mA');assertEqual(b.under<b.nomStart&&b.nomStart<b.nomEnd&&b.nomEnd<b.overflow,true,'Siemens feste Farbbereiche sortiert');
}
{
  class MockElement{
    constructor(id=''){this.id=id;this.value='';this._textContent='';this.hidden=false;this.dataset={};this.children=[];this.attributes={};this.listeners={};this.min='';this.max='';this.step='';this.options=[];this.href='';this.style={values:{},setProperty:(name,value)=>{this.style.values[name]=String(value)}};this.classList={toggle:()=>{},remove:()=>{}};Object.defineProperty(this,'textContent',{get:()=>this._textContent,set:value=>{this._textContent=String(value);if(value==='')this.children=[]}})}
    addEventListener(type,handler){this.listeners[type]=handler}
    dispatch(type){if(this.listeners[type])this.listeners[type]({type,target:this})}
    setAttribute(name,value){this.attributes[name]=String(value)}
    append(child){this.children.push(child);return child}
    replaceChildren(...children){this.children=[...children]}
  }
  const ids=['cardProfile','signalType','inputKind','inputValue','inputValueLabel','inputSuffix','physicalMin','physicalMax','physicalUnit','valueSlider','sliderLabel','sliderScale','sliderReadout','rawResult','signalResult','percentResult','physicalResult','rangeStatus','statusDetail','stateStrip','profileSourceLink','calculationError'];
  const elements=Object.fromEntries(ids.map(id=>[id,new MockElement(id)]));
  elements.cardProfile.value='et200sp_st';elements.signalType.value='4-20mA';elements.inputKind.value='raw';elements.inputValue.value='13824';
  elements.physicalMin.value='-50';elements.physicalMax.value='150';elements.physicalUnit.value='°C';
  elements.signalType.options=['4-20mA','0-20mA','0-10V','2-10V'].map(value=>({value,disabled:false}));
  const states=['underflow','underrange','nominal','overrange','overflow'].map(key=>{const item=new MockElement();item.dataset.stateKey=key;return item});
  const document={getElementById:id=>elements[id]||null,querySelectorAll:selector=>selector==='[data-state-key]'?states:[],createElement:()=>new MockElement()};
  const context={console,Math,Number,Object,Array,String,Intl,Error,document,globalThis:null};context.globalThis=context;vm.createContext(context);
  vm.runInContext(fs.readFileSync(path.join(ROOT,'assets/siemens-analogwert-rechner.js'),'utf8'),context,{filename:'siemens-analogwert-rechner-ui.js'});
  const scale=()=>elements.sliderScale.children.map(item=>item.textContent).join('|');
  assertEqual(elements.rawResult.textContent,'13.824','Siemens UI Start-Rohwert');assertEqual(elements.signalResult.textContent,'12,000 mA','Siemens UI Start-Signalwert');assertEqual(elements.physicalResult.textContent,'50,000 °C','Siemens UI Start-Istwert');
  assertEqual(scale(),'-32.768|-4.865|0|27.648|32.512|32.767','Siemens UI Standard-Rohwertskala');
  elements.inputKind.value='signal';elements.inputKind.dispatch('change');assertEqual(Number(elements.inputValue.value),12,'Siemens UI Eingaberichtung synchronisiert Wert');
  elements.signalType.value='0-20mA';elements.signalType.dispatch('change');assertEqual(Number(elements.inputValue.value),10,'Siemens UI Signalbereich erhält Rohwert');
  elements.valueSlider.value='15';elements.valueSlider.dispatch('input');assertEqual(elements.rawResult.textContent,'20.736','Siemens UI Signalregler aktualisiert Rohwert');
  elements.signalType.value='4-20mA';elements.signalType.dispatch('change');
  elements.inputKind.value='physical';elements.inputKind.dispatch('change');assertEqual(Number(elements.inputValue.value),100,'Siemens UI physikalische Eingaberichtung synchronisiert Istwert');
  elements.inputValue.value='0';elements.inputValue.dispatch('input');assertEqual(elements.rawResult.textContent,'6.912','Siemens UI Istwert aktualisiert Rohwert');assertEqual(elements.signalResult.textContent,'8,000 mA','Siemens UI Istwert aktualisiert Signal');assertEqual(elements.percentResult.textContent,'25,0 %','Siemens UI Istwert aktualisiert Prozent');
  elements.physicalUnit.value='bar';elements.physicalUnit.dispatch('input');assertEqual(elements.physicalResult.textContent,'0,000 bar','Siemens UI frei wählbare Einheit');assertEqual(elements.inputSuffix.textContent,'bar','Siemens UI Einheit am Eingabefeld');
  elements.physicalMin.value='-100';elements.physicalMax.value='100';elements.physicalMax.dispatch('change');assertEqual(elements.physicalResult.textContent,'-50,000 bar','Siemens UI geänderter negativer Messbereich hält Rohwert');
  elements.inputKind.value='raw';elements.inputKind.dispatch('change');assertEqual(elements.inputValue.value,'6912','Siemens UI Rückkehr zur Rohwerteingabe synchron');
  elements.cardProfile.value='et200spha_on';elements.cardProfile.dispatch('change');elements.inputValue.value='-691';elements.inputValue.dispatch('input');assertEqual(elements.rangeStatus.textContent,'Unterlauf','Siemens UI NE43 Unterlaufgrenze');
  assertEqual(elements.sliderScale.children[1].textContent,'-691','Siemens UI NE43 Rohwertskala');assertEqual(Boolean(elements.valueSlider.style.values['--b1']),true,'Siemens UI setzt feste Bereichsgrenze');
  elements.cardProfile.value='s71500_fai_scale';elements.cardProfile.dispatch('change');assertEqual(elements.rangeStatus.textContent,'Nur Umrechnung','F-AI Profil ohne unbestätigte Diagnosegrenzen');assertEqual(elements.stateStrip.hidden,true,'F-AI blendet unbestätigte Grenzbereiche aus');
}
{
  const html=fs.readFileSync(path.join(ROOT,'index.html'),'utf8');
  const external=html.match(/<a[^>]*class="[^"]*sk-external-card[^"]*"[^>]*href="([^"]+)"[^>]*>/i);
  assertEqual(Boolean(external),true,'E+H Device Viewer Kachel vorhanden');
  assertEqual(external[1],'https://netilion.endress.com/app/library/device_viewer','E+H Device Viewer Zieladresse');
  assertEqual(/target="_blank"/.test(external[0]),true,'E+H Device Viewer neuer Tab');
  assertEqual(/rel="external noopener noreferrer"/.test(external[0]),true,'E+H Device Viewer sichere Externkennzeichnung');
  assertEqual(/referrerpolicy="no-referrer"/.test(external[0]),true,'E+H Device Viewer ohne Referrer');
  assertEqual(/data-filter="EXTERN"/.test(html),true,'Filter Externe Dienste vorhanden');
}
console.log('OK: Bestehende Rechner, Inhalte und übrige Module geprüft.');
