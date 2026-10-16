/* SK PCT Tools 2.6.1.9-Beta — zentrale Laufzeit: Layout, Version, Favoriten, Suche, Sortierung, Navigation und Controls. */

/* Gemeinsame, kleine Laufzeithilfen für Speicherung, Suche und sicheres Markup. */
(()=>{'use strict';
const readJSON=(key,fallback)=>{try{const value=JSON.parse(localStorage.getItem(key));return value??fallback}catch{return fallback}};
const writeJSON=(key,value)=>{try{localStorage.setItem(key,JSON.stringify(value));return true}catch(error){console.warn('Einstellung konnte nicht gespeichert werden.',error);return false}};
const foldText=value=>String(value||'').toLocaleLowerCase('de-DE').normalize('NFD').replace(/[\u0300-\u036f]/g,'').replace(/ß/g,'ss').replace(/[^a-z0-9+]+/g,' ').trim();
const sortText=value=>String(value||'').trim().toLocaleLowerCase('de-DE').normalize('NFD').replace(/[\u0300-\u036f]/g,'');
const escapeHTML=value=>String(value||'').replace(/[&<>"']/g,char=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#039;'}[char]));
window.SK_PCT_SHARED=Object.freeze({readJSON,writeJSON,foldText,sortText,escapeHTML});
})();

/* === Modul: Startseite und App-Reihenfolge === */
/* SK PCT Tools 2.6.1.9-Beta — reduzierter PCT Home-Screen mit Long-Press-Bearbeitungsmodus. */
(()=>{'use strict';
const RELEASE='2.6.1.9-Beta';
const ORDER_KEY='skPctHomeOrderV1';
const root=document.documentElement;
const byId=id=>document.getElementById(id);
const {readJSON:read,writeJSON:write}=window.SK_PCT_SHARED;
const cards=grid=>[...grid.querySelectorAll(':scope > .sk-home-app')];
function boot(){
  const grid=byId('pctHomeGrid');
  if(!grid||document.body?.dataset.skHome!=='ios')return;
  const defaultOrder=cards(grid).map(card=>card.dataset.appId);
  const doneButton=byId('pctHomeDone'),resetButton=byId('pctHomeReset'),announcement=byId('pctHomeAnnouncement');
  let editing=false,pending=null,dragging=null,ghost=null,suppressClick=false;
  const announce=text=>{if(announcement){announcement.textContent='';requestAnimationFrame(()=>announcement.textContent=text)}};
  const currentOrder=()=>cards(grid).map(card=>card.dataset.appId);
  const notifyOrder=()=>document.dispatchEvent(new CustomEvent('sk:home-order-changed',{detail:{order:currentOrder(),version:RELEASE}}));
  function applyOrder(order){const lookup=new Map(cards(grid).map(card=>[card.dataset.appId,card]));[...order,...defaultOrder].forEach(id=>{const card=lookup.get(id);if(card){grid.append(card);lookup.delete(id)}});lookup.forEach(card=>grid.append(card));notifyOrder()}
  function saveOrder(){write(ORDER_KEY,currentOrder());notifyOrder()}
  applyOrder(read(ORDER_KEY,defaultOrder));
  function setEditing(value){editing=Boolean(value);document.body.classList.toggle('pct-home-editing',editing);grid.setAttribute('aria-label',editing?'PCT Apps anordnen. Ziehen oder mit Pfeiltasten verschieben.':'PCT Apps');cards(grid).forEach(card=>card.setAttribute('aria-grabbed',String(editing&&card===dragging)));if(!editing)finishDrag();announce(editing?'Bearbeitungsmodus aktiv. Apps wackeln und können verschoben werden.':'Anordnung gespeichert.')}
  doneButton?.addEventListener('click',()=>setEditing(false));
  resetButton?.addEventListener('click',()=>{localStorage.removeItem(ORDER_KEY);applyOrder(defaultOrder);const sort=byId('skToolSort');if(sort)sort.value='default';announce('Standardreihenfolge wiederhergestellt.')});
  byId('skToolSort')?.addEventListener('change',event=>{if(event.target.value!=='default')setEditing(false)});
  function makeGhost(card,event){ghost=card.cloneNode(true);ghost.removeAttribute('href');ghost.removeAttribute('id');ghost.classList.remove('is-dragging');ghost.classList.add('pct-home-drag-ghost');ghost.setAttribute('aria-hidden','true');ghost.querySelectorAll('button').forEach(button=>button.remove());document.body.append(ghost);moveGhost(event)}
  function moveGhost(event){if(!ghost)return;const rect=ghost.getBoundingClientRect();ghost.style.left=`${event.clientX-rect.width/2}px`;ghost.style.top=`${event.clientY-rect.height/2}px`}
  function beginDrag(card,event){if(dragging)return;setEditing(true);dragging=card;suppressClick=true;card.classList.add('is-dragging');card.setAttribute('aria-grabbed','true');try{card.setPointerCapture(event.pointerId)}catch{}makeGhost(card,event);navigator.vibrate?.(8);announce(`${card.querySelector('h2')?.textContent||'App'} wird verschoben.`)}
  function finishDrag(){if(pending){clearTimeout(pending.timer);pending=null}if(!dragging)return;const card=dragging;dragging=null;card.classList.remove('is-dragging');card.setAttribute('aria-grabbed','false');ghost?.remove();ghost=null;saveOrder();card.focus({preventScroll:true});announce(`${card.querySelector('h2')?.textContent||'App'} abgelegt.`);setTimeout(()=>suppressClick=false,100)}
  function reorderAt(event){if(!dragging)return;dragging.style.pointerEvents='none';const target=document.elementFromPoint(event.clientX,event.clientY)?.closest('.sk-home-app');dragging.style.pointerEvents='';if(!target||target===dragging||target.parentElement!==grid||target.hidden)return;const rect=target.getBoundingClientRect();const after=event.clientY>rect.top+rect.height/2||(Math.abs(event.clientY-(rect.top+rect.height/2))<rect.height*.35&&event.clientX>rect.left+rect.width/2);grid.insertBefore(dragging,after?target.nextSibling:target)}
  grid.addEventListener('pointerdown',event=>{const card=event.target.closest('.sk-home-app');if(!card||event.target.closest('button,input,select,textarea')||event.button>0)return;const startX=event.clientX,startY=event.clientY;if(editing){event.preventDefault();beginDrag(card,event);return}pending={card,pointerId:event.pointerId,startX,startY,timer:setTimeout(()=>{if(pending?.pointerId===event.pointerId)beginDrag(card,event)},480)}});
  document.addEventListener('pointermove',event=>{if(dragging){event.preventDefault();moveGhost(event);reorderAt(event);return}if(!pending||pending.pointerId!==event.pointerId)return;const distance=Math.hypot(event.clientX-pending.startX,event.clientY-pending.startY);if(distance>8){clearTimeout(pending.timer);pending=null}},{passive:false});
  document.addEventListener('pointerup',event=>{if(pending?.pointerId===event.pointerId){clearTimeout(pending.timer);pending=null}if(dragging)finishDrag()});
  document.addEventListener('pointercancel',()=>finishDrag());
  grid.addEventListener('contextmenu',event=>{if(editing||pending||dragging)event.preventDefault()});
  grid.addEventListener('click',event=>{const card=event.target.closest('.sk-home-app');if(!card)return;if((editing&&!event.target.closest('button'))||suppressClick){event.preventDefault();event.stopPropagation()}},true);
  grid.addEventListener('keydown',event=>{const card=event.target.closest('.sk-home-app');if(!card)return;if(!editing&&event.key===' '){event.preventDefault();setEditing(true);card.focus();return}if(!editing||!['ArrowLeft','ArrowRight','ArrowUp','ArrowDown'].includes(event.key))return;const visible=cards(grid).filter(item=>!item.hidden),index=visible.indexOf(card);if(index<0)return;const tops=[...new Set(visible.map(item=>Math.round(item.getBoundingClientRect().top)))],columns=Math.max(1,visible.filter(item=>Math.round(item.getBoundingClientRect().top)===tops[0]).length);const delta={ArrowLeft:-1,ArrowRight:1,ArrowUp:-columns,ArrowDown:columns}[event.key],next=Math.max(0,Math.min(visible.length-1,index+delta));if(next===index)return;event.preventDefault();const target=visible[next];grid.insertBefore(card,delta>0?target.nextSibling:target);saveOrder();card.focus();announce(`${card.querySelector('h2')?.textContent||'App'} Position ${next+1} von ${visible.length}.`)});
  document.addEventListener('keydown',event=>{if(event.key==='Escape'&&editing)setEditing(false)});
}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',boot,{once:true});else boot();
})();


/* === Modul: Basis, Layout und PWA === */
/* SK PCT Tools 2.6.1.9-Beta — gemeinsame Laufzeitmodule: Basis, Favoriten, Suche und Sortierung. */
/* === app.js === */
(()=>{'use strict';
const RELEASE='2.6.1.9-Beta';
const DISPLAY_RELEASE='2.6.1.9-Beta';
const scriptUrl=document.currentScript?.src||'';
const root=scriptUrl?new URL('../',scriptUrl):new URL('./',location.href);
window.SK_PCT=Object.freeze({version:RELEASE,channel:'beta',name:'SK PCT Tools',root,utils:window.SK_PCT_SHARED});
window.$=id=>document.getElementById(id);
window.num=value=>Number.parseFloat(String(value).replace(',','.'));
window.de=(value,digits=3)=>{if(!Number.isFinite(value))return'–';const absolute=Math.abs(value),maximum=absolute!==0&&absolute<0.01?Math.max(digits,6):digits;return value.toLocaleString('de-DE',{minimumFractionDigits:0,maximumFractionDigits:maximum,useGrouping:true})};
function buildSharedLayout(){
 const header=document.querySelector('[data-sk-shared-header]');
 if(header&&!header.firstElementChild)header.innerHTML=`<div class="sk-header-inner"><div class="sk-logo-version-stack"><img alt="S.K. PCT TOOL" class="logo sk-global-logo sk-header-logo" src="${new URL(`assets/icon-192.png?v=${RELEASE}`,root).href}"></div><span aria-label="Aktuelle Version ${DISPLAY_RELEASE}" class="sk-header-version">V${DISPLAY_RELEASE}</span><a aria-label="Zur Startseite" class="home sk-header-home" href="${root.href}">← Startseite</a></div>`;
 document.querySelectorAll('[data-sk-shared-footer]').forEach(footer=>footer.textContent=`SK PCT Tools · Entwickelt von Simon Kiesler · V${DISPLAY_RELEASE}`);
}
function syncVersion(){document.querySelectorAll('.badge,.sk-header-version,.pct-home-version').forEach(node=>{const text=(node.textContent||'').trim();if(node.matches('.sk-header-version,.pct-home-version')||/^Version\s+/i.test(text))node.textContent=node.classList.contains('badge')?`Version ${DISPLAY_RELEASE}`:`V${DISPLAY_RELEASE}`;})}
function addSignControls(){if(document.body?.dataset.signControls!=='true')return;document.querySelectorAll('input[type=number]').forEach(input=>{if(input.dataset.s)return;input.dataset.s='1';const wrapper=document.createElement('div');wrapper.className='number';input.parentNode.insertBefore(wrapper,input);wrapper.append(input);const button=document.createElement('button');button.type='button';button.className='sign';button.textContent='±';button.setAttribute('aria-label','Vorzeichen wechseln');button.addEventListener('click',()=>{const value=window.num(input.value);input.value=Number.isFinite(value)?(value===0?0:-value):'-';input.dispatchEvent(new Event('input',{bubbles:true}));input.dispatchEvent(new Event('change',{bubbles:true}))});wrapper.append(button)})}
function registerWorker(){if(!('serviceWorker' in navigator))return;const worker=new URL(`service-worker.js?release=${encodeURIComponent(RELEASE)}`,root),reloadKey=`skPctReloaded:${RELEASE}`,hadController=Boolean(navigator.serviceWorker.controller);navigator.serviceWorker.addEventListener('controllerchange',()=>{if(!hadController)return;try{if(sessionStorage.getItem(reloadKey))return;sessionStorage.setItem(reloadKey,'1');location.reload()}catch{location.reload()}});navigator.serviceWorker.register(worker,{scope:root.pathname,updateViaCache:'none'}).then(registration=>{const activate=()=>registration.waiting?.postMessage({type:'SKIP_WAITING'});activate();registration.addEventListener('updatefound',()=>{const installing=registration.installing;installing?.addEventListener('statechange',()=>{if(installing.state==='installed')activate()})});return registration.update()}).catch(error=>console.warn('Service Worker konnte nicht registriert werden.',error));}
function init(){buildSharedLayout();syncVersion();addSignControls();registerWorker()}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init,{once:true});else init();
})();

/* === Modul: Favoriten === */
(()=>{'use strict';
const KEY='skPctToolsFavoritesV2';
const PATH='M12 2.75l2.82 5.72 6.31.92-4.57 4.45 1.08 6.29L12 17.16l-5.64 2.97 1.08-6.29-4.57-4.45 6.31-.92L12 2.75z';
const esc=window.SK_PCT_SHARED.escapeHTML;
const svg=on=>`<svg class="sk-star-svg" viewBox="0 0 24 24" aria-hidden="true"><path d="${PATH}"${on?' class="sk-star-fill"':''}></path></svg>`;
const load=()=>{const value=window.SK_PCT_SHARED.readJSON(KEY,[]);return Array.isArray(value)?value:[]};
const save=value=>window.SK_PCT_SHARED.writeJSON(KEY,value);
const cardUrl=card=>{try{return new URL(card.getAttribute('href')||'',location.href).href}catch{return card.getAttribute('href')||''}};
const info=card=>({url:cardUrl(card),title:card.querySelector('h1,h2,h3')?.textContent.trim()||'Favorit',description:card.querySelector('p')?.textContent.trim()||'',category:card.querySelector('.sk-card-category,.eyebrow')?.textContent.trim()||'FAVORIT',external:card.target==='_blank'});
const isOn=card=>load().some(item=>item.url===cardUrl(card));
function state(button,on){button.dataset.active=String(on);button.classList.toggle('active',on);button.setAttribute('aria-pressed',String(on));button.innerHTML=svg(on);button.title=on?'Aus Favoriten entfernen':'Zu Favoriten hinzufügen';button.setAttribute('aria-label',button.title)}
function sync(){document.querySelectorAll('.sk-favorite-button').forEach(button=>{const card=button.closest('a.card,a.tool-card');if(card)state(button,isOn(card))});const count=document.querySelector('.sk-favorites-count');if(count){const total=load().length;count.textContent=String(total);count.hidden=total===0}}
function toggle(card){const item=info(card),items=load(),index=items.findIndex(entry=>entry.url===item.url);index>=0?items.splice(index,1):items.push(item);save(items);sync();render()}
function prepare(){document.querySelectorAll('a.card,a.tool-card').forEach(card=>{const href=card.getAttribute('href')||'';if(!href||href.endsWith('.docx')||href.endsWith('.pdf')||card.classList.contains('sk-favorite-entry'))return;card.classList.add('sk-favorite-capable');const iconWrapper=card.querySelector(':scope > .sk-home-icon')||card.querySelector('.knowledge-home-icon');if(iconWrapper)iconWrapper.classList.add('sk-app-icon-wrapper');const host=iconWrapper||card;let button=card.querySelector('.sk-favorite-button');if(!button){button=document.createElement('button');button.type='button';button.className='sk-favorite-button'}if(button.parentElement!==host)host.append(button);if(button.dataset.bound)return;button.dataset.bound='true';button.addEventListener('click',event=>{event.preventDefault();event.stopPropagation();toggle(card)})});sync()}
let drawer,backdrop;
function ensure(){const trigger=document.querySelector('.sk-favorites-trigger')||document.body.appendChild(Object.assign(document.createElement('button'),{type:'button',className:'sk-favorites-trigger'}));if(trigger.dataset.bound)return;trigger.dataset.bound='true';trigger.setAttribute('aria-label','Favoriten öffnen');if(!trigger.querySelector('.sk-trigger-star'))trigger.innerHTML=`<span class="sk-trigger-star">${svg(true)}</span><span class="sk-favorites-count" hidden>0</span>`;backdrop=document.querySelector('.sk-favorites-backdrop')||document.body.appendChild(Object.assign(document.createElement('div'),{className:'sk-favorites-backdrop'}));drawer=document.querySelector('.sk-favorites-drawer')||document.body.appendChild(Object.assign(document.createElement('aside'),{className:'sk-favorites-drawer'}));drawer.setAttribute('aria-hidden','true');if(!drawer.querySelector('.sk-favorites-head'))drawer.innerHTML='<div class="sk-favorites-head"><div><div class="sk-favorites-kicker">SCHNELLZUGRIFF</div><h2>Meine Favoriten</h2></div><button class="sk-favorites-close" type="button" aria-label="Favoriten schließen">×</button></div><div class="sk-favorites-list"></div>';const open=()=>{render();drawer.classList.add('open');backdrop.classList.add('open');drawer.setAttribute('aria-hidden','false');document.body.classList.add('sk-drawer-open')};const close=()=>{drawer.classList.remove('open');backdrop.classList.remove('open');drawer.setAttribute('aria-hidden','true');document.body.classList.remove('sk-drawer-open')};trigger.addEventListener('click',open);backdrop.addEventListener('click',close);drawer.querySelector('.sk-favorites-close').addEventListener('click',close);document.addEventListener('keydown',event=>{if(event.key==='Escape')close()});sync()}
function render(){const list=document.querySelector('.sk-favorites-list');if(!list)return;const items=load();if(!items.length){list.innerHTML=`<div class="sk-favorites-empty">${svg(false)}<strong>Noch keine Favoriten</strong><p>Markiere eine Kachel über den Stern.</p></div>`;return}list.replaceChildren();items.forEach(item=>{const row=document.createElement('div');row.className='sk-favorite-row';const link=document.createElement('a');link.className='sk-favorite-entry';link.href=item.url;if(item.external){link.target='_blank';link.rel='external noopener noreferrer';link.referrerPolicy='no-referrer'}link.innerHTML=`<span class="sk-favorite-category">${esc(item.category)}</span><strong>${esc(item.title)}</strong>${item.description?`<small>${esc(item.description)}</small>`:''}`;const remove=document.createElement('button');remove.type='button';remove.className='sk-favorite-remove';remove.innerHTML=svg(true);remove.title='Aus Favoriten entfernen';remove.addEventListener('click',()=>{save(load().filter(value=>value.url!==item.url));sync();render()});row.append(link,remove);list.append(row)})}
function refresh(){prepare();sync();render()}
function init(){ensure();refresh();document.addEventListener('sk:cards-updated',refresh)}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init,{once:true});else init();
})();

