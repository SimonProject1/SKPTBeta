(()=>{'use strict';
const PROFILES=Object.freeze({
 et200sp_st:Object.freeze({
  label:'ET 200SP · AI 4xI ST',partNumber:'6ES7134-6GD01-0BA1',supported:['4-20mA','0-20mA'],mode:'standard',rawMin:-32768,rawMax:32767,nomMax:27648,
  note:'Bestätigte S7-Grenzen des Gerätehandbuchs. Bei 0–20 mA mit 2-Draht-Messumformer sind negative Werte und damit Untersteuerung/Unterlauf nicht möglich.'
 }),
 et200spha_off:Object.freeze({
  label:'ET 200SP HA · AI 16xI HART · NE43 aus',partNumber:'6DL1134-6TH00-0PH1',supported:['4-20mA','0-20mA'],mode:'standard',rawMin:-32768,rawMax:32767,nomMax:27648,
  note:'Ausfallüberwachung nach NE43 deaktiviert: systemische S7-Grenzen laut Gerätehandbuch.'
 }),
 et200spha_on:Object.freeze({
  label:'ET 200SP HA · AI 16xI HART · NE43 ein',partNumber:'6DL1134-6TH00-0PH1',supported:['4-20mA'],mode:'ne43',rawMin:-32768,rawMax:32767,nomMax:27648,
  note:'Alte NE43-Ausfallüberwachung des Moduls: ungültig ab 3,6 mA bzw. 21 mA; Wiedergültigwerden erst oberhalb 3,8 mA bzw. unterhalb 20,5 mA.'
 }),
 s71500_fai_scale:Object.freeze({
  label:'S7-1500/ET 200MP · F-AI 8xI · nur Skalierung',partNumber:'6ES7536-1MF00-0AB0',supported:['4-20mA','0-20mA'],mode:'scale-only',rawMin:0,rawMax:27648,nomMax:27648,
  note:'Nur bestätigte Nennskalierung. Diagnosegrenzen werden bewusst nicht bewertet; maßgeblich sind Gerätehandbuch, Firmware und Kanalparametrierung.'
 }),
 generic_scale:Object.freeze({
  label:'Generische Umrechnung · ohne Kartenfreigabe',partNumber:'–',supported:['4-20mA','0-20mA','0-10V','2-10V'],mode:'scale-only',rawMin:0,rawMax:27648,nomMax:27648,
  note:'Nur lineare Umrechnung 0…27.648. Keine kartenspezifische Aussage zu Unterlauf, Überlauf oder Diagnose.'
 })
});
const TYPES=Object.freeze({
 '4-20mA':Object.freeze({min:4,max:20,unit:'mA',label:'4–20 mA'}),
 '0-20mA':Object.freeze({min:0,max:20,unit:'mA',label:'0–20 mA'}),
 '0-10V':Object.freeze({min:0,max:10,unit:'V',label:'0–10 V'}),
 '2-10V':Object.freeze({min:2,max:10,unit:'V',label:'2–10 V'})
});
const STATES=Object.freeze({
 underflow:Object.freeze({label:'Unterlauf',color:'#ff7b83'}),
 underrange:Object.freeze({label:'Untersteuerung',color:'#f5b942'}),
 nominal:Object.freeze({label:'Nennbereich',color:'#89d329'}),
 overrange:Object.freeze({label:'Übersteuerung',color:'#f5b942'}),
 overflow:Object.freeze({label:'Überlauf',color:'#ff7b83'}),
 scaleOnly:Object.freeze({label:'Nur Umrechnung',color:'#00b7e8'})
});
const profile=value=>typeof value==='object'&&value?value:(PROFILES[value]||PROFILES.et200sp_st);
const type=value=>TYPES[value]||TYPES['4-20mA'];
const clamp=(value,min,max)=>Math.min(max,Math.max(min,value));
function limitsFor(profileId='et200sp_st',typeId='4-20mA'){
 const p=profile(profileId);
 if(p.mode==='scale-only')return null;
 if(typeId==='0-20mA')return Object.freeze({rawMin:0,underEnd:null,nomStart:0,nomEnd:27648,overflowStart:32512,rawMax:32767,lowerPossible:false});
 if(p.mode==='ne43')return Object.freeze({rawMin:-32768,underEnd:-691,nomStart:-345,nomEnd:28511,overflowStart:29376,rawMax:32767,lowerPossible:true,hysteresis:true});
 return Object.freeze({rawMin:-32768,underEnd:-4865,nomStart:0,nomEnd:27648,overflowStart:32512,rawMax:32767,lowerPossible:true});
}
function statusForRaw(raw,profileId='et200sp_st',typeId='4-20mA'){
 const p=profile(profileId),limits=limitsFor(p,typeId),value=Number(raw);
 if(!limits)return'scaleOnly';
 if(!limits.lowerPossible&&value<0)throw new Error('Bei 0–20 mA mit 2-Draht-Messumformer sind negative Prozesswerte laut Siemens nicht möglich.');
 if(limits.underEnd!==null&&value<=limits.underEnd)return'underflow';
 if(value<limits.nomStart)return'underrange';
 if(value<=limits.nomEnd)return'nominal';
 if(value<limits.overflowStart)return'overrange';
 return'overflow';
}
function signalFromRaw(typeId,raw,profileId='et200sp_st'){
 const t=type(typeId),p=profile(profileId);
 return t.min+(Number(raw)/p.nomMax)*(t.max-t.min);
}
function rawFromSignal(typeId,value,profileId='et200sp_st'){
 const t=type(typeId),p=profile(profileId);
 return (Number(value)-t.min)/(t.max-t.min)*p.nomMax;
}
function calculate(typeId,inputKind,value,profileId='et200sp_st'){
 const input=Number(value),p=profile(profileId),t=type(typeId),limits=limitsFor(p,typeId);
 if(!Number.isFinite(input))throw new Error('Bitte einen gültigen Zahlenwert eingeben.');
 if(!p.supported.includes(typeId))throw new Error(`${t.label} ist für dieses Profil nicht freigegeben.`);
 if(inputKind!=='raw'&&inputKind!=='signal')throw new Error('Unbekannte Eingaberichtung.');
 const rawExact=inputKind==='raw'?input:rawFromSignal(typeId,input,p);
 const raw=Math.round(rawExact);
 const min=limits?limits.rawMin:p.rawMin,max=limits?limits.rawMax:p.rawMax;
 if(raw<min||raw>max)throw new Error(`Wert außerhalb des bestätigten Bereichs ${min}…${max}.`);
 const signal=signalFromRaw(typeId,raw,p);
 return Object.freeze({raw,rawExact,signal,percent:raw/p.nomMax*100,status:statusForRaw(raw,p,typeId),profile:p,type:t,limits});
}
function boundaries(profileId='et200sp_st',typeId='4-20mA'){
 const limits=limitsFor(profileId,typeId);if(!limits)return null;
 const span=limits.rawMax-limits.rawMin,position=value=>((value-limits.rawMin)/span*100);
 return Object.freeze({under:limits.underEnd===null?0:position(limits.underEnd+.5),nomStart:position(limits.nomStart),nomEnd:position(limits.nomEnd+.5),overflow:position(limits.overflowStart-.5)});
}
function signalScaleForType(typeId){const t=type(typeId);return Object.freeze(Array.from({length:5},(_,index)=>t.min+(t.max-t.min)*(index/4)));}
function profileScale(typeId,profileId='et200sp_st',mode='raw'){
 const p=profile(profileId),limits=limitsFor(p,typeId);
 if(!limits){const raw=[p.rawMin,p.nomMax];return Object.freeze(mode==='signal'?raw.map(value=>signalFromRaw(typeId,value,p)):raw)}
 const raw=limits.lowerPossible?[limits.rawMin,limits.underEnd,limits.nomStart,limits.nomEnd,limits.overflowStart,limits.rawMax]:[limits.nomStart,limits.nomEnd,limits.overflowStart,limits.rawMax];
 return Object.freeze(mode==='signal'?raw.map(value=>signalFromRaw(typeId,value,p)):raw);
}
const api=Object.freeze({PROFILES,TYPES,STATES,limitsFor,statusForRaw,signalFromRaw,rawFromSignal,calculate,boundaries,signalScaleForType,profileScale});
if(typeof globalThis!=='undefined')globalThis.SK_SIEMENS_ANALOG=api;
if(typeof document==='undefined')return;

const $=id=>document.getElementById(id);
const elements={profile:$('cardProfile'),signalType:$('signalType'),inputKind:$('inputKind'),inputValue:$('inputValue'),inputLabel:$('inputValueLabel'),inputSuffix:$('inputSuffix'),slider:$('valueSlider'),sliderLabel:$('sliderLabel'),sliderScale:$('sliderScale'),sliderReadout:$('sliderReadout'),rawResult:$('rawResult'),signalResult:$('signalResult'),percentResult:$('percentResult'),rangeStatus:$('rangeStatus'),statusDetail:$('statusDetail'),stateStrip:$('stateStrip'),sourceLink:$('profileSourceLink'),error:$('calculationError')};
if(Object.values(elements).some(element=>!element))return;
let currentRaw=13824;
const parse=value=>Number.parseFloat(String(value).replace(',','.'));
const format=(value,digits=3)=>Number.isFinite(value)?value.toLocaleString('de-DE',{minimumFractionDigits:digits,maximumFractionDigits:digits}):'–';
const formatRaw=value=>Number.isFinite(value)?Math.round(value).toLocaleString('de-DE'):'–';
const formatScale=(value,mode,unit)=>mode==='raw'?formatRaw(value):`${format(value,3)} ${unit}`;
function syncSupportedTypes(){
 const p=profile(elements.profile.value);
 [...elements.signalType.options].forEach(option=>{option.disabled=!p.supported.includes(option.value)});
 if(!p.supported.includes(elements.signalType.value))elements.signalType.value=p.supported[0];
}
function setTrack(profileId,typeId){
 const b=boundaries(profileId,typeId),diagnostic=Boolean(b);elements.slider.dataset.diagnostic=diagnostic?'on':'off';elements.stateStrip.hidden=!diagnostic;
 if(!b)return;
 elements.slider.style.setProperty('--b1',`${b.under.toFixed(4)}%`);elements.slider.style.setProperty('--b2',`${b.nomStart.toFixed(4)}%`);elements.slider.style.setProperty('--b3',`${b.nomEnd.toFixed(4)}%`);elements.slider.style.setProperty('--b4',`${b.overflow.toFixed(4)}%`);
}
function renderScale(mode,p,t){
 elements.sliderScale.replaceChildren();
 profileScale(elements.signalType.value,p,mode).forEach(value=>{const item=document.createElement('span');item.textContent=formatScale(value,mode,t.unit);elements.sliderScale.append(item)});
 elements.sliderScale.dataset.mode=mode;elements.sliderScale.style.setProperty('--analog-scale-count',String(elements.sliderScale.children.length));
}
function syncInput(){
 const mode=elements.inputKind.value,t=type(elements.signalType.value),p=profile(elements.profile.value),limits=limitsFor(p,elements.signalType.value);
 const min=limits?limits.rawMin:p.rawMin,max=limits?limits.rawMax:p.rawMax;
 elements.inputLabel.textContent=mode==='raw'?'Rohwert':`Signalwert (${t.unit})`;elements.inputSuffix.textContent=mode==='raw'?'INT':t.unit;elements.inputValue.step=mode==='raw'?'1':'0.001';elements.inputValue.inputMode=mode==='raw'?'numeric':'decimal';elements.inputValue.setAttribute('aria-label',mode==='raw'?'Rohwert eingeben':`Signalwert in ${t.unit} eingeben`);
 elements.inputValue.min=mode==='raw'?String(min):String(signalFromRaw(elements.signalType.value,min,p));elements.inputValue.max=mode==='raw'?String(max):String(signalFromRaw(elements.signalType.value,max,p));
 elements.inputValue.value=mode==='raw'?String(currentRaw):String(Number(signalFromRaw(elements.signalType.value,currentRaw,p).toFixed(6)));
}
function renderFromRaw(){
 const p=profile(elements.profile.value),t=type(elements.signalType.value),mode=elements.inputKind.value,result=calculate(elements.signalType.value,'raw',currentRaw,p),state=STATES[result.status],limits=result.limits;
 elements.error.hidden=true;elements.rawResult.textContent=formatRaw(result.raw);elements.signalResult.textContent=`${format(result.signal,3)} ${t.unit}`;elements.percentResult.textContent=`${format(result.percent,1)} %`;elements.rangeStatus.textContent=state.label;elements.rangeStatus.dataset.state=result.status;
 elements.statusDetail.textContent=`${p.label} (${p.partNumber}): ${p.note}`;elements.sourceLink.href='../SIEMENS-QUELLEN-UND-GRENZWERTE.md';
 const min=limits?limits.rawMin:p.rawMin,max=limits?limits.rawMax:p.rawMax;
 elements.slider.min=mode==='raw'?String(min):String(signalFromRaw(elements.signalType.value,min,p));elements.slider.max=mode==='raw'?String(max):String(signalFromRaw(elements.signalType.value,max,p));elements.slider.step=mode==='raw'?'1':'0.001';elements.slider.value=mode==='raw'?String(result.raw):String(result.signal);
 elements.sliderLabel.textContent=mode==='raw'?'Rohwert stufenlos einstellen':`${t.label} stufenlos einstellen`;elements.sliderReadout.textContent=mode==='raw'?`${formatRaw(result.raw)} · ${format(result.signal,3)} ${t.unit}`:`${format(result.signal,3)} ${t.unit} · ${formatRaw(result.raw)}`;elements.slider.setAttribute('aria-valuetext',elements.sliderReadout.textContent);elements.slider.setAttribute('aria-label',elements.sliderLabel.textContent);elements.slider.style.setProperty('--thumb-color',state.color);
 setTrack(p,elements.signalType.value);renderScale(mode,p,t);document.querySelectorAll('[data-state-key]').forEach(item=>item.classList.toggle('active',item.dataset.stateKey===result.status));
}
function renderFromInput(){try{const result=calculate(elements.signalType.value,elements.inputKind.value,parse(elements.inputValue.value),elements.profile.value);currentRaw=result.raw;renderFromRaw()}catch(error){elements.error.textContent=error.message;elements.error.hidden=false;elements.rangeStatus.textContent='Eingabe prüfen';elements.rangeStatus.dataset.state='error'}}
elements.inputValue.addEventListener('input',renderFromInput);elements.inputValue.addEventListener('change',renderFromInput);elements.inputValue.addEventListener('focus',event=>event.currentTarget.select());
elements.slider.addEventListener('input',()=>{const mode=elements.inputKind.value;currentRaw=mode==='raw'?Math.round(Number(elements.slider.value)):Math.round(rawFromSignal(elements.signalType.value,elements.slider.value,elements.profile.value));syncInput();renderFromRaw()});
elements.inputKind.addEventListener('change',()=>{syncInput();renderFromRaw()});elements.signalType.addEventListener('change',()=>{syncInput();renderFromRaw()});elements.profile.addEventListener('change',()=>{syncSupportedTypes();const p=profile(elements.profile.value),limits=limitsFor(p,elements.signalType.value),min=limits?limits.rawMin:p.rawMin,max=limits?limits.rawMax:p.rawMax;currentRaw=clamp(currentRaw,min,max);syncInput();renderFromRaw()});
syncSupportedTypes();syncInput();renderFromRaw();
})();
