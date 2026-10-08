'use strict';
const ENGINE=window.SK_VDE_ENGINE,$=id=>document.getElementById(id);
const state={schema:null,current:'voltageDrop',values:{},results:{}};
const escapeHtml=value=>String(value??'').replace(/[&<>'"]/g,char=>({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#039;','"':'&quot;'}[char]));

function currentValues(){return state.values[state.current]||(state.values[state.current]={})}
function currentDefinition(){return state.schema?.measurementTypes?.[state.current]}
function visible(field,values){const rule=field.showWhen;if(!rule)return true;return rule.values.includes(values[rule.field])}
function clearFeedback(){
  $('inputAlert').hidden=true;$('inputAlertList').replaceChildren();$('resultPanel').hidden=true;
  $('measurementForm').querySelectorAll('[aria-invalid="true"]').forEach(item=>item.removeAttribute('aria-invalid'));
}
function invalidateCurrentResult(){if(state.results[state.current])delete state.results[state.current];renderNavigation();renderLedger();$('resultPanel').hidden=true}

function createField(field,required){
  const values=currentValues(),wrapper=document.createElement('label');wrapper.className='input-field';wrapper.dataset.fieldWrap=field.id;
  const heading=document.createElement('span');heading.className='input-label';heading.innerHTML=`${escapeHtml(field.label)}${required?'<em>erforderlich</em>':''}`;wrapper.append(heading);
  const shell=document.createElement('div');shell.className='input-shell';let control;
  if(field.type==='choice'){
    control=document.createElement('select');control.innerHTML='<option value="">Bitte auswählen</option>'+field.options.map(([value,label])=>`<option value="${escapeHtml(value)}">${escapeHtml(label)}</option>`).join('');
  }else{
    control=document.createElement('input');control.type='text';control.inputMode='decimal';control.autocomplete='off';control.placeholder='Wert eingeben';
  }
  control.id=field.id;control.name=field.id;control.value=values[field.id]??'';control.required=required;control.setAttribute('aria-label',field.label);
  if(field.unit){const unit=document.createElement('span');unit.className='input-unit';unit.textContent=field.unit;shell.append(control,unit)}else shell.append(control);
  wrapper.append(shell);
  if(field.help){const help=document.createElement('small');help.textContent=field.help;wrapper.append(help)}
  control.addEventListener('input',()=>{
    values[field.id]=control.value;invalidateCurrentResult();
    if(field.type==='choice'){renderFields();requestAnimationFrame(()=>$(field.id)?.focus())}
  });
  control.addEventListener('change',()=>{
    values[field.id]=control.value;invalidateCurrentResult();
    if(field.type==='choice')renderFields();
  });
  return wrapper;
}

function renderFields(){
  const definition=currentDefinition(),values=currentValues(),host=$('inputGrid');host.replaceChildren();clearFeedback();
  const required=new Set(ENGINE.requiredFields(state.current,values));
  for(const field of definition.fields){if(visible(field,values))host.append(createField(field,required.has(field.id)))}
}

function renderNavigation(){
  const nav=$('measurementNav');nav.replaceChildren();
  for(const [key,definition] of Object.entries(state.schema.measurementTypes)){
    const button=document.createElement('button'),result=state.results[key];button.type='button';button.className=`measurement-button${key===state.current?' active':''}${result?` ${result.status}`:''}`;button.dataset.measurement=key;button.setAttribute('aria-current',key===state.current?'page':'false');
    button.innerHTML=`<span>${escapeHtml(definition.number)}</span><div><strong>${escapeHtml(definition.title)}</strong><small>${escapeHtml(definition.code)}</small></div><i>${result?(result.status==='pass'?'i. O.':'n. i. O.'):'offen'}</i>`;
    button.onclick=()=>selectMeasurement(key);nav.append(button);
  }
}

function renderHeader(){const definition=currentDefinition();$('measurementSection').textContent=`MESSGRÖSSE ${definition.number}`;$('measurementTitle').textContent=definition.title;$('measurementDescription').textContent=definition.description;$('measurementCode').textContent=definition.code}
function renderLedger(){const results=Object.values(state.results),failed=results.filter(item=>item.status==='fail').length;$('sessionCount').textContent=String(results.length);$('sessionState').textContent=!results.length?'Noch kein Ergebnis':failed?`${failed} × nicht i. O.`:`${results.length} × i. O.`}
function selectMeasurement(key){if(!state.schema.measurementTypes[key])return;state.current=key;renderNavigation();renderHeader();renderFields();const result=state.results[key];if(result)renderResult(result);window.scrollTo({top:Math.max(0,$('measurementForm').getBoundingClientRect().top+window.scrollY-130),behavior:'smooth'})}

