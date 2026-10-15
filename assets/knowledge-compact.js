/* SK PCT Tools 2.6.0.2-Beta — progressive Verdichtung langer Wissensbeiträge. */
(()=>{'use strict';
function compact(){
  const article=document.querySelector('.knowledge-standard article');if(!article||article.dataset.compactReady==='true')return;article.dataset.compactReady='true';
  const sections=[...article.querySelectorAll(':scope > .kb-section')];if(!sections.length)return;
  const meta=sections.find(section=>section.getAttribute('aria-label')==='Beitragsmetadaten');if(meta)meta.classList.add('kb-meta-section');
  const contentSections=sections.filter(section=>section!==meta);
  const shortAnswer=contentSections[0];
  if(shortAnswer){shortAnswer.classList.add('kb-short-answer');const badge=document.createElement('div');badge.className='kb-short-answer-label';badge.textContent='Kurzantwort';shortAnswer.prepend(badge)}

  const sources=[];article.querySelectorAll('.kb-source').forEach(source=>{sources.push(source);source.remove()});
  contentSections.slice(1).forEach(section=>{
    const kicker=section.querySelector(':scope > .kb-kicker')?.textContent.trim()||'Fachdetails';
    const title=section.querySelector(':scope > h2')?.textContent.trim()||'Weitere Informationen';
    const safety=[...section.querySelectorAll(':scope > .kb-callout.danger,:scope > .kb-callout.warning')];safety.forEach(node=>node.remove());
    const details=document.createElement('details');details.className='kb-detail-group';
    const summary=document.createElement('summary');summary.innerHTML=`<span class="kb-detail-summary-copy"><small>${escapeText(kicker)}</small><strong>${escapeText(title)}</strong></span>`;
    const content=document.createElement('div');content.className='kb-detail-content';
    while(section.firstChild)content.append(section.firstChild);
    const heading=content.querySelector(':scope > h2');if(heading)heading.classList.add('sr-only');
    const existingKicker=content.querySelector(':scope > .kb-kicker');if(existingKicker)existingKicker.classList.add('sr-only');
    details.append(summary,content);section.classList.add('kb-collapsible');section.append(details);
    safety.forEach(node=>{node.classList.add('kb-visible-safety');section.append(node)});
  });
  if(sources.length){
    const bundle=document.createElement('details');bundle.className='kb-source-bundle';
    const summary=document.createElement('summary');summary.textContent='Quellen, Gültigkeit und Anwendungshinweise';
    const body=document.createElement('div');body.className='kb-source-bundle-body';sources.forEach(source=>body.append(source));bundle.append(summary,body);article.append(bundle);
  }
}
function escapeText(value){return String(value).replace(/[&<>"']/g,char=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#039;'}[char]))}
document.readyState==='loading'?document.addEventListener('DOMContentLoaded',compact,{once:true}):compact();
})();
