/* SK PCT Tools 2.6.8.0-Beta — zentrale Laufzeit: Layout, Version, Favoriten, Suche, Sortierung, Navigation und Controls. */

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
/* SK PCT Tools 2.6.8.0-Beta — viewportfeste Drag-Ebene, stabiler Rasterplatzhalter und headerneutrales Sortier-Dock. */
(()=>{'use strict';
const RELEASE='2.6.8.0-Beta';
const ORDER_KEY='skPctHomeOrderV1';
const LONG_PRESS_TOUCH=420;
const LONG_PRESS_MOUSE=300;
const MOVE_TOLERANCE_TOUCH=12;
const MOVE_TOLERANCE_MOUSE=6;
const byId=id=>document.getElementById(id);
const {readJSON:read,writeJSON:write}=window.SK_PCT_SHARED;
const cardTitle=card=>card?.querySelector('h2')?.textContent?.trim()||'App';
const cards=grid=>[...grid.querySelectorAll(':scope > .sk-home-app')];
const clamp=(value,min,max)=>Math.max(min,Math.min(max,value));
const sameOrder=(a,b)=>a.length===b.length&&a.every((id,index)=>id===b[index]);

function boot(){
  const grid=byId('pctHomeGrid');
  if(!grid||document.body?.dataset.skHome!=='ios')return;

  const editActions=document.querySelector('.pct-home-edit-actions');
  const doneButton=byId('pctHomeDone');
  const resetButton=byId('pctHomeReset');
  const undoButton=byId('pctHomeUndo');
  const redoButton=byId('pctHomeRedo');
  const announcement=byId('pctHomeAnnouncement');
  const defaultOrder=cards(grid).map(card=>card.dataset.appId);
  const validIds=new Set(defaultOrder);
  const state={
    mode:'navigate',phase:'idle',pointerId:null,pointerType:'',card:null,timer:0,
    startX:0,startY:0,lastX:0,lastY:0,offsetX:0,offsetY:0,
    orderBefore:[],placeholder:null,dragLayer:null,overlay:null,swallowClickCard:null,
    autoScrollFrame:0,autoScrollVelocity:0,history:[],historyIndex:-1
  };

  const announce=text=>{
    if(!announcement)return;
    announcement.textContent='';
    requestAnimationFrame(()=>{announcement.textContent=text});
  };
  const currentOrder=()=>cards(grid).map(card=>card.dataset.appId);
  const sanitizedOrder=value=>{
    if(!Array.isArray(value))return [...defaultOrder];
    const seen=new Set();
    const known=value.filter(id=>validIds.has(id)&&!seen.has(id)&&seen.add(id));
    return [...known,...defaultOrder.filter(id=>!seen.has(id))];
  };
  const notifyOrder=()=>document.dispatchEvent(new CustomEvent('sk:home-order-changed',{detail:{order:currentOrder(),version:RELEASE}}));
  function applyOrder(value,{notify=true}={}){
    const order=sanitizedOrder(value);
    const lookup=new Map(cards(grid).map(card=>[card.dataset.appId,card]));
    order.forEach(id=>{const card=lookup.get(id);if(card){grid.append(card);lookup.delete(id)}});
    lookup.forEach(card=>grid.append(card));
    if(notify)notifyOrder();
    return currentOrder();
  }
  function saveOrder(){
    const order=currentOrder();
    const stored=write(ORDER_KEY,order);
    notifyOrder();
    if(!stored)announce('Die Reihenfolge konnte auf diesem Gerät nicht gespeichert werden.');
    return stored;
  }
  function updateHistoryButtons(){
    if(undoButton)undoButton.disabled=state.historyIndex<=0||state.phase==='dragging';
    if(redoButton)redoButton.disabled=state.historyIndex<0||state.historyIndex>=state.history.length-1||state.phase==='dragging';
  }
  function pushHistory(order=currentOrder()){
    const clean=sanitizedOrder(order);
    const active=state.history[state.historyIndex];
    if(active&&sameOrder(active,clean)){updateHistoryButtons();return}
    state.history=state.history.slice(0,state.historyIndex+1);
    state.history.push([...clean]);
    state.historyIndex=state.history.length-1;
    updateHistoryButtons();
  }

  applyOrder(read(ORDER_KEY,defaultOrder));
  pushHistory(currentOrder());
  grid.dataset.reorderEngine='pointer-overlay-v3';
  cards(grid).forEach(card=>{
    card.setAttribute('draggable','false');
    card.setAttribute('aria-grabbed','false');
    card.querySelectorAll('img').forEach(image=>image.setAttribute('draggable','false'));
  });

  function clearTimer(){if(state.timer){clearTimeout(state.timer);state.timer=0}}
  function stopAutoScroll(){
    if(state.autoScrollFrame)cancelAnimationFrame(state.autoScrollFrame);
    state.autoScrollFrame=0;state.autoScrollVelocity=0;
  }
  function scrollHost(){
    const candidates=[grid,grid.closest('.pct-home-screen'),grid.closest('.shell'),document.scrollingElement];
    return candidates.find(node=>node&&node.scrollHeight>node.clientHeight+1)||document.scrollingElement;
  }
  function autoScrollStep(){
    state.autoScrollFrame=0;
    if(state.phase!=='dragging'||!state.autoScrollVelocity)return;
    const host=scrollHost();let changed=false;
    if(host===document.scrollingElement){const before=window.scrollY;window.scrollBy(0,state.autoScrollVelocity);changed=Math.abs(window.scrollY-before)>.25}
    else{const before=host.scrollTop;host.scrollTop+=state.autoScrollVelocity;changed=Math.abs(host.scrollTop-before)>.25}
    moveOverlay(state.lastX,state.lastY);if(changed)reorderAt(state.lastX,state.lastY);
    state.autoScrollFrame=requestAnimationFrame(autoScrollStep);
  }
  function updateAutoScroll(y){
    const safe=dragSafeBounds(0,0),headerBottom=safe.headerBottom-4,bottom=safe.bottom;
    const edge=Math.min(96,Math.max(54,innerHeight*.12));
    let velocity=0;
    if(y<headerBottom+edge*.45)velocity=-Math.ceil((headerBottom+edge*.45-y)/edge*12);
    else if(y>bottom-edge)velocity=Math.ceil((y-(bottom-edge))/edge*12);
    state.autoScrollVelocity=velocity;
    if(velocity&&!state.autoScrollFrame)state.autoScrollFrame=requestAnimationFrame(autoScrollStep);
    if(!velocity)stopAutoScroll();
  }
  function syncMode(){
    const sorting=state.mode==='sort';
    if(editActions){editActions.hidden=!sorting;editActions.setAttribute('aria-hidden',String(!sorting))}
    document.body.classList.toggle('pct-home-editing',sorting);
    document.body.classList.toggle('pct-home-dragging',state.phase==='dragging');
    grid.dataset.mode=state.mode;
    grid.setAttribute('aria-label',sorting?'PCT Apps anordnen. Navigation ist gesperrt. Ziehen oder mit Pfeiltasten verschieben. Rückgängig, Wiederholen oder Fertig verwenden.':'PCT Apps');
    cards(grid).forEach(card=>card.setAttribute('aria-grabbed',String(state.phase==='dragging'&&card===state.card)));
    updateHistoryButtons();
  }
  function enterSort(reason='manual'){
    if(state.mode==='sort')return;
    state.mode='sort';syncMode();
    if(reason!=='longpress')announce('Sortiermodus aktiv. Nur die Iconkörper wackeln. Antippen öffnet jetzt keine App.');
  }
  function exitSort({message='Anordnung gespeichert.',focusCard=null}={}){
    clearTimer();stopAutoScroll();state.mode='navigate';syncMode();
    if(focusCard?.isConnected)focusCard.focus({preventScroll:true});
    announce(message);
  }
  function resetPress(){
    clearTimer();
    if(state.phase==='pressing')state.phase='idle';
    if(state.phase==='idle'){state.pointerId=null;state.pointerType='';state.card=null}
  }
  function makePlaceholder(card,rect){
    const iconRect=card.querySelector('.sk-app-icon-wrapper,.sk-home-icon')?.getBoundingClientRect();
    const placeholder=document.createElement('div');
    placeholder.className='pct-home-drop-placeholder';
    placeholder.setAttribute('aria-hidden','true');
    placeholder.style.width=`${rect.width}px`;
    placeholder.style.height=`${rect.height}px`;
    placeholder.style.setProperty('--pct-placeholder-icon-width',`${iconRect?.width||64}px`);
    placeholder.style.setProperty('--pct-placeholder-icon-height',`${iconRect?.height||64}px`);
    placeholder.innerHTML='<span class="pct-home-placeholder-icon"></span><span class="pct-home-placeholder-label">Position</span>';
    card.before(placeholder);
    state.placeholder=placeholder;
  }
  function makeOverlay(card,x,y){
    const wrapper=card.querySelector('.sk-app-icon-wrapper,.sk-home-icon');
    const rect=(wrapper||card).getBoundingClientRect();
    const inside=x>=rect.left&&x<=rect.right&&y>=rect.top&&y<=rect.bottom;
    state.offsetX=inside?clamp(x-rect.left,0,rect.width):rect.width/2;
    state.offsetY=inside?clamp(y-rect.top,0,rect.height):rect.height/2;
    const layer=document.createElement('div');
    layer.className='pct-home-drag-layer';layer.setAttribute('aria-hidden','true');
    const overlay=document.createElement('div');
    overlay.className='pct-home-drag-overlay';
    overlay.style.width=`${rect.width}px`;overlay.style.height=`${rect.height}px`;
    const visual=(wrapper||card).cloneNode(true);
    visual.querySelectorAll('button').forEach(button=>button.remove());
    visual.removeAttribute('id');visual.removeAttribute('href');
    overlay.append(visual);layer.append(overlay);document.body.append(layer);
    state.dragLayer=layer;state.overlay=overlay;moveOverlay(x,y);
  }
  function dragSafeBounds(width,height){
    const headerBottom=(document.querySelector('.pct-home-head')?.getBoundingClientRect().bottom||0)+4;
    let right=innerWidth-4,bottom=innerHeight-4;
    if(editActions&&!editActions.hidden){
      const dock=editActions.getBoundingClientRect();
      if(dock.width>=dock.height)bottom=Math.min(bottom,dock.top-4);
      else right=Math.min(right,dock.left-4);
    }
    return{headerBottom,maxLeft:Math.max(4,right-width),maxTop:Math.max(headerBottom,bottom-height),bottom};
  }
  function moveOverlay(x,y){
    if(!state.overlay)return;
    const width=state.overlay.offsetWidth||72,height=state.overlay.offsetHeight||72;
    const bounds=dragSafeBounds(width,height);
    const left=clamp(x-state.offsetX,4,bounds.maxLeft);
    const top=clamp(y-state.offsetY,bounds.headerBottom,bounds.maxTop);
    state.overlay.style.transform=`translate3d(${Math.round(left)}px,${Math.round(top)}px,0)`;
  }
  function beginDrag(card,{pointerId,pointerType,x,y}){
    clearTimer();
    if(!card?.isConnected||state.phase==='dragging')return;
    enterSort('longpress');
    const cardRect=card.getBoundingClientRect();
    state.phase='dragging';state.pointerId=pointerId;state.pointerType=pointerType||'mouse';state.card=card;
    state.startX=state.lastX=x;state.startY=state.lastY=y;state.orderBefore=currentOrder();state.swallowClickCard=null;
    makePlaceholder(card,cardRect);makeOverlay(card,x,y);
    card.classList.add('is-dragging');card.setAttribute('aria-grabbed','true');card.remove();
    try{grid.setPointerCapture?.(pointerId)}catch{}
    navigator.vibrate?.(8);syncMode();
    announce(`${cardTitle(card)} aufgenommen. Freie Drag-Ebene aktiv; die markierte Rasterposition bleibt stabil.`);
  }
  function nearestCard(x,y){
    const available=cards(grid).filter(card=>!card.hidden);
    let best=null,bestDistance=Infinity;
    available.forEach(card=>{
      const rect=card.getBoundingClientRect();
      const dx=x-(rect.left+rect.width/2),dy=y-(rect.top+rect.height/2),distance=dx*dx+dy*dy;
      if(distance<bestDistance){bestDistance=distance;best=card}
    });
    return best;
  }
  function targetCardAt(x,y){
    const fromPoint=document.elementsFromPoint?.(x,y)||[];
    for(const element of fromPoint){
      const card=element.closest?.('.sk-home-app');
      if(card&&card.parentElement===grid&&!card.hidden)return card;
    }
    return nearestCard(x,y);
  }
  function reorderAt(x,y){
    if(state.phase!=='dragging'||!state.placeholder)return;
    const headerBottom=document.querySelector('.pct-home-head')?.getBoundingClientRect().bottom||0;
    if(y<headerBottom)return;
    const target=targetCardAt(x,y);
    if(!target)return;
    const rect=target.getBoundingClientRect();
    const sameRow=Math.abs(y-(rect.top+rect.height/2))<=Math.min(rect.height*.48,64);
    const after=sameRow?x>rect.left+rect.width/2:y>rect.top+rect.height/2;
    const reference=after?target.nextSibling:target;
    if(reference===state.placeholder||(!after&&state.placeholder.nextSibling===target)||(after&&target.nextSibling===state.placeholder))return;
    grid.insertBefore(state.placeholder,reference);
    state.placeholder.dataset.target=target.dataset.appId||'';
    navigator.vibrate?.(3);
  }
  function releaseCapture(pointerId){try{if(grid.hasPointerCapture?.(pointerId))grid.releasePointerCapture(pointerId)}catch{}}
  function reinsertDraggedCard(){
    const card=state.card,placeholder=state.placeholder;
    if(card){
      if(placeholder?.isConnected)placeholder.replaceWith(card);else grid.append(card);
      card.classList.remove('is-dragging');card.setAttribute('aria-grabbed','false');
    }else placeholder?.remove();
    state.placeholder=null;
    return card;
  }
  function cleanDragVisuals(){
    const pointerId=state.pointerId;
    state.phase='idle';stopAutoScroll();state.dragLayer?.remove();state.dragLayer=null;state.overlay=null;
    const card=reinsertDraggedCard();releaseCapture(pointerId);
    state.pointerId=null;state.pointerType='';state.card=null;syncMode();return card;
  }
  function commitDrag(pointerId=null){
    if(state.phase!=='dragging'||(pointerId!==null&&state.pointerId!==pointerId))return false;
    const title=cardTitle(state.card),before=[...state.orderBefore],card=cleanDragVisuals(),after=currentOrder();
    const moved=!sameOrder(before,after);
    if(moved)pushHistory(after);saveOrder();state.swallowClickCard=card;
    exitSort({message:moved?`${title} abgelegt und gespeichert. Normaler Navigationsmodus ist wieder aktiv.`:`${title} nicht verschoben. Normaler Navigationsmodus ist wieder aktiv.`,focusCard:card});
    return true;
  }
  function cancelDrag(reason='Sortierung abgebrochen.'){
    if(state.phase!=='dragging')return false;
    const card=state.card,before=[...state.orderBefore];cleanDragVisuals();applyOrder(before);state.swallowClickCard=card;
    exitSort({message:`${reason} Ausgangsreihenfolge wiederhergestellt; Navigation ist aktiv.`,focusCard:card});return true;
  }
  function cancelInteraction(reason){
    if(state.phase==='dragging')return cancelDrag(reason);
    resetPress();if(state.mode==='sort')exitSort({message:`${reason} Normaler Navigationsmodus ist wieder aktiv.`});return false;
  }
  function historyStep(delta){
    if(state.phase==='dragging')return;
    const next=clamp(state.historyIndex+delta,0,state.history.length-1);
    if(next===state.historyIndex)return;
    state.historyIndex=next;applyOrder(state.history[next]);saveOrder();updateHistoryButtons();
    announce(delta<0?'Letzte Anordnung rückgängig gemacht.':'Anordnung wiederholt.');
  }

  doneButton?.addEventListener('click',()=>{if(state.phase==='dragging')commitDrag(state.pointerId);else exitSort()});
  undoButton?.addEventListener('click',()=>historyStep(-1));
  redoButton?.addEventListener('click',()=>historyStep(1));
  resetButton?.addEventListener('click',()=>{
    if(state.phase==='dragging')cancelDrag('Laufendes Verschieben beendet.');
    localStorage.removeItem(ORDER_KEY);applyOrder(defaultOrder);pushHistory(defaultOrder);saveOrder();
    const select=byId('skToolSort');if(select)select.value='default';
    exitSort({message:'Standardreihenfolge wiederhergestellt. Normaler Navigationsmodus ist aktiv.'});
  });
  byId('skToolSort')?.addEventListener('change',event=>{if(event.target.value!=='default')cancelInteraction('Manuelle Sortierung beendet.')});

  grid.addEventListener('pointerdown',event=>{
    if(event.isPrimary===false||event.button>0)return;
    const card=event.target.closest('.sk-home-app');
    if(!card||card.parentElement!==grid||event.target.closest('button,input,select,textarea'))return;
    if(state.swallowClickCard===card)state.swallowClickCard=null;
    if(state.phase==='dragging')cancelDrag('Vorheriges Verschieben abgebrochen.');
    clearTimer();
    const point={pointerId:event.pointerId,pointerType:event.pointerType||'mouse',x:event.clientX,y:event.clientY};
    if(state.mode==='sort'){if(event.cancelable)event.preventDefault();beginDrag(card,point);return}
    state.phase='pressing';state.pointerId=event.pointerId;state.pointerType=point.pointerType;state.card=card;
    state.startX=state.lastX=point.x;state.startY=state.lastY=point.y;
    const delay=point.pointerType==='mouse'?LONG_PRESS_MOUSE:LONG_PRESS_TOUCH;
    state.timer=setTimeout(()=>{state.timer=0;if(state.phase==='pressing'&&state.pointerId===point.pointerId)beginDrag(card,{...point,x:state.lastX,y:state.lastY})},delay);
  });
  document.addEventListener('pointermove',event=>{
    if(state.pointerId!==event.pointerId)return;
    state.lastX=event.clientX;state.lastY=event.clientY;
    if(state.phase==='pressing'){
      const tolerance=state.pointerType==='mouse'?MOVE_TOLERANCE_MOUSE:MOVE_TOLERANCE_TOUCH;
      if(Math.hypot(event.clientX-state.startX,event.clientY-state.startY)>tolerance)resetPress();
      return;
    }
    if(state.phase!=='dragging')return;
    if(event.cancelable)event.preventDefault();moveOverlay(event.clientX,event.clientY);reorderAt(event.clientX,event.clientY);updateAutoScroll(event.clientY);
  },{passive:false});
  document.addEventListener('pointerup',event=>{
    if(state.pointerId!==event.pointerId)return;
    if(state.phase==='pressing'){resetPress();return}
    commitDrag(event.pointerId);
  });
  document.addEventListener('pointercancel',event=>{
    if(state.pointerId!==event.pointerId)return;
    if(state.phase==='pressing'){resetPress();return}
    cancelDrag('Sortierung durch das Gerät abgebrochen.');
  });
  grid.addEventListener('lostpointercapture',event=>{if(state.phase==='dragging'&&state.pointerId===event.pointerId)cancelDrag('Zeigerkontakt verloren.')},true);

  grid.addEventListener('click',event=>{
    const card=event.target.closest('.sk-home-app');
    if(!card||event.target.closest('button'))return;
    const block=state.mode==='sort'||state.phase==='dragging'||state.swallowClickCard===card;
    if(!block)return;
    event.preventDefault();event.stopImmediatePropagation();if(state.swallowClickCard===card)state.swallowClickCard=null;
  },true);
  grid.addEventListener('contextmenu',event=>{if(state.mode==='sort'||state.phase==='pressing'||state.phase==='dragging')event.preventDefault()});
  grid.addEventListener('keydown',event=>{
    const card=event.target.closest('.sk-home-app');if(!card)return;
    if(state.mode==='navigate'&&event.key===' '){event.preventDefault();enterSort('keyboard');card.focus({preventScroll:true});return}
    if(state.mode!=='sort')return;
    if(event.key==='Enter'||event.key===' '){event.preventDefault();return}
    if(!['ArrowLeft','ArrowRight','ArrowUp','ArrowDown'].includes(event.key))return;
    const visible=cards(grid).filter(item=>!item.hidden),index=visible.indexOf(card);if(index<0)return;
    const firstTop=Math.round(visible[0].getBoundingClientRect().top);
    const columns=Math.max(1,visible.filter(item=>Math.round(item.getBoundingClientRect().top)===firstTop).length);
    const delta={ArrowLeft:-1,ArrowRight:1,ArrowUp:-columns,ArrowDown:columns}[event.key];
    const next=clamp(index+delta,0,visible.length-1);if(next===index)return;
    event.preventDefault();const target=visible[next];grid.insertBefore(card,delta>0?target.nextSibling:target);
    pushHistory(currentOrder());saveOrder();card.focus({preventScroll:true});announce(`${cardTitle(card)} Position ${next+1} von ${visible.length}. Sortiermodus bleibt aktiv.`);
  });
  document.addEventListener('keydown',event=>{
    if((event.ctrlKey||event.metaKey)&&event.key.toLowerCase()==='z'&&state.mode==='sort'){
      event.preventDefault();historyStep(event.shiftKey?1:-1);return;
    }
    if(event.key!=='Escape')return;
    if(state.phase==='dragging'){event.preventDefault();cancelDrag('Sortierung mit Escape abgebrochen.');return}
    if(state.mode==='sort'){event.preventDefault();exitSort({message:'Sortiermodus beendet. Normaler Navigationsmodus ist aktiv.'})}
  });

  const suspend=()=>cancelInteraction('Interaktion unterbrochen.');
  window.addEventListener('blur',suspend);window.addEventListener('pagehide',suspend);
  document.addEventListener('visibilitychange',()=>{if(document.hidden)suspend()});
  window.addEventListener('resize',()=>{if(state.phase==='dragging')moveOverlay(state.lastX,state.lastY)});
  window.addEventListener('storage',event=>{
    if(event.key!==ORDER_KEY||state.mode!=='navigate'||state.phase!=='idle')return;
    const order=applyOrder(read(ORDER_KEY,defaultOrder));pushHistory(order);announce('Reihenfolge wurde aus einem anderen Fenster aktualisiert.');
  });

  syncMode();
}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',boot,{once:true});else boot();
})();


