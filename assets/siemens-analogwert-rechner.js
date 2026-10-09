(()=>{'use strict';
const PROFILES=Object.freeze({
 et200sp_st:Object.freeze({label:'ET 200SP · AI 4xI ST',partNumber:'6ES7134-6GD01-0BA1',supported:['4-20mA','0-20mA'],mode:'standard',rawMin:-32768,rawMax:32767,nomMax:27648,note:'Bestätigte S7-Grenzen des Gerätehandbuchs. Bei 0–20 mA mit 2-Draht-Messumformer sind negative Werte und damit Untersteuerung/Unterlauf nicht möglich.'}),
 et200spha_off:Object.freeze({label:'ET 200SP HA · AI 16xI HART · NE43 aus',partNumber:'6DL1134-6TH00-0PH1',supported:['4-20mA','0-20mA'],mode:'standard',rawMin:-32768,rawMax:32767,nomMax:27648,note:'Ausfallüberwachung nach NE43 deaktiviert: systemische S7-Grenzen laut Gerätehandbuch.'}),
 et200spha_on:Object.freeze({label:'ET 200SP HA · AI 16xI HART · NE43 ein',partNumber:'6DL1134-6TH00-0PH1',supported:['4-20mA'],mode:'ne43',rawMin:-32768,rawMax:32767,nomMax:27648,note:'Alte NE43-Ausfallüberwachung des Moduls: ungültig ab 3,6 mA bzw. 21 mA; Wiedergültigwerden erst oberhalb 3,8 mA bzw. unterhalb 20,5 mA.'}),
 s71500_fai_scale:Object.freeze({label:'S7-1500/ET 200MP · F-AI 8xI · nur Skalierung',partNumber:'6ES7536-1MF00-0AB0',supported:['4-20mA','0-20mA'],mode:'scale-only',rawMin:0,rawMax:27648,nomMax:27648,note:'Nur bestätigte Nennskalierung. Diagnosegrenzen werden bewusst nicht bewertet; maßgeblich sind Gerätehandbuch, Firmware und Kanalparametrierung.'}),
 generic_scale:Object.freeze({label:'Generische Umrechnung · ohne Kartenfreigabe',partNumber:'–',supported:['4-20mA','0-20mA','0-10V','2-10V'],mode:'scale-only',rawMin:0,rawMax:27648,nomMax:27648,note:'Nur lineare Umrechnung 0…27.648. Keine kartenspezifische Aussage zu Unterlauf, Überlauf oder Diagnose.'})
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
 scaleOnly:Object.freeze({label:'Nur Skalierung',color:'#00b7e8'})
});
const DEFAULT_PHYSICAL_RANGE=Object.freeze({min:-50,max:150,unit:'°C'});
const profile=value=>typeof value==='object'&&value?value:(PROFILES[value]||PROFILES.et200sp_st);
const type=value=>TYPES[value]||TYPES['4-20mA'];
const clamp=(value,min,max)=>Math.min(max,Math.max(min,value));
function normalizePhysicalRange(range=DEFAULT_PHYSICAL_RANGE){
 const min=Number(range&&range.min),max=Number(range&&range.max),unit=String(range&&range.unit!==undefined?range.unit:'').trim();
 if(!Number.isFinite(min)||!Number.isFinite(max))throw new Error('Bitte gültige Zahlen für Messbereich Minimum und Maximum eingeben.');
 if(max<=min)throw new Error('Das Messbereichs-Maximum muss größer als das Minimum sein.');
 if(!unit)throw new Error('Bitte eine physikalische Einheit eingeben.');
 if(unit.length>24)throw new Error('Die physikalische Einheit darf höchstens 24 Zeichen lang sein.');
 return Object.freeze({min,max,unit});
}
function toggleSignValue(value){
 const normalized=String(value??'').trim().replace(',','.');
 const number=Number(normalized);
 if(!normalized||!Number.isFinite(number))throw new Error('Bitte zuerst einen gültigen Zahlenwert eingeben.');
 return number===0?0:-number;
}
function limitsFor(profileId='et200sp_st',typeId='4-20mA'){
 const p=profile(profileId);
 if(p.mode==='scale-only')return null;
 if(typeId==='0-20mA')return Object.freeze({rawMin:0,underEnd:null,nomStart:0,nomEnd:27648,overflowStart:32512,rawMax:32767,lowerPossible:false});
 if(p.mode==='ne43')return Object.freeze({rawMin:-32768,underEnd:-691,nomStart:-345,nomEnd:28511,overflowStart:29376,rawMax:32767,lowerPossible:true,hysteresis:true});
 return Object.freeze({rawMin:-32768,underEnd:-4865,nomStart:0,nomEnd:27648,overflowStart:32512,rawMax:32767,lowerPossible:true});
}
function statusForRaw(raw,profileId='et200sp_st',typeId='4-20mA'){
 const limits=limitsFor(profileId,typeId),value=Number(raw);
 if(!limits)return'scaleOnly';
 if(!limits.lowerPossible&&value<0)throw new Error('Bei 0–20 mA mit 2-Draht-Messumformer sind negative Prozesswerte laut Siemens nicht möglich.');
 if(limits.underEnd!==null&&value<=limits.underEnd)return'underflow';
 if(value<limits.nomStart)return'underrange';
 if(value<=limits.nomEnd)return'nominal';
 if(value<limits.overflowStart)return'overrange';
 return'overflow';
}
function signalFromRaw(typeId,raw,profileId='et200sp_st'){const t=type(typeId),p=profile(profileId);return t.min+(Number(raw)/p.nomMax)*(t.max-t.min)}
function rawFromSignal(typeId,value,profileId='et200sp_st'){const t=type(typeId),p=profile(profileId);return (Number(value)-t.min)/(t.max-t.min)*p.nomMax}
function physicalFromPercent(percent,physicalRange=DEFAULT_PHYSICAL_RANGE){const range=normalizePhysicalRange(physicalRange);return range.min+(Number(percent)/100)*(range.max-range.min)}
function percentFromPhysical(value,physicalRange=DEFAULT_PHYSICAL_RANGE){const range=normalizePhysicalRange(physicalRange);return (Number(value)-range.min)/(range.max-range.min)*100}
function physicalFromRaw(raw,profileId='et200sp_st',physicalRange=DEFAULT_PHYSICAL_RANGE){const p=profile(profileId);return physicalFromPercent(Number(raw)/p.nomMax*100,physicalRange)}
function rawFromPhysical(value,profileId='et200sp_st',physicalRange=DEFAULT_PHYSICAL_RANGE){const p=profile(profileId);return percentFromPhysical(value,physicalRange)/100*p.nomMax}
function calculate(typeId,inputKind,value,profileId='et200sp_st',physicalRange=DEFAULT_PHYSICAL_RANGE){
 const input=Number(value),p=profile(profileId),t=type(typeId),limits=limitsFor(p,typeId),range=normalizePhysicalRange(physicalRange);
 if(!Number.isFinite(input))throw new Error('Bitte einen gültigen Zahlenwert eingeben.');
 if(!p.supported.includes(typeId))throw new Error(`${t.label} ist für dieses Profil nicht freigegeben.`);
 if(!['raw','signal','physical'].includes(inputKind))throw new Error('Unbekannte Eingabeart.');
 const rawExact=inputKind==='raw'?input:(inputKind==='signal'?rawFromSignal(typeId,input,p):rawFromPhysical(input,p,range));
 const raw=Math.round(rawExact),min=limits?limits.rawMin:p.rawMin,max=limits?limits.rawMax:p.rawMax;
 if(raw<min||raw>max)throw new Error(`Wert außerhalb des bestätigten Bereichs ${min}…${max}.`);
 const signal=signalFromRaw(typeId,raw,p),percent=raw/p.nomMax*100,physical=physicalFromPercent(percent,range);
 return Object.freeze({raw,rawExact,signal,percent,physical,physicalRange:range,status:statusForRaw(raw,p,typeId),profile:p,type:t,limits});
}
function boundaries(profileId='et200sp_st',typeId='4-20mA'){
 const limits=limitsFor(profileId,typeId);if(!limits)return null;
 const span=limits.rawMax-limits.rawMin,position=value=>(value-limits.rawMin)/span*100;
 return Object.freeze({under:limits.underEnd===null?0:position(limits.underEnd+.5),nomStart:position(limits.nomStart),nomEnd:position(limits.nomEnd+.5),overflow:position(limits.overflowStart-.5)});
}
function signalScaleForType(typeId){const t=type(typeId);return Object.freeze(Array.from({length:5},(_,index)=>t.min+(t.max-t.min)*(index/4)))}
function profileScale(typeId,profileId='et200sp_st',mode='raw',physicalRange=DEFAULT_PHYSICAL_RANGE){
 const p=profile(profileId),limits=limitsFor(p,typeId),raw=limits?(limits.lowerPossible?[limits.rawMin,limits.underEnd,limits.nomStart,limits.nomEnd,limits.overflowStart,limits.rawMax]:[limits.nomStart,limits.nomEnd,limits.overflowStart,limits.rawMax]):[p.rawMin,p.nomMax];
 if(mode==='signal')return Object.freeze(raw.map(value=>signalFromRaw(typeId,value,p)));
 if(mode==='physical')return Object.freeze(raw.map(value=>physicalFromRaw(value,p,physicalRange)));
 return Object.freeze(raw);
}
const api=Object.freeze({PROFILES,TYPES,STATES,DEFAULT_PHYSICAL_RANGE,normalizePhysicalRange,toggleSignValue,limitsFor,statusForRaw,signalFromRaw,rawFromSignal,physicalFromPercent,percentFromPhysical,physicalFromRaw,rawFromPhysical,calculate,boundaries,signalScaleForType,profileScale});
if(typeof globalThis!=='undefined')globalThis.SK_SIEMENS_ANALOG=api;
if(typeof document==='undefined')return;

const $=id=>document.getElementById(id);
const elements={profile:$('cardProfile'),signalType:$('signalType'),tabs:[...document.querySelectorAll('.analog-tab[data-input-kind]')],panel:$('primaryInputPanel'),inputValue:$('inputValue'),inputLabel:$('inputValueLabel'),inputShell:$('primaryInputShell'),inputSign:$('inputSignToggle'),inputSuffix:$('inputSuffix'),inputState:$('rawInputState'),physicalMin:$('physicalMin'),physicalMax:$('physicalMax'),physicalUnit:$('physicalUnit'),signButtons:[...document.querySelectorAll('.analog-sign-button[data-sign-target]')],outputCards:[...document.querySelectorAll('.analog-value-card[data-output-kind]')],rawCard:$('rawOutputCard'),rawResult:$('rawResult'),rawStatus:$('rawStatus'),signalResult:$('signalResult'),physicalResult:$('physicalResult'),diagnostic:$('diagnosticSummary'),rangeStatus:$('rangeStatus'),statusDetail:$('statusDetail'),sourceLink:$('profileSourceLink'),error:$('calculationError')};
if(Object.values(elements).some(value=>!value||(Array.isArray(value)&&value.length===0)))return;
let activeMode='signal',currentRaw=13824;
const parse=value=>Number.parseFloat(String(value).replace(',','.'));
const format=(value,digits=3)=>Number.isFinite(value)?value.toLocaleString('de-DE',{minimumFractionDigits:digits,maximumFractionDigits:digits}):'–';
const formatRaw=value=>Number.isFinite(value)?Math.round(value).toLocaleString('de-DE'):'–';
const inputNumber=value=>Number.isFinite(value)?String(Number(value.toFixed(9))):'';
const physicalRange=()=>normalizePhysicalRange({min:parse(elements.physicalMin.value),max:parse(elements.physicalMax.value),unit:elements.physicalUnit.value});
function bounds(p){const limits=limitsFor(p,elements.signalType.value);return{min:limits?limits.rawMin:p.rawMin,max:limits?limits.rawMax:p.rawMax}}
function valueForMode(mode,raw,p,range){return mode==='raw'?raw:(mode==='signal'?signalFromRaw(elements.signalType.value,raw,p):physicalFromRaw(raw,p,range))}
function syncSupportedTypes(){const p=profile(elements.profile.value);[...elements.signalType.options].forEach(option=>{option.disabled=!p.supported.includes(option.value)});if(!p.supported.includes(elements.signalType.value))elements.signalType.value=p.supported[0]}
function syncTabs(){elements.tabs.forEach(tab=>{const selected=tab.dataset.inputKind===activeMode;tab.setAttribute('aria-selected',String(selected));tab.tabIndex=selected?0:-1});const selected=elements.tabs.find(tab=>tab.dataset.inputKind===activeMode);elements.panel.setAttribute('aria-labelledby',selected.id)}
function syncPrimaryInput(){
 const p=profile(elements.profile.value),t=type(elements.signalType.value),range=physicalRange(),{min,max}=bounds(p),suffix=activeMode==='raw'?'INT':(activeMode==='signal'?t.unit:range.unit);
 elements.inputLabel.textContent=activeMode==='raw'?'Rohwert':(activeMode==='signal'?'Signal':`Phys. Wert (${range.unit})`);
 const signSubject=activeMode==='raw'?'Rohwert':(activeMode==='signal'?'Signal':`physikalischen Wert in ${range.unit}`);
 elements.inputSign.setAttribute('aria-label',`Vorzeichen für ${signSubject} wechseln`);elements.inputSign.title=`Vorzeichen für ${signSubject} wechseln`;
 elements.inputSuffix.textContent=suffix;elements.inputValue.step=activeMode==='raw'?'1':'any';elements.inputValue.inputMode=activeMode==='raw'?'numeric':'decimal';
 elements.inputValue.setAttribute('aria-label',activeMode==='raw'?'Rohwert eingeben':(activeMode==='signal'?`Signalwert in ${t.unit} eingeben`:`Physikalischen Wert in ${range.unit} eingeben`));
 elements.inputValue.min=inputNumber(valueForMode(activeMode,min,p,range));elements.inputValue.max=inputNumber(valueForMode(activeMode,max,p,range));elements.inputValue.value=inputNumber(valueForMode(activeMode,currentRaw,p,range));
 elements.outputCards.forEach(card=>{card.hidden=card.dataset.outputKind===activeMode});
 syncTabs();
}
function paintState(state){
 elements.rawCard.dataset.state=state;elements.diagnostic.dataset.state=state;elements.rangeStatus.textContent=STATES[state].label;elements.rawStatus.textContent=STATES[state].label;
 const rawActive=activeMode==='raw';elements.inputShell.dataset.state=rawActive?state:'neutral';elements.inputState.hidden=!rawActive;elements.inputState.dataset.state=state;elements.inputState.textContent=STATES[state].label;
}
function renderFromRaw(){
 const p=profile(elements.profile.value),t=type(elements.signalType.value),range=physicalRange(),result=calculate(elements.signalType.value,'raw',currentRaw,p,range);
 elements.error.hidden=true;elements.rawResult.textContent=formatRaw(result.raw);elements.signalResult.textContent=`${format(result.signal,3)} ${t.unit}`;elements.physicalResult.textContent=`${format(result.physical,3)} ${range.unit}`;
 paintState(result.status);elements.statusDetail.textContent=`${p.label} (${p.partNumber}): ${p.note}`;elements.sourceLink.href='../SIEMENS-QUELLEN-UND-GRENZWERTE.md';
}
function showError(error){elements.error.textContent=error.message;elements.error.hidden=false;elements.diagnostic.dataset.state='error';elements.rangeStatus.textContent='Eingabe prüfen'}
function renderFromInput(){try{const result=calculate(elements.signalType.value,activeMode,parse(elements.inputValue.value),elements.profile.value,physicalRange());currentRaw=result.raw;renderFromRaw()}catch(error){showError(error)}}
function commitInput(){renderFromInput();if(elements.error.hidden)syncPrimaryInput()}
function dismissInputFocus(){
 const active=document.activeElement;
 if(active&&active.matches&&active.matches('input,textarea,select,[contenteditable="true"]'))active.blur();
}
function toggleInputSign(input){
 try{
  input.value=inputNumber(toggleSignValue(input.value));
  input.dispatchEvent(new Event('input',{bubbles:true}));
  input.dispatchEvent(new Event('change',{bubbles:true}));
 }catch(error){showError(error)}
}
function bindSignButtons(){
 elements.signButtons.forEach(button=>{
  const input=$(button.dataset.signTarget);if(!input)return;
  // pointerdown verhindert, dass iOS/Safari das Zahlenfeld über die umgebende
  // Bedienfläche fokussiert und dabei die Bildschirmtastatur öffnet.
  button.addEventListener('pointerdown',event=>{event.preventDefault();dismissInputFocus()});
  button.addEventListener('click',event=>{event.preventDefault();event.stopPropagation();dismissInputFocus();toggleInputSign(input)});
 });
}
function setMode(mode,dismissKeyboard=false){
 if(!['signal','raw','physical'].includes(mode))return;
 if(dismissKeyboard)dismissInputFocus();
 activeMode=mode;
 // Reiterauswahl sofort aktualisieren. So bleibt der Wechsel auch dann sichtbar,
 // wenn ein gerade unvollständiger Messbereich die Neuberechnung verhindert.
 syncTabs();
 try{syncPrimaryInput();renderFromRaw()}catch(error){showError(error)}
}
function resyncAndRender(){try{syncPrimaryInput();renderFromRaw()}catch(error){showError(error)}}

elements.tabs.forEach((tab,index)=>{tab.addEventListener('click',event=>{event.preventDefault();setMode(tab.dataset.inputKind,true)});tab.addEventListener('keydown',event=>{if(!['ArrowLeft','ArrowRight','Home','End'].includes(event.key))return;event.preventDefault();let next=index;if(event.key==='ArrowLeft')next=(index-1+elements.tabs.length)%elements.tabs.length;if(event.key==='ArrowRight')next=(index+1)%elements.tabs.length;if(event.key==='Home')next=0;if(event.key==='End')next=elements.tabs.length-1;setMode(elements.tabs[next].dataset.inputKind);elements.tabs[next].focus({preventScroll:true})})});
elements.inputValue.addEventListener('input',renderFromInput);elements.inputValue.addEventListener('change',commitInput);elements.inputValue.addEventListener('focus',event=>event.currentTarget.select());
elements.signalType.addEventListener('change',resyncAndRender);
elements.profile.addEventListener('change',()=>{try{syncSupportedTypes();const p=profile(elements.profile.value),{min,max}=bounds(p);currentRaw=clamp(currentRaw,min,max);syncPrimaryInput();renderFromRaw()}catch(error){showError(error)}});
[elements.physicalMin,elements.physicalMax,elements.physicalUnit].forEach(element=>{element.addEventListener('input',resyncAndRender);element.addEventListener('change',resyncAndRender);element.addEventListener('focus',event=>event.currentTarget.select())});
bindSignButtons();syncSupportedTypes();setMode('signal');
})();
