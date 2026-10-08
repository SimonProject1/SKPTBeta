/* SK PLT Tools · manueller VDE-Messwertprüfer · 2.1.1.0-Beta */
(function(root,factory){
  const api=factory();
  if(typeof module==='object'&&module.exports)module.exports=api;
  root.SK_VDE_ENGINE=Object.freeze(api);
})(typeof globalThis!=='undefined'?globalThis:this,function(){
  'use strict';

  const VERSION='2.1.1.0-Beta';

  const FIELD_DEFS=Object.freeze({
    voltageDropMode:{label:'Eingabeart',type:'choice'},
    measuredDropPercent:{label:'Gemessener Spannungsfall',unit:'%',type:'number',min:0},
    measuredDropVolts:{label:'Gemessener Spannungsfall ΔU',unit:'V',type:'number',min:0},
    nominalVoltage:{label:'Bezugsspannung Un',unit:'V',type:'number',exclusiveMin:0},
    approvedMaxDropPercent:{label:'Freigegebener maximaler Spannungsfall',unit:'%',type:'number',exclusiveMin:0},
    measuredInsulation:{label:'Kleinster gemessener Isolationswiderstand',unit:'MΩ',type:'number',min:0},
    approvedMinInsulation:{label:'Freigegebener Mindest-Isolationswiderstand',unit:'MΩ',type:'number',min:0},
    disconnectionMode:{label:'Bewertungsweg',type:'choice'},
    measuredLoopImpedance:{label:'Gemessene Schleifenimpedanz Zs',unit:'Ω',type:'number',min:0},
    approvedMaxLoopImpedance:{label:'Freigegebene maximale Schleifenimpedanz Zs,max',unit:'Ω',type:'number',exclusiveMin:0},
    phaseVoltage:{label:'Außenleiter-Erde-Spannung U0',unit:'V',type:'number',exclusiveMin:0},
    requiredTripCurrent:{label:'Erforderlicher Auslösestrom Ia aus freigegebener Schutzgerätebasis',unit:'A',type:'number',exclusiveMin:0},
    measuredShortCircuitCurrent:{label:'Gemessener Kurzschlussstrom Ik',unit:'A',type:'number',min:0},
    rcdMode:{label:'Prüfumfang',type:'choice'},
    measuredRcdTime:{label:'Gemessene RCD-Auslösezeit',unit:'ms',type:'number',min:0},
    approvedMaxRcdTime:{label:'Freigegebene maximale RCD-Auslösezeit',unit:'ms',type:'number',exclusiveMin:0},
    measuredRcdCurrent:{label:'Gemessener RCD-Auslösestrom',unit:'mA',type:'number',min:0},
    approvedMinRcdCurrent:{label:'Freigegebene untere Auslösestromgrenze',unit:'mA',type:'number',min:0},
    approvedMaxRcdCurrent:{label:'Freigegebene obere Auslösestromgrenze',unit:'mA',type:'number',exclusiveMin:0},
    measuredContinuity:{label:'Gemessener Niederohmigkeitswert',unit:'Ω',type:'number',min:0},
    approvedMaxContinuity:{label:'Freigegebener maximaler Niederohmigkeitswert',unit:'Ω',type:'number',exclusiveMin:0},
    measuredBonding:{label:'Gemessener Widerstand des Schutzpotentialausgleichs',unit:'Ω',type:'number',min:0},
    approvedMaxBonding:{label:'Freigegebener maximaler Widerstand des Schutzpotentialausgleichs',unit:'Ω',type:'number',exclusiveMin:0}
  });

  const MEASUREMENT_TYPES=Object.freeze({
    voltageDrop:{title:'Spannungsfall',code:'ΔU',section:'Leitungsbewertung'},
    insulation:{title:'Isolationsmessung',code:'RISO',section:'Isolationswiderstand'},
    disconnection:{title:'Schleifenimpedanz / Kurzschlussstrom',code:'Zs · Ik',section:'Automatische Abschaltung'},
    rcd:{title:'RCD-Prüfung',code:'RCD',section:'Fehlerstrom-Schutzeinrichtung'},
    continuity:{title:'Niederohmigkeit',code:'RPE',section:'Schutzleiter-Durchgängigkeit'},
    bonding:{title:'Schutzpotentialausgleich',code:'RPA',section:'Potentialausgleich'}
  });

  const present=value=>value!==null&&value!==undefined&&String(value).trim()!=='';
  function number(value){
    if(typeof value==='number')return Number.isFinite(value)?value:null;
    const source=String(value??'').trim().replace(/\s/g,'').replace(',','.');
    if(!/^[+-]?(?:\d+(?:\.\d*)?|\.\d+)$/.test(source))return null;
    const parsed=Number(source);
    return Number.isFinite(parsed)?parsed:null;
  }
  const format=(value,digits=3)=>new Intl.NumberFormat('de-DE',{maximumFractionDigits:digits,minimumFractionDigits:0}).format(value);
  const valueWithUnit=(value,unit,digits=3)=>`${format(value,digits)} ${unit}`;

  function requiredFields(type,input={}){
    switch(type){
      case 'voltageDrop':
        return input.voltageDropMode==='volts'
          ? ['voltageDropMode','measuredDropVolts','nominalVoltage','approvedMaxDropPercent']
          : ['voltageDropMode','measuredDropPercent','approvedMaxDropPercent'];
      case 'insulation': return ['measuredInsulation','approvedMinInsulation'];
      case 'disconnection':
        if(input.disconnectionMode==='loop-approved')return ['disconnectionMode','measuredLoopImpedance','approvedMaxLoopImpedance'];
        if(input.disconnectionMode==='loop-formula')return ['disconnectionMode','measuredLoopImpedance','phaseVoltage','requiredTripCurrent'];
        if(input.disconnectionMode==='short-current')return ['disconnectionMode','measuredShortCircuitCurrent','requiredTripCurrent'];
        return ['disconnectionMode'];
      case 'rcd':
        if(input.rcdMode==='time')return ['rcdMode','measuredRcdTime','approvedMaxRcdTime'];
        if(input.rcdMode==='current')return ['rcdMode','measuredRcdCurrent','approvedMinRcdCurrent','approvedMaxRcdCurrent'];
        if(input.rcdMode==='both')return ['rcdMode','measuredRcdTime','approvedMaxRcdTime','measuredRcdCurrent','approvedMinRcdCurrent','approvedMaxRcdCurrent'];
        return ['rcdMode'];
      case 'continuity': return ['measuredContinuity','approvedMaxContinuity'];
      case 'bonding': return ['measuredBonding','approvedMaxBonding'];
      default: return [];
    }
  }

  function incomplete(type,missing){
    return {
      version:VERSION,type,status:'incomplete',complete:false,
      title:MEASUREMENT_TYPES[type]?.title||'Unbekannte Messgröße',
      missing:missing.map(field=>({field,label:FIELD_DEFS[field]?.label||field})),
      errors:[],checks:[],limitText:'',formula:'',calculation:'',resultLabel:''
    };
  }

  function validate(type,input,fields){
    const errors=[];
    for(const field of fields){
      const def=FIELD_DEFS[field];
      if(!def||def.type!=='number')continue;
      const parsed=number(input[field]);
      if(parsed===null){errors.push({field,label:def.label,message:`${def.label}: gültige Zahl erforderlich.`});continue;}
      if(def.min!==undefined&&parsed<def.min)errors.push({field,label:def.label,message:`${def.label}: Wert muss mindestens ${def.min} ${def.unit||''} betragen.`});
      if(def.exclusiveMin!==undefined&&parsed<=def.exclusiveMin)errors.push({field,label:def.label,message:`${def.label}: Wert muss größer als ${def.exclusiveMin} ${def.unit||''} sein.`});
    }
    if((input.rcdMode==='current'||input.rcdMode==='both')&&present(input.approvedMinRcdCurrent)&&present(input.approvedMaxRcdCurrent)){
      const lower=number(input.approvedMinRcdCurrent),upper=number(input.approvedMaxRcdCurrent);
      if(lower!==null&&upper!==null&&lower>upper)errors.push({field:'approvedMaxRcdCurrent',label:FIELD_DEFS.approvedMaxRcdCurrent.label,message:'Die obere Auslösestromgrenze muss mindestens so groß wie die untere Grenze sein.'});
    }
    return errors;
  }

  function check(id,title,passed,measuredText,limitText,formula,calculation){
    return {id,title,status:passed?'pass':'fail',passed,measuredText,limitText,formula,calculation,resultLabel:passed?'i. O.':'nicht i. O.'};
  }

  function completeResult(type,checks){
    const passed=checks.every(item=>item.passed);
    const first=checks[0]||{};
    return {
      version:VERSION,type,title:MEASUREMENT_TYPES[type].title,status:passed?'pass':'fail',complete:true,
      missing:[],errors:[],checks,resultLabel:passed?'i. O.':'nicht i. O.',
      measuredText:checks.map(item=>item.measuredText).join(' · '),
      limitText:checks.map(item=>item.limitText).join(' · '),
      formula:checks.map(item=>item.formula).join(' | '),
      calculation:checks.map(item=>item.calculation).join(' | ')
    };
  }

  function evaluate(type,input={}){
    if(!MEASUREMENT_TYPES[type])return {version:VERSION,type,status:'error',complete:false,title:'Unbekannte Messgröße',missing:[],errors:[{field:'type',label:'Messgröße',message:'Die ausgewählte Messgröße ist nicht definiert.'}],checks:[],limitText:'',formula:'',calculation:'',resultLabel:''};
    const fields=requiredFields(type,input);
    const missing=fields.filter(field=>!present(input[field]));
    if(missing.length)return incomplete(type,missing);
    const errors=validate(type,input,fields);
    if(errors.length)return {version:VERSION,type,title:MEASUREMENT_TYPES[type].title,status:'error',complete:false,missing:[],errors,checks:[],limitText:'',formula:'',calculation:'',resultLabel:''};
    const n=field=>number(input[field]);
    const checks=[];

    if(type==='voltageDrop'){
      const limit=n('approvedMaxDropPercent');
      if(input.voltageDropMode==='volts'){
        const drop=n('measuredDropVolts'),voltage=n('nominalVoltage'),percent=drop/voltage*100;
        checks.push(check('VD-DU','Spannungsfall',percent<=limit,valueWithUnit(percent,'%',3),`≤ ${valueWithUnit(limit,'%',3)}`,'ΔU% = ΔU / Un × 100',`${format(drop)} V / ${format(voltage)} V × 100 = ${format(percent,3)} %; ${format(percent,3)} % ${percent<=limit?'≤':'>'} ${format(limit,3)} %`));
      }else{
        const measured=n('measuredDropPercent');
        checks.push(check('VD-PERCENT','Spannungsfall',measured<=limit,valueWithUnit(measured,'%',3),`≤ ${valueWithUnit(limit,'%',3)}`,'ΔU%gemessen ≤ ΔU%max',`${format(measured,3)} % ${measured<=limit?'≤':'>'} ${format(limit,3)} %`));
      }
    }

    if(type==='insulation'){
      const measured=n('measuredInsulation'),limit=n('approvedMinInsulation');
      checks.push(check('INS-MIN','Isolationswiderstand',measured>=limit,valueWithUnit(measured,'MΩ',3),`≥ ${valueWithUnit(limit,'MΩ',3)}`,'RISO,min gemessen ≥ RISO,min freigegeben',`${format(measured,3)} MΩ ${measured>=limit?'≥':'<'} ${format(limit,3)} MΩ`));
    }

    if(type==='disconnection'){
      const mode=input.disconnectionMode;
      if(mode==='loop-approved'){
        const measured=n('measuredLoopImpedance'),limit=n('approvedMaxLoopImpedance');
        checks.push(check('DISC-ZS-APPROVED','Schleifenimpedanz',measured<=limit,valueWithUnit(measured,'Ω',3),`≤ ${valueWithUnit(limit,'Ω',3)}`,'Zs,gemessen ≤ Zs,max freigegeben',`${format(measured,3)} Ω ${measured<=limit?'≤':'>'} ${format(limit,3)} Ω`));
      }else if(mode==='loop-formula'){
        const measured=n('measuredLoopImpedance'),u0=n('phaseVoltage'),ia=n('requiredTripCurrent'),limit=u0/ia;
        checks.push(check('DISC-ZS-FORMULA','Schleifenimpedanz',measured<=limit,valueWithUnit(measured,'Ω',3),`≤ ${valueWithUnit(limit,'Ω',3)}`,'Zs,max = U0 / Ia',`${format(u0,3)} V / ${format(ia,3)} A = ${format(limit,3)} Ω; ${format(measured,3)} Ω ${measured<=limit?'≤':'>'} ${format(limit,3)} Ω`));
      }else if(mode==='short-current'){
        const measured=n('measuredShortCircuitCurrent'),ia=n('requiredTripCurrent');
        checks.push(check('DISC-IK','Kurzschlussstrom',measured>=ia,valueWithUnit(measured,'A',3),`≥ ${valueWithUnit(ia,'A',3)}`,'Ik,gemessen ≥ Ia,erforderlich',`${format(measured,3)} A ${measured>=ia?'≥':'<'} ${format(ia,3)} A`));
      }
    }

    if(type==='rcd'){
      if(input.rcdMode==='time'||input.rcdMode==='both'){
        const measured=n('measuredRcdTime'),limit=n('approvedMaxRcdTime');
        checks.push(check('RCD-TIME','RCD-Auslösezeit',measured<=limit,valueWithUnit(measured,'ms',3),`≤ ${valueWithUnit(limit,'ms',3)}`,'tA,gemessen ≤ tA,max freigegeben',`${format(measured,3)} ms ${measured<=limit?'≤':'>'} ${format(limit,3)} ms`));
      }
      if(input.rcdMode==='current'||input.rcdMode==='both'){
        const measured=n('measuredRcdCurrent'),lower=n('approvedMinRcdCurrent'),upper=n('approvedMaxRcdCurrent'),passed=measured>=lower&&measured<=upper;
        checks.push(check('RCD-CURRENT','RCD-Auslösestrom',passed,valueWithUnit(measured,'mA',3),`${valueWithUnit(lower,'mA',3)} bis ${valueWithUnit(upper,'mA',3)}`,'IΔ,min freigegeben ≤ IΔ,gemessen ≤ IΔ,max freigegeben',`${format(lower,3)} mA ≤ ${format(measured,3)} mA ≤ ${format(upper,3)} mA`));
      }
    }

    if(type==='continuity'){
      const measured=n('measuredContinuity'),limit=n('approvedMaxContinuity');
      checks.push(check('CONT-MAX','Niederohmigkeit',measured<=limit,valueWithUnit(measured,'Ω',3),`≤ ${valueWithUnit(limit,'Ω',3)}`,'RPE,gemessen ≤ RPE,max freigegeben',`${format(measured,3)} Ω ${measured<=limit?'≤':'>'} ${format(limit,3)} Ω`));
    }

    if(type==='bonding'){
      const measured=n('measuredBonding'),limit=n('approvedMaxBonding');
      checks.push(check('BOND-MAX','Schutzpotentialausgleich',measured<=limit,valueWithUnit(measured,'Ω',3),`≤ ${valueWithUnit(limit,'Ω',3)}`,'RPA,gemessen ≤ RPA,max freigegeben',`${format(measured,3)} Ω ${measured<=limit?'≤':'>'} ${format(limit,3)} Ω`));
    }

    return completeResult(type,checks);
  }

  return {VERSION,FIELD_DEFS,MEASUREMENT_TYPES,present,number,format,requiredFields,validate,evaluate};
});
