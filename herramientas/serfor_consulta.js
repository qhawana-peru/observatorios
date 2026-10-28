// Qhawana · Consulta del corte de incendios a SERFOR
// Uso: abre en el navegador
//   https://geo.serfor.gob.pe/geoservicios/rest/services/UFMS/Incendios_SAMIv21/MapServer
// abre la consola (F12 › Consola), pega TODO este archivo y pulsa Enter.
// Descarga un archivo serfor_AAAA-MM-DD.json. Súbelo a incendios/cortes/ y
// corre herramientas/actualizar_incendios.py (lo hace la automatización).
// Solo consulta conteos agregados: no descarga datos de personas.
(async () => {
  const BASE = "https://geo.serfor.gob.pe/geoservicios/rest/services/UFMS/Incendios_SAMIv21/MapServer/";
  const REGIONES = { CUSCO: "Cusco", CAJAMARCA: "Cajamarca" };
  const NPP = "SENSAT IN ('N','NPP')";
  const hoy = new Date();
  const corte = `${hoy.getFullYear()}-${String(hoy.getMonth() + 1).padStart(2, "0")}-${String(hoy.getDate()).padStart(2, "0")}`;
  const anio = hoy.getFullYear();
  const md = corte.slice(5);
  const iso = t => new Date(t).toISOString().slice(0, 10);
  const manana = y => { const d = new Date(Date.UTC(y, +md.slice(0, 2) - 1, +md.slice(3) + 1)); return iso(d); };
  const stats = encodeURIComponent(JSON.stringify([
    { statisticType: "count", onStatisticField: "OBJECTID", outStatisticFieldName: "n" },
    { statisticType: "min", onStatisticField: "FECHA", outStatisticFieldName: "desde" },
    { statisticType: "max", onStatisticField: "FECHA", outStatisticFieldName: "hasta" }]));
  async function q(capa, where, extra = "") {
    const r = await fetch(`${BASE}${capa}/query?f=json&where=${encodeURIComponent(where)}${extra}`);
    const j = await r.json();
    if (j.error) throw new Error(`SERFOR capa ${capa}: ${JSON.stringify(j.error)}`);
    return j;
  }
  const contar = async (capa, where) => (await q(capa, where, "&returnCountOnly=true")).count;
  const agrupar = async (capa, where, campo) => (await q(capa, where,
    `&outStatistics=${stats}${campo ? "&groupByFieldsForStatistics=" + campo : ""}`)).features.map(f => {
      const a = f.attributes; return { clave: campo ? a[campo] : null, n: a.n, desde: a.desde ? iso(a.desde) : null, hasta: a.hasta ? iso(a.hasta) : null };
    });
  const out = { corte, consultado: new Date().toISOString(), servicio: BASE, regiones: {}, peru: {} };
  out.peru.alertas = (await agrupar(0, "1=1"))[0];
  out.peru.focos_3d = (await agrupar(2, "1=1"))[0];
  // Panorama nacional: todos los departamentos, con pocas consultas agrupadas por NOMDEP.
  console.log("Consultando todos los departamentos …");
  const porDep = async (capa, where, campos) => (await q(capa, where,
    `&outStatistics=${stats}&groupByFieldsForStatistics=${campos}`)).features.map(f => f.attributes);
  out.departamentos = { alertas_estado: [], focos_3d: {}, focos_anual: {} };
  for (const a of await porDep(0, "1=1", "NOMDEP,ESTADO"))
    out.departamentos.alertas_estado.push({ dep: a.NOMDEP, estado: a.ESTADO, n: a.n,
      desde: a.desde ? iso(a.desde) : null, hasta: a.hasta ? iso(a.hasta) : null });
  for (const a of await porDep(2, "1=1", "NOMDEP")) out.departamentos.focos_3d[a.NOMDEP] = a.n;
  for (const y of [anio - 2, anio - 1, anio]) {
    out.departamentos.focos_anual[y] = {};
    for (const a of await porDep(3, `FECHA>=DATE '${y}-01-01' AND FECHA<DATE '${manana(y)}'`, "NOMDEP"))
      out.departamentos.focos_anual[y][a.NOMDEP] = a.n;
  }
  for (const [dep, nombre] of Object.entries(REGIONES)) {
    console.log("Consultando", nombre, "…");
    const R = {};
    R.alertas_estado = await agrupar(0, `NOMDEP='${dep}'`, "ESTADO");
    R.alertas_provincia = await agrupar(0, `NOMDEP='${dep}'`, "NOMPRO");
    R.focos_3d = (await agrupar(2, `NOMDEP='${dep}'`))[0] || { n: 0, desde: null, hasta: null };
    R.focos_anual = {};
    for (const y of [anio - 2, anio - 1, anio])
      R.focos_anual[y] = await contar(3, `NOMDEP='${dep}' AND FECHA>=DATE '${y}-01-01' AND FECHA<DATE '${manana(y)}'`);
    R.npp = {};
    for (let y = 2012; y <= anio; y++) {
      if (y === 2022) continue;
      const hasta = await contar(3, `NOMDEP='${dep}' AND ${NPP} AND FECHA>=DATE '${y}-01-01' AND FECHA<DATE '${manana(y)}'`);
      const total = y < anio ? await contar(3, `NOMDEP='${dep}' AND ${NPP} AND FECHA>=DATE '${y}-01-01' AND FECHA<DATE '${y + 1}-01-01'`) : null;
      R.npp[y] = { hasta_corte: hasta, total_anio: total };
    }
    const dias = await agrupar(3, `NOMDEP='${dep}' AND ${NPP} AND FECHA>=DATE '${anio}-01-01' AND FECHA<DATE '${manana(anio)}'`, "FECHA");
    R.npp_diario = Object.fromEntries(dias.map(d => [iso(d.clave), d.n]).sort());
    out.regiones[nombre] = R;
  }
  const texto = JSON.stringify(out, null, 1);
  const a = document.createElement("a");
  a.href = URL.createObjectURL(new Blob([texto], { type: "application/json" }));
  a.download = `serfor_${corte}.json`;
  document.body.appendChild(a); a.click(); a.remove();
  console.log(`Listo: se descargó serfor_${corte}.json`);
  return out;
})();
