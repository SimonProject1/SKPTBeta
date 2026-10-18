/* SK PCT Tools 2.6.6.1-Beta — kompakte Hersteller → Gerät/Familie/Thema → Beitrag-Navigation. */
(()=>{'use strict';
const RELEASE='2.6.6.1-Beta';
const ROOT=window.SK_PCT?.root||new URL('../',document.currentScript?.src||location.href);
const KNOWLEDGE_ROOT=new URL('wissensdatenbank/',ROOT);
const ICON_ROOT=new URL('assets/navigation-icons/',ROOT);
const norm=window.SK_PCT_SHARED.foldText;
const isPlain=e=>!e.defaultPrevented&&e.button<=0&&!e.metaKey&&!e.ctrlKey&&!e.shiftKey&&!e.altKey;
const DATA=[
 {slug:'air-torque',name:'Air Torque',label:['Air','Torque'],description:'Pneumatische Antriebe und eindeutige Wirkrichtungen.',icon:'manufacturer-air-torque',search:'Airtorque pneumatisch Antrieb Drehrichtung SCO SCC',families:[
  {slug:'pneumatischer-antrieb',name:'Pneumatischer Antrieb',label:['Pneumatischer','Antrieb'],description:'Antrieb, Federwirkung und Drehrichtung.',icon:'device-air-torque-pneumatic-actuator',search:'Antrieb pneumatisch Federkraft',articles:[
   {slug:'air-torque-antrieb-drehrichtung',name:'Drehrichtung SCO/SCC',label:['Drehrichtung','SCO/SCC'],description:'Bedeutung von SCO und SCC sicher zuordnen.',icon:'knowledge-air-torque-antrieb-drehrichtung',search:'Uhrzeigersinn gegen Uhrzeigersinn Typenschild'}]}]},
 {slug:'endress-hauser',name:'Endress+Hauser',nowrap:true,description:'Gerätefamilien für Durchfluss- und Prozessmesstechnik.',icon:'manufacturer-endress-hauser',search:'E+H Endress Hauser Coriolis Massedurchfluss',families:[
  {slug:'promass',name:'Promass',description:'Coriolis-Massedurchflussmessung und sichere Einbausituationen.',icon:'device-endress-hauser-promass',search:'Promass Coriolis Massedurchfluss',articles:[
   {slug:'endress-hauser-promass-einbaulage',name:'Einbaulage und Einbausituation',label:['Einbaulage und','Einbausituation'],description:'Füllung, Druckhaltung, Gasblasen, Feststoffe und Armaturen.',icon:'knowledge-endress-hauser-promass-einbaulage',search:'Steigleitung Druckseite Pumpe Fallleitung freier Auslauf Saugseite Ventil Rohrerweiterung'}]}]},
 {slug:'siemens',name:'Siemens',description:'Geräte-, SPS- und Analogkartenwissen für die PCT-Praxis.',icon:'manufacturer-siemens',search:'Siemens SIMATIC PDM SPS Analogkarte Rohwert',families:[
  {slug:'sitrans-p320',name:'SITRANS P320',label:['SITRANS','P320'],description:'Druckmessumformer und SIL-relevante Bedienhinweise.',icon:'device-siemens-sitrans-p320',search:'Sitrans P320 Druckmessumformer SIL',articles:[
   {slug:'siemens-sitrans-p320-sil-verriegelung',name:'SIL-Verriegelung',nowrap:true,description:'SIMATIC PDM, Schreibschutz und Initial-PIN 2457.',icon:'knowledge-siemens-sitrans-p320-sil-verriegelung',search:'SIL Verriegelung Schreibschutz PIN 2457'}]},
  {slug:'sps-analogkarte',name:'SPS / Analogkarte',label:['SPS /','Analogkarte'],description:'Analogwerte, Rohwerte, Skalierung und Diagnosebereiche.',icon:'device-siemens-sps-analogkarte',search:'SPS Analogkarte S7 ET200 A/D Wandler',articles:[
   {slug:'siemens-sps-rohwert',name:'Rohwert und Skalierung',label:['Rohwert und','Skalierung'],description:'Nennbereiche, Skalierungsmodelle und Diagnosegrenzen.',icon:'knowledge-siemens-sps-rohwert',search:'Rohwert Skalierung 27648 5530 NE43 Unterlauf Überlauf'}]}]},
 {slug:'vacon',name:'Vacon',description:'Frequenzumrichter und Diagnosehinweise für den PLS-Betrieb.',icon:'manufacturer-vacon',search:'Vacon FU Frequenzumrichter PLS',families:[
  {slug:'frequenzumrichter',name:'Frequenzumrichter',nowrap:true,description:'Sollwert, Istwert, Frequenzgrenzen und Parametrierung.',icon:'device-vacon-frequenzumrichter',search:'FU Umrichter Frequenz Sollwert Istwert',articles:[
   {slug:'vacon-frequenzumrichter-ist-sollwert-abweichung',name:'Ist-/Sollwert-Abweichung im PLS',label:['Ist-/Sollwert-','Abweichung im PLS'],description:'Parameter 2.2.3.7 und maximale Frequenz prüfen.',icon:'knowledge-vacon-frequenzumrichter-ist-sollwert-abweichung',search:'PLS Parameter 2.2.3.7 maximale Frequenz Abweichung'}]}]},
 {slug:'sonstiges',name:'Sonstiges',description:'Herstellerunabhängige Beiträge – aktuell ohne vorhandene Inhalte.',icon:'manufacturer-sonstiges',search:'Sonstiges herstellerunabhängig allgemein',families:[]}
];
const byId=id=>document.getElementById(id);
const iconUrl=stem=>new URL(`v2-6-6-1-${stem}.png?v=${RELEASE}`,ICON_ROOT).href;
const params=()=>new URL(location.href).searchParams;
const manufacturer=()=>DATA.find(x=>x.slug===params().get('manufacturer'))||null;
const family=m=>m?.families.find(x=>x.slug===params().get('family'))||null;
const hrefFor=(m,f)=>{const url=new URL(KNOWLEDGE_ROOT);if(m)url.searchParams.set('manufacturer',m.slug);if(f)url.searchParams.set('family',f.slug);return url.href};
function controlledLabel(node,item){
 node.replaceChildren();node.classList.toggle('sk-label-nowrap',Boolean(item.nowrap));
 if(item.nowrap||!item.label){node.textContent=item.name;return}
 item.label.forEach((part,index)=>{const span=document.createElement('span');span.className='sk-label-segment';span.textContent=part;node.append(span);if(index<item.label.length-1)node.append(document.createElement('wbr'),document.createTextNode(' '))});
}
function card(item,meta,href){
 const link=document.createElement('a');link.className='knowledge-tile tool-card';link.href=href;link.dataset.search=meta.search;link.dataset.level=meta.level;link.dataset.category=meta.category;link.setAttribute('aria-label',`${item.name} öffnen`);
 const icon=document.createElement('span');icon.className='sk-home-icon knowledge-home-icon';const image=document.createElement('img');image.alt='';image.decoding='sync';image.src=iconUrl(item.icon);icon.append(image);
 const title=document.createElement('h2');controlledLabel(title,item);link.append(icon,title);
 if(meta.path){const path=document.createElement('div');path.className='knowledge-tile-path';path.textContent=meta.path;link.append(path)}
 return link;
}
function allSearchItems(){const out=[];DATA.forEach(m=>{out.push({item:m,level:'manufacturer',category:'HERSTELLER',path:'Hersteller',href:hrefFor(m),search:`${m.name} ${m.description} ${m.search}`});m.families.forEach(f=>{out.push({item:f,level:'family',category:'GERÄT / FAMILIE / THEMA',path:m.name,href:hrefFor(m,f),search:`${m.name} ${f.name} ${f.description} ${f.search}`});f.articles.forEach(a=>out.push({item:a,level:'article',category:'WISSENSBEITRAG',path:`${m.name} › ${f.name}`,href:new URL(a.slug+'/',KNOWLEDGE_ROOT).href,search:`${m.name} ${m.search} ${f.name} ${f.search} ${a.name} ${a.description} ${a.search}`}))})});return out}
function setTitle(node,text){node.replaceChildren();const parts=text==='Wissensdatenbank'?['Wissens','datenbank']:text==='Endress+Hauser'?['Endress+Hauser']:[text];parts.forEach((part,i)=>{if(i)node.append(document.createElement('wbr'));node.append(document.createTextNode(part))})}
function breadcrumb(m,f){const nav=byId('knowledgeBreadcrumb');nav.replaceChildren();const add=(label,url)=>{if(nav.childElementCount){const sep=document.createElement('span');sep.textContent='›';nav.append(sep)}const n=url?document.createElement('a'):document.createElement('span');n.textContent=label;if(url)n.href=url;nav.append(n)};add('Startseite',new URL('./',ROOT));add('Wissensdatenbank',m?KNOWLEDGE_ROOT:null);if(m)add(m.name,f?hrefFor(m):null);if(f)add(f.name,null)}
function modeItems(m,f){if(!m)return DATA.map(item=>({item,level:'manufacturer',category:'HERSTELLER',path:'',href:hrefFor(item),search:`${item.name} ${item.description} ${item.search}`}));if(!f)return m.families.map(item=>({item,level:'family',category:'GERÄT / FAMILIE / THEMA',path:'',href:hrefFor(m,item),search:`${m.name} ${item.name} ${item.description} ${item.search}`}));return f.articles.map(item=>({item,level:'article',category:'WISSENSBEITRAG',path:'',href:new URL(item.slug+'/',KNOWLEDGE_ROOT).href,search:`${m.name} ${f.name} ${item.name} ${item.description} ${item.search}`}))}
function render(){const m=manufacturer(),f=family(m),q=norm(byId('knowledgeSearch').value),searching=Boolean(q);breadcrumb(m,f);const hero=byId('knowledgeHeroIcon'),title=byId('knowledgeTitle'),kicker=byId('knowledgeKicker'),desc=byId('knowledgeDescription'),back=byId('knowledgeViewBack'),backLabel=byId('knowledgeBackLabel');let items;
 if(searching){items=allSearchItems().filter(x=>q.split(/\s+/).every(term=>norm(x.search+' '+x.path).includes(term)));kicker.textContent='SUCHE';setTitle(title,'Wissensdatenbank');desc.textContent='Treffer aus allen Ebenen.';hero.src=iconUrl('app-wissensdatenbank')}
 else if(!m){items=modeItems(null,null);kicker.textContent='WISSEN';setTitle(title,'Wissensdatenbank');desc.textContent='Hersteller wählen und direkt zum Gerät oder Beitrag navigieren.';hero.src=iconUrl('app-wissensdatenbank')}
 else if(!f){items=modeItems(m,null);kicker.textContent='GERÄTE UND THEMEN';setTitle(title,m.name);desc.textContent='Gerät, Familie oder Themenbereich wählen.';hero.src=iconUrl(m.icon)}
 else{items=modeItems(m,f);kicker.textContent='BEITRÄGE';setTitle(title,f.name);desc.textContent='Wissensbeitrag öffnen.';hero.src=iconUrl(f.icon)}
 const grid=byId('knowledgeGrid');grid.replaceChildren(...items.map(x=>card(x.item,x,x.href)));const empty=byId('knowledgeEmpty');empty.hidden=items.length!==0;if(!items.length&&!searching){empty.querySelector('strong').textContent='Noch keine Wissensbeiträge vorhanden.';empty.querySelector('span').textContent='Für diesen Bereich sind noch keine Inhalte hinterlegt.'}else{empty.querySelector('strong').textContent='Keine passenden Inhalte gefunden.';empty.querySelector('span').textContent='Suchbegriff verkürzen oder Suche zurücksetzen.'}
 const label=searching?'Treffer':(!m?'Hersteller':!f?'Bereiche':'Beiträge');byId('knowledgeResultCount').textContent=`${items.length} ${label} angezeigt`;byId('knowledgeSearchReset').hidden=!searching;
 if(searching||!m){back.hidden=true}else{back.hidden=false;back.href=f?hrefFor(m):KNOWLEDGE_ROOT.href;backLabel.textContent=f?m.name:'Wissensdatenbank'}
 document.title=`${f?f.name:m?m.name:'Wissensdatenbank'} | SK PCT Tools`;document.dispatchEvent(new CustomEvent('sk:cards-updated',{detail:{source:'knowledge-navigation',version:RELEASE}}))}
function navigate(url){history.pushState({},'',url);byId('knowledgeSearch').value='';render();document.querySelector('.knowledge-app-scroll')?.scrollTo({top:0,behavior:'auto'})}
function init(){if(!byId('knowledgeGrid'))return;byId('knowledgeSearch').addEventListener('input',render);byId('knowledgeSearchReset').addEventListener('click',()=>{byId('knowledgeSearch').value='';render();byId('knowledgeSearch').focus()});byId('knowledgeGrid').addEventListener('click',e=>{if(e.target.closest('.sk-favorite-button'))return;const link=e.target.closest('a.knowledge-tile');if(!link||!isPlain(e))return;const target=new URL(link.href);if(target.pathname.replace(/index\.html$/,'')===KNOWLEDGE_ROOT.pathname&&target.search){e.preventDefault();navigate(link.href)}});byId('knowledgeViewBack').addEventListener('click',e=>{if(!isPlain(e))return;e.preventDefault();navigate(e.currentTarget.href)});addEventListener('popstate',render);render()}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init,{once:true});else init();
})();
