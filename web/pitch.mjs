import {pitchMaterial} from './pitch-content.mjs';
export function createPitch(root,release,onSlide,onObserve=()=>{}) {
 const slides=pitchMaterial(release);
 root.innerHTML=`<div class="pitch-toolbar"><button id="pitchPrev">Previous</button><span id="pitchCounter" aria-live="polite"></span><button id="pitchNext">Next</button><button id="pitchFullscreen">Fullscreen</button><label><input type="checkbox" id="pitchNotes"> Presenter notes</label><button id="pitchPrint">Print / PDF</button><a href="/assets/ember-atlas-pitch.pdf">PDF snapshot</a></div><div class="pitch-deck">${slides.map((s,i)=>`<section class="pitch-slide" id="slide-${i+1}" aria-labelledby="slide-title-${i+1}"><p class="slide-label">${i+1} / ${slides.length} · ${s.label}</p><h1 id="slide-title-${i+1}">${s.title}</h1><div class="slide-body">${s.body}</div><aside class="presenter-notes" hidden><h2>Presenter notes</h2><p>${s.notes}</p></aside></section>`).join('')}</div>`;
 let current=1,frame=0;
 const sections=[...root.querySelectorAll('.pitch-slide')];
 function paint(n){current=n;sections.forEach((s,i)=>s.classList.toggle('active',i===n-1));root.querySelector('#pitchCounter').textContent=`Slide ${n} of ${slides.length}`;root.querySelector('#pitchPrev').disabled=n===1;root.querySelector('#pitchNext').disabled=n===slides.length;}
 const change=delta=>onSlide(Math.max(1,Math.min(slides.length,current+delta)));
 root.querySelector('#pitchPrev').onclick=()=>change(-1);root.querySelector('#pitchNext').onclick=()=>change(1);
 root.querySelector('#pitchFullscreen').onclick=async()=>{try{if(document.fullscreenElement)await document.exitFullscreen();else await root.requestFullscreen();}catch{root.querySelector('#pitchFullscreen').textContent='Fullscreen unavailable';}};
 root.querySelector('#pitchNotes').onchange=e=>root.querySelectorAll('.presenter-notes').forEach(n=>n.hidden=!e.target.checked);
 root.querySelector('#pitchPrint').onclick=()=>window.print();
 const mobile=()=>matchMedia('(max-width:700px)').matches;
 // Scroll reading and button navigation have one counter and one inspectable URL.
 function observe(){
  if(frame||root.hidden||location.pathname!=='/pitch'||!mobile())return;
  frame=requestAnimationFrame(()=>{
   frame=0;
   // A queued scroll must not restore the pitch URL after an Explore link starts loading.
   if(root.hidden||location.pathname!=='/pitch'||!mobile())return;
   const toolbar=root.querySelector('.pitch-toolbar').getBoundingClientRect(),top=Math.max(0,toolbar.bottom),bottom=innerHeight;
   const heights=sections.map(s=>{const r=s.getBoundingClientRect();return Math.max(0,Math.min(bottom,r.bottom)-Math.max(top,r.top));});
   const maximum=Math.max(...heights),n=heights.indexOf(maximum)+1;
   if(maximum>0&&n!==current){paint(n);onObserve(n);}
  });
 }
 window.addEventListener('scroll',observe,{passive:true});window.addEventListener('resize',observe,{passive:true});root.addEventListener('scroll',observe,{passive:true});
 document.addEventListener('keydown',e=>{
  if(root.hidden||e.altKey||e.ctrlKey||e.metaKey||e.target.matches('input,select,textarea,[contenteditable]'))return;
  if(e.key===' '&&e.target.closest('button,a,summary'))return;
  if(mobile()&&['ArrowDown','ArrowUp',' '].includes(e.key))return;
  if(['ArrowRight','ArrowDown','PageDown',' '].includes(e.key)){e.preventDefault();change(1);}
  if(['ArrowLeft','ArrowUp','PageUp'].includes(e.key)){e.preventDefault();change(-1);}
  if(e.key==='Home'){e.preventDefault();onSlide(1);}if(e.key==='End'){e.preventDefault();onSlide(slides.length);}
 });
 return {setSlide(n,scroll=false){paint(n);if((scroll||n>1)&&mobile())sections[n-1].scrollIntoView({block:'start',behavior:'instant'});},slides};
}
