(function(){
const $=s=>document.querySelector(s);
const slug=s=>(s||"").normalize("NFKD").replace(/[\u0300-\u036f]/g,"").toLowerCase().replace(/[^a-z0-9]+/g,"-").replace(/^-|-$/g,"");
const P=new URLSearchParams(location.search),k=slug(P.get("g")),f=(P.get("f")||"").toLowerCase();
function enlace(t,h){const a=document.createElement("a");a.href=h;a.textContent=t;return a}
fetch("galerias.json").then(r=>r.json()).then(G=>{
const g=G[k],R=$("#rejilla"),d=$("#gd");
if(!g){$("#gt").textContent="Galería no encontrada";d.textContent="Galerías disponibles: ";
 Object.keys(G).forEach(n=>d.append(enlace(G[n].titulo,"galeria.html?g="+n)," · "));return}
if(f){const i=g.items.findIndex(o=>{const n=(o.origen||"").toLowerCase();return n==f||n.replace(/\.[^.]+$/,"")==f});
 d.textContent="De la galería ";d.append(enlace(g.titulo,"galeria.html?g="+k));
 if(i<0){$("#gt").textContent="Foto no encontrada";return}
 const o=g.items[i];document.title=o.titulo+" · Un poco de historia";$("#gt").textContent=o.titulo;
 R.classList.add("una");R.append(Visor.tarjeta(o,[o],0));$("#q").hidden=true;return}
document.title=g.titulo+" · Un poco de historia";$("#gt").textContent=g.titulo;d.textContent=g.descripcion||"";
g.items.forEach((o,i)=>R.append(Visor.tarjeta(o,g.items,i)));
$("#q").oninput=e=>{const q=e.target.value.toLowerCase();R.childNodes.forEach(c=>c.hidden=q&&!c.dataset.t.includes(q))};
}).catch(()=>{$("#gd").textContent="No se pudo cargar galerias.json."});
})();
