(()=>{'use strict';
function init(){
  const image=document.getElementById('moduleLogo');
  if(!image)return;
  const sources=['../assets/logo.png','../assets/icon-512.png','../assets/apple-touch-icon.png'];
  let index=Math.max(0,sources.indexOf(image.getAttribute('src')));
  image.addEventListener('error',()=>{
    index+=1;
    if(index<sources.length){image.src=sources[index];return}
    image.hidden=true;
    document.documentElement.classList.add('sk-module-logo-missing');
  });
}
document.readyState==='loading'?document.addEventListener('DOMContentLoaded',init,{once:true}):init();
})();
