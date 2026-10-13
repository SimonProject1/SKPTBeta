/* SK PCT Tools 2.6.0.1-Beta — reduzierter PCT Home-Screen mit Long-Press-Bearbeitungsmodus. */
(()=>{'use strict';
const RELEASE='2.6.0.1-Beta';
const ORDER_KEY='skPctHomeOrderV1';
const root=document.documentElement;
const byId=id=>document.getElementById(id);
const read=(key,fallback)=>{try{const value=JSON.parse(localStorage.getItem(key));return value??fallback}catch{return fallback}};
const write=(key,value)=>{try{localStorage.setItem(key,JSON.stringify(value))}catch(error){console.warn('Startseiten-Einstellung konnte nicht gespeichert werden.',error)}};
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
