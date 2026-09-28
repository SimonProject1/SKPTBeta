(()=>{'use strict';
const RAW_MAX=27648;
const TYPES=Object.freeze({
 '4-20mA':Object.freeze({min:4,max:20,unit:'mA',label:'4–20 mA'}),
 '0-20mA':Object.freeze({min:0,max:20,unit:'mA',label:'0–20 mA'}),
 '0-10V':Object.freeze({min:0,max:10,unit:'V',label:'0–10 V'}),
 '2-10V':Object.freeze({min:2,max:10,unit:'V',label:'2–10 V'})
});
function calculate(type,inputKind,value,physicalMin,physicalMax){
 const signal=TYPES[type];
 if(!signal)throw new Error('Unbekannte Signalart.');
 const numbers=[value,physicalMin,physicalMax].map(Number);
 if(numbers.some(number=>!Number.isFinite(number)))throw new Error('Bitte alle Zahlenfelder vollständig ausfüllen.');
 const [input,min,max]=numbers;
 if(min===max)throw new Error('Der physikalische Minimal- und Maximalwert müssen unterschiedlich sein.');
 let percent;
 if(inputKind==='raw')percent=input/RAW_MAX*100;
 else if(inputKind==='signal')percent=(input-signal.min)/(signal.max-signal.min)*100;
 else if(inputKind==='percent')percent=input;
 else if(inputKind==='physical')percent=(input-min)/(max-min)*100;
 else throw new Error('Unbekannte Eingabeart.');
 const rawExact=percent/100*RAW_MAX;
 return Object.freeze({raw:Math.round(rawExact),rawExact,signal:signal.min+percent/100*(signal.max-signal.min),signalUnit:signal.unit,signalLabel:signal.label,percent,physical:min+percent/100*(max-min),physicalMin:min,physicalMax:max});
}
const api=Object.freeze({RAW_MAX,TYPES,calculate});
if(typeof globalThis!=='undefined')globalThis.SK_SIEMENS_ANALOG=api;
if(typeof document==='undefined')return;
const byId=id=>document.getElementById(id);
const elements={signalType:byId('signalType'),inputKind:byId('inputKind'),physicalMin:byId('physicalMin'),physicalMax:byId('physicalMax'),physicalUnit:byId('physicalUnit'),inputValue:byId('inputValue'),inputValueLabel:byId('inputValueLabel'),rawResult:byId('rawResult'),rawExact:byId('rawExact'),signalResult:byId('signalResult'),signalRange:byId('signalRange'),percentResult:byId('percentResult'),physicalResult:byId('physicalResult'),physicalRange:byId('physicalRange'),rangeStatus:byId('rangeStatus'),error:byId('calculationError')};
if(Object.values(elements).some(element=>!element))return;
const parse=value=>Number.parseFloat(String(value).replace(',','.'));
const format=(value,digits=3)=>Number.isFinite(value)?value.toLocaleString('de-DE',{minimumFractionDigits:digits,maximumFractionDigits:digits}):'–';
const formatRaw=value=>Number.isFinite(value)?Math.round(value).toLocaleString('de-DE'):'–';
function inputLabel(){const signal=TYPES[elements.signalType.value];const labels={raw:'Siemens-Rohwert',signal:`Signalwert (${signal.unit})`,percent:'Prozentwert (%)',physical:`Physikalischer Wert (${elements.physicalUnit.value.trim()||'Einheit'})`};elements.inputValueLabel.textContent=labels[elements.inputKind.value]||'Eingabewert'}
function render(){
 inputLabel();elements.error.hidden=true;
 try{
  const result=calculate(elements.signalType.value,elements.inputKind.value,parse(elements.inputValue.value),parse(elements.physicalMin.value),parse(elements.physicalMax.value));
  const unit=elements.physicalUnit.value.trim()||'Einheit';
  elements.rawResult.textContent=formatRaw(result.raw);elements.rawExact.textContent=`rechnerisch ${format(result.rawExact,3)}`;
  elements.signalResult.textContent=`${format(result.signal,3)} ${result.signalUnit}`;elements.signalRange.textContent=`Nennbereich ${result.signalLabel}`;
  elements.percentResult.textContent=`${format(result.percent,2)} %`;
  elements.physicalResult.textContent=`${format(result.physical,3)} ${unit}`;elements.physicalRange.textContent=`Messbereich ${format(result.physicalMin,3)}…${format(result.physicalMax,3)} ${unit}`;
  const outside=result.percent<0||result.percent>100;elements.rangeStatus.textContent=outside?(result.percent<0?'Unterbereich':'Überbereich'):'Nennbereich';elements.rangeStatus.classList.toggle('outside',outside);
 }catch(error){
  elements.error.textContent=error.message;elements.error.hidden=false;elements.rangeStatus.textContent='Eingabe prüfen';elements.rangeStatus.classList.add('outside');
  [elements.rawResult,elements.signalResult,elements.percentResult,elements.physicalResult].forEach(element=>element.textContent='–');
  [elements.rawExact,elements.signalRange,elements.physicalRange].forEach(element=>element.textContent='–');
 }
}
Object.values(elements).filter(element=>element&&('value' in element)).forEach(element=>{element.addEventListener('input',render);element.addEventListener('change',render)});
render();
})();
