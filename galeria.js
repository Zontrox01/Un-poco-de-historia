(function(){
const k=new URLSearchParams(location.search).get("g"),$=s=>document.querySelector(s);
fetch("galerias.json").then(r=>r.json()).then(G=>{
const g=G[k]||G[Object.keys(G)[0]],R=$("#rejilla");
document.title=g.titulo+" · Un poco de historia";$("#gt").textContent=g.titulo;$("#gd").textContent=g.descripcion||"";
g.items.forEach((o,i)=>R.append(Visor.tarjeta(o,g.items,i)));
$("#q").oninput=e=>{const q=e.target.value.toLowerCase();R.childNodes.forEach(c=>c.hidden=q&&!c.dataset.t.includes(q))};
}).catch(()=>{$("#gd").textContent="No se pudo cargar galerias.json."});
})();
