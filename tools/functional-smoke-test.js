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
  assertEqual(tiles.length,4,'Wissensdatenbank Anzahl Wissenskacheln');
  const expected=['air-torque-antrieb-drehrichtung/','siemens-sitrans-p320-sil-verriegelung/','vacon-frequenzumrichter-ist-sollwert-abweichung/','werkstoff-nachschlagewerk/'];
  assertEqual(tiles.map(tile=>tile.href).sort().join(','),expected.join(','),'Wissensdatenbank erwartete Kachelziele');
  assertEqual(tiles.every(tile=>tile.classes.includes('tool-card')),true,'Wissensdatenbank alle Kacheln favoritenfähig');
  const favorites=fs.readFileSync(path.join(ROOT,'assets/favorites.js'),'utf8');
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
  const context={console,Math,Number,Object,globalThis:null};context.globalThis=context;vm.createContext(context);
  vm.runInContext(fs.readFileSync(path.join(ROOT,'assets/siemens-analogwert-rechner.js'),'utf8'),context,{filename:'siemens-analogwert-rechner.js'});
  const api=context.SK_SIEMENS_ANALOG,calc=api.calculate;
  let result=calc('4-20mA','raw',13824);
  assertEqual(result.raw,13824,'Siemens 4–20 mA Rohwert');assertEqual(result.signal,12,'Siemens 4–20 mA Signal');assertEqual(result.percent,50,'Siemens 4–20 mA Nennbereichsanteil');assertEqual(result.status,'nominal','Siemens Nennbereich');
  result=calc('0-20mA','signal',20);
  assertEqual(result.raw,27648,'Siemens 0–20 mA Signal zu Rohwert');assertEqual(result.signal,20,'Siemens 0–20 mA Rückrechnung');assertEqual(result.status,'nominal','Siemens Nennbereich Obergrenze');
  result=calc('0-10V','signal',2.5);
  assertEqual(result.raw,6912,'Siemens 0–10 V Signal zu Rohwert');assertEqual(result.signal,2.5,'Siemens 0–10 V Rückrechnung');
  result=calc('2-10V','raw',20736);
  assertEqual(result.raw,20736,'Siemens 2–10 V Rohwert');assertEqual(result.signal,8,'Siemens 2–10 V Signal');
  assertEqual(api.signalScaleForType('4-20mA').join(','),'4,8,12,16,20','Siemens Signalskala 4–20 mA');
  assertEqual(api.signalScaleForType('0-20mA').join(','),'0,5,10,15,20','Siemens Signalskala 0–20 mA');
  assertEqual(api.signalScaleForType('0-10V').join(','),'0,2.5,5,7.5,10','Siemens Signalskala 0–10 V');
  assertEqual(api.signalScaleForType('2-10V').join(','),'2,4,6,8,10','Siemens Signalskala 2–10 V');
  assertEqual(api.statusForRaw(-4865),'underflow','Siemens Status Unterlauf');assertEqual(api.statusForRaw(-4864),'underrange','Siemens Status Unterbereich');
  assertEqual(api.statusForRaw(0),'nominal','Siemens Status Nennbereich Untergrenze');assertEqual(api.statusForRaw(27648),'nominal','Siemens Status Nennbereich Obergrenze');
  assertEqual(api.statusForRaw(27649),'overrange','Siemens Status Überbereich');assertEqual(api.statusForRaw(32512),'overflow','Siemens Status Überlauf');
  const colorStart=api.sliderColorForRaw(-4864),colorMiddle=api.sliderColorForRaw(-2432),colorEnd=api.sliderColorForRaw(0);
  assertEqual(colorStart!==colorMiddle&&colorMiddle!==colorEnd,true,'Siemens Slider-Farbe wird zwischen Zustandsankern kontinuierlich interpoliert');
}
{
  class MockElement{
    constructor(id=''){this.id=id;this.value='';this._textContent='';this.hidden=false;this.dataset={};this.children=[];this.attributes={};this.listeners={};this.style={values:{},setProperty:(name,value)=>{this.style.values[name]=String(value)}};Object.defineProperty(this,'textContent',{get:()=>this._textContent,set:value=>{this._textContent=String(value);if(value==='')this.children=[]}})}
    addEventListener(type,handler){this.listeners[type]=handler}
    dispatch(type){if(this.listeners[type])this.listeners[type]({type,target:this})}
    setAttribute(name,value){this.attributes[name]=String(value)}
    appendChild(child){this.children.push(child);return child}
  }
  const ids=['signalType','inputKind','inputValue','inputValueLabel','inputSuffix','valueSlider','sliderLabel','sliderScale','sliderHelp','sliderReadout','rawResult','rawExact','signalResult','signalResultLabel','signalRange','percentResult','rangeStatus','statusDetail','calculationError'];
  const elements=Object.fromEntries(ids.map(id=>[id,new MockElement(id)]));
  elements.signalType.value='4-20mA';elements.inputKind.value='raw';elements.inputValue.value='13824';
  const states=['underflow','underrange','nominal','overrange','overflow'].map(key=>{const item=new MockElement();item.dataset.stateKey=key;item.classList={toggle:()=>{},remove:()=>{}};return item});
  const quickValues=['-4865','-4864','0','13824','27648','27649','32512'].map(raw=>{const item=new MockElement();item.dataset.raw=raw;return item});
  const document={
    getElementById:id=>elements[id]||null,
    querySelectorAll:selector=>selector==='[data-state-key]'?states:selector==='[data-raw]'?quickValues:[],
    createElement:()=>new MockElement()
  };
  const context={console,Math,Number,Object,Array,String,Intl,Error,document,globalThis:null};context.globalThis=context;vm.createContext(context);
  vm.runInContext(fs.readFileSync(path.join(ROOT,'assets/siemens-analogwert-rechner.js'),'utf8'),context,{filename:'siemens-analogwert-rechner-ui.js'});
  const scale=()=>elements.sliderScale.children.map(item=>item.textContent).join('|');
  assertEqual(elements.valueSlider.min,'-32768','Siemens UI Rohwertregler Minimum');
  assertEqual(elements.valueSlider.max,'32767','Siemens UI Rohwertregler Maximum');
  assertEqual(scale(),'−32.768|−4.864|0|27.648|32.511|32.767','Siemens UI Rohwertskala');
  elements.inputKind.value='signal';elements.inputKind.dispatch('change');
  for(const [type,expected] of [
    ['4-20mA','4 mA|8 mA|12 mA|16 mA|20 mA'],
    ['0-20mA','0 mA|5 mA|10 mA|15 mA|20 mA'],
    ['0-10V','0 V|2,5 V|5 V|7,5 V|10 V'],
    ['2-10V','2 V|4 V|6 V|8 V|10 V']
  ]){
    elements.signalType.value=type;elements.signalType.dispatch('change');
    assertEqual(scale(),expected,`Siemens UI Signalskala ${type}`);
  }
  elements.signalType.value='0-10V';elements.signalType.dispatch('change');elements.valueSlider.value='7.5';elements.valueSlider.dispatch('input');
  assertEqual(elements.rawResult.textContent,'20.736','Siemens UI Signalregler aktualisiert Rohwert');
  elements.inputKind.value='raw';elements.inputKind.dispatch('change');
  assertEqual(scale(),'−32.768|−4.864|0|27.648|32.511|32.767','Siemens UI Rückkehr zur Rohwertskala');
}
console.log('OK: Bestehende Funktionen sowie bidirektionaler Siemens-SPS-Analogwert-Rechner mit fünf Bereichszuständen geprüft.');
