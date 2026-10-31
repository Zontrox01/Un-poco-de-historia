/* Visor común (index.html y galeria.html): tarjetas de foto/vídeo y visor sobre fondo negro.
   Los vídeos se abren a pantalla completa y en bucle. */
const Visor=(()=>{
const BUCLE_AUDIO=false; // true = el audio se repite en bucle
let lb,L=[],cur=0;
const el=(t,c,x)=>{const e=document.createElement(t);if(c)e.className=c;if(x!=null)e.textContent=x;return e};
function tarjeta(o,lista,i){
 const c=el("div","obra"+(o.medio&&o.medio!="imagen"?" "+o.medio:"")),im=el("div","img"),a=el("a"),t=el("img"),inf=el("div","info"),m=el("div","om");
 c.dataset.t=(o.titulo+" "+(o.detalle||"")).toLowerCase();
 a.href=o.imagen;t.src=o.miniatura||o.imagen;t.alt=o.titulo;t.loading="lazy";
 if(o.medio=="pdf"){a.target="_blank";a.rel="noopener"}else a.onclick=e=>{e.preventDefault();abrir(lista,i)};
 a.append(t);im.append(a);inf.append(el("div","ot",o.titulo));if(o.detalle)inf.append(el("div","od",o.detalle));
 m.append(el("span",0,o.tipo||""),el("span",0,o.fecha||""));inf.append(m);c.append(im,inf);return c}
function mostrar(){
 lb.replaceChildren();const o=L[cur],v=o.medio=="video";let m;
 const au=o.medio=="audio";let w=null;
 if(v){m=el("video");m.src=o.imagen;m.loop=true;m.autoplay=true;m.controls=true}
 else if(au){m=el("audio");m.src=o.imagen;m.controls=true;m.autoplay=true;m.loop=BUCLE_AUDIO;w=el("div","aud");w.append(el("p",0,o.titulo),m)}
 else{m=el("img");m.src=o.imagen;m.alt=o.titulo}
 const b=el("button",0,"Cerrar");b.onclick=e=>{e.stopPropagation();cerrar()};lb.append(w||m,b);
 if(au)m.play().catch(()=>{});
 if(v){m.play().catch(()=>{});entrar(m)}}
function entrar(v){try{const f=lb.requestFullscreen||lb.webkitRequestFullscreen;if(f)f.call(lb);else if(v.webkitEnterFullscreen)v.webkitEnterFullscreen()}catch(e){}}
function abrir(lista,i){L=lista;cur=i;if(!lb){lb=el("div","lb");lb.onclick=e=>{if(e.target===lb||e.target.tagName=="IMG")cerrar()};document.body.append(lb)}mostrar()}
function cerrar(){if(document.fullscreenElement)document.exitFullscreen().catch(()=>{});if(lb){lb.remove();lb=null}}
function ir(d){let n=L.length;do{cur=(cur+d+L.length)%L.length}while(L[cur].medio=="pdf"&&n--);mostrar()}
document.addEventListener("keydown",e=>{if(!lb)return;if(e.key=="Escape")cerrar();if(e.key=="ArrowRight")ir(1);if(e.key=="ArrowLeft")ir(-1)});
document.addEventListener("fullscreenchange",()=>{if(!document.fullscreenElement&&lb)cerrar()});
return {tarjeta,abrir,cerrar,el}})();
