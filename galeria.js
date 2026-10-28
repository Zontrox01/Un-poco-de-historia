(function(){
const k=new URLSearchParams(location.search).get("g"),$=s=>document.querySelector(s);
function el(t,c,x){const e=document.createElement(t);if(c)e.className=c;if(x!=null)e.textContent=x;return e}
fetch("galerias.json").then(r=>r.json()).then(G=>{
const g=G[k]||G[Object.keys(G)[0]],L=g.items,R=$("#rejilla");let lb,cur=0;
document.title=g.titulo+" · Un poco de historia";$("#gt").textContent=g.titulo;$("#gd").textContent=g.descripcion||"";
L.forEach((o,i)=>{const c=el("div","obra"),im=el("div","img"),a=el("a"),t=el("img"),inf=el("div","info"),m=el("div","om");
c.dataset.t=(o.titulo+" "+(o.detalle||"")).toLowerCase();a.href=o.imagen;a.dataset.i=i;t.src=o.miniatura||o.imagen;t.alt=o.titulo;t.loading="lazy";
a.append(t);im.append(a);inf.append(el("div","ot",o.titulo));if(o.detalle)inf.append(el("div","od",o.detalle));
m.append(el("span",0,o.tipo||""),el("span",0,o.fecha||""));inf.append(m);c.append(im,inf);R.append(c)});
function ver(i){cur=(i+L.length)%L.length;if(!lb){lb=el("div","lb");lb.append(el("img"),el("button",0,"Cerrar"));lb.onclick=cerrar;document.body.append(lb)}
const im=lb.firstChild;im.src=L[cur].imagen;im.alt=L[cur].titulo}
function cerrar(){if(lb){lb.remove();lb=null}}
R.onclick=e=>{const a=e.target.closest("a[data-i]");if(a){e.preventDefault();ver(+a.dataset.i)}};
document.onkeydown=e=>{if(!lb)return;if(e.key=="Escape")cerrar();if(e.key=="ArrowRight")ver(cur+1);if(e.key=="ArrowLeft")ver(cur-1)};
$("#q").oninput=e=>{const q=e.target.value.toLowerCase();R.childNodes.forEach(c=>c.hidden=q&&!c.dataset.t.includes(q))};
}).catch(()=>{$("#gd").textContent="No se pudo cargar galerias.json."});
})();
