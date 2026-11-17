// Qhawana · Consulta de avisos del SENAMHI (lluvia y ríos)
// Uso (lo hace Claude o una persona de datos, en un navegador en el Perú; el SENAMHI no responde a servidores de fuera):
//  1. Abre https://www.senamhi.gob.pe/?p=aviso-meteorologico y, en la consola, corre PASO 1. Copia el resultado.
//  2. Abre https://idesep.senamhi.gob.pe/geoserver/ows?service=WFS&request=GetCapabilities y corre PASO 2,
//     pegando en AVISOS la lista del paso 1. Descarga avisos_lluvia_AAAA-MM-DD.txt.
//  3. Abre https://www.senamhi.gob.pe/?p=avisos-hidrologicos y corre PASO 3. Descarga avisos_rios_AAAA-MM-DD.txt.
//  4. python herramientas/procesar_avisos_senamhi.py <lluvia.txt> <rios.txt>
// Solo consulta avisos públicos y límites del INEI. No descarga datos de personas.

// PASO 1 · lista de avisos de lluvia (página de avisos meteorológicos)
const DESDE = "2026-09-01";
(() => {
  const tx = h => { const e = document.createElement("div"); e.innerHTML = h; return e.textContent.trim(); };
  const d = jQuery("table").first().DataTable().rows().data().toArray();
  return d.map(r => [tx(r[1]).replace(/\s*\(.*$/, "").trim(), tx(r[0]), r[2], r[3], r[4], tx(r[6])])
    .filter(x => x[3] >= DESDE && /PRECIPITAC|LLUVIA/i.test(x[1]) && !/CANCELAD/i.test(x[1]))
    .map(x => x.join("|")).join("\n");
})();

// PASO 2 · zonas de cada aviso cruzadas con los departamentos (servidor IDESEP)
// Pega aquí el resultado del paso 1 entre las comillas invertidas:
const AVISOS = ``;
(async () => {
  const anio = DESDE.slice(0, 4);
  const X0 = -81.5, X1 = -68.5, Y0 = -18.5, Y1 = 0.1, R = 0.02;              // cuadrícula de ~2 km
  const W = Math.ceil((X1 - X0) / R), H = Math.ceil((Y1 - Y0) / R);
  const cx = new OffscreenCanvas(W, H).getContext("2d");
  const px = (x, y) => [(x - X0) / R, (Y1 - y) / R];
  const draw = g => { cx.beginPath(); for (const p of (g.type === "Polygon" ? [g.coordinates] : g.coordinates)) for (const ring of p) {
    ring.forEach(([x, y], i) => { const [a, b] = px(x, y); i ? cx.lineTo(a, b) : cx.moveTo(a, b); }); cx.closePath(); } cx.fill("evenodd"); };
  const mask = gs => { cx.clearRect(0, 0, W, H); cx.fillStyle = "#fff"; gs.forEach(draw);
    const d = cx.getImageData(0, 0, W, H).data, m = new Uint8Array(W * H); for (let i = 0; i < W * H; i++) m[i] = d[i * 4 + 3] > 127 ? 1 : 0; return m; };
  const wfs = q => fetch("/geoserver/ows?service=WFS&version=1.0.0&request=GetFeature&outputFormat=application/json&" + q).then(r => r.json());
  const dep = await wfs("typeName=g_carto_fundamento:departamentos&propertyName=departamento,geom");
  const id = new Uint8Array(W * H), nom = [], tot = [];
  dep.features.forEach((f, k) => { const m = mask([f.geometry]); nom.push(f.properties.departamento); let c = 0;
    for (let i = 0; i < m.length; i++) if (m[i] && !id[i]) { id[i] = k + 1; c++; } tot.push(c); });
  const filas = [];
  for (const l of AVISOS.trim().split("\n")) {
    const n = l.split("|")[0];
    for (let mp = 1; mp <= 7; mp++) {
      const j = await wfs(`typeName=g_aviso:view_aviso&viewparams=qry:${n}_${mp}_${anio}&cql_filter=${encodeURIComponent("nivel<>'Nivel 1'")}`);
      if (!j.features.length) break;
      const fecha = (j.features[0].properties.fech_ini || "").slice(0, 10), cnt = {};
      for (const lv of [2, 3, 4]) { const gs = j.features.filter(f => +f.properties.nivel.replace(/\D/g, "") >= lv).map(f => f.geometry);
        if (!gs.length) continue; const m = mask(gs), c = new Array(nom.length).fill(0);
        for (let i = 0; i < m.length; i++) if (m[i] && id[i]) c[id[i] - 1]++; cnt[lv] = c; }
      nom.forEach((dn, k) => { const p = lv => cnt[lv] ? Math.round(cnt[lv][k] / tot[k] * 1000) / 10 : 0;
        if (p(2) >= 5) filas.push([n, mp, fecha, dn, p(2), p(3), p(4)].join("|")); });
    }
  }
  const txt = "#AVISOS\n" + AVISOS.trim() + "\n#ZONAS\n" + filas.join("\n");
  const a = document.createElement("a"); a.href = URL.createObjectURL(new Blob([txt])); a.download = `avisos_lluvia_${new Date().toISOString().slice(0, 10)}.txt`; a.click();
  return filas.length + " filas";
})();

// PASO 3 · avisos de ríos (página de avisos hidrológicos)
(() => {
  const tx = h => { const e = document.createElement("div"); e.innerHTML = h; return e.textContent.trim(); };
  const d = jQuery("table").first().DataTable().rows().data().toArray();
  const txt = d.map(r => [tx(r[1]).replace(/\s*\(.*$/, ""), tx(r[0]), r[2], r[3], r[4], tx(r[5])]).filter(x => x[2] >= DESDE).map(x => x.join("|")).join("\n");
  const a = document.createElement("a"); a.href = URL.createObjectURL(new Blob([txt])); a.download = `avisos_rios_${new Date().toISOString().slice(0, 10)}.txt`; a.click();
  return txt.split("\n").length + " avisos";
})();
