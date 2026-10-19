/* Analogsignal-Rechner · einheitenlose TÜV-Skalierung · 3.1.0.4 */
(()=>{'use strict';
const SIGNALS=Object.freeze({
  '4-20mA':Object.freeze({min:4,max:20,unit:'mA',label:'4–20 mA'}),
  '0-20mA':Object.freeze({min:0,max:20,unit:'mA',label:'0–20 mA'}),
  '0-10V':Object.freeze({min:0,max:10,unit:'V',label:'0–10 V'}),
  '2-10V':Object.freeze({min:2,max:10,unit:'V',label:'2–10 V'})
});
const $=id=>document.getElementById(id);
const signal=()=>SIGNALS[$('signalType').value]||SIGNALS['4-20mA'];
const fields=()=>[$('p0'),$('p1'),$('x')];
const labels=new Map([['p0','Messbereichsanfang MA'],['p1','Messbereichsende ME'],['x','Eingabewert']]);
function clearResult(){$('out').textContent='–';$('pct').textContent='–'}
function validate(strict=false){
 const issues=[];let pending=false;
 fields().forEach(input=>{const result=SK_NUMERIC.analyze(input.value);if(result.state==='intermediate'){pending=true;if(strict)issues.push({input,message:`${labels.get(input.id)}: Zahl bitte vollständig eingeben.`})}else if(result.state==='invalid')issues.push({input,message:`${labels.get(input.id)}: ${result.reason}`})});
 if(pending&&!strict&&!issues.length){SK_NUMERIC.clear(fields(),$('analogError'));clearResult();return null}
 if(SK_NUMERIC.report(fields(),$('analogError'),issues)){clearResult();return null}
 return fields().map(input=>SK_NUMERIC.parse(input.value));
}
function syncLabels(){const processToSignal=$('dir').value==='ps',type=signal();$('inputLabel').textContent=processToSignal?'Skalierungswert (einheitenlos)':`Signalwert (${type.unit})`;$('outputLabel').textContent=processToSignal?`Signalwert (${type.label})`:'Skalierungswert (einheitenlos)';$('x').setAttribute('aria-label',$('inputLabel').textContent)}
function calculate(strict=false){
 syncLabels();const values=validate(strict);if(!values)return false;
 const [ma,me,value]=values,type=signal(),signalMin=type.min,signalMax=type.max;
 if(ma===me){SK_NUMERIC.report(fields(),$('analogError'),[{input:$('p0'),message:'Messbereich: MA und ME müssen unterschiedlich sein.'},{input:$('p1'),message:'Messbereich: MA und ME müssen unterschiedlich sein.'}]);clearResult();return false}
 SK_NUMERIC.clear(fields(),$('analogError'));let result,percent;
 if($('dir').value==='ps'){percent=(value-ma)/(me-ma)*100;result=signalMin+(value-ma)/(me-ma)*(signalMax-signalMin);$('out').textContent=`${window.de(result)} ${type.unit}`}
 else{percent=(value-signalMin)/(signalMax-signalMin)*100;result=ma+(value-signalMin)/(signalMax-signalMin)*(me-ma);$('out').textContent=window.de(result)}
 $('pct').textContent=`${window.de(percent,1)} %`;return true;
}
function init(){const form=$('analogForm');if(!form)return;form.addEventListener('submit',event=>{event.preventDefault();calculate(true)});for(const id of ['p0','p1','x']){$(id).addEventListener('input',()=>calculate(false));$(id).addEventListener('change',()=>calculate(true))}for(const id of ['signalType','dir'])$(id).addEventListener('change',()=>calculate(true));calculate(true)}
document.readyState==='loading'?document.addEventListener('DOMContentLoaded',init,{once:true}):init();
})();
