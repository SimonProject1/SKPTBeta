/* Analogsignal-Rechner · einheitenlose TÜV-Skalierung · 2.6.6.1-Beta */
(()=>{'use strict';
const SIGNALS=Object.freeze({
  '4-20mA':Object.freeze({min:4,max:20,unit:'mA',label:'4–20 mA'}),
  '0-20mA':Object.freeze({min:0,max:20,unit:'mA',label:'0–20 mA'}),
  '0-10V':Object.freeze({min:0,max:10,unit:'V',label:'0–10 V'}),
  '2-10V':Object.freeze({min:2,max:10,unit:'V',label:'2–10 V'})
});
const $=id=>document.getElementById(id);
const number=id=>window.num($(id).value);
const signal=()=>SIGNALS[$('signalType').value]||SIGNALS['4-20mA'];
function setError(message=''){
  const error=$('analogError');
  error.textContent=message;
  error.hidden=!message;
  if(message){$('out').textContent='–';$('pct').textContent='–'}
}
function syncLabels(){
  const processToSignal=$('dir').value==='ps',type=signal();
  $('inputLabel').textContent=processToSignal?'Skalierungswert (einheitenlos)':`Signalwert (${type.unit})`;
  $('outputLabel').textContent=processToSignal?`Signalwert (${type.label})`:'Skalierungswert (einheitenlos)';
  $('x').setAttribute('aria-label',$('inputLabel').textContent);
}
function calculate(){
  const ma=number('p0'),me=number('p1'),value=number('x'),type=signal(),signalMin=type.min,signalMax=type.max;
  syncLabels();
  if([ma,me,value].some(Number.isNaN)){
    setError('Ungültige Eingabe: Bitte MA, ME und Eingabewert vollständig als Zahlen eingeben.');
    return false;
  }
  if(ma===me){
    setError('Ungültige Eingabe: MA und ME müssen unterschiedlich sein.');
    return false;
  }
  setError();
  let result,percent;
  if($('dir').value==='ps'){
    percent=(value-ma)/(me-ma)*100;
    result=signalMin+(value-ma)/(me-ma)*(signalMax-signalMin);
    $('out').textContent=`${window.de(result)} ${type.unit}`;
  }else{
    percent=(value-signalMin)/(signalMax-signalMin)*100;
    result=ma+(value-signalMin)/(signalMax-signalMin)*(me-ma);
    $('out').textContent=window.de(result);
  }
  $('pct').textContent=`${window.de(percent,1)} %`;
  return true;
}
function init(){
  const form=$('analogForm');
  if(!form)return;
  form.addEventListener('submit',event=>{event.preventDefault();calculate()});
  for(const id of ['p0','p1','x']){
    $(id).addEventListener('input',calculate);
    $(id).addEventListener('change',calculate);
  }
  for(const id of ['signalType','dir'])$(id).addEventListener('change',calculate);
  calculate();
}
document.readyState==='loading'?document.addEventListener('DOMContentLoaded',init,{once:true}):init();
})();