/* === Modul: Startseitensuche === */
(()=>{'use strict';
let searchIndex=[];
let materialCatalog=[];
const RELEASE='2.6.1.9-Beta';
const norm=window.SK_PCT_SHARED.foldText;
const isStartPage=()=>document.body?.dataset.skPage==='start';
const root=()=>window.SK_PCT?.root||new URL('./',location.href);
const cards=()=>[...document.querySelectorAll('.tools a.card,.start-tools a.tool-card')];
const category=card=>(card.querySelector('.sk-card-category')?.textContent||'').trim().toUpperCase();
const escapeText=window.SK_PCT_SHARED.escapeHTML;
function matchIndex(item,query,active){const categoryMatch=active==='ALLE'||active==='WISSEN'&&item.category==='WISSEN';if(!categoryMatch||!query)return false;const catalogTerms=item.catalog==='materials'?materialCatalog.flatMap(material=>[material.materialNumber,material.shortName,material.uns,...(material.internationalDesignations||[]),...(material.searchTerms||[])]):[];const haystack=norm([item.type,item.category,item.manufacturer,item.device,item.topic,item.title,item.description,(item.breadcrumb||[]).join(' '),(item.keywords||[]).join(' '),catalogTerms.join(' ')].join(' '));return query.split(/\s+/).every(term=>haystack.includes(term))}
function renderKnowledge(query,active,rawQuery){const section=document.getElementById('skKnowledgeResults'),list=document.getElementById('skKnowledgeResultList'),count=document.getElementById('skKnowledgeResultCount');if(!section||!list)return 0;const results=searchIndex.filter(item=>matchIndex(item,query,active));list.replaceChildren();results.forEach(item=>{const card=document.createElement('a');card.className='card sk-search-result-card';const target=new URL(item.url,root());if(item.passthroughQuery&&rawQuery.trim())target.searchParams.set('q',rawQuery.trim());card.href=target.href;const breadcrumb=(item.breadcrumb||[]).map(escapeText).join('<span>›</span>');card.innerHTML=`<div class="sk-card-category">${escapeText(item.type)}</div><h3>${escapeText(item.title)}</h3><p>${escapeText(item.description)}</p><div class="sk-result-path">${breadcrumb}</div>`;list.append(card)});section.hidden=results.length===0;if(count)count.textContent=`${results.length} ${results.length===1?'Beitrag':'Beiträge'} gefunden`;return results.length}
function applyFilter(){const rawQuery=document.getElementById('skToolSearch')?.value||'',query=norm(rawQuery),active=document.querySelector('.sk-filter-button.active')?.dataset.filter||'ALLE';let tools=0;cards().forEach(card=>{const haystack=norm(`${category(card)} ${card.querySelector('h1,h2,h3')?.textContent||''} ${card.querySelector('p')?.textContent||''}`),categoryMatch=active==='ALLE'||category(card)===active,textMatch=!query||query.split(/\s+/).every(term=>haystack.includes(term)),show=categoryMatch&&textMatch;card.hidden=!show;card.classList.toggle('sk-filter-hidden',!show);if(show)tools++});const knowledge=renderKnowledge(query,active,rawQuery),empty=document.getElementById('skFilterEmpty'),result=document.getElementById('skFilterResult');if(empty)empty.hidden=tools+knowledge!==0;if(result)result.textContent=query?`${tools} ${tools===1?'App':'Apps'} und ${knowledge} ${knowledge===1?'Beitrag':'Beiträge'} angezeigt`:`${tools} ${tools===1?'App':'Apps'} angezeigt`;document.dispatchEvent(new CustomEvent('sk:cards-updated',{detail:{source:'filter',version:RELEASE}}))}
function resetFilter(){const input=document.getElementById('skToolSearch');if(input)input.value='';document.querySelectorAll('.sk-filter-button').forEach(button=>button.classList.toggle('active',button.dataset.filter==='ALLE'));applyFilter()}
async function loadIndex(){try{const [indexResponse,materialsResponse]=await Promise.all([fetch(new URL(`assets/search-index-v2-6-1-9.json?v=${RELEASE}`,root()),{cache:'no-store'}),fetch(new URL(`assets/materials.json?v=${RELEASE}`,root()),{cache:'no-store'})]);if(!indexResponse.ok)throw new Error(`Suchindex ${indexResponse.status}`);const indexData=await indexResponse.json();searchIndex=Array.isArray(indexData)?indexData:[];if(materialsResponse.ok){const materialData=await materialsResponse.json();materialCatalog=Array.isArray(materialData.materials)?materialData.materials:[]}}catch(error){console.warn('Der Suchindex konnte nicht vollständig geladen werden.',error);searchIndex=[];materialCatalog=[]}}
async function init(){if(!isStartPage())return;const panel=document.getElementById('skToolFilter');if(!panel)return;panel.querySelectorAll('.sk-filter-button').forEach(button=>button.addEventListener('click',()=>{panel.querySelectorAll('.sk-filter-button').forEach(item=>item.classList.remove('active'));button.classList.add('active');applyFilter()}));document.getElementById('skToolSearch')?.addEventListener('input',applyFilter);document.getElementById('skFilterReset')?.addEventListener('click',resetFilter);await loadIndex();applyFilter()}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init,{once:true});else init();
})();