/* === Modul: Basis, Layout und PWA === */
/* SK PCT Tools 2.6.8.0-Beta — gemeinsame Laufzeitmodule: Basis, Favoriten, Suche und Sortierung. */
/* === app.js === */
(()=>{'use strict';
const RELEASE='2.6.8.0-Beta';
const DISPLAY_RELEASE='2.6.8.0-Beta';
const scriptUrl=document.currentScript?.src||'';
const root=scriptUrl?new URL('../',scriptUrl):new URL('./',location.href);
window.SK_PCT=Object.freeze({version:RELEASE,channel:'beta',name:'SK PCT Tools',root,utils:window.SK_PCT_SHARED});
window.$=id=>document.getElementById(id);
window.num=value=>Number.parseFloat(String(value).replace(',','.'));
window.de=(value,digits=3)=>{if(!Number.isFinite(value))return'–';const absolute=Math.abs(value),maximum=absolute!==0&&absolute<0.01?Math.max(digits,6):digits;return value.toLocaleString('de-DE',{minimumFractionDigits:0,maximumFractionDigits:maximum,useGrouping:true})};
function buildSharedLayout(){
 const header=document.querySelector('[data-sk-shared-header]');
 if(header&&!header.firstElementChild)header.innerHTML=`<div class="sk-header-inner"><div class="sk-logo-version-stack"><img alt="SK PCT Tools" class="logo sk-global-logo sk-header-logo" src="${new URL(`assets/header-logo-simple.png?v=${RELEASE}`,root).href}"></div><span aria-label="Aktuelle Version ${DISPLAY_RELEASE} · Tool by S.K." class="sk-header-release-module pct-release-module"><img class="pct-release-module-skin" src="${new URL(`assets/release-module-v2-6-8-0.png?v=${RELEASE}`,root).href}" alt="" aria-hidden="true" decoding="sync"><span class="pct-release-module-copy"><span class="sk-release-number">V${DISPLAY_RELEASE}</span><span class="sk-release-credit">Tool by S.K.</span></span></span><a aria-label="Zur Startseite" class="home sk-header-home" href="${root.href}">← Startseite</a></div>`;
 document.querySelectorAll('[data-sk-shared-footer]').forEach(footer=>footer.textContent='SK PCT Tools · Simon Kiesler · Offline verfügbar');
}
function syncVersion(){document.querySelectorAll('.sk-release-number').forEach(node=>node.textContent=`V${DISPLAY_RELEASE}`);document.querySelectorAll('.badge').forEach(node=>{const text=(node.textContent||'').trim();if(/^Version\s+/i.test(text))node.textContent=`Version ${DISPLAY_RELEASE}`})}
function fitReleaseModules(){document.querySelectorAll('.pct-release-module').forEach(module=>{const number=module.querySelector('.sk-release-number');if(!number)return;number.style.removeProperty('font-size');const available=Math.max(1,module.clientWidth-24),width=number.scrollWidth,base=Number.parseFloat(getComputedStyle(number).fontSize)||10,minFont=number.textContent.trim()===`V${DISPLAY_RELEASE}`?10:7;if(width>available)number.style.fontSize=`${Math.max(minFont,base*available/width).toFixed(2)}px`})}
let releaseFitQueued=false;function scheduleReleaseFit(){if(releaseFitQueued)return;releaseFitQueued=true;requestAnimationFrame(()=>{releaseFitQueued=false;fitReleaseModules()})}
function addSignControls(){if(document.body?.dataset.signControls!=='true')return;document.querySelectorAll('input[type=number]').forEach(input=>{if(input.dataset.s)return;input.dataset.s='1';const wrapper=document.createElement('div');wrapper.className='number';input.parentNode.insertBefore(wrapper,input);wrapper.append(input);const button=document.createElement('button');button.type='button';button.className='sign';button.textContent='±';button.setAttribute('aria-label','Vorzeichen wechseln');button.addEventListener('click',()=>{const value=window.num(input.value);input.value=Number.isFinite(value)?(value===0?0:-value):'-';input.dispatchEvent(new Event('input',{bubbles:true}));input.dispatchEvent(new Event('change',{bubbles:true}))});wrapper.append(button)})}
function registerWorker(){if(!('serviceWorker' in navigator))return;const worker=new URL(`service-worker.js?release=${encodeURIComponent(RELEASE)}`,root),reloadKey=`skPctReloaded:${RELEASE}`,hadController=Boolean(navigator.serviceWorker.controller);navigator.serviceWorker.addEventListener('controllerchange',()=>{if(!hadController)return;try{if(sessionStorage.getItem(reloadKey))return;sessionStorage.setItem(reloadKey,'1');location.reload()}catch{location.reload()}});navigator.serviceWorker.register(worker,{scope:root.pathname,updateViaCache:'none'}).then(registration=>{const activate=()=>registration.waiting?.postMessage({type:'SKIP_WAITING'});activate();registration.addEventListener('updatefound',()=>{const installing=registration.installing;installing?.addEventListener('statechange',()=>{if(installing.state==='installed')activate()})});return registration.update()}).catch(error=>console.warn('Service Worker konnte nicht registriert werden.',error));}
function init(){buildSharedLayout();syncVersion();fitReleaseModules();addSignControls();registerWorker();window.addEventListener('resize',scheduleReleaseFit,{passive:true})}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init,{once:true});else init();
})();

