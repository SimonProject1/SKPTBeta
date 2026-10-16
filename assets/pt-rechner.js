/* Pt100-/Pt1000-Rechner mit IEC-60751-Bereichsprüfung · 2.6.1.9-Beta */
(()=>{
  'use strict';
  const $=id=>document.getElementById(id);
  const MIN_C=-200;
  const MAX_C=850;
  function resistance(t,r0){
    const A=3.9083e-3,B=-5.775e-7,C=-4.183e-12;
    return t>=0?r0*(1+A*t+B*t*t):r0*(1+A*t+B*t*t+C*(t-100)*t*t*t);
  }
  function outOfRange(){
    $('out').textContent='Außerhalb IEC 60751 (−200 bis 850 °C)';
    $('out').dataset.state='error';
  }
  function show(value,digits,symbol){
    $('out').textContent=`${window.de(value,digits)} ${symbol}`;
    delete $('out').dataset.state;
  }
  function calculate(){
    const value=window.num($('x').value),r0=window.num($('sensor').value);
    if(!Number.isFinite(value)){$('out').textContent='–';return;}
    if($('dir').value==='tr'){
      const celsius=SK_UNITS.convert(value,'temperature',$('inputUnit').value,'celsius');
      if(!Number.isFinite(celsius)||celsius<MIN_C||celsius>MAX_C){outOfRange();return;}
      const ohm=resistance(celsius,r0);
      const result=SK_UNITS.convert(ohm,'resistance','ohm',$('outputUnit').value);
      show(result,3,SK_UNITS.unit('resistance',$('outputUnit').value).symbol);
      return;
    }
    const ohm=SK_UNITS.convert(value,'resistance',$('inputUnit').value,'ohm');
    const minOhm=resistance(MIN_C,r0),maxOhm=resistance(MAX_C,r0);
    if(!Number.isFinite(ohm)||ohm<minOhm||ohm>maxOhm){outOfRange();return;}
    let lo=MIN_C,hi=MAX_C;
    for(let index=0;index<50;index++){
      const middle=(lo+hi)/2;
      resistance(middle,r0)<ohm?lo=middle:hi=middle;
    }
    const calculated=SK_UNITS.convert((lo+hi)/2,'temperature','celsius',$('outputUnit').value);
    const result=Math.abs(calculated)<5e-9?0:calculated;
    show(result,2,SK_UNITS.unit('temperature',$('outputUnit').value).symbol);
  }
  function configure(resetValue=false){
    const tempToResistance=$('dir').value==='tr';
    const inputCategory=tempToResistance?'temperature':'resistance';
    const outputCategory=tempToResistance?'resistance':'temperature';
    SK_UNITS.populateSelect($('inputUnit'),inputCategory,SK_UNITS.category(inputCategory).defaultUnit,{includeAll:true});
    SK_UNITS.populateSelect($('outputUnit'),outputCategory,SK_UNITS.category(outputCategory).defaultUnit,{includeAll:true});
    $('inputUnitLabel').textContent=`Eingabeeinheit (${SK_UNITS.category(inputCategory).name})`;
    $('outputUnitLabel').textContent=`Ergebniseinheit (${SK_UNITS.category(outputCategory).name})`;
    if(resetValue)$('x').value=tempToResistance?'0':$('sensor').value;
    calculate();
  }
  async function init(){
    await SK_UNITS.ready;
    configure();
    $('dir').addEventListener('change',()=>configure(true));
    $('sensor').addEventListener('input',calculate);
    $('x').addEventListener('input',calculate);
    $('inputUnit').addEventListener('sk:unit-change',event=>{
      const field=$('x'),value=window.num(field.value);
      if(Number.isFinite(value))field.value=SK_UNITS.inputValue(SK_UNITS.convert(value,event.detail.categoryId,event.detail.oldUnit,event.detail.newUnit));
      calculate();
    });
    $('outputUnit').addEventListener('sk:unit-change',calculate);
    calculate();
  }
  document.readyState==='loading'?document.addEventListener('DOMContentLoaded',init,{once:true}):init();
  window.SK_PT=Object.freeze({resistance,minC:MIN_C,maxC:MAX_C});
})();