/* === Modul: Mobile Startseitensuche === */
(()=>{'use strict';
function init(){if(document.body?.dataset.skPage!=='start')return;const panel=document.getElementById('skToolFilter'),button=document.getElementById('skFilterToggle'),content=document.getElementById('skFilterContent'),input=document.getElementById('skToolSearch'),results=document.getElementById('skKnowledgeResults');if(!panel||!button||!content)return;if(results&&!content.contains(results))content.append(results);const setExpanded=expanded=>{panel.classList.toggle('is-expanded',expanded);panel.classList.toggle('is-collapsed',!expanded);document.body.classList.toggle('pct-home-search-open',expanded);button.setAttribute('aria-expanded',String(expanded));button.setAttribute('aria-label',expanded?'Suche und Filter schließen':'Apps und Wissensbeiträge durchsuchen');content.hidden=!expanded;if(expanded)requestAnimationFrame(()=>input?.focus())};button.addEventListener('click',()=>setExpanded(button.getAttribute('aria-expanded')!=='true'));document.addEventListener('keydown',event=>{if(event.key==='Escape'&&button.getAttribute('aria-expanded')==='true'){setExpanded(false);button.focus()}});setExpanded(false)}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init,{once:true});else init();
})();

/* === Modul: Sortierung === */
(()=>{'use strict';
const SELECT_ID='skToolSort';let originalOrder=[];
const norm=window.SK_PCT_SHARED.sortText;
const host=()=>document.querySelector('.tools,.start-tools');
const cards=()=>{const grid=host();return grid?[...grid.querySelectorAll('a.card,a.tool-card')]:[]};
const category=card=>norm(card.querySelector('.sk-card-category,.eyebrow')?.textContent||'');
const title=card=>norm(card.querySelector('h1,h2,h3')?.textContent||'');
function captureOriginal(){cards().forEach(card=>{if(!originalOrder.includes(card))originalOrder.push(card)})}
function compareText(a,b,key,direction){const result=key(a).localeCompare(key(b),'de',{sensitivity:'base',numeric:true});if(result!==0)return direction==='asc'?result:-result;return originalOrder.indexOf(a)-originalOrder.indexOf(b)}
function sortCards(mode){const grid=host();if(!grid)return;captureOriginal();let ordered=[...cards()];if(mode==='category-asc')ordered.sort((a,b)=>compareText(a,b,category,'asc')||compareText(a,b,title,'asc'));if(mode==='category-desc')ordered.sort((a,b)=>compareText(a,b,category,'desc')||compareText(a,b,title,'asc'));if(mode==='title-asc')ordered.sort((a,b)=>compareText(a,b,title,'asc'));if(mode==='title-desc')ordered.sort((a,b)=>compareText(a,b,title,'desc'));if(mode==='default')ordered=[...originalOrder].filter(card=>card.isConnected&&grid.contains(card));ordered.forEach(card=>grid.append(card));document.dispatchEvent(new CustomEvent('sk:cards-sorted',{detail:{mode}}))}
function bind(){const select=document.getElementById(SELECT_ID);if(!select||select.dataset.bound)return;select.dataset.bound='true';select.addEventListener('change',()=>sortCards(select.value));document.getElementById('skFilterReset')?.addEventListener('click',()=>{select.value='default';sortCards('default')})}
function refresh(){captureOriginal();bind();const select=document.getElementById(SELECT_ID);if(select)sortCards(select.value)}
function init(){refresh();document.addEventListener('sk:cards-updated',refresh);document.addEventListener('sk:home-order-changed',()=>{originalOrder=cards()})}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init,{once:true});else init();
})();