/* === Modul: Favoriten === */
/* V2.6.8.0-Beta: Favoriten als reguläre Unteransicht innerhalb des verbindlichen App-Rahmens. */
(()=>{'use strict';
const KEY='skPctToolsFavoritesV2';
const PATH='M12 2.75l2.82 5.72 6.31.92-4.57 4.45 1.08 6.29L12 17.16l-5.64 2.97 1.08-6.29-4.57-4.45 6.31-.92L12 2.75z';
const esc=window.SK_PCT_SHARED.escapeHTML;
const svg=on=>`<svg class="sk-star-svg" viewBox="0 0 24 24" aria-hidden="true"><path d="${PATH}"${on?' class="sk-star-fill"':''}></path></svg>`;
const load=()=>{const value=window.SK_PCT_SHARED.readJSON(KEY,[]);return Array.isArray(value)?value:[]};
const save=value=>window.SK_PCT_SHARED.writeJSON(KEY,value);
const cardUrl=card=>{try{return new URL(card.getAttribute('href')||'',location.href).href}catch{return card.getAttribute('href')||''}};
const info=card=>({url:cardUrl(card),title:card.querySelector('h1,h2,h3')?.textContent.trim()||'Favorit',description:card.querySelector('p')?.textContent.trim()||'',category:card.querySelector('.sk-card-category,.eyebrow')?.textContent.trim()||card.dataset.category||'FAVORIT',external:card.target==='_blank',icon:card.querySelector('.sk-home-icon img,.knowledge-home-icon img')?.src||''});
const FAVORITE_ICONS=Object.freeze({'/analogsignal/':'app-analogsignal','/pf-rechner/':'app-pf-rechner','/pt-rechner/':'app-pt-rechner','/einheitenrechner/':'app-einheitenrechner','/einheitendatenbank/':'app-einheitendatenbank','/werkstoffdatenbank/':'app-werkstoffdatenbank','/wissensdatenbank/':'app-wissensdatenbank','/spannungsfall-rechner/':'app-spannungsfall','/siemens-analogwert-rechner/':'app-siemens-rohwert','/wissensdatenbank/air-torque-antrieb-drehrichtung/':'knowledge-air-torque-antrieb-drehrichtung','/wissensdatenbank/endress-hauser-promass-einbaulage/':'knowledge-endress-hauser-promass-einbaulage','/wissensdatenbank/endress-hauser-micropilot-grundlagen-radar-fuellstandmessung/':'knowledge-eh-micropilot-radar-grundlagen','/wissensdatenbank/endress-hauser-micropilot-reflexion-dk-wert/':'knowledge-eh-micropilot-dk-reflexion','/wissensdatenbank/endress-hauser-micropilot-pulse-radar-time-of-flight/':'knowledge-eh-micropilot-pulse-tof','/wissensdatenbank/endress-hauser-micropilot-fmcw-radar-80-ghz/':'knowledge-eh-micropilot-fmcw-80ghz','/wissensdatenbank/endress-hauser-micropilot-frequenz-abstrahlwinkel/':'knowledge-eh-micropilot-frequency-beam','/wissensdatenbank/endress-hauser-micropilot-produktuebersicht-geraeteauswahl/':'knowledge-eh-micropilot-product-selection','/wissensdatenbank/endress-hauser-micropilot-einbauposition-antennenausrichtung/':'knowledge-eh-micropilot-install-alignment','/wissensdatenbank/endress-hauser-micropilot-stutzen-antenne-prozessanschluss/':'knowledge-eh-micropilot-nozzle-antenna','/wissensdatenbank/endress-hauser-micropilot-sonderfaelle-einbau/':'knowledge-eh-micropilot-special-install','/wissensdatenbank/endress-hauser-micropilot-gehaeuse-anzeigemodul-ausrichten/':'knowledge-eh-micropilot-housing-display','/wissensdatenbank/endress-hauser-micropilot-elektrischer-anschluss-bedienzugaenge/':'knowledge-eh-micropilot-electrical-access','/wissensdatenbank/endress-hauser-micropilot-grundabgleich-inbetriebnahme/':'knowledge-eh-micropilot-commissioning','/wissensdatenbank/endress-hauser-micropilot-huellkurve-verstehen-auswerten/':'knowledge-eh-micropilot-envelope-curve','/wissensdatenbank/endress-hauser-micropilot-fehler-falscher-hoher-fuellstand-stoerechoausblendung/':'knowledge-eh-micropilot-fault-high-level','/wissensdatenbank/endress-hauser-micropilot-fehler-null-prozent-fuellstandsignal-ausgeblendet/':'knowledge-eh-micropilot-fault-zero-level','/wissensdatenbank/endress-hauser-micropilot-fehler-unplausible-distanz-stutzen-stoersignal/':'knowledge-eh-micropilot-fault-nozzle','/wissensdatenbank/endress-hauser-micropilot-fehler-ueber-hundert-prozent-ansatz-antenne/':'knowledge-eh-micropilot-fault-buildup','/wissensdatenbank/endress-hauser-micropilot-fehler-kein-mediumsignal-medium-in-antenne/':'knowledge-eh-micropilot-fault-medium-antenna','/wissensdatenbank/endress-hauser-micropilot-fehler-f941-echo-verloren-tankbodenbereich/':'knowledge-eh-micropilot-fault-f941','/wissensdatenbank/siemens-sitrans-p320-sil-verriegelung/':'knowledge-siemens-sitrans-p320-sil-verriegelung','/wissensdatenbank/siemens-sps-rohwert/':'knowledge-siemens-sps-rohwert','/wissensdatenbank/vacon-frequenzumrichter-ist-sollwert-abweichung/':'knowledge-vacon-frequenzumrichter-ist-sollwert-abweichung'});
function favoriteIcon(item){if(item.icon){try{const url=new URL(item.icon,location.href);if(url.origin===location.origin&&url.pathname.includes('/navigation-icons/v2-6-8-0-'))return url.href}catch{}}let pathname='';try{const url=new URL(item.url,location.href);if(url.origin!==location.origin)return new URL(`assets/navigation-icons/v2-6-8-0-app-eh-viewer.png?v=${window.SK_PCT?.version||'2.6.8.0-Beta'}`,window.SK_PCT?.root||location.href).href;pathname=url.pathname}catch{}const key=Object.keys(FAVORITE_ICONS).sort((a,b)=>b.length-a.length).find(value=>pathname.endsWith(value));const stem=key?FAVORITE_ICONS[key]:'app-wissensdatenbank';return new URL(`assets/navigation-icons/v2-6-8-0-${stem}.png?v=${window.SK_PCT?.version||'2.6.8.0-Beta'}`,window.SK_PCT?.root||location.href).href}
const isOn=card=>load().some(item=>item.url===cardUrl(card));
let drawer,trigger,lastFocus,frame,suspended=[];
const frameHost=()=>document.querySelector('body[data-sk-home="ios"] .pct-home-screen,body[data-sk-layout="framed"] .sk-app-frame');
function state(button,on){button.dataset.active=String(on);button.classList.toggle('active',on);button.setAttribute('aria-pressed',String(on));button.innerHTML=svg(on);button.title=on?'Aus Favoriten entfernen':'Zu Favoriten hinzufügen';button.setAttribute('aria-label',button.title)}
function sync(){
  document.querySelectorAll('.sk-favorite-button').forEach(button=>{const card=button.closest('a.card,a.tool-card');if(card)state(button,isOn(card))});
  const total=load().length;
  document.querySelectorAll('.sk-favorites-count').forEach(count=>{count.textContent=String(total);count.hidden=total===0});
}
function announce(message){const status=drawer?.querySelector('.sk-favorites-status');if(!status)return;status.textContent='';requestAnimationFrame(()=>{status.textContent=message})}
function toggle(card){const item=info(card),items=load(),index=items.findIndex(entry=>entry.url===item.url);if(index>=0){items.splice(index,1);save(items);announce(`${item.title} aus Favoriten entfernt.`)}else{items.push(item);save(items);announce(`${item.title} zu Favoriten hinzugefügt.`)}sync();render()}
function prepare(){document.querySelectorAll('a.card,a.tool-card').forEach(card=>{const href=card.getAttribute('href')||'';if(!href||href.endsWith('.docx')||href.endsWith('.pdf')||card.classList.contains('sk-favorite-entry'))return;card.classList.add('sk-favorite-capable');const iconWrapper=card.querySelector(':scope > .sk-home-icon')||card.querySelector('.knowledge-home-icon');if(iconWrapper)iconWrapper.classList.add('sk-app-icon-wrapper');const host=iconWrapper||card;let button=card.querySelector('.sk-favorite-button');if(!button){button=document.createElement('button');button.type='button';button.className='sk-favorite-button'}if(button.parentElement!==host)host.append(button);if(button.dataset.bound)return;button.dataset.bound='true';button.addEventListener('click',event=>{event.preventDefault();event.stopPropagation();toggle(card)})});sync()}
const focusable=()=>drawer?[...drawer.querySelectorAll('a[href],button:not([disabled]),[tabindex]:not([tabindex="-1"])')].filter(node=>node.offsetParent!==null):[];
function mount(){frame=frameHost();if(!frame||!drawer)return false;const footer=[...frame.children].find(node=>node.matches?.('.sk-footer,.pct-home-footer'));if(drawer.parentElement!==frame)frame.insertBefore(drawer,footer||null);return true}
function suspendFrame(){if(!frame)return;suspended=[];[...frame.children].forEach(node=>{if(node===drawer||node.matches?.('.pct-home-head,.sk-global-header,.sk-footer,.pct-home-footer,h1.visually-hidden'))return;suspended.push({node,ariaHidden:node.getAttribute('aria-hidden'),inert:node.inert});node.classList.add('sk-favorites-suspended');node.setAttribute('aria-hidden','true');node.inert=true});frame.classList.add('sk-favorites-open')}
function restoreFrame(){suspended.forEach(({node,ariaHidden,inert})=>{node.classList.remove('sk-favorites-suspended');if(ariaHidden===null)node.removeAttribute('aria-hidden');else node.setAttribute('aria-hidden',ariaHidden);node.inert=inert});suspended=[];frame?.classList.remove('sk-favorites-open')}
function close({restoreFocus=true}={}){if(!drawer||drawer.hidden)return;restoreFrame();drawer.classList.remove('open');drawer.hidden=true;drawer.setAttribute('aria-hidden','true');document.body.classList.remove('sk-favorites-page-open');trigger?.setAttribute('aria-expanded','false');trigger?.setAttribute('aria-label','Favoriten öffnen');if(restoreFocus)(lastFocus?.isConnected?lastFocus:trigger)?.focus({preventScroll:true})}
function open(){if(!drawer||!mount())return;if(!drawer.hidden){close();return}lastFocus=document.activeElement;render();suspendFrame();drawer.hidden=false;drawer.classList.add('open');drawer.setAttribute('aria-hidden','false');document.body.classList.add('sk-favorites-page-open');trigger?.setAttribute('aria-expanded','true');trigger?.setAttribute('aria-label','Favoriten schließen');drawer.querySelector('.sk-favorites-list')?.scrollTo({top:0,behavior:'auto'});requestAnimationFrame(()=>drawer.querySelector('.sk-favorites-close')?.focus({preventScroll:true}))}
function removeFavorite(item){const items=load().filter(value=>value.url!==item.url);save(items);sync();render();announce(`${item.title} aus Favoriten entfernt.`);const candidates=focusable();(candidates.find(node=>node.classList.contains('sk-favorite-remove'))||drawer.querySelector('.sk-favorites-clear:not([disabled])')||drawer.querySelector('.sk-favorites-close'))?.focus({preventScroll:true})}
function render(){
  const list=drawer?.querySelector('.sk-favorites-list'),clear=drawer?.querySelector('.sk-favorites-clear'),summary=drawer?.querySelector('.sk-favorites-summary');if(!list)return;
  const items=load(),total=items.length;
  if(summary)summary.textContent=total===1?'1 gespeicherter Favorit':`${total} gespeicherte Favoriten`;
  if(clear){clear.disabled=total===0;clear.setAttribute('aria-disabled',String(total===0))}
  if(!total){list.innerHTML=`<div class="sk-favorites-empty">${svg(false)}<span><strong>Noch keine Favoriten</strong><small>Apps oder Wissen per Stern speichern.</small></span><b aria-label="Anzahl Favoriten">0</b></div>`;return}
  list.replaceChildren();
  items.forEach(item=>{const row=document.createElement('article');row.className='sk-favorite-row';const iconHost=document.createElement('span');iconHost.className='sk-favorite-icon-host';iconHost.setAttribute('aria-hidden','true');const image=document.createElement('img');image.alt='';image.decoding='async';image.src=favoriteIcon(item);iconHost.append(image);const link=document.createElement('a');link.className='sk-favorite-entry';link.href=item.url;if(item.external){link.target='_blank';link.rel='external noopener noreferrer';link.referrerPolicy='no-referrer'}link.innerHTML=`<span class="sk-favorite-category">${esc(item.category)}</span><strong>${esc(item.title)}</strong>${item.description?`<small>${esc(item.description)}</small>`:''}`;link.setAttribute('aria-label',`${item.title} öffnen`);const remove=document.createElement('button');remove.type='button';remove.className='sk-favorite-remove';remove.innerHTML=svg(true);remove.title=`${item.title} aus Favoriten entfernen`;remove.setAttribute('aria-label',remove.title);remove.addEventListener('click',()=>removeFavorite(item));row.append(iconHost,link,remove);list.append(row)})
}
function ensure(){
  trigger=document.querySelector('.sk-favorites-trigger')||document.body.appendChild(Object.assign(document.createElement('button'),{type:'button',className:'sk-favorites-trigger'}));if(trigger.dataset.bound)return;
  trigger.dataset.bound='true';trigger.setAttribute('aria-label','Favoriten öffnen');trigger.setAttribute('aria-haspopup','dialog');trigger.setAttribute('aria-controls','skFavoritesDrawer');trigger.setAttribute('aria-expanded','false');
  if(!trigger.querySelector('.sk-trigger-star'))trigger.innerHTML=`<span class="sk-trigger-star"><img class="pct-nav-graphic" src="${new URL(`assets/navigation-icons/v2-6-8-0-nav-favorite.png?v=${window.SK_PCT?.version||'2.6.8.0-Beta'}`,window.SK_PCT?.root||new URL('./',location.href)).href}" alt="" aria-hidden="true" decoding="sync"></span><span class="sk-favorites-count" hidden>0</span>`;
  drawer=document.querySelector('.sk-favorites-drawer')||Object.assign(document.createElement('section'),{className:'sk-favorites-drawer'});drawer.id='skFavoritesDrawer';drawer.setAttribute('role','dialog');drawer.setAttribute('aria-modal','false');drawer.setAttribute('aria-labelledby','skFavoritesTitle');drawer.setAttribute('aria-hidden','true');drawer.tabIndex=-1;drawer.hidden=true;
  if(!drawer.querySelector('.sk-favorites-head'))drawer.innerHTML='<div class="sk-favorites-head"><div><div class="sk-favorites-kicker">SCHNELLZUGRIFF</div><h2 id="skFavoritesTitle">Meine Favoriten</h2></div><button class="sk-favorites-close" type="button" aria-label="Favoriten schließen und zurück"></button></div><div class="sk-favorites-toolbar"><span class="sk-favorites-summary">0 gespeicherte Favoriten</span><button class="sk-favorites-clear" type="button">Alle leeren</button></div><p class="sk-favorites-status sr-only" aria-live="polite"></p><div aria-label="Favoritenliste" class="sk-favorites-list" tabindex="0"></div>';
  mount();trigger.addEventListener('click',open);drawer.querySelector('.sk-favorites-close').addEventListener('click',()=>close());drawer.querySelector('.sk-favorites-clear').addEventListener('click',()=>{const total=load().length;if(!total)return;save([]);sync();render();announce(`${total} ${total===1?'Favorit wurde':'Favoriten wurden'} entfernt.`);drawer.querySelector('.sk-favorites-close')?.focus({preventScroll:true})});
  drawer.addEventListener('keydown',event=>{if(event.key==='Escape'){event.preventDefault();close();return}if(event.key!=='Tab')return;const nodes=focusable();if(!nodes.length){event.preventDefault();drawer.focus();return}const first=nodes[0],last=nodes[nodes.length-1];if(event.shiftKey&&document.activeElement===first){event.preventDefault();last.focus()}else if(!event.shiftKey&&document.activeElement===last){event.preventDefault();first.focus()}});
  sync();render();
}
function refresh(){prepare();sync();render()}
function init(){ensure();refresh();document.addEventListener('sk:cards-updated',refresh)}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init,{once:true});else init();
})();

