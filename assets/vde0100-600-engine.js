/* SK PLT Tools · VDE 0100-600 Messwert-Plausibilitätsengine · 2.1.0.5-Beta */
(function(root,factory){
  const api=factory();
  if(typeof module==='object'&&module.exports)module.exports=api;
  root.SK_VDE_ENGINE=Object.freeze(api);
})(typeof globalThis!=='undefined'?globalThis:this,function(){
  'use strict';

  const VERSION='2.1.0.5-Beta';
  const optional=definition=>({required:false,...definition});
  const FIELD_DEFS={
    bondingMain:optional({label:'Schutzpotenzialausgleich Haupterdungsschiene',shortLabel:'RPA Haupt',section:'Durchgängigkeit',type:'number',unit:'Ω',min:0,max:100,measurement:true}),
    bondingAdditional:optional({label:'Zusätzlicher Schutzpotenzialausgleich',shortLabel:'RPA Zusatz',section:'Durchgängigkeit',type:'number',unit:'Ω',min:0,max:100,measurement:true}),
    continuity:optional({label:'Schutzleiter / Niederohmmessung',shortLabel:'RPE',section:'Durchgängigkeit',type:'number',unit:'Ω',min:0,max:100,measurement:true}),
    networkImpedance:optional({label:'Netzinnenimpedanz Zi',shortLabel:'Zi',section:'Impedanz',type:'number',unit:'Ω',min:0,max:100,measurement:true}),
    insulationValues:optional({label:'Isolationswiderstände',shortLabel:'RISO',section:'Isolation',type:'text',unit:'MΩ',measurement:true,placeholder:'z. B. >300; >300; >300'}),
    loopImpedance:optional({label:'Schleifenimpedanz Zs',shortLabel:'Zs',section:'Automatische Abschaltung',type:'number',unit:'Ω',min:0,max:100,measurement:true}),
    shortCircuitCurrent:optional({label:'Kurzschlussstrom Ik',shortLabel:'Ik',section:'Automatische Abschaltung',type:'number',unit:'A',min:0,max:100000,measurement:true}),
    protectiveResistance:optional({label:'Schutzwiderstand RPE + RA',shortLabel:'RPE + RA',section:'Automatische Abschaltung',type:'number',unit:'Ω',min:0,max:10000,measurement:true}),
    loadCurrent:optional({label:'Verbraucherstrom Ib',shortLabel:'Ib',section:'Stromrelation',type:'number',unit:'A',min:0,max:1600,measurement:true}),
    voltageDrop:optional({label:'Spannungsfall ΔU',shortLabel:'ΔU',section:'Spannungsfall',type:'number',unit:'V',min:0,max:1000,measurement:true}),
    voltageDropPercent:optional({label:'Spannungsfall ε',shortLabel:'ε',section:'Spannungsfall',type:'number',unit:'%',min:0,max:100,measurement:true}),
    rcdTripCurrent:optional({label:'RCD-Auslösestrom IΔ',shortLabel:'IΔ',section:'RCD',type:'number',unit:'mA',min:0,max:2000,measurement:true}),
    rcdTripTime:optional({label:'RCD-Auslösezeit tA',shortLabel:'tA',section:'RCD',type:'number',unit:'ms',min:0,max:5000,measurement:true}),

    shutdownDeviceType:optional({label:'Auslösekennlinie des Überstromschutzes',shortLabel:'Kennlinie',section:'Bezugsdaten',type:'choice',options:[['B','B'],['C','C'],['D','D']]}),
    shutdownNominalCurrent:optional({label:'Nennstrom des Überstromschutzes',shortLabel:'In',section:'Bezugsdaten',type:'number',unit:'A',min:.1,max:1600}),
    phaseVoltage:optional({label:'Außenleiter-Erde-Spannung U0',shortLabel:'U0',section:'Bezugsdaten',type:'number',unit:'V',min:12,max:1000}),
    nominalCurrent:optional({label:'Nennstrom In',shortLabel:'In',section:'Bezugsdaten',type:'number',unit:'A',min:.1,max:1600}),
    nominalVoltage:optional({label:'Nennspannung Un',shortLabel:'Un',section:'Bezugsdaten',type:'number',unit:'V',min:12,max:1500}),
    rcdNominalResidual:optional({label:'RCD-Bemessungsdifferenzstrom IΔn',shortLabel:'IΔn',section:'Bezugsdaten',type:'number',unit:'mA',min:1,max:1000})
  };

  const MEASUREMENT_GROUPS={
    bondingMain:{label:'Schutzpotenzialausgleich Haupterdungsschiene',section:'Durchgängigkeit',measurements:['bondingMain'],references:[],rule:'continuity'},
    bondingAdditional:{label:'Zusätzlicher Schutzpotenzialausgleich',section:'Durchgängigkeit',measurements:['bondingAdditional'],references:[],rule:'continuity'},
    continuity:{label:'Schutzleiter / Niederohmmessung',section:'Durchgängigkeit',measurements:['continuity'],references:[],rule:'continuity'},
    networkImpedance:{label:'Netzinnenimpedanz Zi',section:'Impedanz',measurements:['networkImpedance'],references:[],rule:'range'},
    insulation:{label:'Isolationswiderstand',section:'Isolation',measurements:['insulationValues'],references:[],rule:'insulation'},
    loop:{label:'Schleifenimpedanz Zs',section:'Automatische Abschaltung',measurements:['loopImpedance'],references:['shutdownDeviceType','shutdownNominalCurrent','phaseVoltage'],rule:'loop'},
    shortCircuit:{label:'Kurzschlussstrom Ik',section:'Automatische Abschaltung',measurements:['shortCircuitCurrent'],references:['loopImpedance','phaseVoltage'],rule:'shortCircuit'},
    protectiveResistance:{label:'Schutzwiderstand RPE + RA',section:'Automatische Abschaltung',measurements:['protectiveResistance'],references:[],rule:'range'},
    loadCurrent:{label:'Verbraucherstrom Ib gegen Nennstrom In',section:'Stromrelation',measurements:['loadCurrent'],references:['nominalCurrent'],rule:'loadCurrent'},
    voltageDrop:{label:'Spannungsfall',section:'Spannungsfall',measurements:['voltageDrop','voltageDropPercent'],references:[],rule:'voltageDrop',anyMeasurement:true},
    rcdCurrent:{label:'RCD-Auslösestrom',section:'RCD',measurements:['rcdTripCurrent'],references:['rcdNominalResidual'],rule:'rcdCurrent'},
    rcdTime:{label:'RCD-Auslösezeit',section:'RCD',measurements:['rcdTripTime'],references:[],rule:'rcdTime'}
  };

  const present=value=>value!==null&&value!==undefined&&String(value).trim()!=='';
  const number=value=>{
    if(typeof value==='number')return Number.isFinite(value)?value:null;
    const normalized=String(value??'').trim().replace(/\s/g,'').replace(/(?<=\d)[.](?=\d{3}(?:\D|$))/g,'').replace(',','.').replace(/[^0-9+\-.]/g,'');
    const parsed=Number.parseFloat(normalized);return Number.isFinite(parsed)?parsed:null;
  };
  const valuesList=value=>String(value??'').match(/[<>]?\s*\d+(?:[.,]\d+)?/g)?.map(number).filter(Number.isFinite)||[];
  const normalize=data=>{const out={...data};for(const [key,def] of Object.entries(FIELD_DEFS))if(def.type==='number'&&present(out[key]))out[key]=number(out[key]);return out};
  const curveFactor=value=>({B:5,C:10,D:20})[String(value||'').trim().toUpperCase()]||null;
  const confidenceThreshold=def=>def?.type==='number'||def?.type==='choice'?0.82:0.76;
  const selectedGroups=data=>Array.isArray(data?._measurementScope)?data._measurementScope.filter(key=>MEASUREMENT_GROUPS[key]):[];
  const detectedMeasurementGroups=data=>Object.entries(MEASUREMENT_GROUPS).filter(([,group])=>group.measurements.some(field=>present(data?.[field]))).map(([key])=>key);

  function addCheck(checks,id,section,status,title,detail,fields=[],meta={}){
    checks.push({id,section,status,title,detail,fields,severity:status==='fail'?'error':status==='open'?'warning':'info',...meta});
  }

  function requiredFieldsForGroup(groupKey,data){
    const group=MEASUREMENT_GROUPS[groupKey],required=[];
    if(!group)return required;
    if(group.anyMeasurement){
      if(!group.measurements.some(field=>present(data[field])))required.push('voltageDropPercent');
    }else required.push(...group.measurements);
    required.push(...group.references);
    if(groupKey==='voltageDrop'&&present(data.voltageDrop)&&!present(data.voltageDropPercent))required.push('nominalVoltage');
    if(groupKey==='voltageDrop'&&present(data.voltageDrop)&&present(data.voltageDropPercent))required.push('nominalVoltage');
    return [...new Set(required)];
  }

  function checkData(input,config={}){
    const data=normalize(input),checks=[];
    if(!data._scopeConfirmed){
      addCheck(checks,'SCOPE-CONFIRM','Messumfang','open','Welche Messwerte sind eingetragen?','Bestätigen Sie ausschließlich die Messgrößen, die im hochgeladenen Dokument tatsächlich eingetragen sind. Form, Kreuze, Namen, Datum, Ort und Unterschriften bleiben unberücksichtigt.',[],{groupControl:'measurementScope',technicalOnly:true});
      return checks;
    }
    const scope=selectedGroups(data);
    if(!scope.length){
      addCheck(checks,'SCOPE-EMPTY','Messumfang','open','Mindestens eine Messgröße auswählen','Ohne eine eingetragene Messgröße kann keine rechnerische Plausibilitätsprüfung durchgeführt werden.',[],{groupControl:'measurementScope',technicalOnly:true});
      return checks;
    }

    const required=new Set(scope.flatMap(group=>requiredFieldsForGroup(group,data)));
    for(const key of required){
      const def=FIELD_DEFS[key];
      if(!def)continue;
      if(!present(data[key])){
        const isMeasurement=Boolean(def.measurement);
        addCheck(checks,`REQ-${key}`,def.section,'open',`${def.label} fehlt`,isMeasurement?'Der Messwert wurde nicht sicher erkannt. Bitte lesen Sie ihn am eingeblendeten Originalausschnitt ab und tragen Sie ihn ein.':'Diese Bezugsgröße wird für die rechnerische Bewertung benötigt. Bitte am Original prüfen und ergänzen.',[key],{kind:isMeasurement?'missing-measurement':'missing-reference'});
      }
    }

    const relevantFields=new Set(scope.flatMap(group=>[...MEASUREMENT_GROUPS[group].measurements,...requiredFieldsForGroup(group,data)]));
    for(const key of relevantFields){
      const def=FIELD_DEFS[key];if(!def||!present(data[key]))continue;
      if(def.type==='number'){
        const value=number(data[key]);
        if(value===null||value<def.min||value>def.max)addCheck(checks,`RANGE-${key}`,def.section,'fail',`${def.label} rechnerisch unplausibel`,`Eingetragen: ${data[key]} ${def.unit||''}. Der verarbeitbare Bereich liegt zwischen ${def.min} und ${def.max} ${def.unit||''}.`,[key],{kind:'range'});
      }
      const confidence=Number(data._confidence?.[key]??1),threshold=confidenceThreshold(def);
      if(confidence<threshold&&!checks.some(item=>item.fields.includes(key)&&item.status==='fail'))addCheck(checks,`CONF-${key}`,def.section,'open',`${def.label} unsicher erkannt`,`Erkennungsqualität ${Math.round(confidence*100)} %. Bitte den Wert am Originalausschnitt bestätigen oder korrigieren.`,[key],{kind:def.measurement?'uncertain-measurement':'uncertain-reference'});
    }

    const blocked=field=>checks.some(item=>item.status!=='pass'&&item.fields.includes(field));
    const usable=field=>present(data[field])&&!blocked(field);
    const addRule=(id,group,status,title,detail,fields)=>addCheck(checks,id,MEASUREMENT_GROUPS[group].section,status,title,detail,fields,{calculation:true,group});

    for(const groupKey of scope){
      const group=MEASUREMENT_GROUPS[groupKey];
      if(requiredFieldsForGroup(groupKey,data).some(field=>!usable(field)))continue;
      if(group.rule==='continuity'){
        const field=group.measurements[0],value=number(data[field]),limit=number(config.continuityMaxOhm)??number(config.continuityWarningOhm)??1,ok=value<=limit;
        addRule(`MEAS-${field}`,groupKey,ok?'pass':'fail',ok?`${FIELD_DEFS[field].label} i. O.`:`${FIELD_DEFS[field].label} nicht i. O.`,`${value} Ω ${ok?'≤':'>'} ${limit} Ω hinterlegter Rechen-/Prüfwert.`,[field]);
      }else if(group.rule==='range'){
        const field=group.measurements[0],value=number(data[field]);
        if(Number.isFinite(value))addRule(`MEAS-${field}`,groupKey,'pass',`${FIELD_DEFS[field].label} numerisch plausibel`,`${value} ${FIELD_DEFS[field].unit} ist als nichtnegativer Messwert verarbeitbar; ohne zusätzlichen dokumentierten Grenzwert erfolgt keine weitergehende Normbewertung.`,[field]);
      }else if(group.rule==='insulation'){
        const values=valuesList(data.insulationValues),limit=number(config.insulationMinMOhm)??1;
        if(!values.length)addRule('MEAS-INS-FORMAT',groupKey,'fail','Isolationswerte nicht numerisch auswertbar','Mindestens ein numerischer Wert in MΩ ist erforderlich.',['insulationValues']);
        else{const min=Math.min(...values),ok=min>=limit;addRule('MEAS-INS',groupKey,ok?'pass':'fail',ok?'Isolationswiderstände i. O.':'Isolationswiderstand nicht i. O.',`${values.length} Wert(e), kleinster Wert ${min} MΩ ${ok?'≥':'<'} ${limit} MΩ.`,['insulationValues']);}
      }else if(group.rule==='loop'){
        const zs=number(data.loopImpedance),current=number(data.shutdownNominalCurrent),u0=number(data.phaseVoltage),factor=curveFactor(data.shutdownDeviceType),max=u0/(factor*current),ok=zs<=max;
        addRule('MEAS-ZS',groupKey,ok?'pass':'fail',ok?'Schleifenimpedanz i. O.':'Schleifenimpedanz nicht i. O.',`Zs ${zs} Ω ${ok?'≤':'>'} ${max.toFixed(3)} Ω = U0 ${u0} V / (${factor} × In ${current} A).`,['loopImpedance','shutdownDeviceType','shutdownNominalCurrent','phaseVoltage']);
      }else if(group.rule==='shortCircuit'){
        const ik=number(data.shortCircuitCurrent),zs=number(data.loopImpedance),u0=number(data.phaseVoltage),calculated=u0/zs,tolerance=number(config.shortCircuitTolerancePercent)??30,diff=Math.abs(ik-calculated)/calculated*100,ok=diff<=tolerance;
        addRule('MEAS-IK-CONSISTENCY',groupKey,ok?'pass':'fail',ok?'Kurzschlussstrom rechnerisch plausibel':'Kurzschlussstrom rechnerisch unplausibel',`Ik eingetragen ${ik} A; aus U0/Zs ergeben sich ${calculated.toFixed(1)} A. Abweichung ${diff.toFixed(1)} % ${ok?'≤':'>'} ${tolerance} %.`,['shortCircuitCurrent','loopImpedance','phaseVoltage']);
      }else if(group.rule==='loadCurrent'){
        const ib=number(data.loadCurrent),rated=number(data.nominalCurrent),ok=ib<=rated;
        addRule('CIRCUIT-IB-IN',groupKey,ok?'pass':'fail',ok?'Stromrelation i. O.':'Stromrelation nicht i. O.',`Ib ${ib} A ${ok?'≤':'>'} In ${rated} A.`,['loadCurrent','nominalCurrent']);
      }else if(group.rule==='voltageDrop'){
        const percent=number(data.voltageDropPercent),drop=number(data.voltageDrop),voltage=number(data.nominalVoltage),limit=number(config.voltageDropLimitPercent)??5;
        let evaluated=percent;
        if(!Number.isFinite(evaluated)&&Number.isFinite(drop)&&Number.isFinite(voltage))evaluated=drop/voltage*100;
        if(Number.isFinite(evaluated)){
          const ok=evaluated<=limit;addRule('MEAS-DU',groupKey,ok?'pass':'fail',ok?'Spannungsfall i. O.':'Spannungsfall nicht i. O.',`${evaluated.toFixed(2)} % ${ok?'≤':'>'} ${limit} % hinterlegtes Prüfziel.`,Number.isFinite(percent)?['voltageDropPercent']:['voltageDrop','nominalVoltage']);
          if(Number.isFinite(percent)&&Number.isFinite(drop)&&Number.isFinite(voltage)){
            const calculated=drop/voltage*100,diff=Math.abs(calculated-percent),consistent=diff<=(number(config.voltageDropConsistencyTolerancePercent)??.3);
            addRule('MEAS-DU-CONSISTENCY',groupKey,consistent?'pass':'fail',consistent?'Spannungsfallangaben konsistent':'Spannungsfallangaben widersprüchlich',`Aus ΔU ${drop} V und Un ${voltage} V ergeben sich ${calculated.toFixed(2)} %, eingetragen sind ${percent} %.`,['voltageDrop','nominalVoltage','voltageDropPercent']);
          }
        }
      }else if(group.rule==='rcdCurrent'){
        const trip=number(data.rcdTripCurrent),rated=number(data.rcdNominalResidual),ok=trip<=rated;
        addRule('RCD-I',groupKey,ok?'pass':'fail',ok?'RCD-Auslösestrom i. O.':'RCD-Auslösestrom nicht i. O.',`IΔ ${trip} mA ${ok?'≤':'>'} IΔn ${rated} mA.`,['rcdTripCurrent','rcdNominalResidual']);
      }else if(group.rule==='rcdTime'){
        const time=number(data.rcdTripTime),limit=number(config.rcdTripTimeLimitMs)??300,ok=time<=limit;
        addRule('RCD-T',groupKey,ok?'pass':'fail',ok?'RCD-Auslösezeit i. O.':'RCD-Auslösezeit nicht i. O.',`tA ${time} ms ${ok?'≤':'>'} ${limit} ms hinterlegter Standard-Prüfwert.`,['rcdTripTime']);
      }
    }
    return checks;
  }

  function issueFromCheck(check,data){
    const field=check.fields?.[0]||'',definition=FIELD_DEFS[field]||{label:'Messumfang',section:check.section,type:'text'};
    return{id:check.id,title:check.title,message:check.detail,section:check.section,field,fields:check.fields||[],definition,detected:data[field],status:check.status,groupControl:check.groupControl||null,kind:check.kind||null,technicalOnly:Boolean(check.technicalOnly),calculation:Boolean(check.calculation)};
  }
  function buildIssues(data,config){const seen=new Set();return checkData(data,config).filter(item=>item.status==='open'||item.status==='fail').map(item=>issueFromCheck(item,data)).filter(item=>!seen.has(item.id)&&seen.add(item.id))}
  function finalState(data,config={},confirmedDefects=[]){
    const checks=checkData(data,config),open=checks.filter(item=>item.status==='open'),failed=checks.filter(item=>item.status==='fail');
    return{complete:Boolean(data._scopeConfirmed)&&open.length===0,plausible:Boolean(data._scopeConfirmed)&&open.length===0&&failed.length===0&&confirmedDefects.length===0,open,failed,confirmedDefects:[...confirmedDefects],checks};
  }

  function parseText(text,baseConfidence=.88){
    const raw=String(text||''),compact=raw.replace(/\s+/g,' '),data={_confidence:{},_confidenceReason:{}};
    const set=(key,value,confidence=baseConfidence,reason='Dokumenttext')=>{if(present(value)&&FIELD_DEFS[key]&&confidence>=Number(data._confidence[key]||0)){data[key]=typeof value==='number'?value:String(value).trim();data._confidence[key]=confidence;data._confidenceReason[key]=reason}};
    const match=(key,re,confidence=baseConfidence)=>{const found=compact.match(re);if(found)set(key,number(found[1]),confidence)};
    match('bondingMain',/(?:Haupterdungsschiene|RPA\s*Haupt)\D{0,35}(\d+(?:[.,]\d+)?)\s*(?:Ω|Ohm)/i);
    match('bondingAdditional',/(?:zus[aä]tzlicher\s+Schutzpotenzialausgleich|RPA\s*Zusatz)\D{0,35}(\d+(?:[.,]\d+)?)\s*(?:Ω|Ohm)/i);
    match('continuity',/(?:Niederohm\w*|Schutzleiter\w*|RPE\b)\D{0,35}(\d+(?:[.,]\d+)?)\s*(?:Ω|Ohm)/i);
    match('networkImpedance',/(?:Netzinnenimpedanz|\bZi\b)\D{0,30}(\d+(?:[.,]\d+)?)\s*(?:Ω|Ohm)/i);
    match('loopImpedance',/(?:Schleifenimpedanz|\bZs\b)\D{0,30}(\d+(?:[.,]\d+)?)\s*(?:Ω|Ohm)/i);
    match('shortCircuitCurrent',/(?:Kurzschlussstrom|\bIk\b)\D{0,30}(\d+(?:[.,]\d+)?)\s*A/i);
    match('protectiveResistance',/(?:RPE\s*\+\s*RA|Schutzwiderstand)\D{0,30}(\d+(?:[.,]\d+)?)\s*(?:Ω|Ohm)/i);
    match('loadCurrent',/(?:Verbraucherstrom|\bIb\b)\D{0,24}(\d+(?:[.,]\d+)?)\s*A/i);
    match('nominalCurrent',/(?:Nennstrom|\bIn\b)\D{0,24}(\d+(?:[.,]\d+)?)\s*A/i);
    match('nominalVoltage',/(?:Nennspannung|\bUn\b)\D{0,24}(\d+(?:[.,]\d+)?)\s*V/i);
    match('phaseVoltage',/(?:Außenleiter.Erde.Spannung|\bU0\b)\D{0,24}(\d+(?:[.,]\d+)?)\s*V/i);
    match('voltageDropPercent',/(?:Spannungsfall|\bepsilon\b|\bε\b)\D{0,35}(\d+(?:[.,]\d+)?)\s*%/i);
    match('voltageDrop',/(?:Spannungsfall|\bΔU\b|\bdU\b)\D{0,35}(\d+(?:[.,]\d+)?)\s*V/i);
    match('rcdNominalResidual',/(?:I\s*[ΔA]?\s*n|Bemessungsdifferenzstrom)\D{0,24}(\d+(?:[.,]\d+)?)\s*mA/i);
    match('rcdTripCurrent',/(?:Ausl[öo]sestrom|I\s*[ΔA](?!\s*n))\D{0,24}(\d+(?:[.,]\d+)?)\s*mA/i);
    match('rcdTripTime',/(?:Ausl[öo]sezeit|\btA\b)\D{0,24}(\d+(?:[.,]\d+)?)\s*ms/i);
    const breaker=compact.match(/(?:Kennlinie|LS|Überstromschutz)?\s*\b([BCD])\s*(\d{1,3}(?:[.,]\d+)?)\s*A?\b/i);
    if(breaker){set('shutdownDeviceType',breaker[1].toUpperCase(),baseConfidence);set('shutdownNominalCurrent',number(breaker[2]),baseConfidence)}
    const isolationSegment=compact.match(/(?:Isolationswiderst[aä]nd\w*|Isolation|RISO)\D{0,24}((?:[<>]?\s*\d+(?:[.,]\d+)?(?:\s*(?:MΩ|MOhm|MΩ)?)[;\s,/|]*){1,8})/i);
    if(isolationSegment){const values=isolationSegment[1].match(/[<>]?\s*\d+(?:[.,]\d+)?/g);if(values?.length)set('insulationValues',values.join('; '),baseConfidence)}
    return data;
  }

  return{VERSION,FIELD_DEFS,MEASUREMENT_GROUPS,present,number,valuesList,normalize,curveFactor,confidenceThreshold,selectedGroups,detectedMeasurementGroups,requiredFieldsForGroup,checkData,buildIssues,finalState,parseText};
});
