/* SK PCT Tools 2.6.1.5-Beta — zentrale Einheitendatenbank und Umrechnungslaufzeit. */
(()=>{'use strict';
const RELEASE='2.6.1.5-Beta';
const STORAGE_KEY='skPctUnitFavoritesV1';
const source=document.currentScript?.src||'';
const root=source?new URL('../',source):(window.SK_PCT?.root||new URL('./',location.href));
let model=null;
const selects=new Set();
const listeners=new Set();
const esc=value=>String(value??'').replace(/[&<>"']/g,char=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#039;'}[char]));
const number=value=>Number.parseFloat(String(value).replace(',','.'));
const favoriteKey=(categoryId,unitId)=>`${categoryId}:${unitId}`;
function storedFavorites(){const direct=localStorage.getItem(STORAGE_KEY);if(direct!==null)return direct;const previous=Object.keys(localStorage).find(item=>item!==STORAGE_KEY&&item.startsWith('sk')&&item.endsWith('UnitFavoritesV1'));const value=previous?localStorage.getItem(previous):null;if(value!==null)localStorage.setItem(STORAGE_KEY,value);return value}
function loadFavorites(){try{const value=JSON.parse(storedFavorites()||'[]');return Array.isArray(value)?[...new Set(value.filter(item=>typeof item==='string'))]:[]}catch{return []}}
function saveFavorites(items){const clean=[...new Set(items)];try{localStorage.setItem(STORAGE_KEY,JSON.stringify(clean))}catch(error){console.warn('Einheitenfavoriten konnten nicht gespeichert werden.',error)};listeners.forEach(listener=>listener(clean));document.dispatchEvent(new CustomEvent('sk:unit-favorites-changed',{detail:{favorites:clean}}));refreshSelects();return clean}
function isFavorite(categoryId,unitId){return loadFavorites().includes(favoriteKey(categoryId,unitId))}
function toggleFavorite(categoryId,unitId){const key=favoriteKey(categoryId,unitId),items=loadFavorites(),index=items.indexOf(key);index>=0?items.splice(index,1):items.push(key);saveFavorites(items);return index<0}
function subscribe(listener){listeners.add(listener);return()=>listeners.delete(listener)}
function category(categoryId){const found=model?.categories.find(item=>item.id===categoryId);if(!found)throw new Error(`Unbekannte Einheitenkategorie: ${categoryId}`);return found}
function unit(categoryId,unitId){const found=category(categoryId).units.find(item=>item.id===unitId);if(!found)throw new Error(`Unbekannte Einheit ${unitId} in ${categoryId}`);return found}
function toBase(value,categoryId,unitId){const item=unit(categoryId,unitId),input=Number(value);if(!Number.isFinite(input))return NaN;return input*Number(item.toBase.factor)+Number(item.toBase.offset||0)}
function fromBase(value,categoryId,unitId){const item=unit(categoryId,unitId),input=Number(value);if(!Number.isFinite(input))return NaN;return(input-Number(item.toBase.offset||0))/Number(item.toBase.factor)}
function convert(value,categoryId,fromUnitId,toUnitId){if(fromUnitId===toUnitId)return Number(value);return fromBase(toBase(value,categoryId,fromUnitId),categoryId,toUnitId)}
function inputValue(value){return Number.isFinite(value)?String(Number(value.toPrecision(15))):''}
function format(value,digits=6){if(!Number.isFinite(Number(value)))return'–';const absolute=Math.abs(Number(value)),maximum=absolute!==0&&absolute<0.01?Math.max(digits,8):digits;return Number(value).toLocaleString('de-DE',{maximumFractionDigits:maximum,minimumFractionDigits:0,useGrouping:true})}
function option(group,item,selected){const node=document.createElement('option');node.value=item.id;node.textContent=item.symbol;node.label=item.symbol;node.title=item.name;node.dataset.unitName=item.name;node.selected=item.id===selected;group.append(node)}
function syncSelectMeta(select,categoryId){const item=unit(categoryId,select.value);const fieldLabel=select.closest('label,.analog-physical-field,.analog-config-field')?.querySelector('span,label')?.textContent?.trim()||'Einheit';select.title=`${fieldLabel}: ${item.name} (${item.symbol})`;select.setAttribute('aria-label',`${fieldLabel}: ${item.name}, ${item.symbol}`)}
function populateSelect(select,categoryId,selectedUnitId,settings={}){
 const entry=category(categoryId),favorites=entry.units.filter(item=>isFavorite(categoryId,item.id)),selected=entry.units.some(item=>item.id===selectedUnitId)?selectedUnitId:(settings.preferredUnit&&entry.units.some(item=>item.id===settings.preferredUnit)?settings.preferredUnit:entry.defaultUnit);
 select.replaceChildren();
 const standard=document.createElement('optgroup');standard.label='Standardeinheit';option(standard,unit(categoryId,entry.defaultUnit),selected);select.append(standard);
 const favoriteGroup=document.createElement('optgroup');favoriteGroup.label='Favoriten';favorites.filter(item=>item.id!==entry.defaultUnit).forEach(item=>option(favoriteGroup,item,selected));if(!favoriteGroup.children.length){const empty=document.createElement('option');empty.disabled=true;empty.textContent='Keine Favoriten markiert';favoriteGroup.append(empty)}select.append(favoriteGroup);
 if(settings.includeAll!==false){const more=document.createElement('optgroup');more.label='Weitere Einheiten';entry.units.filter(item=>item.id!==entry.defaultUnit&&!favorites.some(fav=>fav.id===item.id)).forEach(item=>option(more,item,selected));if(more.children.length)select.append(more)}
 select.value=selected;select.dataset.unitCategory=categoryId;select.dataset.previousUnit=selected;selects.add(select);bindSelect(select);syncSelectMeta(select,categoryId);return selected;
}
function convertTargets(select,oldUnit,newUnit){const ids=(select.dataset.unitTargets||'').split(',').map(value=>value.trim()).filter(Boolean);if(!ids.length||oldUnit===newUnit)return;const categoryId=select.dataset.unitCategory,changed=[];ids.forEach(id=>{const target=document.getElementById(id);if(!target)return;const value=number(target.value);if(!Number.isFinite(value))return;target.value=inputValue(convert(value,categoryId,oldUnit,newUnit));changed.push(target)});changed.forEach(target=>{target.dispatchEvent(new Event('input',{bubbles:true}));target.dispatchEvent(new Event('change',{bubbles:true}))})}
function bindSelect(select){if(select.dataset.unitBound==='true')return;select.dataset.unitBound='true';select.addEventListener('change',()=>{const oldUnit=select.dataset.previousUnit||select.value,newUnit=select.value,categoryId=select.dataset.unitCategory;convertTargets(select,oldUnit,newUnit);select.dataset.previousUnit=newUnit;syncSelectMeta(select,categoryId);select.dispatchEvent(new CustomEvent('sk:unit-change',{bubbles:true,detail:{categoryId,oldUnit,newUnit}}))})}
function refreshSelects(){if(!model)return;selects.forEach(select=>{if(!select.isConnected){selects.delete(select);return}const value=select.value,categoryId=select.dataset.unitCategory;populateSelect(select,categoryId,value,{includeAll:select.dataset.unitIncludeAll!=='false',preferredUnit:select.dataset.unitPreferred})})}
function validate(data){if(!data||!Array.isArray(data.categories)||data.categories.length!==19)throw new Error('Die Einheitendatenbank ist unvollständig.');const categoryIds=new Set(),keys=new Set();data.categories.forEach(entry=>{if(categoryIds.has(entry.id))throw new Error(`Doppelte Kategorie ${entry.id}`);categoryIds.add(entry.id);if(!entry.units.some(item=>item.id===entry.defaultUnit))throw new Error(`Standardeinheit fehlt: ${entry.id}`);entry.units.forEach(item=>{const key=favoriteKey(entry.id,item.id);if(keys.has(key))throw new Error(`Doppelte Einheit ${key}`);keys.add(key);if(!Number.isFinite(Number(item.toBase?.factor))||Number(item.toBase.factor)===0||!Number.isFinite(Number(item.toBase?.offset||0)))throw new Error(`Ungültige Umrechnung ${key}`)})});return data}
async function load(){const response=await fetch(new URL(`assets/units.json?v=${RELEASE}`,root),{cache:'no-store'});if(!response.ok)throw new Error(`Einheitendatenbank konnte nicht geladen werden (${response.status}).`);model=validate(await response.json());return model}
const ready=load().then(data=>{document.dispatchEvent(new CustomEvent('sk:units-ready',{detail:{model:data}}));document.querySelectorAll('select[data-unit-category]').forEach(select=>populateSelect(select,select.dataset.unitCategory,select.value||select.dataset.unitPreferred,{includeAll:select.dataset.unitIncludeAll!=='false',preferredUnit:select.dataset.unitPreferred}));return data}).catch(error=>{console.error(error);throw error});
window.SK_UNITS=Object.freeze({release:RELEASE,storageKey:STORAGE_KEY,ready,get model(){return model},category,unit,toBase,fromBase,convert,inputValue,format,populateSelect,refreshSelects,loadFavorites,isFavorite,toggleFavorite,subscribe,favoriteKey,escape:esc});
})();
