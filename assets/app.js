(()=>{'use strict';
const RELEASE='2.0.1.2';
const scriptUrl=document.currentScript?.src||'';
const root=scriptUrl?new URL('../',scriptUrl):new URL('./',location.href);
window.SK_PLT=Object.freeze({version:RELEASE,root});
window.$=id=>document.getElementById(id);
window.num=value=>Number.parseFloat(String(value).replace(',','.'));
window.de=(value,digits=3)=>Number.isFinite(value)?value.toLocaleString('de-DE',{minimumFractionDigits:digits,maximumFractionDigits:digits}):'–';
function syncVersion(){
  document.querySelectorAll('.sk-logo-version,.stb-version,.badge').forEach(node=>{
    if(/^Version\s+[0-9]+(?:\.[0-9]+){2,3}$/i.test((node.textContent||'').trim()))node.textContent=`Version ${RELEASE}`;
  });
}
function addSignControls(){
  if(document.body?.dataset.signControls!=='true')return;
  document.querySelectorAll('input[type=number]').forEach(input=>{
    if(input.dataset.s)return;
    input.dataset.s='1';
    const wrapper=document.createElement('div');wrapper.className='number';
    input.parentNode.insertBefore(wrapper,input);wrapper.append(input);
    const button=document.createElement('button');button.type='button';button.className='sign';button.textContent='±';button.setAttribute('aria-label','Vorzeichen wechseln');
    button.addEventListener('click',()=>{const value=window.num(input.value);input.value=Number.isFinite(value)?(value===0?0:-value):'-';input.dispatchEvent(new Event('input',{bubbles:true}));input.dispatchEvent(new Event('change',{bubbles:true}))});
    wrapper.append(button);
  });
}
function purgeRemovedServiceFavorite(){
  try{
    const key='skPltToolsFavoritesV2';const items=JSON.parse(localStorage.getItem(key)||'[]');if(!Array.isArray(items))return;
    const pattern=/(servicewerte|initial[- ]?pins?|initialwerte)/i;const clean=items.filter(item=>!pattern.test(`${item?.url||''} ${item?.title||''} ${item?.description||''} ${item?.category||''}`));
    if(clean.length!==items.length)localStorage.setItem(key,JSON.stringify(clean));
  }catch(error){console.warn('Veralteter Service-Favorit konnte nicht bereinigt werden.',error)}
}
function registerWorker(){
  if(!('serviceWorker' in navigator))return;
  navigator.serviceWorker.register(new URL('service-worker.js',root),{updateViaCache:'none'}).then(registration=>registration.update()).catch(error=>console.warn('Service Worker konnte nicht registriert werden.',error));
}
function init(){syncVersion();addSignControls();purgeRemovedServiceFavorite();registerWorker()}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init,{once:true});else init();
})();