function showProblems(result){
  const items=result.status==='incomplete'?result.missing:result.errors;$('inputAlertTitle').textContent=result.status==='incomplete'?'Berechnungsgrundlage unvollständig':'Eingabe nicht berechenbar';const list=$('inputAlertList');list.replaceChildren();
  for(const item of items){const row=document.createElement('li');row.textContent=result.status==='incomplete'?`${item.label} fehlt.`:item.message;list.append(row);const field=$(item.field);if(field)field.setAttribute('aria-invalid','true')}
  $('inputAlert').hidden=false;$('resultPanel').hidden=true;const first=items[0]?.field?$(items[0].field):null;if(first)first.focus();$('inputAlert').scrollIntoView({behavior:'smooth',block:'center'});
}
function renderCheck(check){const row=document.createElement('article');row.className=`check-row ${check.status}`;row.innerHTML=`<b>${check.passed?'✓':'×'}</b><div><span>${escapeHtml(check.title)}</span><strong>${escapeHtml(check.resultLabel)}</strong><small>${escapeHtml(check.calculation)}</small></div>`;return row}
function renderResult(result){
  if(!result.complete){showProblems(result);return}$('inputAlert').hidden=true;const passed=result.status==='pass',panel=$('resultPanel'),banner=$('resultBanner');banner.classList.toggle('fail',!passed);$('resultIcon').textContent=passed?'✓':'×';$('resultTitle').textContent=passed?'i. O.':'nicht i. O.';$('resultSubtitle').textContent=passed?'Der Messwert erfüllt die vollständig angegebene Bewertungsgrundlage.':'Mindestens ein Messwert verletzt den verwendeten Grenzwert.';$('resultLimit').textContent=result.limitText;$('resultFormula').textContent=result.formula;$('resultCalculation').textContent=result.calculation;const checks=$('resultChecks');checks.replaceChildren();result.checks.forEach(item=>checks.append(renderCheck(item)));panel.hidden=false;panel.scrollIntoView({behavior:'smooth',block:'start'});
}
function evaluateCurrent(){
  clearFeedback();const result=ENGINE.evaluate(state.current,{...currentValues()});
  if(!result.complete){showProblems(result);return result}
  state.results[state.current]=result;renderNavigation();renderLedger();renderResult(result);return result;
}
function resetCurrent(){state.values[state.current]={};delete state.results[state.current];renderNavigation();renderLedger();renderFields();$(currentDefinition().fields[0]?.id)?.focus()}
function setValues(values){state.values[state.current]={...currentValues(),...values};delete state.results[state.current];renderNavigation();renderLedger();renderFields()}
function summary(){return{version:ENGINE.VERSION,mode:'manual-only',current:state.current,values:JSON.parse(JSON.stringify(state.values)),results:Object.fromEntries(Object.entries(state.results).map(([key,value])=>[key,{status:value.status,resultLabel:value.resultLabel,complete:value.complete}])),resultVisible:!$('resultPanel').hidden,automaticDocumentAnalysis:false}}

async function init(){
  if(!ENGINE)throw new Error('VDE-Messwertengine fehlt.');
  try{const response=await fetch('../assets/vde0100-600-input-schema.json?v=2.1.1.0-Beta',{cache:'no-store'});if(!response.ok)throw new Error(`Eingabeschema nicht verfügbar (${response.status}).`);state.schema=await response.json()}catch(error){$('inputAlertTitle').textContent='Messwertprüfer nicht gestartet';$('inputAlertList').innerHTML=`<li>${escapeHtml(error.message||String(error))}</li>`;$('inputAlert').hidden=false;return}
  $('measurementForm').addEventListener('submit',event=>{event.preventDefault();evaluateCurrent()});$('resetMeasurement').onclick=resetCurrent;renderNavigation();renderHeader();renderFields();renderLedger();window.SK_VDE_CHECKER=Object.freeze({summary,selectMeasurement,setValues,evaluate:evaluateCurrent,reset:resetCurrent});
}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init);else init();
