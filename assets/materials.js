(()=>{'use strict';
const RELEASE='2.0.2.0';
const normalize=value=>String(value||'').toLocaleLowerCase('de-DE').normalize('NFD').replace(/[\u0300-\u036f]/g,'').replace(/ß/g,'ss').replace(/[^a-z0-9]+/g,'');
const searchable=material=>[material.materialNumber,material.shortName,material.uns,...(material.internationalDesignations||[]),...(material.searchTerms||[])].map(normalize).join(' ');
const matches=(material,query)=>{const terms=String(query||'').trim().split(/\s+/).map(normalize).filter(Boolean);if(!terms.length)return true;const haystack=searchable(material);return terms.every(term=>haystack.includes(term))};
const filterMaterials=(materials,query,group='all')=>(materials||[]).filter(material=>(group==='all'||material.group===group)&&matches(material,query));
window.SK_MATERIALS=Object.freeze({normalize,matches,filterMaterials});
if(typeof document==='undefined')return;
const byId=id=>document.getElementById(id);
const root=()=>window.SK_PLT?.root||new URL('../../',location.href);
const create=(tag,className,text)=>{const node=document.createElement(tag);if(className)node.className=className;if(text!==undefined)node.textContent=text;return node};
let data={groups:[],materials:[],comparisons:[],safetyNotice:''};
let activeGroup='all';
const materialById=id=>data.materials.find(item=>item.id===id);
function chip(text,className='material-chip'){return create('span',className,text)}
function addList(parent,title,items,className){if(!items?.length)return;const section=create('section',className);section.append(create('h3','material-card-subtitle',title));const list=create('ul','material-list');items.forEach(item=>{const li=create('li','',item);list.append(li)});section.append(list);parent.append(section)}
function renderMaterial(material){
  const article=create('article','material-card');article.id=`material-${material.id}`;
  const head=create('div','material-card-head');
  const identity=create('div','material-identity');identity.append(chip(material.materialNumber,'material-number'),create('h2','',material.shortName));
  head.append(identity,chip(data.groups.find(group=>group.id===material.group)?.label||material.group,'material-group'));
  article.append(head);
  const designations=create('div','material-designations');(material.internationalDesignations||[]).forEach(value=>designations.append(chip(value)));if(material.uns)designations.append(chip(`UNS ${material.uns}`,'material-chip material-chip-uns'));article.append(designations);
  const facts=create('dl','material-facts');
  [['Werkstoffgruppe',data.groups.find(group=>group.id===material.group)?.label||material.group],['Erzeugnisform',material.productForm]].forEach(([term,value])=>{facts.append(create('dt','',term),create('dd','',value))});
  article.append(facts,create('p','material-explanation',material.explanation));
  addList(article,'Verwandte Werkstoffe',material.related,'material-related');
  addList(article,'Nicht verwechseln mit',material.doNotConfuseWith,'material-not-confuse');
  const sourceSection=create('section','material-sources');sourceSection.append(create('h3','material-card-subtitle','Quellen'));
  const sourceList=create('ul','material-source-list');(material.sources||[]).forEach(source=>{const li=create('li');const link=create('a','',source.label);link.href=source.url;link.target='_blank';link.rel='noopener noreferrer';li.append(link);sourceList.append(li)});sourceSection.append(sourceList);article.append(sourceSection);
  const notice=create('p','material-safety',data.safetyNotice);notice.setAttribute('role','note');article.append(notice);
  return article;
}
function renderResults(){
  const query=byId('materialSearch')?.value||'';
  const results=filterMaterials(data.materials,query,activeGroup);
  const list=byId('materialResults');if(!list)return;
  list.replaceChildren(...results.map(renderMaterial));
  const status=byId('materialResultCount');if(status){const suffix=query&&results.length>1?' · Mehrfachtreffer – Werkstoffnummer und Erzeugnisform prüfen':'';status.textContent=`${results.length} ${results.length===1?'Werkstoff':'Werkstoffe'} gefunden${suffix}`}
  const empty=byId('materialEmpty');if(empty)empty.hidden=results.length!==0;
}
function renderFilters(){
  const box=byId('materialGroupFilters');if(!box)return;
  const groups=[{id:'all',label:'Alle'},...data.groups];
  box.replaceChildren(...groups.map(group=>{const button=create('button',`material-filter${group.id===activeGroup?' active':''}`,group.label);button.type='button';button.dataset.group=group.id;button.setAttribute('aria-pressed',String(group.id===activeGroup));button.addEventListener('click',()=>{activeGroup=group.id;renderFilters();renderResults()});return button}));
}
function renderComparison(){
  const select=byId('materialCompareSelect'),target=byId('materialComparison');if(!select||!target)return;
  const comparison=data.comparisons.find(item=>item.id===select.value)||data.comparisons[0];if(!comparison){target.replaceChildren();return}
  const left=materialById(comparison.left),right=materialById(comparison.right);
  const title=create('h3','',comparison.title),summary=create('p','material-compare-summary',comparison.summary),table=create('table','material-compare-table');
  const thead=create('thead'),headRow=create('tr');headRow.append(create('th','','Merkmal'),create('th','',left?.materialNumber||'Links'),create('th','',right?.materialNumber||'Rechts'));thead.append(headRow);
  const tbody=create('tbody');comparison.rows.forEach(row=>{const tr=create('tr');tr.append(create('th','',row.label),create('td','',row.left),create('td','',row.right));tbody.append(tr)});table.append(thead,tbody);
  target.replaceChildren(title,summary,table,create('p','material-safety',data.safetyNotice));
}
function setFromQuery(){const query=new URLSearchParams(location.search).get('q');if(query&&byId('materialSearch'))byId('materialSearch').value=query}
async function init(){
  if(!byId('materialLookup'))return;
  try{const response=await fetch(new URL(`assets/materials.json?v=${RELEASE}`,root()),{cache:'no-store'});if(!response.ok)throw new Error(String(response.status));data=await response.json()}catch(error){console.error('Werkstoffdaten konnten nicht geladen werden.',error);const errorBox=byId('materialLoadError');if(errorBox)errorBox.hidden=false;return}
  setFromQuery();renderFilters();renderResults();
  const select=byId('materialCompareSelect');if(select){select.replaceChildren(...data.comparisons.map(item=>{const option=create('option','',item.title);option.value=item.id;return option}));select.addEventListener('change',renderComparison);renderComparison()}
  byId('materialSearch')?.addEventListener('input',renderResults);
  byId('materialReset')?.addEventListener('click',()=>{byId('materialSearch').value='';activeGroup='all';history.replaceState(null,'',location.pathname);renderFilters();renderResults();byId('materialSearch').focus()});
  document.dispatchEvent(new CustomEvent('sk:cards-updated',{detail:{source:'materials',version:RELEASE}}));
}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init,{once:true});else init();
})();
