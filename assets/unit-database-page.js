/* Einheitendatenbank · SK PCT Tools 2.6.2.0-Beta — kompakte Kategorien und Favoriten. */
(()=>{'use strict';
const $=id=>document.getElementById(id);
const norm=value=>String(value||'').toLocaleLowerCase('de-DE').normalize('NFD').replace(/[\u0300-\u036f]/g,'').replace(/ß/g,'ss');
function star(active){return `<svg class="sk-star-svg" viewBox="0 0 24 24" aria-hidden="true"><path${active?' class="sk-star-fill"':''} d="M12 2.75l2.82 5.72 6.31.92-4.57 4.45 1.08 6.29L12 17.16l-5.64 2.97 1.08-6.29-4.57-4.45 6.31-.92L12 2.75z"></path></svg>`}
function formula(item){return item.toBase.offset?`Basis = Wert × ${item.toBase.factor} ${item.toBase.offset>=0?'+':'−'} ${Math.abs(item.toBase.offset)}`:`Basis = Wert × ${item.toBase.factor}`}
function favoriteButton(category,item){
  const active=SK_UNITS.isFavorite(category.id,item.id),button=document.createElement('button');
  button.type='button';button.className='unit-favorite-button';button.dataset.unitKey=SK_UNITS.favoriteKey(category.id,item.id);button.dataset.active=String(active);button.setAttribute('aria-pressed',String(active));
  const label=()=>SK_UNITS.isFavorite(category.id,item.id)?`${item.name} aus Favoriten entfernen`:`${item.name} zu Favoriten hinzufügen`;
  button.setAttribute('aria-label',label());button.title=label();button.innerHTML=star(active);
  button.addEventListener('click',event=>{event.stopPropagation();SK_UNITS.toggleFavorite(category.id,item.id);syncFavoriteButtons();renderFavorites()});
  return button;
}
function detailBlock(category,item){
  const details=document.createElement('details');details.className='unit-row-details';
  const aliases=(item.aliases||[]).join(', ')||'—';
  details.innerHTML=`<summary>Details</summary><dl class="unit-detail-grid"><dt>Kategorie</dt><dd>${SK_UNITS.escape(category.name)}</dd><dt>Umrechnung</dt><dd><code>${SK_UNITS.escape(formula(item))}</code></dd><dt>Bezeichnungen</dt><dd>${SK_UNITS.escape(aliases)}</dd></dl>`;
  return details;
}
function unitRow(category,item){
  const row=document.createElement('li');row.className='unit-row';row.dataset.unitKey=SK_UNITS.favoriteKey(category.id,item.id);row.dataset.search=norm([category.name,item.name,item.symbol,...(item.aliases||[])].join(' '));
  const main=document.createElement('div');main.className='unit-main';main.innerHTML=`<strong>${SK_UNITS.escape(item.symbol)}</strong><span>${SK_UNITS.escape(item.name)}</span>${item.id===category.defaultUnit?'<span class="unit-default-badge">Standard</span>':''}`;
  row.append(favoriteButton(category,item),main,detailBlock(category,item));return row;
}
function categoryCard(category){
  const details=document.createElement('details');details.className='panel unit-category-card';details.dataset.category=category.id;details.dataset.search=norm(`${category.name} ${category.description}`);
  const summary=document.createElement('summary');summary.className='unit-category-head';summary.innerHTML=`<div><div class="eyebrow">EINHEITENKATEGORIE</div><h2>${SK_UNITS.escape(category.name)}</h2><p class="unit-category-description">${SK_UNITS.escape(category.description)}</p></div><span class="unit-category-count">${category.units.length}</span>`;
  const list=document.createElement('ul');list.className='unit-list';category.units.forEach(item=>list.append(unitRow(category,item)));details.append(summary,list);return details;
}
function favoriteEntries(){const keys=new Set(SK_UNITS.loadFavorites());const result=[];SK_UNITS.model.categories.forEach(category=>category.units.forEach(item=>{if(keys.has(SK_UNITS.favoriteKey(category.id,item.id)))result.push([category,item])}));return result}
function renderFavorites(){
  const list=$('unitFavoritesList'),empty=$('unitFavoritesEmpty'),count=$('unitFavoriteCount');if(!list)return;
  const favorites=favoriteEntries();list.replaceChildren(...favorites.map(([category,item])=>unitRow(category,item)));empty.hidden=favorites.length!==0;count.textContent=String(favorites.length);
  document.dispatchEvent(new CustomEvent('sk:cards-updated',{detail:{source:'unit-favorites'}}));
}
function syncFavoriteButtons(){document.querySelectorAll('.unit-favorite-button[data-unit-key]').forEach(button=>{const [categoryId,unitId]=button.dataset.unitKey.split(':'),active=SK_UNITS.isFavorite(categoryId,unitId),item=SK_UNITS.unit(categoryId,unitId);button.dataset.active=String(active);button.setAttribute('aria-pressed',String(active));button.setAttribute('aria-label',active?`${item.name} aus Favoriten entfernen`:`${item.name} zu Favoriten hinzufügen`);button.title=button.getAttribute('aria-label');button.innerHTML=star(active)})}
function render(){
  const model=SK_UNITS.model,filter=$('unitCategoryFilter'),host=$('unitCategoryList');
  filter.innerHTML='<option value="all">Alle Kategorien</option>'+model.categories.map(category=>`<option value="${category.id}">${SK_UNITS.escape(category.name)}</option>`).join('');
  host.replaceChildren(...model.categories.map(categoryCard));renderFavorites();apply();
}
function apply(){
  const query=norm($('unitSearch').value).trim(),categoryId=$('unitCategoryFilter').value||'all';let visibleCategories=0,visibleUnits=0;
  document.querySelectorAll('#unitCategoryList .unit-category-card').forEach(card=>{let categoryUnits=0;card.querySelectorAll('.unit-row').forEach(row=>{const matchCategory=categoryId==='all'||card.dataset.category===categoryId,matchQuery=!query||`${card.dataset.search} ${row.dataset.search}`.includes(query),show=matchCategory&&matchQuery;row.hidden=!show;if(show)categoryUnits++});card.hidden=categoryUnits===0;if(categoryUnits){visibleCategories++;visibleUnits+=categoryUnits}if(query||categoryId!=='all')card.open=categoryUnits>0});
  $('unitResult').textContent=`${visibleUnits} ${visibleUnits===1?'Einheit':'Einheiten'} in ${visibleCategories} ${visibleCategories===1?'Kategorie':'Kategorien'}`;$('unitEmpty').hidden=visibleUnits!==0;
}
async function init(){
  await SK_UNITS.ready;render();
  $('unitSearch').addEventListener('input',apply);$('unitCategoryFilter').addEventListener('change',apply);
  $('unitReset').addEventListener('click',()=>{$('unitSearch').value='';$('unitCategoryFilter').value='all';document.querySelectorAll('#unitCategoryList .unit-category-card').forEach(card=>card.open=false);apply();$('unitSearch').focus()});
  SK_UNITS.subscribe(()=>{syncFavoriteButtons();renderFavorites()});
}
document.readyState==='loading'?document.addEventListener('DOMContentLoaded',init,{once:true}):init();
})();
