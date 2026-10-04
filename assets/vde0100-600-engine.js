/* SK PLT Tools · VDE 0100-600 Plausibilitäts-Engine · 2.1.0.1-Beta */
(function(root,factory){
  const api=factory();
  if(typeof module==='object'&&module.exports)module.exports=api;
  root.SK_VDE_ENGINE=Object.freeze(api);
})(typeof globalThis!=='undefined'?globalThis:this,function(){
  'use strict';
  const VERSION='2.1.0.1-Beta';
  const NUMBER_FIELDS=new Set(['conductors','crossSection','length','nominalCurrent','nominalVoltage','loadCurrent','continuity','loopImpedance','voltageDrop','voltageDropPercent','rcdRatedCurrent','rcdNominalResidual','rcdTripCurrent','rcdTripTime']);
  const FIELD_DEFS={
    protocolType:{label:'Protokolltyp',section:'Dokument',type:'choice',required:true,options:[['supported','VDE 0100-600 / Einzelprüfer'],['other','Anderer Protokolltyp']]},
    testReason:{label:'Prüfgrund',section:'Stammdaten',type:'choice',required:true,options:[['Erstprüfung','Erstprüfung'],['Wiederholungsprüfung','Wiederholungsprüfung'],['Änderung','Nach Änderung / Instandsetzung'],['other','Sonstiger Prüfgrund']]},
    building:{label:'Gebäude',section:'Stammdaten',type:'text',required:true},room:{label:'PLT-Raum',section:'Stammdaten',type:'text',required:true},cabinet:{label:'Schrank',section:'Stammdaten',type:'text',required:true},feeder:{label:'Abgang',section:'Stammdaten',type:'text',required:true},
    deviceName:{label:'Messgerät / Fabrikat',section:'Messgerät',type:'text',required:true},deviceNumber:{label:'Typ / Gerätenummer',section:'Messgerät',type:'text',required:true},calibrationState:{label:'Kalibrierstatus',section:'Messgerät',type:'choice',required:true,options:[['valid','Gültig / im Protokoll nachgewiesen'],['expired','Abgelaufen'],['unknown','Nicht feststellbar']]},
    cableType:{label:'Kabel-/Leitungstyp',section:'Stromkreis',type:'text',required:true},conductors:{label:'Aderzahl',section:'Stromkreis',type:'number',unit:'',required:true,min:1,max:20},crossSection:{label:'Leiterquerschnitt',section:'Stromkreis',type:'number',unit:'mm²',required:true,min:0.25,max:630},length:{label:'Leitungslänge',section:'Stromkreis',type:'number',unit:'m',required:true,min:0,max:5000},protectiveDevice:{label:'Überstromschutzeinrichtung',section:'Stromkreis',type:'text',required:true},nominalCurrent:{label:'Nennstrom In',section:'Stromkreis',type:'number',unit:'A',required:true,min:0.1,max:1600},nominalVoltage:{label:'Nennspannung Un',section:'Stromkreis',type:'number',unit:'V',required:true,min:12,max:1500},loadCurrent:{label:'Verbraucherstrom Ib',section:'Stromkreis',type:'number',unit:'A',required:false,min:0,max:1600},
    visualStatus:{label:'Besichtigen',section:'Besichtigen',type:'choice',required:true,options:[['io','i.O.'],['nio','n.i.O.'],['nrel','nicht relevant']]},measurementStatus:{label:'Messen',section:'Messen',type:'choice',required:true,options:[['io','i.O.'],['nio','n.i.O.'],['nrel','nicht relevant']]},functionalStatus:{label:'Erproben',section:'Erproben',type:'choice',required:true,options:[['io','i.O.'],['nio','n.i.O.'],['nrel','nicht relevant']]},
    continuity:{label:'Schutzleiter-/Niederohmwert',section:'Messwerte',type:'number',unit:'Ω',required:true,min:0,max:100},insulationValues:{label:'Isolationswiderstände',section:'Messwerte',type:'text',unit:'MΩ',required:true},loopImpedance:{label:'Schleifenimpedanz Zs',section:'Messwerte',type:'number',unit:'Ω',required:true,min:0,max:100},voltageDrop:{label:'Spannungsfall ΔU',section:'Messwerte',type:'number',unit:'V',required:false,min:0,max:1000},voltageDropPercent:{label:'Spannungsfall ε',section:'Messwerte',type:'number',unit:'%',required:true,min:0,max:100},
    rcdType:{label:'RCD-Typ',section:'RCD',type:'choice',required:false,options:[['A','Typ A'],['AC','Typ AC'],['F','Typ F'],['B','Typ B'],['none','Keine RCD vorhanden']]},rcdRatedCurrent:{label:'RCD-Nennstrom',section:'RCD',type:'number',unit:'A',required:false,min:1,max:1000},rcdNominalResidual:{label:'RCD-Nennfehlerstrom IΔn',section:'RCD',type:'number',unit:'mA',required:false,min:1,max:1000},rcdTripCurrent:{label:'RCD-Auslösestrom',section:'RCD',type:'number',unit:'mA',required:false,min:0,max:2000},rcdTripTime:{label:'RCD-Auslösezeit',section:'RCD',type:'number',unit:'ms',required:false,min:0,max:5000},
    remarks:{label:'Bemerkungen / Maßnahmen',section:'Abschluss',type:'text',required:false},signatureState:{label:'Prüferbestätigung / Unterschrift',section:'Abschluss',type:'choice',required:true,options:[['present','Vorhanden'],['missing','Fehlt']]},testDate:{label:'Prüfdatum',section:'Abschluss',type:'date',required:true},tester:{label:'Prüfer',section:'Abschluss',type:'text',required:true}
  };
  const number=value=>{if(typeof value==='number')return Number.isFinite(value)?value:null;const normalized=String(value??'').trim().replace(/\s/g,'').replace(/(?<=\d)[.](?=\d{3}(?:\D|$))/g,'').replace(',','.').replace(/[^0-9+\-.]/g,'');const parsed=Number.parseFloat(normalized);return Number.isFinite(parsed)?parsed:null};
  const valuesList=value=>String(value??'').split(/[;|/\s]+/).map(number).filter(Number.isFinite);
  const present=value=>value!==null&&value!==undefined&&String(value).trim()!=='';
  function normalize(data){const out={...data};NUMBER_FIELDS.forEach(key=>{if(present(out[key]))out[key]=number(out[key])});return out}
  function curveFactor(device){const value=String(device||'').toUpperCase();if(/(^|\W)D\s*\d/.test(value))return 20;if(/(^|\W)C\s*\d/.test(value))return 10;if(/(^|\W)B\s*\d/.test(value))return 5;return null}
  function checkData(input,config={}){
    const data=normalize(input), checks=[], skipped=new Set(data._notRelevant||[]);
    const add=(id,section,status,title,detail,fields=[],severity='error',limit=null)=>checks.push({id,section,status,title,detail,fields,severity,limit});
    Object.entries(FIELD_DEFS).forEach(([key,def])=>{if(def.required&&!skipped.has(key)&&!present(data[key]))add(`REQ-${key}`,def.section,'open',`${def.label} ist offen`,'Kein sicherer Wert erkannt. Bitte Original prüfen und ergänzen oder als nicht relevant kennzeichnen.',[key],'warning')});
    Object.entries(FIELD_DEFS).forEach(([key,def])=>{if(skipped.has(key)||!present(data[key])||def.type!=='number')return;const value=number(data[key]);if(value===null||value<def.min||value>def.max)add(`RANGE-${key}`,def.section,'fail',`${def.label} liegt außerhalb des Erfassungsbereichs`,`Erkannt: ${data[key]} ${def.unit||''}. Zulässiger Eingabebereich: ${def.min} bis ${def.max} ${def.unit||''}.`,[key],'error',{min:def.min,max:def.max,unit:def.unit||''})});
    if(data.protocolType&&data.protocolType!=='supported')add('DOC-TYPE','Dokument','fail','Protokolltyp nicht unterstützt','Die automatische Formularzuordnung passt nicht zum hinterlegten Prüfbericht nach VDE 0100-600.', ['protocolType']);
    if(!skipped.has('calibrationState')&&data.calibrationState==='expired')add('DEV-CAL','Messgerät','fail','Kalibrierstatus abgelaufen','Das Protokoll weist keinen gültigen Kalibrierstatus des Messgeräts aus.',['calibrationState']);
    if(!skipped.has('calibrationState')&&data.calibrationState==='unknown')add('DEV-CAL-OPEN','Messgerät','open','Kalibrierstatus nicht feststellbar','Gültigkeit oder Nachweis des verwendeten Messgeräts am Original kontrollieren.',['calibrationState'],'warning');
    if(!skipped.has('signatureState')&&data.signatureState==='missing')add('SIGN-MISSING','Abschluss','fail','Prüferbestätigung fehlt','Unterschrift beziehungsweise Prüferbestätigung ist nicht vorhanden.',['signatureState']);
    for(const key of ['visualStatus','measurementStatus','functionalStatus'])if(data[key]==='nio')add(`STATUS-${key}`,'Bewertung','fail',`${FIELD_DEFS[key].label} ist n.i.O.`, 'Die negative Einzelbewertung führt zu einem nicht plausiblen Gesamtergebnis.',[key]);
    const insulation=valuesList(data.insulationValues);if(!skipped.has('insulationValues')&&present(data.insulationValues)){
      const threshold=number(config.insulationMinMOhm)??1;
      if(!insulation.length)add('MEAS-INS-FORMAT','Messwerte','open','Isolationswerte nicht sicher lesbar','Mindestens ein numerischer Isolationswert in MΩ ist erforderlich.', ['insulationValues'],'warning');
      else if(insulation.some(value=>value<threshold))add('MEAS-INS','Messwerte','fail','Isolationswiderstand unterschreitet den Prüfwert',`Mindestens ein Wert liegt unter ${threshold} MΩ.`,['insulationValues'],'error',{min:threshold,unit:'MΩ'});
      else add('MEAS-INS','Messwerte','pass','Isolationswiderstände plausibel',`${insulation.length} Wert(e), kleinster Wert ${Math.min(...insulation)} MΩ; hinterlegter Prüfwert ≥ ${threshold} MΩ.`,['insulationValues'],'info',{min:threshold,unit:'MΩ'});
    }
    if(!skipped.has('continuity')&&Number.isFinite(data.continuity)){
      const warn=number(config.continuityWarningOhm)??1;
      if(data.continuity>warn)add('MEAS-RLOW','Messwerte','open','Niederohmwert auffällig hoch',`Erkannt: ${data.continuity} Ω. Der interne Hinweiswert von ${warn} Ω ist kein allgemeiner Normgrenzwert; Leiterlänge und Querschnitt fachlich prüfen.`,['continuity'],'warning',{max:warn,unit:'Ω'});
      else add('MEAS-RLOW','Messwerte','pass','Niederohmwert unauffällig',`${data.continuity} Ω liegt unter dem internen Hinweiswert ${warn} Ω.`,['continuity'],'info',{max:warn,unit:'Ω'});
    }
    if(!skipped.has('loopImpedance')&&!skipped.has('nominalCurrent')&&Number.isFinite(data.loopImpedance)&&Number.isFinite(data.nominalCurrent)){
      const factor=curveFactor(data.protectiveDevice);if(!factor)add('MEAS-ZS-CURVE','Messwerte','open','Auslösekennlinie für Zs fehlt','B-, C- oder D-Kennlinie ergänzen, damit der rechnerische Zs-Vergleich möglich ist.',['protectiveDevice'],'warning');
      else{const u0=number(config.phaseVoltage)??230,max=u0/(factor*data.nominalCurrent),ok=data.loopImpedance<=max;add('MEAS-ZS','Messwerte',ok?'pass':'fail',ok?'Schleifenimpedanz rechnerisch plausibel':'Schleifenimpedanz überschreitet den Rechenwert',`Zs ${data.loopImpedance} Ω; Rechenwert ${max.toFixed(3)} Ω aus U₀ ${u0} V / (${factor} × ${data.nominalCurrent} A).`,['loopImpedance','protectiveDevice','nominalCurrent'],ok?'info':'error',{max,unit:'Ω'});}
    }
    if(!skipped.has('loadCurrent')&&!skipped.has('nominalCurrent')&&Number.isFinite(data.loadCurrent)&&Number.isFinite(data.nominalCurrent)){const ok=data.loadCurrent<=data.nominalCurrent;add('CIRCUIT-IB-IN','Stromkreis',ok?'pass':'fail',ok?'Belastungsstrom und Nennstrom plausibel':'Belastungsstrom größer als Nennstrom',`Ib ${data.loadCurrent} A; In ${data.nominalCurrent} A.`,['loadCurrent','nominalCurrent'],ok?'info':'error')}
    if(!skipped.has('voltageDropPercent')&&Number.isFinite(data.voltageDropPercent)){const limit=number(config.voltageDropLimitPercent)??5,ok=data.voltageDropPercent<=limit;add('MEAS-DU','Messwerte',ok?'pass':'fail',ok?'Spannungsfall innerhalb des Prüfziels':'Spannungsfall überschreitet das Prüfziel',`Erkannt: ${data.voltageDropPercent} %; hinterlegtes Prüfziel ≤ ${limit} %.`,['voltageDropPercent'],ok?'info':'error',{max:limit,unit:'%'})}
    const rcdPresent=!skipped.has('rcdType')&&(data.rcdType&&data.rcdType!=='none'||[data.rcdNominalResidual,data.rcdTripCurrent,data.rcdTripTime].some(Number.isFinite));
    if(rcdPresent){
      if(!Number.isFinite(data.rcdNominalResidual))add('RCD-IDN','RCD','open','RCD-Nennfehlerstrom fehlt','IΔn wird für die Plausibilitätsprüfung benötigt.',['rcdNominalResidual'],'warning');
      if(Number.isFinite(data.rcdNominalResidual)&&Number.isFinite(data.rcdTripCurrent)){const ok=data.rcdTripCurrent<=data.rcdNominalResidual;add('RCD-I','RCD',ok?'pass':'fail',ok?'RCD-Auslösestrom plausibel':'RCD-Auslösestrom zu hoch',`IΔ ${data.rcdTripCurrent} mA; IΔn ${data.rcdNominalResidual} mA.`,['rcdTripCurrent','rcdNominalResidual'],ok?'info':'error')}
      if(Number.isFinite(data.rcdTripTime)){const limit=number(config.rcdTripTimeLimitMs)??300,ok=data.rcdTripTime<=limit;add('RCD-T','RCD',ok?'pass':'fail',ok?'RCD-Auslösezeit plausibel':'RCD-Auslösezeit zu lang',`tA ${data.rcdTripTime} ms; hinterlegter Standard-Prüfwert ≤ ${limit} ms. Abweichende RCD-Typen/Prüfbedingungen fachlich berücksichtigen.`,['rcdTripTime'],ok?'info':'error',{max:limit,unit:'ms'})}
    }
    if(['nio'].includes(data.visualStatus)||['nio'].includes(data.measurementStatus)||['nio'].includes(data.functionalStatus)){if(!present(data.remarks))add('CONS-REMARK','Abschluss','fail','Bemerkung zu n.i.O. fehlt','Eine negative Bewertung benötigt eine dokumentierte Feststellung oder Maßnahme.',['remarks'])}
    const confidence=data._confidence||{};Object.entries(confidence).forEach(([key,value])=>{if(!skipped.has(key)&&FIELD_DEFS[key]&&present(data[key])&&Number(value)<0.72&&!checks.some(item=>item.fields.includes(key)&&item.status!=='pass'))add(`CONF-${key}`,FIELD_DEFS[key].section,'open',`${FIELD_DEFS[key].label} unsicher erkannt`,`Erkennungsqualität ${Math.round(Number(value)*100)} %. Bitte Wert am Original bestätigen oder korrigieren.`,[key],'warning')});
    return checks;
  }
  function issueFromCheck(check,data){const field=check.fields[0],def=FIELD_DEFS[field]||{label:field,type:'text',section:check.section};return{id:check.id,title:check.title,message:check.detail,section:check.section,severity:check.severity,field,fields:check.fields,definition:def,detected:data[field],status:check.status,resolution:null}}
  function buildIssues(data,config){return checkData(data,config).filter(item=>item.status==='open'||item.status==='fail').map(item=>issueFromCheck(item,data))}
  function finalState(data,issues,config){const unresolved=issues.filter(item=>!item.resolution),checks=checkData(data,config),failed=checks.filter(item=>item.status==='fail');return{complete:unresolved.length===0,plausible:unresolved.length===0&&failed.length===0,unresolved,failed,checks}}
  function parseText(text){
    const raw=String(text||''),compact=raw.replace(/\s+/g,' '),data={_confidence:{}};
    const set=(key,value,confidence=.76)=>{if(present(value)){data[key]=typeof value==='number'?value:String(value).trim();data._confidence[key]=confidence}};
    if(/VDE\s*0100[-–]?600/i.test(raw))set('protocolType','supported',.98);
    if(/Erstpr[uü]fung/i.test(raw))set('testReason','Erstprüfung',.9);else if(/Wiederholungspr[uü]fung/i.test(raw))set('testReason','Wiederholungsprüfung',.9);else if(/Instandsetzung|Änderung|Aenderung/i.test(raw))set('testReason','Änderung',.86);
    const patterns={nominalVoltage:/\b(?:Un|Nennspannung)\D{0,15}(\d{2,4})\s*V/i,nominalCurrent:/\b(?:In|Nennstrom)\D{0,12}(\d{1,4}(?:[,.]\d+)?)\s*A/i,continuity:/\b(?:Rlow|Niederohm\w*)\D{0,18}(\d+[,.]\d+)\s*[ΩO]/i,loopImpedance:/\b(?:Zs|Schleifenimpedanz)\D{0,18}(\d+[,.]\d+)\s*[ΩO]/i,voltageDropPercent:/\b(?:Spannungsfall|ε|e\s*\(%\))\D{0,20}(\d+[,.]\d+)\s*%/i,rcdNominalResidual:/I\s*[ΔA]?n?\D{0,12}(\d+(?:[,.]\d+)?)\s*mA/i,rcdTripTime:/\b(?:Ausl[öo]sezeit|ta)\D{0,15}(\d+(?:[,.]\d+)?)\s*ms/i};
    Object.entries(patterns).forEach(([key,re])=>{const match=compact.match(re);if(match)set(key,number(match[1]),.74)});
    const breaker=compact.match(/\b([BCD])\s*(\d{1,3})\s*A?\b/i);if(breaker){set('protectiveDevice',`${breaker[1].toUpperCase()}${breaker[2]}`,.78);if(!present(data.nominalCurrent))set('nominalCurrent',number(breaker[2]),.72)}
    return data;
  }
  return{VERSION,FIELD_DEFS,number,valuesList,normalize,curveFactor,checkData,buildIssues,finalState,parseText};
});