/* === Modul: Navigation, Buttons und Icons === */
/* Gemeinsamer Adapter für PCT-Navigation und Bedienelemente. */
(()=>{'use strict';
const RELEASE='2.6.1.9-Beta';
const root=window.SK_PCT?.root||new URL('../',document.currentScript?.src||location.href);
const sprite=new URL('assets/pct-controls.svg',root).href;
const NAV_GRAPHICS=Object.freeze({
  'app-einheitendatenbank':'v2-6-1-9-app-einheitendatenbank.png',
  'nav-back':'v2-6-1-9-nav-back.png',
  'nav-home':'v2-6-1-9-nav-home.png'
});
const navGraphic=name=>{const file=NAV_GRAPHICS[name];if(!file)throw new Error(`Unbekannte Navigationsgrafik: ${name}`);return `<img class="pct-nav-graphic" src="${new URL(`assets/navigation-icons/${file}`,root).href}" alt="" aria-hidden="true" decoding="sync">`};
const icon=(name,small=false)=>`<svg class="pct-icon${small?' pct-icon--small':''}" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><use href="${sprite}#icon-${name}"></use></svg>`;
const normalized=value=>String(value||'').trim().toLocaleLowerCase('de-DE');
const graphicPrefix=(node,name)=>{if(!node||node.querySelector(':scope > .pct-nav-graphic'))return;node.dataset.pctGraphic=name;node.insertAdjacentHTML('afterbegin',navGraphic(name))};
const add=(node,...classes)=>node?.classList.add(...classes.filter(Boolean));
function iconOnly(node,name){if(!node||(node.dataset.pctIcon===name&&node.querySelector('.pct-icon')))return;node.dataset.pctIcon=name;node.innerHTML=icon(name)}
function prefix(node,name){if(!node||node.querySelector(':scope > .pct-icon'))return;node.dataset.pctIcon=name;node.insertAdjacentHTML('afterbegin',icon(name,true))}
function headerControls(){document.querySelectorAll('.sk-global-header').forEach(header=>{const inner=header.querySelector('.sk-header-inner'),home=inner?.querySelector('.sk-header-home');if(!inner||!home||inner.querySelector('.pct-header-actions'))return;const actions=document.createElement('div');actions.className='pct-header-actions';const favorite=document.querySelector('.sk-favorites-trigger');const back=document.createElement('button');back.type='button';back.className='pct-control pct-control--quiet pct-control--back';back.setAttribute('aria-label','Zurück');back.innerHTML=`${navGraphic('nav-back')}<span class="pct-label">Zurück</span>`;back.addEventListener('click',()=>{try{if(document.referrer&&new URL(document.referrer).origin===location.origin&&history.length>1){history.back();return}}catch{}location.href=root.href});home.href=root.href;home.setAttribute('aria-label','Zur Startseite');home.textContent='';add(home,'pct-control','pct-control--quiet','pct-control--home');home.innerHTML=`${navGraphic('nav-home')}<span class="pct-label">Startseite</span>`;home.parentNode.insertBefore(actions,home);if(favorite)actions.append(favorite);actions.append(back,home)})}
function searches(){document.querySelectorAll('input[type="search"]').forEach(input=>{if(input.parentElement?.classList.contains('pct-search-shell'))return;const shell=document.createElement('span');shell.className='pct-search-shell';input.parentNode.insertBefore(shell,input);shell.append(input);shell.insertAdjacentHTML('afterbegin',icon('search'))})}
function selects(){document.querySelectorAll('select').forEach(select=>select.classList.add('pct-select'))}
function favorites(){document.querySelectorAll('.sk-favorite-button,.unit-favorite-button,.sk-favorite-remove').forEach(button=>{add(button,'pct-control','pct-control--icon','pct-control--favorite');iconOnly(button,'star')});document.querySelectorAll('.sk-favorites-trigger').forEach(button=>{add(button,'pct-control','pct-control--icon','pct-control--favorite');const slot=button.querySelector('.sk-trigger-star');if(slot){if(!slot.querySelector('.pct-icon'))slot.innerHTML=icon('star')}else prefix(button,'star')})}
function drawerControls(){document.querySelectorAll('.sk-favorites-close').forEach(button=>{add(button,'pct-control','pct-control--icon');iconOnly(button,'close')})}
function signControls(){document.querySelectorAll('.sign,.analog-sign-button').forEach(button=>{add(button,'pct-control','pct-control--icon','pct-control--sign');if(button.querySelector('.pct-sign-glyph'))return;button.dataset.pctIcon='sign';button.innerHTML='<span class="pct-sign-glyph" aria-hidden="true">±</span>';button.title=button.title||'Vorzeichen wechseln'})}
function resets(){document.querySelectorAll('button,.sk-filter-reset,.material-reset').forEach(button=>{const value=normalized(button.textContent);if(!(button.matches('.sk-filter-reset,.material-reset,#unitReset')||value.includes('zurücksetzen')||value==='neue messstelle'))return;add(button,'pct-control','pct-control--reset');prefix(button,'reset')})}
function tabs(){document.querySelectorAll('.sk-filter-button,.material-filter,.analog-tab').forEach(button=>button.classList.add('pct-tab'))}
function toggles(){document.querySelectorAll('.knowledge-compact-toggle').forEach(button=>button.classList.add('pct-toggle-control'))}
function collapsibles(){const buttons='.sk-filter-toggle,.knowledge-manufacturer-toggle,.material-card-toggle';document.querySelectorAll(buttons).forEach(button=>button.classList.add('pct-collapse-control'));document.querySelectorAll('.sk-filter-toggle-icon,.knowledge-manufacturer-chevron,.material-toggle-icon').forEach(slot=>{slot.classList.add('pct-chevron-slot');if(!slot.querySelector('.pct-icon'))slot.innerHTML=icon('chevron')})}
async function copy(value){if(navigator.clipboard?.writeText){await navigator.clipboard.writeText(value);return}const area=document.createElement('textarea');area.value=value;area.readOnly=true;area.style.cssText='position:fixed;opacity:0';document.body.append(area);area.select();document.execCommand('copy');area.remove()}
function addCopy(target){const host=target.closest('.calc-value-card,.analog-value-card,.voltage-result,.result')||target.parentElement;if(!host||host.querySelector(':scope > .pct-copy-button'))return;host.classList.add('pct-copy-host');const button=document.createElement('button');button.type='button';button.className='pct-copy-button pct-control pct-control--icon pct-control--copy';button.setAttribute('aria-label','Wert kopieren');button.title='Wert kopieren';button.innerHTML=icon('copy');button.addEventListener('click',async()=>{const value=(target.textContent||'').trim();if(!value||value==='–')return;try{await copy(value);button.classList.add('is-success');button.innerHTML=icon('check');button.setAttribute('aria-label','Kopiert');button.title='Kopiert';setTimeout(()=>{button.classList.remove('is-success');button.innerHTML=icon('copy');button.setAttribute('aria-label','Wert kopieren');button.title='Wert kopieren'},1400)}catch(error){console.warn('Kopieren nicht möglich.',error)}});host.append(button)}
function copyControls(){document.querySelectorAll('.result strong[id],.calc-value-card strong[id],.analog-value-card strong[id],.voltage-result strong[id]').forEach(addCopy);document.querySelectorAll('button').forEach(button=>{if(normalized(button.textContent).includes('kopier')){add(button,'pct-control','pct-control--copy');prefix(button,'copy')}})}
function message(node,type){if(!node||node.querySelector(':scope > .pct-message-icon'))return;node.classList.add('pct-message',`pct-message--${type}`);const slot=document.createElement('span');slot.className='pct-message-icon';slot.innerHTML=icon(type==='warning'?'warning':type==='success'?'check':'info');node.prepend(slot)}
function messages(){document.querySelectorAll('.kb-callout.warning,.kb-callout.danger,.material-global-safety,.material-safety,.material-load-error,.calculation-error,[role="alert"]').forEach(node=>message(node,'warning'));document.querySelectorAll('.kb-callout:not(.warning):not(.danger):not(.success),.kb-source,.unit-model-note,.calc-notice,.knowledge-standard-note,.material-data-note,.material-search-help').forEach(node=>message(node,'info'));document.querySelectorAll('.kb-callout.success').forEach(node=>message(node,'success'))}
function infoControls(){document.querySelectorAll('.analog-card-info summary').forEach(summary=>{summary.classList.add('pct-info-control');prefix(summary,'info')})}
function actionControls(){document.querySelectorAll('.toolbar button,.actions button,button.primary,button.secondary,.sk-unit-database-button,.knowledge-proposal-link,.knowledge-view-back,.pct-home-done').forEach(button=>button.classList.add('pct-control'));document.querySelectorAll('.toolbar button,.photo button,button.primary,button.secondary,.sk-unit-database-button,.knowledge-proposal-link,.knowledge-view-back,.pct-home-done').forEach(button=>{const value=normalized(button.textContent);if(value.includes('pdf')||value.includes('druck'))prefix(button,'print');if(value.includes('lösch')){add(button,'pct-control','pct-control--danger');prefix(button,'trash')}if(button.matches('.sk-unit-database-button'))graphicPrefix(button,'app-einheitendatenbank');if(button.matches('.knowledge-proposal-link'))prefix(button,'download');if(button.matches('.knowledge-view-back'))graphicPrefix(button,'nav-back');if(button.matches('button.primary'))prefix(button,'calculate');if(button.matches('button.secondary'))prefix(button,'reset');if(button.matches('.pct-home-done'))prefix(button,'done')})}
function apply(){headerControls();searches();selects();favorites();drawerControls();signControls();resets();tabs();toggles();collapsibles();copyControls();messages();infoControls();actionControls();document.documentElement.dataset.pctControls=RELEASE}
let queued=false;const schedule=()=>{if(queued)return;queued=true;queueMicrotask(()=>{queued=false;apply()})};
function init(){apply();new MutationObserver(schedule).observe(document.body,{subtree:true,childList:true});document.addEventListener('sk:cards-updated',schedule);document.addEventListener('sk:cards-sorted',schedule)}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init,{once:true});else init();
})();
