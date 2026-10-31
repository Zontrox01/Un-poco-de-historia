(function(){
const $=s=>document.querySelector(s);
const slug=s=>(s||"").normalize("NFKD").replace(/[\u0300-\u036f]/g,"").toLowerCase().replace(/[^a-z0-9]+/g,"-").replace(/^-|-$/g,"");
const k=slug(new URLSearchParams(location.search).get("g"));
fetch("galerias.json").then(r=>r.json()).then(G=>{
const g=G[k],R=$("#rejilla");
if(!g){$("#gt").textContent="Galería no encontrada";const d=$("#gd");d.textContent="Galerías disponibles: ";
 Object.keys(G).forEach(n=>{const a=document.createElement("a");a.href="galeria.html?g="+n;a.textContent=G[n].titulo;d.append(a," · ")});return}
document.title=g.titulo+" · Un poco de historia";$("#gt").textContent=g.titulo;$("#gd").textContent=g.descripcion||"";
g.items.forEach((o,i)=>R.append(Visor.tarjeta(o,g.items,i)));
$("#q").oninput=e=>{const q=e.target.value.toLowerCase();R.childNodes.forEach(c=>c.hidden=q&&!c.dataset.t.includes(q))};
}).catch(()=>{$("#gd").textContent="No se pudo cargar galerias.json."});
})();