/* === Modul: Startseitensuche === */
(()=>{'use strict';
let searchIndex=[];
let materialCatalog=[];
const RELEASE='2.6.8.0-Beta';
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
async function loadIndex(){try{const [indexResponse,materialsResponse]=await Promise.all([fetch(new URL(`assets/search-index-v2-6-8-0.json?v=${RELEASE}`,root()),{cache:'no-store'}),fetch(new URL(`assets/materials.json?v=${RELEASE}`,root()),{cache:'no-store'})]);if(!indexResponse.ok)throw new Error(`Suchindex ${indexResponse.status}`);const indexData=await indexResponse.json();searchIndex=Array.isArray(indexData)?indexData:[];if(materialsResponse.ok){const materialData=await materialsResponse.json();materialCatalog=Array.isArray(materialData.materials)?materialData.materials:[]}}catch(error){console.warn('Der Suchindex konnte nicht vollständig geladen werden.',error);searchIndex=[];materialCatalog=[]}}
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
const RELEASE='2.6.8.0-Beta';
const root=window.SK_PCT?.root||new URL('../',document.currentScript?.src||location.href);
const sprite=new URL('assets/pct-controls.svg',root).href;
const NAV_GRAPHICS=Object.freeze({
  'app-einheitendatenbank':'v2-6-8-0-app-einheitendatenbank.png',
  'nav-back':'v2-6-8-0-nav-back.png',
  'nav-home':'v2-6-8-0-nav-home.png',
  'nav-search':'v2-6-8-0-nav-search.png',
  'nav-favorite':'v2-6-8-0-nav-favorite.png'
});
const navGraphic=name=>{const file=NAV_GRAPHICS[name];if(!file)throw new Error(`Unbekannte Navigationsgrafik: ${name}`);return `<img class="pct-nav-graphic" src="${new URL(`assets/navigation-icons/${file}`,root).href}" alt="" aria-hidden="true" decoding="sync">`};
const icon=(name,small=false)=>`<svg class="pct-icon${small?' pct-icon--small':''}" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><use href="${sprite}#icon-${name}"></use></svg>`;
const normalized=value=>String(value||'').trim().toLocaleLowerCase('de-DE');
const graphicPrefix=(node,name)=>{if(!node||node.querySelector(':scope > .pct-nav-graphic'))return;node.dataset.pctGraphic=name;node.insertAdjacentHTML('afterbegin',navGraphic(name))};
const add=(node,...classes)=>node?.classList.add(...classes.filter(Boolean));
function iconOnly(node,name){if(!node||(node.dataset.pctIcon===name&&node.querySelector('.pct-icon')))return;node.dataset.pctIcon=name;node.innerHTML=icon(name)}
function prefix(node,name){if(!node||node.querySelector(':scope > .pct-icon'))return;node.dataset.pctIcon=name;node.insertAdjacentHTML('afterbegin',icon(name,true))}
function logicalParentURL(){const body=document.body;try{if(body?.dataset.skParentDetail&&new URL(location.href).searchParams.has('material'))return new URL(body.dataset.skParentDetail,location.href);if(body?.dataset.skParent)return new URL(body.dataset.skParent,location.href)}catch(error){console.warn('Logisches Elternziel ist ungültig.',error)}return new URL(root.href)}
function syncHeaderBack(back){const target=logicalParentURL();back.href=target.href;back.dataset.logicalParent=target.href;back.title='Eine fachliche Ebene zurück'}
function headerControls(){document.querySelectorAll('.sk-global-header').forEach(header=>{const inner=header.querySelector('.sk-header-inner'),home=inner?.querySelector('.sk-header-home');if(!inner||!home||inner.querySelector('.pct-header-actions'))return;const actions=document.createElement('div');actions.className='pct-header-actions';const favorite=document.querySelector('.sk-favorites-trigger');const back=document.createElement('a');back.className='pct-control pct-control--quiet pct-control--back';back.setAttribute('aria-label','Eine fachliche Ebene zurück');back.innerHTML=`${navGraphic('nav-back')}<span class="pct-label">Zurück</span>`;syncHeaderBack(back);back.addEventListener('click',()=>syncHeaderBack(back));const sync=()=>syncHeaderBack(back);addEventListener('popstate',sync);document.addEventListener('sk:route-updated',sync);new MutationObserver(sync).observe(document.body,{attributes:true,attributeFilter:['data-sk-parent','data-sk-parent-detail']});home.href=root.href;home.setAttribute('aria-label','Zur Startseite');home.textContent='';add(home,'pct-control','pct-control--quiet','pct-control--home');home.innerHTML=`${navGraphic('nav-home')}<span class="pct-label">Startseite</span>`;home.parentNode.insertBefore(actions,home);if(favorite)actions.append(favorite);actions.append(back,home)})}
function searches(){document.querySelectorAll('input[type="search"]').forEach(input=>{if(input.parentElement?.classList.contains('pct-search-shell'))return;const shell=document.createElement('span');shell.className='pct-search-shell';input.parentNode.insertBefore(shell,input);shell.append(input);shell.insertAdjacentHTML('afterbegin',icon('search'))})}
function selects(){document.querySelectorAll('select').forEach(select=>select.classList.add('pct-select'))}
function favorites(){document.querySelectorAll('.sk-favorite-button,.unit-favorite-button').forEach(button=>{add(button,'pct-control','pct-control--icon','pct-control--favorite');iconOnly(button,'star')});document.querySelectorAll('.sk-favorite-remove').forEach(button=>{add(button,'pct-control','pct-control--icon','pct-control--danger');iconOnly(button,'trash')});document.querySelectorAll('.sk-favorites-trigger').forEach(button=>{add(button,'pct-control','pct-control--icon','pct-control--favorite');const slot=button.querySelector('.sk-trigger-star')||button.appendChild(Object.assign(document.createElement('span'),{className:'sk-trigger-star'}));if(!slot.querySelector('img.pct-nav-graphic'))slot.innerHTML=navGraphic('nav-favorite')})}
function drawerControls(){document.querySelectorAll('.sk-favorites-close').forEach(button=>{add(button,'pct-control','pct-control--icon');iconOnly(button,'close')});document.querySelectorAll('.sk-favorites-clear').forEach(button=>{add(button,'pct-control','pct-control--danger');prefix(button,'clear-all')})}
function signControls(){document.querySelectorAll('.sign,.analog-sign-button').forEach(button=>{add(button,'pct-control','pct-control--icon','pct-control--sign');if(button.querySelector('.pct-sign-glyph'))return;button.dataset.pctIcon='sign';button.innerHTML='<span class="pct-sign-glyph" aria-hidden="true">±</span>';button.title=button.title||'Vorzeichen wechseln'})}
function resets(){document.querySelectorAll('button,.sk-filter-reset,.material-reset').forEach(button=>{const value=normalized(button.textContent);if(!(button.matches('.sk-filter-reset,.material-reset,#unitReset')||value.includes('zurücksetzen')||value==='neue messstelle'))return;add(button,'pct-control','pct-control--reset');prefix(button,'reset')})}
function tabs(){document.querySelectorAll('.sk-filter-button,.material-filter,.analog-tab').forEach(button=>button.classList.add('pct-tab'))}
function toggles(){document.querySelectorAll('.knowledge-compact-toggle').forEach(button=>button.classList.add('pct-toggle-control'))}
function collapsibles(){const buttons='.sk-filter-toggle,.knowledge-manufacturer-toggle,.material-card-toggle';document.querySelectorAll(buttons).forEach(button=>button.classList.add('pct-collapse-control'));document.querySelectorAll('.sk-filter-toggle-icon,.knowledge-manufacturer-chevron,.material-toggle-icon').forEach(slot=>{slot.classList.add('pct-chevron-slot');if(!slot.querySelector('.pct-icon'))slot.innerHTML=icon('chevron-down')});document.querySelectorAll('.unit-category-head').forEach(summary=>{let slot=summary.querySelector('.unit-category-chevron');if(!slot){slot=document.createElement('span');slot.className='unit-category-chevron pct-chevron-slot';slot.innerHTML=icon('chevron-down');summary.append(slot)}});document.querySelectorAll('.unit-row-details>summary').forEach(summary=>{let slot=summary.querySelector('.pct-chevron-slot');if(!slot){slot=document.createElement('span');slot.className='pct-chevron-slot';slot.innerHTML=icon('chevron-down',true);summary.append(slot)}})}
async function copy(value){if(navigator.clipboard?.writeText){await navigator.clipboard.writeText(value);return}const area=document.createElement('textarea');area.value=value;area.readOnly=true;area.style.cssText='position:fixed;opacity:0';document.body.append(area);area.select();document.execCommand('copy');area.remove()}
function addCopy(target){const host=target.closest('.calc-value-card,.analog-value-card,.voltage-result,.result')||target.parentElement;if(!host||host.querySelector(':scope > .pct-copy-button'))return;host.classList.add('pct-copy-host');const button=document.createElement('button');button.type='button';button.className='pct-copy-button pct-control pct-control--icon pct-control--copy';button.setAttribute('aria-label','Wert kopieren');button.title='Wert kopieren';button.innerHTML=icon('copy');button.addEventListener('click',async()=>{const value=(target.textContent||'').trim();if(!value||value==='–')return;try{await copy(value);button.classList.add('is-success');button.innerHTML=icon('check');button.setAttribute('aria-label','Kopiert');button.title='Kopiert';setTimeout(()=>{button.classList.remove('is-success');button.innerHTML=icon('copy');button.setAttribute('aria-label','Wert kopieren');button.title='Wert kopieren'},1400)}catch(error){console.warn('Kopieren nicht möglich.',error)}});host.append(button)}
function copyControls(){if(document.body.matches('[data-sk-result-copy="disabled"]'))return;document.querySelectorAll('.result strong[id],.calc-value-card strong[id],.analog-value-card strong[id],.voltage-result strong[id]').forEach(addCopy);document.querySelectorAll('button').forEach(button=>{if(normalized(button.textContent).includes('kopier')){add(button,'pct-control','pct-control--copy');prefix(button,'copy')}})}
function message(node,type){if(!node||node.querySelector(':scope > .pct-message-icon'))return;node.classList.add('pct-message',`pct-message--${type}`);const body=document.createElement('span');body.className='pct-message-body';while(node.firstChild)body.append(node.firstChild);const slot=document.createElement('span');slot.className='pct-message-icon';slot.innerHTML=icon(type==='warning'?'warning':type==='success'?'success':type==='error'?'error':'info');node.append(slot,body)}
function messages(){document.querySelectorAll('.material-safety').forEach(node=>message(node,'warning'));document.querySelectorAll('.material-load-error,.calculation-error,[role="alert"]').forEach(node=>message(node,'error'));document.querySelectorAll('.unit-model-note,.calc-notice,.knowledge-standard-note,.material-data-note,.material-search-help').forEach(node=>message(node,'info'));document.querySelectorAll('.kb-callout.success').forEach(node=>message(node,'success'))}
function infoControls(){document.querySelectorAll('.analog-card-info summary').forEach(summary=>{summary.classList.add('pct-info-control');prefix(summary,'info')})}
function actionControls(){document.querySelectorAll('.toolbar button,.actions button,button.primary,button.secondary,.sk-unit-database-button,.knowledge-proposal-link,.knowledge-view-back,.pct-home-done').forEach(button=>button.classList.add('pct-control'));document.querySelectorAll('.toolbar button,.photo button,button.primary,button.secondary,.sk-unit-database-button,.knowledge-proposal-link,.knowledge-view-back,.pct-home-done').forEach(button=>{const value=normalized(button.textContent);if(value.includes('pdf')||value.includes('druck'))prefix(button,'print');if(value.includes('lösch')){add(button,'pct-control','pct-control--danger');prefix(button,'trash')}if(button.matches('.sk-unit-database-button'))prefix(button,'database');if(button.matches('.knowledge-proposal-link'))prefix(button,'download');if(button.matches('.knowledge-view-back'))graphicPrefix(button,'nav-back');if(button.matches('button.primary'))prefix(button,'calculate');if(button.matches('button.secondary'))prefix(button,'reset');if(button.matches('.pct-home-done'))prefix(button,'done')})}
function sortControls(){document.querySelectorAll('[data-control-icon]').forEach(node=>prefix(node,node.dataset.controlIcon));const label=document.querySelector('.sk-sort-label[data-control-icon="sort"]');if(label)prefix(label,'sort')}
function apply(){headerControls();searches();selects();favorites();drawerControls();signControls();resets();tabs();toggles();collapsibles();copyControls();messages();infoControls();actionControls();sortControls();document.documentElement.dataset.pctControls=RELEASE}
let queued=false;const schedule=()=>{if(queued)return;queued=true;queueMicrotask(()=>{queued=false;apply()})};
function init(){apply();new MutationObserver(schedule).observe(document.body,{subtree:true,childList:true});document.addEventListener('sk:cards-updated',schedule);document.addEventListener('sk:cards-sorted',schedule)}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init,{once:true});else init();
})();
