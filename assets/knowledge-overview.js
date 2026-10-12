/* SK PCT Tools 2.5.0.3-Beta — Suche, kompakte Ansicht und Herstellergruppen der Wissensdatenbank. */
(()=>{'use strict';
  const RELEASE='2.5.0.3-Beta';
  const MOBILE_QUERY='(max-width: 760px), (min-width: 761px) and (max-width: 932px) and (orientation: landscape) and (max-height: 520px)';
  const GROUP_KEY='skKnowledgeManufacturerStateV1';
  const COMPACT_KEY='skKnowledgeCompactCardsV1';
  const read=(key,fallback)=>{try{const value=JSON.parse(localStorage.getItem(key));return value??fallback}catch{return fallback}};
  const write=(key,value)=>{try{localStorage.setItem(key,JSON.stringify(value))}catch{}};
  const slug=value=>String(value||'sonstige').toLocaleLowerCase('de-DE').normalize('NFD').replace(/[\u0300-\u036f]/g,'').replace(/[^a-z0-9]+/g,'-').replace(/^-|-$/g,'')||'sonstige';
  function init(){
    const input=document.getElementById('knowledgeSearch');
    const grid=document.getElementById('knowledgeGrid');
    const empty=document.getElementById('knowledgeEmpty');
    const resultCount=document.getElementById('knowledgeResultCount');
    const compactToggle=document.getElementById('knowledgeCompactToggle');
    const compactState=document.getElementById('knowledgeCompactState');
    if(!input||!grid)return;
    const media=window.matchMedia(MOBILE_QUERY);
    let groupState=read(GROUP_KEY,{}),scheduled=false;
    const cards=()=>[...grid.querySelectorAll('.knowledge-entry')];
    const setCompact=(enabled,persist=true)=>{document.body.classList.toggle('sk-knowledge-compact-view',enabled);compactToggle?.setAttribute('aria-pressed',String(enabled));compactToggle?.classList.toggle('active',enabled);if(compactState)compactState.textContent=enabled?'Ein':'Aus';if(persist)write(COMPACT_KEY,enabled)};
    setCompact(Boolean(read(COMPACT_KEY,true)),false);
    compactToggle?.addEventListener('click',()=>setCompact(compactToggle.getAttribute('aria-pressed')!=='true'));
    function renderGroups(){
      scheduled=false;
      const items=cards();
      if(!items.length)return;
      const detached=document.createDocumentFragment();
      items.forEach(card=>detached.append(card));
      grid.querySelectorAll(':scope > .knowledge-manufacturer').forEach(section=>section.remove());
      if(!media.matches){grid.classList.remove('sk-mobile-manufacturers');grid.append(detached);return}
      const groups=new Map();
      items.forEach(card=>{const key=(card.dataset.manufacturer||'Herstellerunabhängig').trim();if(!groups.has(key))groups.set(key,[]);groups.get(key).push(card)});
      grid.classList.add('sk-mobile-manufacturers');
      const searching=Boolean(input.value.trim());
      groups.forEach((entries,key)=>{
        const id=`knowledge-manufacturer-${slug(key)}`;
        const visible=entries.filter(card=>!card.hidden).length;
        const expanded=searching?true:groupState[key]!==false;
        const section=document.createElement('section');section.className='knowledge-manufacturer';section.dataset.manufacturer=key;section.hidden=visible===0;
        const button=document.createElement('button');button.type='button';button.className='knowledge-manufacturer-toggle';button.setAttribute('aria-expanded',String(expanded));button.setAttribute('aria-controls',id);button.setAttribute('aria-label',`${key} ${expanded?'einklappen':'ausklappen'}`);button.innerHTML=`<span><span class="knowledge-manufacturer-title">${key}</span><span class="knowledge-manufacturer-count">${visible} von ${entries.length}</span></span><span class="knowledge-manufacturer-chevron" aria-hidden="true">⌄</span>`;
        const content=document.createElement('div');content.className='knowledge-manufacturer-entries';content.id=id;content.hidden=!expanded;entries.forEach(card=>content.append(card));section.append(button,content);grid.append(section);
      });
    }
    const scheduleGroups=()=>{if(scheduled)return;scheduled=true;queueMicrotask(renderGroups)};
    function filter(){
      const q=input.value.trim().toLocaleLowerCase('de-DE');let visible=0;
      cards().forEach(card=>{const match=!q||(`${card.dataset.manufacturer||''} ${card.dataset.search||''} ${card.textContent}`).toLocaleLowerCase('de-DE').includes(q);card.hidden=!match;if(match)visible++});
      empty.classList.toggle('show',visible===0);
      if(resultCount)resultCount.textContent=`${visible} ${visible===1?'Beitrag':'Beiträge'} angezeigt`;
      scheduleGroups();
    }
    grid.addEventListener('click',event=>{const button=event.target.closest('.knowledge-manufacturer-toggle');if(!button)return;const section=button.closest('.knowledge-manufacturer'),content=document.getElementById(button.getAttribute('aria-controls')),expanded=button.getAttribute('aria-expanded')!=='true';button.setAttribute('aria-expanded',String(expanded));button.setAttribute('aria-label',`${section.dataset.manufacturer} ${expanded?'einklappen':'ausklappen'}`);if(content)content.hidden=!expanded;groupState[section.dataset.manufacturer]=expanded;write(GROUP_KEY,groupState)});
    input.addEventListener('input',filter);
    if(typeof media.addEventListener==='function')media.addEventListener('change',scheduleGroups);else media.addListener?.(scheduleGroups);
    filter();renderGroups();
    document.dispatchEvent(new CustomEvent('sk:cards-updated',{detail:{source:'knowledge-index',version:RELEASE}}));
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init,{once:true});else init();
})();
