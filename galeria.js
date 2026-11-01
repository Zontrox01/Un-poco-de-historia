(function(){
const $=s=>document.querySelector(s);
const slug=s=>(s||"").normalize("NFKD").replace(/[\u0300-\u036f]/g,"").toLowerCase().replace(/[^a-z0-9]+/g,"-").replace(/^-|-$/g,"");
const P=new URLSearchParams(location.search),k=slug(P.get("g")),fs=P.getAll("f");
function enlace(t,h){const a=document.createElement("a");a.href=h;a.textContent=t;return a}
const vol=$("#volver");if(vol)vol.onclick=e=>{try{if(history.length>1&&document.referrer&&new URL(document.referrer).origin==location.origin){e.preventDefault();history.back()}}catch(_){}};
fetch("galerias.json").then(r=>r.json()).then(G=>{
const R=$("#rejilla"),d=$("#gd");
if(fs.length){const L=[],gs=new Set();
 fs.forEach(x=>{const j=x.indexOf("/"),gk=j>=0?slug(x.slice(0,j)):k,n=(j>=0?x.slice(j+1):x).toLowerCase(),g=G[gk],o=g&&g.items.find(o=>{const m=(o.origen||"").toLowerCase();return m==n||m.replace(/\.[^.]+$/,"")==n});if(o){L.push(o);gs.add(gk)}});
 if(!L.length){$("#gt").textContent="Foto no encontrada";return}
 const gk=[...gs][0],uno=gs.size==1?G[gk]:null,t=L.length==1?L[0].titulo:(uno?uno.titulo:"Fotos seleccionadas");
 $("#gt").textContent=t;document.title=t+" · Un poco de historia";
 if(uno){d.textContent=(L.length>1?L.length+" fotos de la galería ":"De la galería ");d.append(enlace(uno.titulo,"galeria.html?g="+gk))}
 if(L.length==1)R.classList.add("una");
 L.forEach((o,i)=>R.append(Visor.tarjeta(o,L,i)));$("#q").hidden=true;return}
const g=G[k];
if(!g){$("#gt").textContent="Galería no encontrada";d.textContent="Galerías disponibles: ";
 Object.keys(G).forEach(n=>d.append(enlace(G[n].titulo,"galeria.html?g="+n)," · "));return}
document.title=g.titulo+" · Un poco de historia";$("#gt").textContent=g.titulo;d.textContent=g.descripcion||"";
g.items.forEach((o,i)=>R.append(Visor.tarjeta(o,g.items,i)));
$("#q").oninput=e=>{const q=e.target.value.toLowerCase();R.childNodes.forEach(c=>c.hidden=q&&!c.dataset.t.includes(q))};
}).catch(()=>{$("#gd").textContent="No se pudo cargar galerias.json."});
})();
