(()=>{'use strict';
const RAW_NOMINAL_MAX=27648;
const RAW_UNDERRANGE_MIN=-4864;
const RAW_OVERRANGE_MAX=32511;
const RAW_INT_MIN=-32768;
const RAW_INT_MAX=32767;
const TYPES=Object.freeze({
 '4-20mA':Object.freeze({min:4,max:20,unit:'mA',label:'4–20 mA'}),
 '0-20mA':Object.freeze({min:0,max:20,unit:'mA',label:'0–20 mA'}),
 '0-10V':Object.freeze({min:0,max:10,unit:'V',label:'0–10 V'}),
 '2-10V':Object.freeze({min:2,max:10,unit:'V',label:'2–10 V'})
});
const STATES=Object.freeze({
 underflow:Object.freeze({label:'Unterlauf',detail:'≤ −4.865'}),
 underrange:Object.freeze({label:'Unterbereich',detail:'−4.864…−1'}),
 nominal:Object.freeze({label:'Nennbereich',detail:'0…27.648'}),
 overrange:Object.freeze({label:'Überbereich',detail:'27.649…32.511'}),
 overflow:Object.freeze({label:'Überlauf',detail:'≥ 32.512'})
});
function statusForRaw(raw){
 if(raw<RAW_UNDERRANGE_MIN)return 'underflow';
 if(raw<0)return 'underrange';
 if(raw<=RAW_NOMINAL_MAX)return 'nominal';
 if(raw<=RAW_OVERRANGE_MAX)return 'overrange';
 return 'overflow';
}
function signalFromRaw(type,raw){
 const signal=TYPES[type];
 if(!signal)throw new Error('Unbekannter Signalbereich.');
 return signal.min+(Number(raw)/RAW_NOMINAL_MAX)*(signal.max-signal.min);
}
function rawFromSignal(type,value){
 const signal=TYPES[type];
 if(!signal)throw new Error('Unbekannter Signalbereich.');
 return (Number(value)-signal.min)/(signal.max-signal.min)*RAW_NOMINAL_MAX;
}
function calculate(type,inputKind,value){
 const input=Number(value);
 if(!Number.isFinite(input))throw new Error('Bitte einen gültigen Zahlenwert eingeben.');
 if(inputKind!=='raw'&&inputKind!=='signal')throw new Error('Unbekannte Eingaberichtung.');
 const rawExact=inputKind==='raw'?input:rawFromSignal(type,input);
 const raw=Math.round(rawExact);
 const signal=signalFromRaw(type,raw);
 const config=TYPES[type];
 return Object.freeze({raw,rawExact,signal,signalUnit:config.unit,signalLabel:config.label,percent:raw/RAW_NOMINAL_MAX*100,status:statusForRaw(raw)});
}
const api=Object.freeze({RAW_NOMINAL_MAX,RAW_UNDERRANGE_MIN,RAW_OVERRANGE_MAX,RAW_INT_MIN,RAW_INT_MAX,TYPES,STATES,statusForRaw,signalFromRaw,rawFromSignal,calculate});
if(typeof globalThis!=='undefined')globalThis.SK_SIEMENS_ANALOG=api;
if(typeof document==='undefined')return;

const byId=id=>document.getElementById(id);
const elements={
 signalType:byId('signalType'),inputKind:byId('inputKind'),inputValue:byId('inputValue'),inputValueLabel:byId('inputValueLabel'),inputSuffix:byId('inputSuffix'),
 slider:byId('valueSlider'),sliderReadout:byId('sliderReadout'),rawResult:byId('rawResult'),rawExact:byId('rawExact'),signalResult:byId('signalResult'),
 signalResultLabel:byId('signalResultLabel'),signalRange:byId('signalRange'),percentResult:byId('percentResult'),rangeStatus:byId('rangeStatus'),statusDetail:byId('statusDetail'),error:byId('calculationError')
};
if(Object.values(elements).some(element=>!element))return;
let currentRaw=13824;
const parse=value=>Number.parseFloat(String(value).replace(',','.'));
const format=(value,digits=3)=>Number.isFinite(value)?value.toLocaleString('de-DE',{minimumFractionDigits:digits,maximumFractionDigits:digits}):'–';
const formatRaw=value=>Number.isFinite(value)?Math.round(value).toLocaleString('de-DE'):'–';
const clamp=(value,min,max)=>Math.min(max,Math.max(min,value));
function updateInputMode(){
 const type=TYPES[elements.signalType.value];
 const isRaw=elements.inputKind.value==='raw';
 elements.inputValueLabel.textContent=isRaw?'Siemens-Rohwert':`Signalwert (${type.unit})`;
 elements.inputSuffix.textContent=isRaw?'INT':type.unit;
 elements.inputValue.step=isRaw?'1':'0.001';
}
function syncInputToRaw(){
 const type=elements.signalType.value;
 elements.inputValue.value=elements.inputKind.value==='raw'?String(Math.round(currentRaw)):String(Number(signalFromRaw(type,currentRaw).toFixed(6)));
}
function renderResult(result){
 currentRaw=result.raw;
 const state=STATES[result.status];
 elements.error.hidden=true;
 elements.rawResult.textContent=formatRaw(result.raw);
 elements.rawExact.textContent=Math.abs(result.rawExact-result.raw)>0.0001?`rechnerisch ${format(result.rawExact,3)} · gerundet auf INT`:'Ganzzahliger SPS-Wert';
 elements.signalResult.textContent=`${format(result.signal,3)} ${result.signalUnit}`;
 elements.signalResultLabel.textContent=`Signalwert (${result.signalUnit})`;
 elements.signalRange.textContent=`Nennbereich ${result.signalLabel}`;
 elements.percentResult.textContent=`${format(result.percent,2)} %`;
 elements.rangeStatus.textContent=state.label;
 elements.rangeStatus.dataset.state=result.status;
 elements.statusDetail.textContent=`${state.label} · ${state.detail}`;
 document.querySelectorAll('[data-state-key]').forEach(item=>item.classList.toggle('active',item.dataset.stateKey===result.status));
 elements.slider.value=String(clamp(result.raw,RAW_INT_MIN,RAW_INT_MAX));
 elements.sliderReadout.textContent=`${formatRaw(result.raw)} · ${format(result.signal,3)} ${result.signalUnit}`;
}
function renderFromInput(){
 updateInputMode();
 try{renderResult(calculate(elements.signalType.value,elements.inputKind.value,parse(elements.inputValue.value)))}
 catch(error){
  elements.error.textContent=error.message;elements.error.hidden=false;elements.rangeStatus.textContent='Eingabe prüfen';elements.rangeStatus.dataset.state='error';
  [elements.rawResult,elements.signalResult,elements.percentResult].forEach(element=>element.textContent='–');
  [elements.rawExact,elements.signalRange,elements.statusDetail,elements.sliderReadout].forEach(element=>element.textContent='–');
  document.querySelectorAll('[data-state-key]').forEach(item=>item.classList.remove('active'));
 }
}
function applyRaw(raw){
 currentRaw=Math.round(Number(raw));
 syncInputToRaw();
 renderFromInput();
}
elements.inputValue.addEventListener('input',renderFromInput);
elements.inputValue.addEventListener('change',renderFromInput);
elements.slider.addEventListener('input',()=>applyRaw(elements.slider.value));
elements.inputKind.addEventListener('change',()=>{syncInputToRaw();updateInputMode();renderFromInput()});
elements.signalType.addEventListener('change',()=>{syncInputToRaw();updateInputMode();renderFromInput()});
document.querySelectorAll('[data-raw]').forEach(button=>button.addEventListener('click',()=>applyRaw(button.dataset.raw)));
updateInputMode();renderFromInput();
})();
