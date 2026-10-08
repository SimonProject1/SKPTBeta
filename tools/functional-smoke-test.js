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
  let result=calc('4-20mA','raw',13824,'et200sp_st');
  assertEqual(result.raw,13824,'Siemens 4–20 mA Rohwert');assertEqual(result.signal,12,'Siemens 4–20 mA Signal');assertEqual(result.percent,50,'Siemens 4–20 mA Nennbereichsanteil');assertEqual(result.status,'nominal','Siemens ET 200SP Nennbereich');
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
  const ids=['cardProfile','signalType','inputKind','inputValue','inputValueLabel','inputSuffix','valueSlider','sliderLabel','sliderScale','sliderReadout','rawResult','signalResult','percentResult','rangeStatus','statusDetail','stateStrip','profileSourceLink','calculationError'];
  const elements=Object.fromEntries(ids.map(id=>[id,new MockElement(id)]));
  elements.cardProfile.value='et200sp_st';elements.signalType.value='4-20mA';elements.inputKind.value='raw';elements.inputValue.value='13824';
  elements.signalType.options=['4-20mA','0-20mA','0-10V','2-10V'].map(value=>({value,disabled:false}));
  const states=['underflow','underrange','nominal','overrange','overflow'].map(key=>{const item=new MockElement();item.dataset.stateKey=key;return item});
  const document={getElementById:id=>elements[id]||null,querySelectorAll:selector=>selector==='[data-state-key]'?states:[],createElement:()=>new MockElement()};
  const context={console,Math,Number,Object,Array,String,Intl,Error,document,globalThis:null};context.globalThis=context;vm.createContext(context);
  vm.runInContext(fs.readFileSync(path.join(ROOT,'assets/siemens-analogwert-rechner.js'),'utf8'),context,{filename:'siemens-analogwert-rechner-ui.js'});
  const scale=()=>elements.sliderScale.children.map(item=>item.textContent).join('|');
  assertEqual(elements.rawResult.textContent,'13.824','Siemens UI Start-Rohwert');assertEqual(elements.signalResult.textContent,'12,000 mA','Siemens UI Start-Signalwert');
  assertEqual(scale(),'-32.768|-4.865|0|27.648|32.512|32.767','Siemens UI Standard-Rohwertskala');
  elements.inputKind.value='signal';elements.inputKind.dispatch('change');assertEqual(Number(elements.inputValue.value),12,'Siemens UI Eingaberichtung synchronisiert Wert');
  elements.signalType.value='0-20mA';elements.signalType.dispatch('change');assertEqual(Number(elements.inputValue.value),10,'Siemens UI Signalbereich erhält Rohwert');
  elements.valueSlider.value='15';elements.valueSlider.dispatch('input');assertEqual(elements.rawResult.textContent,'20.736','Siemens UI Signalregler aktualisiert Rohwert');
  elements.inputKind.value='raw';elements.inputKind.dispatch('change');assertEqual(elements.inputValue.value,'20736','Siemens UI Rückkehr zur Rohwerteingabe synchron');
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
{
  const context={console,Math,Number,Object,Array,String,Intl,Error,globalThis:null};context.globalThis=context;vm.createContext(context);
  vm.runInContext(fs.readFileSync(path.join(ROOT,'assets/vde0100-600-engine.js'),'utf8'),context,{filename:'vde0100-600-engine.js'});
  const engine=context.SK_VDE_ENGINE;
  const schema=JSON.parse(fs.readFileSync(path.join(ROOT,'assets/vde0100-600-input-schema.json'),'utf8'));
  const rules=JSON.parse(fs.readFileSync(path.join(ROOT,'assets/vde0100-600-rules.json'),'utf8'));
  assertEqual(engine.VERSION,'2.1.1.0-Beta','VDE Messwertengine Version');
  assertEqual(Object.keys(engine.MEASUREMENT_TYPES).length,6,'VDE sechs manuelle Messgrößen');
  assertEqual(schema.mode,'manual-only','VDE Eingabeschema ausschließlich manuell');
  assertEqual(schema.automaticDocumentAnalysis,false,'VDE automatische Dokumentanalyse deaktiviert');
  assertEqual(rules.automaticInput.photo||rules.automaticInput.pdf||rules.automaticInput.ocr||rules.automaticInput.protocolRecognition,false,'VDE alle automatischen Eingänge deaktiviert');
  assertEqual(rules.governance.numericDefaultsAllowed,false,'VDE keine numerischen Standardgrenzwerte');
  assertEqual(['parseText','detectedMeasurementGroups','referenceDescriptor'].some(key=>key in engine),false,'VDE keine Erkennungs- oder Vorlagenlogik');

  let result=engine.evaluate('voltageDrop',{voltageDropMode:'percent',measuredDropPercent:'',approvedMaxDropPercent:'3'});
  assertEqual(result.status,'incomplete','Spannungsfall fehlender Messwert bleibt offen');
  assertEqual(result.resultLabel,'','Spannungsfall kein Ergebnis bei Fehlwert');
  assertEqual(result.missing[0].field,'measuredDropPercent','Spannungsfall gezielte Rückfrage');
  result=engine.evaluate('voltageDrop',{voltageDropMode:'percent',measuredDropPercent:'3',approvedMaxDropPercent:'3'});
  assertEqual(result.status,'pass','Spannungsfall Grenzgleichheit i. O.');
  result=engine.evaluate('voltageDrop',{voltageDropMode:'percent',measuredDropPercent:'3,01',approvedMaxDropPercent:'3'});
  assertEqual(result.status,'fail','Spannungsfall oberhalb Grenze n. i. O.');
  result=engine.evaluate('voltageDrop',{voltageDropMode:'volts',measuredDropVolts:'8',nominalVoltage:'400',approvedMaxDropPercent:'2'});
  assertEqual(result.status,'pass','Spannungsfall ΔU/Un Grenzgleichheit');
  assertEqual(result.checks[0].calculation.includes('8 V / 400 V × 100 = 2 %'),true,'Spannungsfall Rechenweg offengelegt');
  result=engine.evaluate('voltageDrop',{voltageDropMode:'volts',measuredDropVolts:'8',nominalVoltage:'0',approvedMaxDropPercent:'2'});
  assertEqual(result.status,'error','Spannungsfall Division durch null gesperrt');

  result=engine.evaluate('insulation',{measuredInsulation:'1',approvedMinInsulation:'1'});
  assertEqual(result.status,'pass','Isolation Grenzgleichheit i. O.');
  assertEqual(engine.evaluate('insulation',{measuredInsulation:'0,99',approvedMinInsulation:'1'}).status,'fail','Isolation unter Mindestwert n. i. O.');
  assertEqual(engine.evaluate('insulation',{measuredInsulation:'',approvedMinInsulation:'1'}).complete,false,'Isolation Fehlwert ohne Ergebnis');

  result=engine.evaluate('disconnection',{disconnectionMode:'loop-approved',measuredLoopImpedance:'2,5',approvedMaxLoopImpedance:'2,5'});
  assertEqual(result.status,'pass','Zs direkter Sollwert Grenzgleichheit');
  assertEqual(engine.evaluate('disconnection',{disconnectionMode:'loop-approved',measuredLoopImpedance:'2,51',approvedMaxLoopImpedance:'2,5'}).status,'fail','Zs direkter Sollwert Überschreitung');
  result=engine.evaluate('disconnection',{disconnectionMode:'loop-formula',measuredLoopImpedance:'2,875',phaseVoltage:'230',requiredTripCurrent:'80'});
  assertEqual(result.status,'pass','Zs U0/Ia Grenzgleichheit');
  assertEqual(result.limitText.includes('2,875 Ω'),true,'Zs berechneter Grenzwert sichtbar');
  assertEqual(engine.evaluate('disconnection',{disconnectionMode:'loop-formula',measuredLoopImpedance:'2,876',phaseVoltage:'230',requiredTripCurrent:'80'}).status,'fail','Zs U0/Ia Überschreitung');
  assertEqual(engine.evaluate('disconnection',{disconnectionMode:'short-current',measuredShortCircuitCurrent:'80',requiredTripCurrent:'80'}).status,'pass','Ik Grenzgleichheit i. O.');
  assertEqual(engine.evaluate('disconnection',{disconnectionMode:'short-current',measuredShortCircuitCurrent:'79,9',requiredTripCurrent:'80'}).status,'fail','Ik unter Ia n. i. O.');
  assertEqual(engine.evaluate('disconnection',{disconnectionMode:'short-current',measuredShortCircuitCurrent:'80',requiredTripCurrent:''}).status,'incomplete','Ik ohne Ia kein Ergebnis');

  assertEqual(engine.evaluate('rcd',{rcdMode:'time',measuredRcdTime:'300',approvedMaxRcdTime:'300'}).status,'pass','RCD-Zeit Grenzgleichheit');
  assertEqual(engine.evaluate('rcd',{rcdMode:'time',measuredRcdTime:'301',approvedMaxRcdTime:'300'}).status,'fail','RCD-Zeit Überschreitung');
  assertEqual(engine.evaluate('rcd',{rcdMode:'current',measuredRcdCurrent:'15',approvedMinRcdCurrent:'15',approvedMaxRcdCurrent:'30'}).status,'pass','RCD-Strom untere Grenzgleichheit');
  assertEqual(engine.evaluate('rcd',{rcdMode:'current',measuredRcdCurrent:'30',approvedMinRcdCurrent:'15',approvedMaxRcdCurrent:'30'}).status,'pass','RCD-Strom obere Grenzgleichheit');
  assertEqual(engine.evaluate('rcd',{rcdMode:'current',measuredRcdCurrent:'14,9',approvedMinRcdCurrent:'15',approvedMaxRcdCurrent:'30'}).status,'fail','RCD-Strom unterhalb Bereich');
  assertEqual(engine.evaluate('rcd',{rcdMode:'current',measuredRcdCurrent:'31',approvedMinRcdCurrent:'15',approvedMaxRcdCurrent:'30'}).status,'fail','RCD-Strom oberhalb Bereich');
  assertEqual(engine.evaluate('rcd',{rcdMode:'current',measuredRcdCurrent:'20',approvedMinRcdCurrent:'31',approvedMaxRcdCurrent:'30'}).status,'error','RCD ungültiger Grenzbereich gesperrt');
  result=engine.evaluate('rcd',{rcdMode:'both',measuredRcdTime:'299',approvedMaxRcdTime:'300',measuredRcdCurrent:'31',approvedMinRcdCurrent:'15',approvedMaxRcdCurrent:'30'});
  assertEqual(result.status,'fail','RCD Gesamtstatus folgt Teilabweichung');
  assertEqual(result.checks.length,2,'RCD beide Rechenwege ausgewiesen');

  assertEqual(engine.evaluate('continuity',{measuredContinuity:'0,5',approvedMaxContinuity:'0,5'}).status,'pass','Niederohmigkeit Grenzgleichheit');
  assertEqual(engine.evaluate('continuity',{measuredContinuity:'0,51',approvedMaxContinuity:'0,5'}).status,'fail','Niederohmigkeit Überschreitung');
  assertEqual(engine.evaluate('continuity',{measuredContinuity:'-0,1',approvedMaxContinuity:'0,5'}).status,'error','Niederohmigkeit negativer Wert gesperrt');
  assertEqual(engine.evaluate('bonding',{measuredBonding:'0,2',approvedMaxBonding:'0,2'}).status,'pass','Schutzpotentialausgleich Grenzgleichheit');
  assertEqual(engine.evaluate('bonding',{measuredBonding:'0,21',approvedMaxBonding:'0,2'}).status,'fail','Schutzpotentialausgleich Überschreitung');
  assertEqual(engine.evaluate('bonding',{measuredBonding:'abc',approvedMaxBonding:'0,2'}).status,'error','Schutzpotentialausgleich ungültige Zahl gesperrt');

  const formalNoise={measuredInsulation:'1',approvedMinInsulation:'1',testerName:'Beliebig',signatureState:'missing',formIdentity:'unknown'};
  assertEqual(engine.evaluate('insulation',formalNoise).status,'pass','Formale Stördaten ohne Einfluss');
}
console.log('OK: Bestehende Funktionen, manueller VDE-Messwertprüfer ohne Dokumentanalyse, vollständige Grenz- und Fehlerfallmatrix sowie übrige Module geprüft.');
