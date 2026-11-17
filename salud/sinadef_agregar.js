// Agrega el archivo abierto del SINADEF (fallecidos_sinadef.csv, MINSA) sin guardar registros individuales.
// Uso: abrir https://drive.minsa.gob.pe/s/PigmdwnCGEdyqos en un navegador, pegar este script en la consola
// y, al terminar, copiar JSON.stringify(window.__S) a salud/datos/mortalidad_sinadef_agregados.json.
// Después: python3 salud/sinadef_resumen.py
// Tarda unos minutos: el archivo pesa alrededor de 380 MB.
window.__S = {done:false, rows:0, bytes:0, err:null, A:{},B:{},C:{},D:{},E:{},F:{},G:{}, t0:Date.now()};
const S = window.__S;
const cl = v => (v||'').replace(/^"+|"+$/g,'').trim();
const inc = (o,k)=>{o[k]=(o[k]||0)+1};
function code3(v){ v=cl(v).toUpperCase().replace(/[^A-Z0-9]/g,''); return /^[A-Z][0-9][0-9]/.test(v)? v.slice(0,3) : null; }
function rng(c,a,b){ return c>=a && c<=b; }
// Códigos poco informativos como causa final (en la línea de los «garbage codes» de la carga de enfermedad)
const POCO = c => c[0]==='R' || c[0]==='Z' || rng(c,'A40','A41') || c==='I46' || rng(c,'I95','I99') || c==='J96' || rng(c,'E86','E87') || c==='K72' || c==='I50' || (c[0]==='U' && !['U07','U09','U10'].includes(c)) || rng(c,'Y10','Y34');
function clasif(c, viol){
  const V = {'ACCIDENTE DE TRANSITO':'Tránsito','HOMICIDIO':'Homicidios','SUICIDIO':'Suicidios','OTRO ACCIDENTE':'Otras lesiones','ACCIDENTE DE TRABAJO':'Otras lesiones'}[viol];
  if (V) return ['III',V];
  if (!c) return ['X','Sin código registrado'];
  if (POCO(c)) return ['X', c[0]==='R' ? 'Síntomas y signos mal definidos' : 'Códigos poco informativos'];
  const L=c[0];
  if (['U07','U09','U10'].includes(c)) return ['I','COVID-19'];
  if (rng(c,'A00','A09')) return ['I','Enfermedades diarreicas'];
  if (rng(c,'A15','A19')||c==='B90') return ['I','Tuberculosis'];
  if (rng(c,'B20','B24')) return ['I','VIH/sida'];
  if (L==='A'||L==='B'||rng(c,'G00','G03')) return ['I','Otras infecciosas y parasitarias'];
  if (rng(c,'J09','J22')) return ['I','Neumonía, influenza y otras infecciones respiratorias'];
  if (L==='O') return ['I','Maternas'];
  if (L==='P') return ['I','Perinatales'];
  if (rng(c,'D50','D53')||rng(c,'E40','E64')) return ['I','Desnutrición y anemia nutricional'];
  if (L==='C'||rng(c,'D00','D48')) return ['II','Cáncer (neoplasias)'];
  if (L==='I') return ['II','Cardiovasculares'];
  if (rng(c,'E10','E14')) return ['II','Diabetes'];
  if (rng(c,'N00','N29')) return ['II','Enfermedad renal'];
  if (L==='J') return ['II','Respiratorias crónicas y otras'];
  if (L==='K') return ['II','Digestivas (incluye cirrosis)'];
  if (L==='G'||rng(c,'F00','F03')) return ['II','Neurológicas (incluye demencias)'];
  if (L==='F') return ['II','Mentales y consumo de sustancias'];
  if (L==='Q') return ['II','Malformaciones congénitas'];
  if (L==='V') return ['III','Tránsito'];
  if (rng(c,'X60','X84')) return ['III','Suicidios'];
  if (rng(c,'X85','Y09')) return ['III','Homicidios'];
  if (L==='S'||L==='T'||L==='W'||L==='X'||L==='Y') return ['III','Otras lesiones'];
  return ['II','Otras no transmisibles'];
}
function edad(e,t){ e=parseInt(cl(e)); t=cl(t); if (t==='AÑOS') { if(isNaN(e)) return 'sin dato'; return e<1?'<1':e<5?'1-4':e<15?'5-14':e<30?'15-29':e<60?'30-59':e<80?'60-79':'80+'; } if (['DIAS','MESES','HORAS','MINUTOS','SEGUNDOS'].includes(t)) return '<1'; return 'sin dato'; }
function fila(f){
  if (f.length<32) return;
  S.rows++;
  const anio=cl(f[14]); const viol=cl(f[18]);
  const codes=[21,23,25,27].map(i=>code3(f[i])); let basic=null; for(const c of codes) if(c) basic=c;
  const [g,sub]=clasif(basic, viol);
  const pais=cl(f[9]); const dep = pais==='PERU' ? cl(f[10]) : 'EXTRANJERO O SIN DATO';
  let seg=cl(f[1]); if(/SANIDAD (FAP|NAVAL|EP)/.test(seg)) seg='SANIDAD FFAA';
  inc(S.A, anio+'|'+g+'|'+sub); inc(S.B, anio+'|'+dep+'|'+g); inc(S.C, anio+'|'+seg+'|'+g); inc(S.D, anio+'|'+edad(f[3],f[4])+'|'+g); inc(S.E, anio+'|'+cl(f[2])+'|'+g);
  if (basic && (anio==='2024'||anio==='2025')) inc(S.F, anio+'|'+basic);
  const q = S.G[anio] || (S.G[anio]={total:0,sinCodigo:0,R:0,poco:0,dVacioEconDato:0,violentaCampo:0});
  q.total++; if(!basic) q.sinCodigo++; if(g==='X'&&sub.startsWith('Síntomas')) q.R++; if(g==='X'&&sub.startsWith('Códigos')) q.poco++;
  if(!codes[3] && cl(f[27])==='SIN REGISTRO' && cl(f[26])==='SIN REGISTRO' && cl(f[28])!=='SIN REGISTRO' && cl(f[28])!=='') q.dVacioEconDato++;
  if(['ACCIDENTE DE TRANSITO','HOMICIDIO','SUICIDIO','OTRO ACCIDENTE','ACCIDENTE DE TRABAJO'].includes(viol)) q.violentaCampo++;
}
(async()=>{ try{
  const r = await fetch('/s/PigmdwnCGEdyqos/download'); const rd=r.body.getReader(); const dec=new TextDecoder('utf-8'); let rest=''; let first=true;
  while(true){ const {value,done}=await rd.read(); if(done) break; S.bytes+=value.length; const txt=rest+dec.decode(value,{stream:true}); const lines=txt.split('\r\n'); rest=lines.pop(); for(const l of lines){ if(first){first=false;continue;} fila(l.split('|')); } }
  if(rest) fila(rest.split('|'));
  S.done=true; S.secs=(Date.now()-S.t0)/1000;
 }catch(e){ S.err=String(e); } })();
