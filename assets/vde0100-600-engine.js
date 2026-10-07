/* SK PLT Tools · VDE 0100-600 Plausibilitäts-Engine · 2.1.0.4-Beta */
(function(root,factory){
  const api=factory();
  if(typeof module==='object'&&module.exports)module.exports=api;
  root.SK_VDE_ENGINE=Object.freeze(api);
})(typeof globalThis!=='undefined'?globalThis:this,function(){
  'use strict';

  const VERSION='2.1.0.4-Beta';
  const statusOptions=[['io','i.O.'],['nio','n.i.O.'],['nrel','nicht relevant']];
  const optional=(definition={})=>({required:false,allowSkip:true,...definition});
  const conditionalStatus=definition=>({required:true,allowSemanticNotRelevant:true,safetyCritical:true,...definition,options:statusOptions});

  const FIELD_DEFS={
    protocolType:{label:'Formularidentität',section:'Dokument',type:'choice',required:true,safetyCritical:false,options:[['supported','VDEProtokoll · Lfd. Nr. 12782'],['other','Abweichendes oder nicht sicher erkanntes Formular']]},
    orderNumber:optional({label:'Auftrags-Nr.',section:'Stammdaten',type:'text'}),
    testReason:{label:'Prüfgrund',section:'Stammdaten',type:'choice',required:true,safetyCritical:true,options:[['Erstprüfung','Erstprüfung'],['Wiederholungsprüfung','Wiederholungsprüfung'],['Änderung','Prüfung nach Instandsetzung'],['Ex-Bereich','Prüfung im Ex-Bereich'],['other','Sonstiger Prüfgrund']]},
    work:optional({label:'Werk',section:'Stammdaten',type:'text'}),building:optional({label:'Gebäude',section:'Stammdaten',type:'text'}),plantComplex:optional({label:'Anlagenkomplex',section:'Stammdaten',type:'text'}),plant:optional({label:'Anlage',section:'Stammdaten',type:'text'}),partialPlant:optional({label:'Teilanlage',section:'Stammdaten',type:'text'}),pltPosition:optional({label:'PLT-Stelle',section:'Stammdaten',type:'text'}),
    pltRoom:optional({label:'PLT-Raum',section:'Stammdaten',type:'text'}),distribution:optional({label:'Verteilung',section:'Stammdaten',type:'text'}),feeder:optional({label:'Abgang',section:'Stammdaten',type:'text'}),subDistribution:optional({label:'Unterverteilung',section:'Stammdaten',type:'text'}),outgoing:optional({label:'Abgang (UV)',section:'Stammdaten',type:'text'}),consumer:optional({label:'Verbraucher',section:'Stammdaten',type:'text'}),
    networkSystem:{label:'Netzsystem',section:'Stammdaten',type:'choice',required:true,safetyCritical:true,options:[['TN','TN'],['IT','IT']]},
    installationCategory:{label:'Anlagenart',section:'Stammdaten',type:'text',required:true,safetyCritical:true},
    device1Name:{label:'Messgerät 1 – Fabrikat',section:'Messgerät',type:'text',required:true,safetyCritical:true},device1Number:{label:'Messgerät 1 – Typ / Nr.',section:'Messgerät',type:'text',required:true,safetyCritical:true},device1Calibration:{label:'Messgerät 1 – Kalibrierdatum',section:'Messgerät',type:'date',required:true,safetyCritical:true},
    device2Name:optional({label:'Messgerät 2 – Fabrikat',section:'Messgerät',type:'text'}),device2Number:optional({label:'Messgerät 2 – Typ / Nr.',section:'Messgerät',type:'text'}),device2Calibration:optional({label:'Messgerät 2 – Kalibrierdatum',section:'Messgerät',type:'date'}),
    device3Name:optional({label:'Messgerät 3 – Fabrikat',section:'Messgerät',type:'text'}),device3Number:optional({label:'Messgerät 3 – Typ / Nr.',section:'Messgerät',type:'text'}),device3Calibration:optional({label:'Messgerät 3 – Kalibrierdatum',section:'Messgerät',type:'date'}),
    cableType:{label:'Kabel-/Leitungstyp',section:'2. Angaben zum Objekt',type:'text',required:true,safetyCritical:true},conductors:{label:'Aderzahl',section:'2. Angaben zum Objekt',type:'number',required:true,safetyCritical:true,min:1,max:20},crossSection:{label:'Querschnitt',section:'2. Angaben zum Objekt',type:'number',unit:'mm²',required:true,safetyCritical:true,min:.25,max:630},length:{label:'Länge',section:'2. Angaben zum Objekt',type:'number',unit:'m',required:true,safetyCritical:true,min:0,max:5000},protectiveDevice:{label:'Überstromschutz – Typ',section:'2. Angaben zum Objekt',type:'text',required:true,safetyCritical:true},nominalCurrent:{label:'Überstromschutz – In',section:'2. Angaben zum Objekt',type:'number',unit:'A',required:true,safetyCritical:true,min:.1,max:1600},nominalVoltage:{label:'Verbraucher – Un',section:'2. Angaben zum Objekt',type:'number',unit:'V',required:true,safetyCritical:true,min:12,max:1500},
    loadCurrent:optional({label:'Verbraucher – Ib',section:'2. Angaben zum Objekt',type:'number',unit:'A',safetyCritical:true,min:0,max:1600}),voltageDrop:optional({label:'Spannungsfall ΔU',section:'2. Angaben zum Objekt',type:'number',unit:'V',safetyCritical:true,min:0,max:1000}),voltageDropPercent:optional({label:'Spannungsfall ε',section:'2. Angaben zum Objekt',type:'number',unit:'%',safetyCritical:true,min:0,max:100}),
    bondingMain:optional({label:'4.1 Schutzpotenzialausgleich Haupterdungsschiene',section:'4. Durchgängigkeit',type:'number',unit:'Ω',safetyCritical:true,min:0,max:100}),bondingMainStatus:conditionalStatus({label:'4.1 Bewertung',section:'4. Durchgängigkeit',type:'choice'}),
    bondingAdditional:optional({label:'4.2 Zusätzlicher Schutzpotenzialausgleich',section:'4. Durchgängigkeit',type:'number',unit:'Ω',safetyCritical:true,min:0,max:100}),bondingAdditionalStatus:conditionalStatus({label:'4.2 Bewertung',section:'4. Durchgängigkeit',type:'choice'}),
    continuity:optional({label:'4.3 Schutzleiter / Niederohmmessung',section:'4. Durchgängigkeit',type:'number',unit:'Ω',safetyCritical:true,min:0,max:100}),continuityStatus:conditionalStatus({label:'4.3 Bewertung',section:'4. Durchgängigkeit',type:'choice'}),
    networkImpedance:optional({label:'4.4 Netzinnenimpedanz Zi',section:'4. Durchgängigkeit',type:'number',unit:'Ω',safetyCritical:true,min:0,max:100}),networkImpedanceStatus:conditionalStatus({label:'4.4 Bewertung',section:'4. Durchgängigkeit',type:'choice'}),
    insulationValues:{label:'5. Isolationswiderstände',section:'5. Isolation',type:'text',unit:'MΩ',required:true,safetyCritical:true},
    shutdownDeviceType:optional({label:'6.1 Überstromschutz – Typ',section:'6. Automatische Abschaltung',type:'text',safetyCritical:true}),shutdownNominalCurrent:optional({label:'6.1 Überstromschutz – In',section:'6. Automatische Abschaltung',type:'number',unit:'A',safetyCritical:true,min:.1,max:1600}),loopImpedance:optional({label:'6.1 Schleifenimpedanz Zs',section:'6. Automatische Abschaltung',type:'number',unit:'Ω',safetyCritical:true,min:0,max:100}),shortCircuitCurrent:optional({label:'6.1 Kurzschlussstrom Ik',section:'6. Automatische Abschaltung',type:'number',unit:'A',safetyCritical:true,min:0,max:100000}),protectiveResistance:optional({label:'6.1 RPE + RA',section:'6. Automatische Abschaltung',type:'number',unit:'Ω',safetyCritical:true,min:0,max:10000}),
    rcdType:optional({label:'6.2 RCD – Typ',section:'6. Automatische Abschaltung',type:'choice',safetyCritical:true,options:[['A','Typ A'],['AC','Typ AC'],['F','Typ F'],['B','Typ B'],['none','Keine RCD vorhanden']]}),rcdRatedCurrent:optional({label:'6.2 RCD – In',section:'6. Automatische Abschaltung',type:'number',unit:'A',safetyCritical:true,min:1,max:1000}),rcdNominalResidual:optional({label:'6.2 RCD – IΔn',section:'6. Automatische Abschaltung',type:'number',unit:'mA',safetyCritical:true,min:1,max:1000}),rcdTripCurrent:optional({label:'6.2 RCD – Auslösestrom IΔ',section:'6. Automatische Abschaltung',type:'number',unit:'mA',safetyCritical:true,min:0,max:2000}),rcdTripTime:optional({label:'6.2 RCD – Auslösezeit tA',section:'6. Automatische Abschaltung',type:'number',unit:'ms',safetyCritical:true,min:0,max:5000}),touchVoltageState:optional({label:'6.2 UB < UL',section:'6. Automatische Abschaltung',type:'choice',safetyCritical:true,allowSemanticNotRelevant:true,options:statusOptions}),
    testerPoints:{label:'Prüfergebnis – Prüfpunkte 2 bis 6',section:'Abschluss',type:'text',required:true,safetyCritical:true},testerName:{label:'Prüfer – Name',section:'Abschluss',type:'text',required:true,safetyCritical:true},testerCompany:optional({label:'Prüfer – Firma',section:'Abschluss',type:'text'}),testDate:{label:'Prüfer – Datum',section:'Abschluss',type:'date',required:true,safetyCritical:true},signatureState:{label:'Prüfer – Unterschrift',section:'Abschluss',type:'choice',required:true,safetyCritical:true,options:[['present','Vorhanden'],['missing','Fehlt']]},
    commissioningPoints:optional({label:'Inbetriebnehmer – Prüfpunkte 6 und 7',section:'Abschluss',type:'text'}),commissioningName:optional({label:'Inbetriebnehmer – Name',section:'Abschluss',type:'text'}),commissioningCompany:optional({label:'Inbetriebnehmer – Firma',section:'Abschluss',type:'text'}),commissioningDate:optional({label:'Inbetriebnehmer – Datum',section:'Abschluss',type:'date'}),commissioningSignature:optional({label:'Inbetriebnehmer – Unterschrift',section:'Abschluss',type:'choice',options:[['present','Vorhanden'],['missing','Fehlt']]}),remarks:optional({label:'Bemerkung',section:'Abschluss',type:'text'})
  };

  const inspectionLabels=['Auswahl der Betriebsmittel gemäß Umgebungsbedingungen','Montage gemäß Herstellerangaben','Anschluss und Zugänglichkeit','Kennzeichnung und Dokumentation','Betriebsmittel ohne erkennbare Schäden','Schutz gegen direktes Berühren','Leitungsauswahl / Strombelastbarkeit','Zuordnung Schutzeinrichtung / Querschnitt','Einstellung Überstromschutz','Anordnung von Trenn- und Schaltgeräten','Einpolige Schaltgeräte im Außenleiter','Leitungsverlegung und Befestigung','Schottung von Leitungsdurchführungen','Schaltungsunterlagen und Hinweisschilder','Kennzeichnung Stromkreise / Abgänge','Richtige Verwendung von Schutzleitern','Kennzeichnung Schutz- und PEN-Leiter','Anschlussstellen Schutz- und PEN-Leiter','Schutzpotenzialausgleich','Zusätzlicher Schutzpotenzialausgleich'];
  inspectionLabels.forEach((label,index)=>FIELD_DEFS[`inspection${31+index}`]=conditionalStatus({label:`3.${index+1} ${label}`,section:'3. Allgemeine Besichtigung',type:'choice'}));
  const testLabels=['Funktion Isolationsüberwachung im IT-System','Prüfung RCD','Spannungspolarität','Drehrichtung bei Motoren','Rechtsdrehfeld bei Steckdosen','Funktionsprüfung der Gerätekombination'];
  testLabels.forEach((label,index)=>FIELD_DEFS[`test${71+index}`]=conditionalStatus({label:`7.${index+1} ${label}`,section:'7. Erproben',type:'choice'}));

  const NUMBER_FIELDS=new Set(Object.entries(FIELD_DEFS).filter(([,def])=>def.type==='number').map(([key])=>key));
  const present=value=>value!==null&&value!==undefined&&String(value).trim()!=='';
  const number=value=>{if(typeof value==='number')return Number.isFinite(value)?value:null;const normalized=String(value??'').trim().replace(/\s/g,'').replace(/(?<=\d)[.](?=\d{3}(?:\D|$))/g,'').replace(',','.').replace(/[^0-9+\-.]/g,'');const parsed=Number.parseFloat(normalized);return Number.isFinite(parsed)?parsed:null};
  const valuesList=value=>String(value??'').match(/[<>]?\s*\d+(?:[.,]\d+)?/g)?.map(number).filter(Number.isFinite)||[];
  function normalize(data){const out={...data};NUMBER_FIELDS.forEach(key=>{if(present(out[key]))out[key]=number(out[key])});return out}
  function curveFactor(device){const value=String(device||'').toUpperCase();if(/(^|\W)D\s*\d/.test(value))return 20;if(/(^|\W)C\s*\d/.test(value))return 10;if(/(^|\W)B\s*\d/.test(value))return 5;return null}
  function validDate(value){if(!/^\d{4}-\d{2}-\d{2}$/.test(String(value||'')))return false;const date=new Date(`${value}T00:00:00Z`);return !Number.isNaN(date.getTime())}
  function confidenceThreshold(def){if(def?.type==='choice'||def?.type==='number'||def?.type==='date')return .80;return .74}
  function canIgnoreMissing(key,data){const def=FIELD_DEFS[key];return Boolean(def?.allowSkip&&!def.required&&(data._notRelevant||[]).includes(key))}

  function checkData(input,config={}){
    const data=normalize(input),checks=[],visual=data._visualPresence||{},choiceMarks=data._choiceMarks||{};
    const add=(id,section,status,title,detail,fields=[],severity='error',limit=null,meta={})=>checks.push({id,section,status,title,detail,fields,severity,limit,...meta});
    const score=Number(data._layoutScore||0),formDecision=data._formIdentityDecision||'';
    if(data._formStatus&&data._formStatus!=='accepted'&&!formDecision){
      add('FORM-IDENTITY','Dokument','open','Formularidentität technisch unsicher',`Die Strukturpassung beträgt ${Math.round(score*100)} %. Dieser Wert ist nur ein technischer Hinweis und keine n.i.O.-Bewertung. Die fachliche Prüfung kann fortgesetzt werden, sofern Prüfbereiche, Kreuze und Messwerte zugeordnet oder manuell bestätigt werden.`,['protocolType'],'warning',null,{groupControl:'formIdentity',safetyCritical:false,technicalOnly:true});
    }

    Object.entries(FIELD_DEFS).forEach(([key,def])=>{
      const mark=choiceMarks[key],confidentCount=Number(mark?.confidentCount||0),allowed=new Set((def.options||[]).map(option=>option[0]));
      const choiceConflict=def.type==='choice'&&confidentCount>1;
      if(choiceConflict)add(`CHOICE-MULTIPLE-${key}`,def.section,'open',`${def.label}: mehrere Kreuze erkannt`,'Für diesen Prüfpunkt ist genau ein zulässiges Kreuz erforderlich. Bitte die eindeutige Bewertung am Original auswählen.',[key],'warning',null,{safetyCritical:Boolean(def.safetyCritical),missingRequired:Boolean(def.required),kind:'multiple-choice'});
      if(present(data[key])&&def.type==='choice'&&!allowed.has(data[key]))add(`CHOICE-INVALID-${key}`,def.section,'open',`${def.label}: Kreuz nicht eindeutig zuordenbar`,'Der erkannte Wert entspricht keiner zulässigen Auswahl. Bitte genau eine zulässige Bewertung bestätigen.',[key],'warning',null,{safetyCritical:Boolean(def.safetyCritical),missingRequired:Boolean(def.required),kind:'uncertain-choice'});
      if(def.required&&!present(data[key])&&!choiceConflict){
        const choice=def.type==='choice'&&key!=='protocolType';
        add(`REQ-${key}`,def.section,'open',choice?`${def.label}: kein eindeutiges Kreuz erkannt`:visual[key]?`${def.label}: Eintrag bestätigen`:`${def.label} ist offen`,choice?'Zu diesem erforderlichen Prüfpunkt muss genau ein zulässiges Kreuz bestätigt werden.':visual[key]?'Im zugeordneten Formularfeld wurde ein Eintrag erkannt, aber nicht sicher gelesen. Bitte den Wert am eingeblendeten Originalausschnitt bestätigen oder korrigieren.':'Im verbindlichen Formularfeld wurde kein sicherer Wert erkannt. Bitte Original prüfen und den Pflichtwert ergänzen.',[key],'warning',null,{safetyCritical:Boolean(def.safetyCritical),missingRequired:true,kind:choice?'missing-choice':'missing-value'});
      }
      if(present(data[key])&&def.type==='number'){
        const value=number(data[key]);if(value===null||value<def.min||value>def.max)add(`RANGE-${key}`,def.section,'fail',`${def.label} liegt außerhalb des Erfassungsbereichs`,`Erkannt: ${data[key]} ${def.unit||''}. Zulässiger Bereich: ${def.min} bis ${def.max} ${def.unit||''}.`,[key],'error',null,{safetyCritical:true});
      }
      if(present(data[key])&&def.type==='date'&&!validDate(data[key]))add(`DATE-${key}`,def.section,'open',`${def.label} ist nicht eindeutig`,'Datum bitte im Format TT.MM.JJJJ beziehungsweise über die Datumsauswahl bestätigen.',[key],'warning',null,{safetyCritical:Boolean(def.safetyCritical)});
    });

    if(formDecision==='manual'){
      const reviewed=new Set(data._manualReviewed||[]),manualFields=Array.isArray(data._manualReviewFields)?data._manualReviewFields:Object.keys(FIELD_DEFS).filter(key=>present(data[key]));
      manualFields.forEach(key=>{const def=FIELD_DEFS[key];if(def&&key!=='protocolType'&&present(data[key])&&!reviewed.has(key)&&!checks.some(item=>item.fields.includes(key)&&item.status!=='pass'))add(`REVIEW-${key}`,def.section,'open',`${def.label}: Zuordnung manuell prüfen`,'Die Formularidentität ist technisch unsicher. Bitte den zugeordneten Wert am Original bestätigen oder korrigieren.',[key],'warning',null,{safetyCritical:Boolean(def.safetyCritical),manualReview:true})});
    }

    const locationKeys=['work','building','plantComplex','plant','partialPlant','pltPosition','pltRoom','distribution','feeder','subDistribution','outgoing','consumer'];
    const locationCount=locationKeys.filter(key=>present(data[key])).length;
    if(locationCount<2)add('MASTER-IDENT','Stammdaten','open','Technischer Platz nicht ausreichend bezeichnet','Mindestens zwei Ortsfelder müssen gemeinsam bestätigt werden. Der Dialog bietet alle zugehörigen Felder an und schließt erst nach zwei Angaben. ',locationKeys,'warning',null,{groupControl:'location',safetyCritical:true});

    const statusKeys=[...inspectionLabels.map((_,i)=>`inspection${31+i}`),'bondingMainStatus','bondingAdditionalStatus','continuityStatus','networkImpedanceStatus',...testLabels.map((_,i)=>`test${71+i}`),'touchVoltageState'];
    statusKeys.forEach(key=>{if(data[key]==='nio')add(`STATUS-${key}`,FIELD_DEFS[key].section,'fail',`${FIELD_DEFS[key].label} ist n.i.O.`,'Die bestätigte negative Einzelbewertung führt zum roten Gesamtergebnis.',[key],'error',null,{safetyCritical:true})});

    for(const [valueKey,statusKey] of [['bondingMain','bondingMainStatus'],['bondingAdditional','bondingAdditionalStatus'],['continuity','continuityStatus'],['networkImpedance','networkImpedanceStatus']]){
      if(data[statusKey]==='io'&&!present(data[valueKey]))add(`MEAS-${valueKey}-VALUE`,FIELD_DEFS[valueKey].section,'open',`${FIELD_DEFS[valueKey].label}: Messwert fehlt`,'Die Bewertung i.O. ist markiert; der zugehörige Messwert muss bestätigt werden.',[valueKey,statusKey],'warning',null,{safetyCritical:true});
      if(Number.isFinite(number(data[valueKey]))){const v=number(data[valueKey]),warn=number(config.continuityWarningOhm)??1;add(`MEAS-${valueKey}`,FIELD_DEFS[valueKey].section,v<=warn?'pass':'open',v<=warn?`${FIELD_DEFS[valueKey].label} unauffällig`:`${FIELD_DEFS[valueKey].label} auffällig hoch`,v<=warn?`${v} Ω liegt unter dem internen Hinweiswert ${warn} Ω.`:`${v} Ω liegt über dem internen Hinweiswert ${warn} Ω. Dieser Hinweiswert ist kein allgemeiner Normgrenzwert; Leiterlänge und Querschnitt fachlich prüfen.`,[valueKey],v<=warn?'info':'warning',{max:warn,unit:'Ω'},{safetyCritical:true})}
    }

    const insulation=valuesList(data.insulationValues);
    if(present(data.insulationValues)){
      const threshold=number(config.insulationMinMOhm)??1;
      if(!insulation.length)add('MEAS-INS-FORMAT','5. Isolation','open','Isolationswerte nicht sicher lesbar','Mindestens ein numerischer Isolationswert in MΩ ist erforderlich.',['insulationValues'],'warning',null,{safetyCritical:true});
      else if(insulation.some(value=>value<threshold))add('MEAS-INS','5. Isolation','fail','Isolationswiderstand unterschreitet den Prüfwert',`Mindestens ein Wert liegt unter ${threshold} MΩ.`,['insulationValues'],'error',null,{safetyCritical:true});
      else add('MEAS-INS','5. Isolation','pass','Isolationswiderstände plausibel',`${insulation.length} Wert(e), kleinster Wert ${Math.min(...insulation)} MΩ; hinterlegter Prüfwert ≥ ${threshold} MΩ.`,['insulationValues'],'info',{min:threshold,unit:'MΩ'});
    }

    const loopPath=[data.shutdownDeviceType,data.shutdownNominalCurrent,data.loopImpedance].some(present),rcdPath=(data.rcdType&&data.rcdType!=='none')||[data.rcdNominalResidual,data.rcdTripCurrent,data.rcdTripTime].some(value=>Number.isFinite(number(value)));
    if(!loopPath&&!rcdPath)add('MEAS-AUTO-PATH','6. Automatische Abschaltung','open','Messweg für automatische Abschaltung ist offen','Mindestens Abschnitt 6.1 oder 6.2 aus dem Original bestätigen. Dieser sicherheitsrelevante Nachweis kann nicht übersprungen werden.',['shutdownDeviceType','rcdType'],'warning',null,{safetyCritical:true});
    if(loopPath){
      for(const key of ['shutdownDeviceType','shutdownNominalCurrent','loopImpedance'])if(!present(data[key]))add(`REQ-${key}-LOOP`,FIELD_DEFS[key].section,'open',`${FIELD_DEFS[key].label} ist offen`,'Für die rechnerische Schleifenimpedanzprüfung wird dieser Wert benötigt.',[key],'warning',null,{safetyCritical:true});
      const zs=number(data.loopImpedance),current=number(data.shutdownNominalCurrent),device=data.shutdownDeviceType||data.protectiveDevice,factor=curveFactor(device);
      if(Number.isFinite(zs)&&Number.isFinite(current)){if(!factor)add('MEAS-ZS-CURVE','6. Automatische Abschaltung','open','Auslösekennlinie für Zs fehlt','B-, C- oder D-Kennlinie ergänzen, damit der rechnerische Zs-Vergleich möglich ist.',['shutdownDeviceType'],'warning',null,{safetyCritical:true});else{const u0=number(config.phaseVoltage)??230,max=u0/(factor*current),ok=zs<=max;add('MEAS-ZS','6. Automatische Abschaltung',ok?'pass':'fail',ok?'Schleifenimpedanz rechnerisch plausibel':'Schleifenimpedanz überschreitet den Rechenwert',`Zs ${zs} Ω; Rechenwert ${max.toFixed(3)} Ω aus U0 ${u0} V / (${factor} × ${current} A).`,['loopImpedance','shutdownDeviceType','shutdownNominalCurrent'],ok?'info':'error',{max,unit:'Ω'},{safetyCritical:true})}}
    }

    const ib=number(data.loadCurrent),inValue=number(data.nominalCurrent);if(Number.isFinite(ib)&&Number.isFinite(inValue)){const ok=ib<=inValue;add('CIRCUIT-IB-IN','2. Angaben zum Objekt',ok?'pass':'fail',ok?'Verbraucherstrom und Nennstrom plausibel':'Verbraucherstrom größer als Nennstrom',`Ib ${ib} A; In ${inValue} A.`,['loadCurrent','nominalCurrent'],ok?'info':'error',null,{safetyCritical:true})}
    const du=number(data.voltageDrop),un=number(data.nominalVoltage),duPercent=number(data.voltageDropPercent);if(Number.isFinite(duPercent)){const limit=number(config.voltageDropLimitPercent)??5,ok=duPercent<=limit;add('MEAS-DU','2. Angaben zum Objekt',ok?'pass':'fail',ok?'Spannungsfall innerhalb des Prüfziels':'Spannungsfall überschreitet das Prüfziel',`Erkannt: ${duPercent} %; hinterlegtes Prüfziel ≤ ${limit} %.`,['voltageDropPercent'],ok?'info':'error',{max:limit,unit:'%'},{safetyCritical:true})}
    if(Number.isFinite(du)&&Number.isFinite(un)&&Number.isFinite(duPercent)){const calculated=du/un*100,diff=Math.abs(calculated-duPercent);add('MEAS-DU-CONSISTENCY','2. Angaben zum Objekt',diff<=.3?'pass':'open',diff<=.3?'Spannungsfallangaben rechnerisch konsistent':'Spannungsfallangaben widersprüchlich',`Aus ΔU ${du} V und Un ${un} V ergeben sich ${calculated.toFixed(2)} %, eingetragen sind ${duPercent} %.`,['voltageDropPercent','voltageDrop','nominalVoltage'],diff<=.3?'info':'warning',null,{safetyCritical:true})}

    if(rcdPath){
      for(const key of ['rcdType','rcdNominalResidual','rcdTripCurrent','rcdTripTime'])if(!present(data[key]))add(`REQ-${key}-RCD`,FIELD_DEFS[key].section,'open',`${FIELD_DEFS[key].label} ist offen`,'Für die RCD-Plausibilitätsprüfung wird dieser Wert benötigt.',[key],'warning',null,{safetyCritical:true});
      const idn=number(data.rcdNominalResidual),trip=number(data.rcdTripCurrent),time=number(data.rcdTripTime);if(Number.isFinite(idn)&&Number.isFinite(trip)){const ok=trip<=idn;add('RCD-I','6. Automatische Abschaltung',ok?'pass':'fail',ok?'RCD-Auslösestrom plausibel':'RCD-Auslösestrom zu hoch',`IΔ ${trip} mA; IΔn ${idn} mA.`,['rcdTripCurrent','rcdNominalResidual'],ok?'info':'error',null,{safetyCritical:true})}
      if(Number.isFinite(time)){const limit=number(config.rcdTripTimeLimitMs)??300,ok=time<=limit;add('RCD-T','6. Automatische Abschaltung',ok?'pass':'fail',ok?'RCD-Auslösezeit plausibel':'RCD-Auslösezeit zu lang',`tA ${time} ms; hinterlegter Standard-Prüfwert ≤ ${limit} ms. Abweichende RCD-Typen und Prüfbedingungen fachlich berücksichtigen.`,['rcdTripTime'],ok?'info':'error',{max:limit,unit:'ms'},{safetyCritical:true})}
    }

    if(data.signatureState==='missing')add('SIGN-MISSING','Abschluss','fail','Prüferunterschrift fehlt','Die Prüferbestätigung ist nicht vorhanden und kann nicht als nicht relevant übersprungen werden.',['signatureState'],'error',null,{safetyCritical:true});

    const confidence=data._confidence||{};
    Object.entries(confidence).forEach(([key,value])=>{
      if(key==='protocolType')return;
      const def=FIELD_DEFS[key],threshold=confidenceThreshold(def);
       if(def&&present(data[key])&&Number(value)<threshold&&!canIgnoreMissing(key,data)&&!checks.some(item=>item.fields.includes(key)&&item.status!=='pass'))add(`CONF-${key}`,def.section,'open',`${def.label} unsicher erkannt`,`Erkennungsqualität ${Math.round(Number(value)*100)} %; erforderlich sind ${Math.round(threshold*100)} %. Bitte Wert am Original bestätigen oder korrigieren.`,[key],'warning',null,{safetyCritical:Boolean(def.safetyCritical),missingRequired:Boolean(def.required),kind:def.type==='choice'?'uncertain-choice':'uncertain-value'});
    });
    return checks;
  }

  function issueFromCheck(check,data){
    const field=check.fields[0],def=FIELD_DEFS[field]||{label:field,type:'text',section:check.section};
    const semantic=check.status==='open'&&check.fields.length===1&&Boolean(def.allowSemanticNotRelevant);
    const skippable=check.status==='open'&&check.fields.length===1&&Boolean(def.allowSkip)&&!def.required&&!check.safetyCritical;
    return{id:check.id,title:check.title,message:check.detail,section:check.section,severity:check.severity,field,fields:check.fields,definition:def,detected:data[field],status:check.status,resolution:null,groupControl:check.groupControl||null,safetyCritical:Boolean(check.safetyCritical||def.safetyCritical),technicalOnly:Boolean(check.technicalOnly),missingRequired:Boolean(check.missingRequired),kind:check.kind||null,manualReview:Boolean(check.manualReview),allowNotRelevant:semantic||skippable,notRelevantMode:semantic?'value':skippable?'skip':null};
  }
  function buildIssues(data,config){const seen=new Set();return checkData(data,config).filter(item=>item.status==='open'||item.status==='fail').map(item=>issueFromCheck(item,data)).filter(item=>!seen.has(item.id)&&seen.add(item.id))}
  function finalState(data,issues=[],config,confirmedDefects=[]){const unresolved=issues.filter(item=>!item.resolution),checks=checkData(data,config),failed=checks.filter(item=>item.status==='fail'),confirmed=[...confirmedDefects];return{complete:unresolved.length===0,plausible:unresolved.length===0&&failed.length===0&&confirmed.length===0,unresolved,failed,confirmedDefects:confirmed,checks}}
  function parseDate(value){const text=String(value||'').trim(),m=text.match(/(\d{1,2})[.\/-](\d{1,2})[.\/-](\d{2,4})/);if(!m)return'';const year=m[3].length===2?`20${m[3]}`:m[3];return `${year}-${m[2].padStart(2,'0')}-${m[1].padStart(2,'0')}`}
  function parseText(text){
    const raw=String(text||''),compact=raw.replace(/\s+/g,' '),data={_confidence:{},_confidenceReason:{}};
    const set=(key,value,confidence=.76,reason='Textmuster')=>{if(present(value)){data[key]=typeof value==='number'?value:String(value).trim();data._confidence[key]=confidence;data._confidenceReason[key]=reason}};
    if(/VDE\s*0100[-–]?600|IEC\s*60364[-–]?6/i.test(raw)&&/12782/i.test(raw))set('protocolType','supported',.98,'eindeutige Formularanker');
    if(/Erstpr[üu]fung/i.test(raw))set('testReason','Erstprüfung',.84);else if(/Wiederholungspr[üu]fung/i.test(raw))set('testReason','Wiederholungsprüfung',.84);else if(/Instandsetzung|Änderung|Aenderung/i.test(raw))set('testReason','Änderung',.82);else if(/Ex[- ]?Bereich/i.test(raw))set('testReason','Ex-Bereich',.82);
    const patterns={nominalVoltage:/\b(?:Un|Nennspannung)\D{0,18}(\d{2,4})\s*V/i,nominalCurrent:/\b(?:In|Nennstrom)\D{0,15}(\d{1,4}(?:[,.]\d+)?)\s*A/i,continuity:/\b(?:Niederohm\w*)\D{0,20}(\d+[,.]\d+)\s*[ΩO]/i,loopImpedance:/\b(?:Zs|Schleifenimpedanz)\D{0,20}(\d+[,.]\d+)\s*[ΩO]/i,voltageDropPercent:/\b(?:Spannungsfall|ε)\D{0,25}(\d+[,.]\d+)\s*%/i,rcdNominalResidual:/I\s*[ΔA]?N?\D{0,14}(\d+(?:[,.]\d+)?)\s*mA/i,rcdTripTime:/\b(?:Ausl[öo]sezeit|tA)\D{0,18}(\d+(?:[,.]\d+)?)\s*ms/i};
    Object.entries(patterns).forEach(([key,re])=>{const match=compact.match(re);if(match)set(key,number(match[1]),.76)});const breaker=compact.match(/\b([BCD])\s*(\d{1,3})\s*A?\b/i);if(breaker){set('protectiveDevice',`${breaker[1].toUpperCase()}${breaker[2]}`,.78);if(!present(data.nominalCurrent))set('nominalCurrent',number(breaker[2]),.74)}
    const date=compact.match(/(?:Datum|Kal\.?\s*Datum)\D{0,18}(\d{1,2}[.\/-]\d{1,2}[.\/-]\d{2,4})/i);if(date)set('testDate',parseDate(date[1]),.76);return data;
  }

  return{VERSION,FIELD_DEFS,number,valuesList,normalize,curveFactor,checkData,buildIssues,finalState,parseDate,parseText,confidenceThreshold};
});
