(()=>{'use strict';
const SELECT_ID='skToolSort';let originalOrder=[];
const norm=value=>String(value||'').trim().toLocaleLowerCase('de-DE').normalize('NFD').replace(/[\u0300-\u036f]/g,'');
const host=()=>document.querySelector('.tools,.start-tools');
const cards=()=>{const grid=host();return grid?[...grid.querySelectorAll(':scope > a.card,:scope > a.tool-card')]:[]};
const category=card=>norm(card.querySelector('.sk-card-category,.eyebrow')?.textContent||'');
const title=card=>norm(card.querySelector('h1,h2,h3')?.textContent||'');
function captureOriginal(){cards().forEach(card=>{if(!originalOrder.includes(card))originalOrder.push(card)})}
function compareText(a,b,key,direction){const result=key(a).localeCompare(key(b),'de',{sensitivity:'base',numeric:true});if(result!==0)return direction==='asc'?result:-result;return originalOrder.indexOf(a)-originalOrder.indexOf(b)}
function sortCards(mode){const grid=host();if(!grid)return;captureOriginal();let ordered=[...cards()];if(mode==='category-asc')ordered.sort((a,b)=>compareText(a,b,category,'asc')||compareText(a,b,title,'asc'));if(mode==='category-desc')ordered.sort((a,b)=>compareText(a,b,category,'desc')||compareText(a,b,title,'asc'));if(mode==='title-asc')ordered.sort((a,b)=>compareText(a,b,title,'asc'));if(mode==='title-desc')ordered.sort((a,b)=>compareText(a,b,title,'desc'));if(mode==='default')ordered=[...originalOrder].filter(card=>card.isConnected&&card.parentElement===grid);ordered.forEach(card=>grid.append(card));document.dispatchEvent(new CustomEvent('sk:cards-sorted',{detail:{mode}}))}
function bind(){const select=document.getElementById(SELECT_ID);if(!select||select.dataset.bound)return;select.dataset.bound='true';select.addEventListener('change',()=>sortCards(select.value));document.getElementById('skFilterReset')?.addEventListener('click',()=>{select.value='default';sortCards('default')})}
function refresh(){captureOriginal();bind();const select=document.getElementById(SELECT_ID);if(select)sortCards(select.value)}
function init(){refresh();document.addEventListener('sk:cards-updated',refresh)}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init,{once:true});else init();
})();
