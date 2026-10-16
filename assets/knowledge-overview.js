/* SK PCT Tools 2.6.1.8-Beta — robuster Hersteller-Hub, sichere Beitragsnavigation, Suche und Kompaktansicht. */
(()=>{'use strict';
  const RELEASE='2.6.1.8-Beta';
  const COMPACT_KEY='skKnowledgeCompactCardsV1';
  const {readJSON:read,writeJSON:write,foldText:norm}=window.SK_PCT_SHARED;
  const isPlainActivation=event=>!event.defaultPrevented&&event.button<=0&&!event.metaKey&&!event.ctrlKey&&!event.shiftKey&&!event.altKey;

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
    const scrollHost=document.querySelector('.knowledge-app-scroll');
    if(!input||!hub||!views||!back)return;

    /* Der Skriptpfad liefert die Projektwurzel auch unter GitHub Pages, in einer
       installierten PWA und bei URLs ohne abschließenden Slash zuverlässig. */
    const projectRoot=window.SK_PCT?.root||new URL('../',document.currentScript?.src||location.href);
    const knowledgeRoot=new URL('wissensdatenbank/',projectRoot);
    const hubCards=[...hub.querySelectorAll('.knowledge-hub-card')];
    const manufacturerViews=[...views.querySelectorAll('.knowledge-manufacturer-view')];
    const entries=[...views.querySelectorAll('.knowledge-entry')];
    const viewBySlug=new Map(manufacturerViews.map(view=>[view.dataset.manufacturerSlug,view]));
    let activeView=null;

    /* Alle Ziele werden einmal absolut normalisiert. Damit hängt kein Beitrag
       mehr davon ab, ob die aktuelle Adresse mit /, index.html oder ?manufacturer= endet. */
    back.href=knowledgeRoot.href;
    hubCards.forEach(card=>{card.href=new URL(`?manufacturer=${encodeURIComponent(card.dataset.manufacturerSlug||'')}`,knowledgeRoot).href});
    entries.forEach(entry=>{
      const relative=(entry.getAttribute('href')||'').replace(/^(?:\.\/|\/)+/,'');
      entry.href=new URL(relative,knowledgeRoot).href;
    });

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
    function resetScroll(){
      const behavior=matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth';
      scrollHost?.scrollTo({top:0,behavior});
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
      if(displayControls)displayControls.hidden=onHub;
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
        empty?.classList.toggle('show',visible===0);
        if(empty)empty.textContent='Keine passenden Hersteller oder Wissensbeiträge gefunden.';
        if(resultCount)resultCount.textContent=`${visible} ${visible===1?'Hersteller-Bereich':'Hersteller-Bereiche'} angezeigt`;
        return;
      }
      const cards=[...activeView.querySelectorAll('.knowledge-entry')];
      let visible=0;
      cards.forEach(card=>{const show=matches(card,query);card.hidden=!show;if(show)visible++});
      const permanentEmpty=activeView.querySelector('.knowledge-section-empty');
      if(permanentEmpty)permanentEmpty.hidden=cards.length>0||Boolean(query);
      const noMatch=cards.length>0&&visible===0;
      empty?.classList.toggle('show',noMatch);
      if(empty)empty.textContent='Keine passenden Wissensbeiträge gefunden.';
      if(resultCount)resultCount.textContent=`${visible} ${visible===1?'Beitrag':'Beiträge'} angezeigt`;
    }

    input.addEventListener('input',applyFilter);
    window.addEventListener('popstate',()=>{showMode();resetScroll()});
    hub.addEventListener('click',event=>{
      const link=event.target.closest('.knowledge-hub-card');
      if(!link||!isPlainActivation(event))return;
      event.preventDefault();
      history.pushState({},'',link.href);
      showMode();
      resetScroll();
    });
    back.addEventListener('click',event=>{
      if(!isPlainActivation(event))return;
      event.preventDefault();
      history.pushState({},'',back.href);
      showMode();
      resetScroll();
    });
    /* Explizite Delegation für Karten-Taps: Safari/PWA muss nicht auf das
       verschachtelte Favoritenelement oder die relative Basis-URL vertrauen. */
    views.addEventListener('click',event=>{
      if(event.target.closest('.sk-favorite-button'))return;
      const link=event.target.closest('.knowledge-entry');
      if(!link||!isPlainActivation(event))return;
      event.preventDefault();
      location.assign(link.href);
    });
    showMode();
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init,{once:true});else init();
})();
