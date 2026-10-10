"""Phase 1 - Finalidad/Funcion panel.

Reads the master extract built by 00_build_master.py. All parsing, typing and
validation happen there; this script only aggregates. Run 00_build_master.py first.
"""
import pandas as pd, json, urllib.request, ssl, os
from pathlib import Path
_ROOT = Path(__file__).resolve().parent.parent      # analysis/D2_budget

# Paths are anchored on the script's own location, so it does not matter
# which directory you run it from.
RAW=_ROOT/'raw'; OUT=_ROOT/'processed'
NUM=['credito_presupuestado','credito_vigente','credito_devengado','credito_pagado']
KEEP=['ejercicio_presupuestario','subsector_desc','caracter_desc',
      'jurisdiccion_id','jurisdiccion_desc','entidad_desc','servicio_id','servicio_desc',
      'programa_id','programa_desc','finalidad_id','finalidad_desc','funcion_id','funcion_desc',
      'inciso_id','inciso_desc']+NUM

def load(y):
    for name in (f'master_{y}.parquet', f'master_{y}.csv.gz'):
        path=OUT/name
        if path.exists():
            return (pd.read_parquet(path, columns=KEEP) if name.endswith('.parquet')
                    else pd.read_csv(path, usecols=KEEP, low_memory=False))
    raise FileNotFoundError(f'no master file for {y} — run 00_build_master.py first')

def ipc_anual():
    ctx=ssl.create_default_context(); ctx.check_hostname=False; ctx.verify_mode=ssl.CERT_NONE
    u=('https://apis.datos.gob.ar/series/api/series/?ids=148.3_INIVELNAL_DICI_M_26'
       '&format=json&limit=5000&start_date=2016-12')
    j=json.loads(urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'}),
                 context=ctx,timeout=60).read())
    s=pd.DataFrame(j['data'],columns=['fecha','ipc']); s['fecha']=pd.to_datetime(s['fecha'])
    s['anio']=s.fecha.dt.year
    return s.groupby('anio')['ipc'].mean()

if __name__=='__main__':
    ipc=ipc_anual(); ipc.to_csv(OUT/'ipc_anual_promedio.csv')
    frames=[]
    for y in [2023,2024,2025,2026]:
        df=load(y); df['anio']=y; frames.append(df)
    all_=pd.concat(frames,ignore_index=True)
    all_.to_csv(OUT/'credito_micro_2023_2026.csv.gz',index=False,compression='gzip')
    # function-level panel
    fn=(all_.groupby(['anio','finalidad_id','finalidad_desc','funcion_id','funcion_desc'],as_index=False)
            [NUM].sum())
    fn.to_csv(OUT/'panel_funcion.csv',index=False)
    print(fn.groupby('anio')[NUM].sum())
