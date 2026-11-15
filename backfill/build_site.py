import os, glob, json, time
import numpy as np, pandas as pd, duckdb
os.makedirs("docs", exist_ok=True)
files=[f.replace("\\","/") for f in glob.glob("data/monthly/*.parquet") if time.time()-os.path.getmtime(f)>90 and "siberia" not in f]
print("arquivos:",len(files),"/243")
con=duckdb.connect()
sql="SELECT region,yr,mo,satellite,daynight,lst_bin,n FROM read_parquet([%s])"%",".join(repr(f) for f in files)
raw=con.execute(sql).df()
raw=raw[raw.n>0].copy()
ang=raw.lst_bin/24*2*np.pi
raw["s_"]=np.sin(ang)*raw.n
raw["c_"]=np.cos(ang)*raw.n
day=raw[raw.daynight=="D"].groupby(["region","yr","satellite"],as_index=False).agg(s_=("s_","sum"),c_=("c_","sum"))
day["lst"]=(np.degrees(np.arctan2(day.s_,day.c_))/15)%24
rawy=raw.groupby(["region","yr"],as_index=False).n.sum()
summ=pd.read_csv("out/summary.csv") if os.path.exists("out/summary.csv") else pd.DataFrame()
LABEL={}
LABEL["pantanal"]="Pantanal (Brazil)"
LABEL["chilecito"]="Chilecito, La Rioja (Argentina)"
LABEL["amazonia_s"]="Southern Amazon arc (Brazil)"
LABEL["cerrado"]="Cerrado (Brazil)"
LABEL["gran_chaco"]="Gran Chaco (Argentina/Paraguay)"
LABEL["california"]="Northern California (USA)"
LABEL["se_australia"]="South-east Australia"
LABEL["iberia"]="Iberian Peninsula"
LABEL["siberia"]="Central Siberia (Russia)"
regions={}
for reg in sorted(raw.region.unique()):
    path="out/harm_%s.csv"%reg
    if not os.path.exists(path): continue
    h=pd.read_csv(path)
    months=[]
    for r in h.itertuples():
        months.append([int(r.yr),int(r.mo),round(float(r.harm),1),round(float(r.lo),1),round(float(r.hi),1),str(r.flag)])
    dr=day[day.region==reg]
    drift=[]
    for yr in sorted(dr.yr.unique()):
        row={"yr":int(yr)}
        for sat,key in (("Terra","terra"),("Aqua","aqua"),("NOAA-20","noaa20")):
            v=dr[(dr.yr==yr)&(dr.satellite==sat)]
            row[key]=round(float(v.lst.iloc[0]),2) if len(v) else None
        drift.append(row)
    ar={}
    for k,v in rawy[rawy.region==reg].set_index("yr").n.items(): ar[int(k)]=int(v)
    ah={}
    for k,v in h.groupby("yr").harm.sum().items(): ah[int(k)]=round(float(v),1)
    pp="out/params_%s.json"%reg
    p=json.load(open(pp)) if os.path.exists(pp) else {}
    bt=p.get("beta_day",{}).get("Terra",0.0)
    tl=[r["terra"] for r in drift if r["terra"] is not None]
    loss=None
    if len(tl)>5:
        loss=round(100*(1-float(np.exp(bt*(tl[-1]-float(np.median(tl)))))),1)
    e={}
    e["label"]=LABEL.get(reg,reg)
    e["months"]=months
    e["drift"]=drift
    e["annual_raw"]=ar
    e["annual_harm"]=ah
    e["params"]=p
    e["terra_loss_pct"]=loss
    regions[reg]=e
data={}
data["regions"]=regions
data["summary"]=summ.where(pd.notnull(summ),None).to_dict("records")
data["challenge"]="Harmonization of MODIS and VIIRS Hot Spots"
data["sources"]="NASA FIRMS MODIS C6.1 + VIIRS 375 m C2"
json.dump(data,open("docs/data.json","w"))
print("regions:",list(regions))
print("bytes:",os.path.getsize("docs/data.json"))
