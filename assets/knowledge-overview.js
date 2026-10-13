/* SK PCT Tools 2.5.0.6-Beta — Hersteller-Hub, Herstelleransichten, Suche und Kompaktansicht. */
(()=>{'use strict';
  const RELEASE='2.5.0.6-Beta';
  const COMPACT_KEY='skKnowledgeCompactCardsV1';
  const read=(key,fallback)=>{try{const value=JSON.parse(localStorage.getItem(key));return value??fallback}catch{return fallback}};
  const write=(key,value)=>{try{localStorage.setItem(key,JSON.stringify(value))}catch{}};
  const norm=value=>String(value||'').toLocaleLowerCase('de-DE').normalize('NFD').replace(/[\u0300-\u036f]/g,'').replace(/ß/g,'ss').replace(/[^a-z0-9+]+/g,' ').trim();

  function init(){
    const input=document.getElementById('knowledgeSearch');
    const hub=document.getElementById('knowledgeHub');
    const views=document.getElementById('knowledgeViews');
    const empty=document.getElementById('knowledgeEmpty');
    const resultCount=document.getElementById('knowledgeResultCount');
    const title=document.getElementById('knowledgeTitle');
    const kicker=document.getElementById('knowledgeKicker');
    const description=document.getElementById('knowledgeDescription');
    const back=document.getElementById('knowledgeViewBack');
    const displayControls=document.getElementById('knowledgeDisplayControls');
    const compactToggle=document.getElementById('knowledgeCompactToggle');
    const compactState=document.getElementById('knowledgeCompactState');
    if(!input||!hub||!views)return;

    const hubCards=[...hub.querySelectorAll('.knowledge-hub-card')];
    const manufacturerViews=[...views.querySelectorAll('.knowledge-manufacturer-view')];
    const viewBySlug=new Map(manufacturerViews.map(view=>[view.dataset.manufacturerSlug,view]));
    let activeView=null;

    const setCompact=(enabled,persist=true)=>{
      document.body.classList.toggle('sk-knowledge-compact-view',enabled);
      compactToggle?.setAttribute('aria-pressed',String(enabled));
      compactToggle?.classList.toggle('active',enabled);
      if(compactState)compactState.textContent=enabled?'Ein':'Aus';
      if(persist)write(COMPACT_KEY,enabled);
    };
    setCompact(Boolean(read(COMPACT_KEY,true)),false);
    compactToggle?.addEventListener('click',()=>setCompact(compactToggle.getAttribute('aria-pressed')!=='true'));

    function currentSlug(){
      const slug=new URL(location.href).searchParams.get('manufacturer');
      return slug&&viewBySlug.has(slug)?slug:null;
    }
    function announceCards(){
      document.dispatchEvent(new CustomEvent('sk:cards-updated',{detail:{source:'knowledge-index',version:RELEASE}}));
    }
    function showMode(){
      const slug=currentSlug();
      activeView=slug?viewBySlug.get(slug):null;
      const onHub=!activeView;
      document.body.classList.toggle('knowledge-mode-hub',onHub);
      document.body.classList.toggle('knowledge-mode-manufacturer',!onHub);
      hub.hidden=!onHub;
      views.hidden=onHub;
      back.hidden=onHub;
      displayControls.hidden=onHub;
      manufacturerViews.forEach(view=>{view.hidden=view!==activeView});
      input.value='';
      if(onHub){
        kicker.textContent='HERSTELLER-HUB';
        title.textContent='Wissensdatenbank';
        description.textContent='Hersteller wählen und direkt zum passenden Know-how wechseln.';
        input.placeholder='Hersteller, Gerät oder Thema eingeben';
        document.title='Wissensdatenbank | SK PCT Tools';
      }else{
        const manufacturer=activeView.dataset.manufacturer;
        kicker.textContent='HERSTELLER-KNOW-HOW';
        title.textContent=manufacturer;
        description.textContent=activeView.dataset.description||`Wissensbeiträge von ${manufacturer}.`;
        input.placeholder=`${manufacturer}: Gerät oder Thema suchen`;
        document.title=`${manufacturer} · Wissensdatenbank | SK PCT Tools`;
      }
      applyFilter();
      announceCards();
    }
    function matches(element,query){
      if(!query)return true;
      const text=norm(`${element.dataset.search||''} ${element.dataset.manufacturer||''} ${element.textContent||''}`);
      return query.split(/\s+/).every(term=>text.includes(term));
    }
    function applyFilter(){
      const query=norm(input.value);
      if(!activeView){
        let visible=0;
        hubCards.forEach(card=>{const show=matches(card,query);card.hidden=!show;if(show)visible++});
        empty.classList.toggle('show',visible===0);
        empty.textContent='Keine passenden Hersteller oder Wissensbeiträge gefunden.';
        if(resultCount)resultCount.textContent=`${visible} ${visible===1?'Hersteller-Bereich':'Hersteller-Bereiche'} angezeigt`;
        return;
      }
      const cards=[...activeView.querySelectorAll('.knowledge-entry')];
      let visible=0;
      cards.forEach(card=>{const show=matches(card,query);card.hidden=!show;if(show)visible++});
      const permanentEmpty=activeView.querySelector('.knowledge-section-empty');
      if(permanentEmpty)permanentEmpty.hidden=cards.length>0||Boolean(query);
      const noMatch=cards.length>0&&visible===0;
      empty.classList.toggle('show',noMatch);
      empty.textContent='Keine passenden Wissensbeiträge gefunden.';
      if(resultCount)resultCount.textContent=`${visible} ${visible===1?'Beitrag':'Beiträge'} angezeigt`;
    }

    input.addEventListener('input',applyFilter);
    window.addEventListener('popstate',showMode);
    hub.addEventListener('click',event=>{
      const link=event.target.closest('.knowledge-hub-card');
      if(!link||event.defaultPrevented||event.button>0||event.metaKey||event.ctrlKey||event.shiftKey||event.altKey)return;
      event.preventDefault();
      history.pushState({},'',link.href);
      showMode();
      title.focus?.({preventScroll:true});
      scrollTo({top:0,behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth'});
    });
    back.addEventListener('click',event=>{
      if(event.defaultPrevented||event.button>0||event.metaKey||event.ctrlKey||event.shiftKey||event.altKey)return;
      event.preventDefault();
      history.pushState({},'',back.href);
      showMode();
      scrollTo({top:0,behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth'});
    });
    showMode();
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init,{once:true});else init();
})();
