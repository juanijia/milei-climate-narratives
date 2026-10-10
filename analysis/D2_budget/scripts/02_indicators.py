"""Phase 1 indicators: FARN reconciliation + function-level real / %GDP / share / RRI."""
import pandas as pd
from pathlib import Path
_ROOT = Path(__file__).resolve().parent.parent      # analysis/D2_budget

OUT=_ROOT/'processed'; RES=_ROOT/'outputs'
ipc=pd.read_csv(OUT/'ipc_anual_promedio.csv',index_col='anio')['ipc']
fn=pd.read_csv(OUT/'panel_funcion.csv')

# nominal GDP at market prices, millones de pesos corrientes.
# Source: INDEC national accounts via apis.datos.gob.ar, VAB a precios basicos
# (8.1_VABPB_2004_A_36) + impuestos netos sobre los productos (8.1_IVA_2004_A_23).
# Written by scripts/03_robustness_2026_and_gdp.py -> processed/pib_nominal_indec.csv
_p=pd.read_csv(OUT/'pib_nominal_indec.csv')
PIB=dict(zip(_p.anio,_p.pib_mm_pesos))

MEAS={2023:'credito_devengado',2024:'credito_devengado',2025:'credito_devengado',
      2026:'credito_vigente'}
fn['monto']=[r[MEAS[r['anio']]] for _,r in fn.iterrows()]

def wide(keys):
    w=fn.groupby(['anio']+keys,as_index=False)['monto'].sum()
    return w.pivot_table(index=keys,columns='anio',values='monto').fillna(0.0)

def real_chg(w,y,base=2023):
    return (w[y]/ipc[y])/(w[base]/ipc[base])-1

# ---------- 1. FARN reconciliation (finalidad level) ----------
f=wide(['finalidad_id','finalidad_desc'])
tot=fn.groupby('anio')['monto'].sum()
farn={'ADMINISTRACION GUBERNAMENTAL':(2349060,6652753,-0.376),
      'DEUDA PUBLICA':(3472801,10352974,-0.343),
      'SERVICIOS DE DEFENSA Y SEGURIDAD':(1710842,6075017,-0.217),
      'SERVICIOS ECONOMICOS':(5647579,9539839,-0.628),
      'SERVICIOS SOCIALES':(24845207,90257189,-0.199)}
rows=[]
for (fid,fd),r in f.iterrows():
    a,b,c=farn[fd]
    rows.append(dict(finalidad=fd, ours_2023=r[2023], farn_2023=a, d23=r[2023]/a-1,
                     ours_2025=r[2025], farn_2025=b, d25=r[2025]/b-1,
                     ours_real=real_chg(f,2025).loc[(fid,fd)], farn_real=c))
rec=pd.DataFrame(rows)
rec.loc[len(rec)]=dict(finalidad='TOTAL',ours_2023=tot[2023],farn_2023=38025489,
    d23=tot[2023]/38025489-1, ours_2025=tot[2025],farn_2025=122877771,
    d25=tot[2025]/122877771-1,
    ours_real=(tot[2025]/ipc[2025])/(tot[2023]/ipc[2023])-1, farn_real=-0.288)
rec.to_csv(RES/'farn_reconciliation.csv',index=False)
print(rec.to_string(index=False,float_format=lambda x:f'{x:,.4f}'))

# ---------- 2. Function-level table ----------
g=wide(['finalidad_id','funcion_id','funcion_desc'])
res=pd.DataFrame(index=g.index)
res['dev_2023']=g[2023]; res['dev_2024']=g[2024]; res['dev_2025']=g[2025]; res['vig_2026']=g[2026]
res['real_24_23']=real_chg(g,2024)
res['real_25_23']=real_chg(g,2025)
res['real_26_23']=real_chg(g,2026)
for y in [2023,2024,2025,2026]:
    res[f'share_{y}']=g[y]/tot[y]*100
res['pibshare_2023']=g[2023]/PIB[2023]*100
res['pibshare_2024']=g[2024]/PIB[2024]*100
res['pibshare_2025']=g[2025]/PIB[2025]*100
res['pibshare_chg_25_23']=res['pibshare_2025']/res['pibshare_2023']-1
tot_real25=(tot[2025]/ipc[2025])/(tot[2023]/ipc[2023])-1
tot_real24=(tot[2024]/ipc[2024])/(tot[2023]/ipc[2023])-1
res['RRI_25']=(res['real_25_23']-tot_real25)*100   # percentage points vs total
res['RRI_24']=(res['real_24_23']-tot_real24)*100
res['priority_ratio_25']=res['share_2025']/res['share_2023']
res=res[res['dev_2023']>0].sort_values('real_25_23')
res.to_csv(RES/'panel_funcion_indicadores.csv')
print(f"\nTOTAL real 2024/2023 {tot_real24:+.3%}  |  2025/2023 {tot_real25:+.3%}")
print(res[['dev_2023','dev_2025','real_25_23','pibshare_chg_25_23','share_2023','share_2025','RRI_25']]
      .to_string(float_format=lambda x:f'{x:,.3f}'))
