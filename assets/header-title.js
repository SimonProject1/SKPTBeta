/* SK PCT Tools 2.4.1.7 · einzeilige, responsive Haupttitel */
(()=>{'use strict';
  const SELECTOR='.sk-page-heading h1';
  const MIN_FONT_SIZE=10;
  let frame=0;
  function setSize(title,value){title.style.setProperty('font-size',`${value}px`,'important')}
  function fitTitle(title){
    title.style.removeProperty('font-size');
    const preferred=parseFloat(getComputedStyle(title).fontSize)||52;
    setSize(title,preferred);
    const available=Math.max(1,title.clientWidth);
    if(title.scrollWidth<=available+1)return;
    let low=MIN_FONT_SIZE,high=preferred;
    for(let i=0;i<12;i++){
      const mid=(low+high)/2;
      setSize(title,mid);
      if(title.scrollWidth<=available+1)low=mid;else high=mid;
    }
    setSize(title,Math.max(MIN_FONT_SIZE,low-.2).toFixed(2));
  }
  function fitAll(){document.querySelectorAll(SELECTOR).forEach(fitTitle)}
  function schedule(){cancelAnimationFrame(frame);frame=requestAnimationFrame(fitAll)}
  function init(){
    fitAll();
    if(document.fonts?.ready)document.fonts.ready.then(schedule).catch(()=>{});
    if('ResizeObserver' in window){
      const observer=new ResizeObserver(schedule);
      document.querySelectorAll('.sk-page-heading').forEach(node=>observer.observe(node));
    }else window.addEventListener('resize',schedule,{passive:true});
    window.addEventListener('orientationchange',schedule,{passive:true});
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init,{once:true});else init();
})();
