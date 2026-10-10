"""Closes the two Phase-1 caveats: INDEC-sourced GDP, and a defensible 2026 deflator."""
import pandas as pd, json, urllib.request, ssl
from pathlib import Path
_ROOT = Path(__file__).resolve().parent.parent      # analysis/D2_budget

ctx=ssl.create_default_context(); ctx.check_hostname=False; ctx.verify_mode=ssl.CERT_NONE
def series(ids,start='2018'):
    u=f'https://apis.datos.gob.ar/series/api/series/?ids={ids}&format=json&limit=1000&start_date={start}'
    r=urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'}),context=ctx,timeout=60)
    return json.loads(r.read())['data']

# --- GDP at market prices, current pesos: VAB a precios basicos + impuestos netos ---
g=pd.DataFrame(series('8.1_VABPB_2004_A_36,8.1_IVA_2004_A_23'),columns=['f','vab','imp'])
g['anio']=pd.to_datetime(g.f).dt.year; g['pib']=g.vab+g.imp
PIB=dict(zip(g.anio,g.pib)); pd.DataFrame({'anio':g.anio,'pib_mm_pesos':g.pib}).to_csv(str(_ROOT/'processed')+'/pib_nominal_indec.csv',index=False)

# --- IPC ---
ipc=pd.read_csv(str(_ROOT/'processed')+'/ipc_anual_promedio.csv',index_col='anio')['ipc'].to_dict()
sc=json.load(open(str(_ROOT/'processed')+'/ipc_2026_scenarios.json'))     # A = Ley 2026 projection, B = YTD carry-forward

fn=pd.read_csv(str(_ROOT/'processed')+'/panel_funcion.csv')
MEAS={2023:'credito_devengado',2024:'credito_devengado',2025:'credito_devengado',2026:'credito_vigente'}
fn['monto']=[r[MEAS[r['anio']]] for _,r in fn.iterrows()]
w=fn.pivot_table(index=['finalidad_id','funcion_id','funcion_desc'],columns='anio',values='monto',aggfunc='sum').fillna(0.)
tot=fn.groupby('anio')['monto'].sum()

def real(col,y,defl): return (col[y]/defl)/(col[2023]/ipc[2023])-1
out=pd.DataFrame(index=w.index)
for y in [2024,2025]:
    out[f'real_{y}']=real(w,y,ipc[y])
out['real_2026_LeyPpto']=real(w,2026,sc['A'])
out['real_2026_YTD']    =real(w,2026,sc['B'])
for y in [2023,2024,2025]:
    out[f'pibshare_{y}']=w[y]/PIB[y]*100
out['pibshare_chg_25_23']=out['pibshare_2025']/out['pibshare_2023']-1
out=out[w[2023]>0].sort_values('real_2025')
out.to_csv(str(_ROOT/'outputs')+'/panel_funcion_robustez.csv')

print('GDP (millones $ corrientes, INDEC):',{k:round(v) for k,v in PIB.items() if k>=2023})
print('\nWHOLE BUDGET')
for y in [2024,2025]:
    print(f'  real {y}/2023 {real(tot,y,ipc[y]):+.1%}   %GDP {tot[y]/PIB[y]*100:.2f} (2023 {tot[2023]/PIB[2023]*100:.2f})')
print(f'  real 2026/2023  Ley Ppto deflator {real(tot,2026,sc["A"]):+.1%} | YTD carry-forward {real(tot,2026,sc["B"]):+.1%}')
foc=['Ecología y Desarrollo Sostenible','Ciencia, Tecnología e Innovación','Educación y Cultura','Inteligencia','Salud']
print('\nFOCAL FUNCTIONS')
print(out.reset_index().set_index('funcion_desc').loc[foc][
    ['real_2024','real_2025','real_2026_LeyPpto','real_2026_YTD','pibshare_2023','pibshare_2025','pibshare_chg_25_23']
].to_string(float_format=lambda x:f'{x:,.4f}'))
