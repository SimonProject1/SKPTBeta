/* SK PCT Tools 3.1.0.0-Beta — zentraler Wissensbeitrags-Baukasten. */
(()=>{'use strict';
const init=()=>{document.querySelectorAll('details.kb-accordion').forEach(details=>{const summary=details.querySelector(':scope>summary');if(!summary)return;const sync=()=>{summary.setAttribute('aria-expanded',String(details.open));details.dataset.state=details.open?'open':'closed'};details.addEventListener('toggle',sync);sync()});document.body.dataset.kbComponents='ready'};
document.readyState==='loading'?document.addEventListener('DOMContentLoaded',init,{once:true}):init();
})();
