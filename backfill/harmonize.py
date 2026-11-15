raise SystemExit("Publication blocked: provide verified Parquet inputs and retrieval manifests; see backfill/README.md. The reviewed model is retained for research, not release generation.")
import os, glob, json, time
import numpy as np, pandas as pd, duckdb
OUT="out"; os.makedirs(OUT, exist_ok=True)
files=[f.replace("\\","/") for f in glob.glob("data/monthly/*.parquet") if time.time()-os.path.getmtime(f)>90]
print("arquivos:",len(files),"/243")
con=duckdb.connect()
raw=con.execute("SELECT region,yr,mo,satellite,daynight,quality,lst_bin,n FROM read_parquet([%s])"%",".join(repr(f) for f in files)).df()
raw=raw[raw.n>0].copy(); raw["t"]=raw.yr*12+raw.mo
a=raw.lst_bin/24*2*np.pi
raw["s_"]=np.sin(a)*raw.n; raw["c_"]=np.cos(a)*raw.n
g=raw.groupby(["region","t","yr","mo","satellite","daynight"],as_index=False).agg(n=("n","sum"),s_=("s_","sum"),c_=("c_","sum"),sp=("quality",lambda q:(q=="sp").any()))
g["lst"]=(np.degrees(np.arctan2(g.s_,g.c_))/15)%24
win=g.groupby("satellite").t.agg(["min","max"]).to_dict("index")
T0,T1=int(g.t.min()),int(g.t.max()); REF="Aqua"
wrap=lambda x:(x+12)%24-12

def panel(region,dn,tmax=None):
    d=g[(g.region==region)&(g.daynight==dn)]
    if d.empty: return None
    base={}
    for s,v in d.groupby("satellite"):
        b=v[(v.yr>=2012)&(v.yr<=2021)&(v.t<=tmax if tmax else True)]
        base[s]=float(np.median(b.lst)) if len(b) else float(np.median(v[v.t<=tmax].lst)) if tmax and len(v[v.t<=tmax]) else float("nan")
    sats=sorted(d.satellite.unique()); rows=[]
    for t in range(T0,T1+1):
        for s in sats:
            if not (win[s]["min"]<=t<=win[s]["max"]): continue
            r=d[(d.t==t)&(d.satellite==s)]
            rows.append(dict(t=t,sat=s,n=float(r.n.iloc[0]) if len(r) else np.nan,
                dlst=wrap(float(r.lst.iloc[0])-base[s]) if len(r) else 0.0,
                sp=bool(r.sp.iloc[0]) if len(r) else False))
    return pd.DataFrame(rows),(REF if REF in sats else sats[0]),base

def fit(p,ref,tmax=None):
    f=p[p.sp & p.n.notna()].copy()
    if tmax: f=f[f.t<=tmax]
    f=f.groupby("t").filter(lambda x:x.n.sum()>0)
    if f.t.nunique()<6: return None
    ts=sorted(f.t.unique()); sats=sorted(f.sat.unique())
    sd=[s for s in sats if s!=ref]; ti={t:i for i,t in enumerate(ts)}
    ds=[]
    for s in sats:
        v=f[(f.sat==s)&(f.n>0)].dlst
        if len(v)>12 and v.std()>0.10 and (v.max()-v.min())>0.30: ds.append(s)
    ncol=len(sd)+len(ts)+len(ds)
    X=np.zeros((len(f),ncol))
    for i,r in enumerate(f.itertuples()):
        if r.sat in sd: X[i,sd.index(r.sat)]=1
        X[i,len(sd)+ti[r.t]]=1
        if r.sat in ds: X[i,len(sd)+len(ts)+ds.index(r.sat)]=r.dlst
    lam=np.array([0.5]*len(sd)+[0.1]*len(ts)+[0.05]*len(ds))
    y=f.n.values; b=np.zeros(ncol)
    for _ in range(80):
        eta=np.clip(X@b,-20,20); mu=np.exp(eta); W=np.maximum(mu,1e-9)
        bn=np.linalg.solve(X.T@(X*W[:,None])+np.diag(lam), X.T@(W*(eta+(y-mu)/W)))
        if np.max(np.abs(bn-b))<1e-9: b=bn; break
        b=bn
    eta=np.clip(X@b,-20,20); W=np.maximum(np.exp(eta),1e-9)
    se=np.sqrt(np.maximum(np.diag(np.linalg.pinv(X.T@(X*W[:,None])+np.diag(lam))),0))
    alpha={ref:0.0}; alpha.update({s:float(b[i]) for i,s in enumerate(sd)})
    betas={s:float(b[len(sd)+len(ts)+i]) for i,s in enumerate(ds)}
    return alpha,betas,{t:len(sd)+i for i,t in enumerate(ts)},b,se

def run(region,dn,tmax=None):
    got=panel(region,dn,tmax)
    if got is None: return None
    p,ref,base=got
    ft=fit(p,ref,tmax)
    if ft is None: return None
    alpha,betas,gi,b,se=ft
    out=[]
    for t,grp in p.groupby("t"):
        if t in gi and not (tmax and t>tmax):
            m=float(np.exp(np.clip(b[gi[t]],-20,20))); s=se[gi[t]]
            out.append((t,m,float(np.exp(np.clip(b[gi[t]]-1.96*s,-20,20))),float(np.exp(np.clip(b[gi[t]]+1.96*s,-20,20))),"sp"))
        else:
            est=[r.n*np.exp(-alpha[r.sat]-betas.get(r.sat,0.0)*r.dlst) for r in grp.itertuples() if r.sat in alpha and np.isfinite(r.n) and np.isfinite(r.dlst)]
            v=float(np.mean(est)) if est else np.nan
            out.append((t,v,np.nan,np.nan,"nrt" if not tmax else "pred"))
    o=pd.DataFrame(out,columns=["t","harm","lo","hi","flag"])
    o["yr"]=(o.t-1)//12; o["mo"]=(o.t-1)%12+1
    return o,alpha,betas,base,p,ref

def denial(region):
    r=run(region,"D",tmax=2018*12+12)
    if r is None: return (None,None)
    _,av,bv,_,pv,_=r
    post=pv[pv.t>2018*12+12].copy(); post["yr"]=(post.t-1)//12
    vi=post[post.sat.isin(av)&post.sat.str.startswith(("Suomi","NOAA"))].copy()
    vi["e"]=vi.n*np.exp(-vi.sat.map(av)-vi.sat.map(bv).fillna(0)*vi.dlst)
    aq=post[post.sat=="Aqua"].copy(); aq["e"]=aq.n*np.exp(-bv.get("Aqua",0.0)*aq.dlst)
    j=pd.concat([vi.groupby(["t","yr"]).e.mean().rename("p"),aq.set_index(["t","yr"]).e.rename("o")],axis=1).dropna().reset_index()
    ann=j.groupby("yr")[["p","o"]].sum()
    ann=ann[ann.o>=50]
    if ann.empty: return (None,None)
    err=(ann.p-ann.o)/ann.o*100
    pre=err[err.index<=2021]; pos=err[err.index>=2022]
    return (round(float(pre.median()),1) if len(pre) else None, round(float(pos.median()),1) if len(pos) else None)

rows=[]
for region in sorted(g.region.unique()):
    D=run(region,"D"); N=run(region,"N")
    if D is None: continue
    oD,aD,bD,base,pD,ref=D
    tot=oD[["t","yr","mo","harm","lo","hi","flag"]].copy()
    if N is not None:
        tot=tot.merge(N[0][["t","harm"]].rename(columns={"harm":"hn"}),on="t",how="left").fillna({"hn":0})
        tot["harm"]=tot.harm+tot.hn; tot=tot.drop(columns="hn")
    tot["lo"]=np.nan; tot["hi"]=np.nan  # No validated interval for the combined day/night estimate.
    tot.to_csv(f"{OUT}/harm_{region}.csv",index=False)
    json.dump({"ref":ref,"alpha_day":aD,"beta_day":bD,"baseline_lst":base},open(f"{OUT}/params_{region}.json","w"),indent=1)
    pre,pos=denial(region)
    rawy=pD.assign(yr=(pD.t-1)//12).groupby("yr").n.sum(); hy=oD.groupby("yr").harm.sum()
    r1211=rawy.get(2012,np.nan)/max(rawy.get(2011,np.nan),1); h1211=hy.get(2012,np.nan)/max(hy.get(2011,np.nan),1e-9)
    rows.append(dict(region=region,bTerra=round(bD.get("Terra",0),3),bAqua=round(bD.get("Aqua",0),3),
        neg_pre=pre,neg_pos=pos,bruto_1211=round(float(r1211),2),harm_1211=round(float(h1211),2),meses=len(tot)))
s=pd.DataFrame(rows); s.to_csv(f"{OUT}/summary.csv",index=False)
print(s.to_string(index=False))
g[g.region=="pantanal"][["yr","mo","satellite","daynight","lst","n"]].to_csv(f"{OUT}/drift_pantanal.csv",index=False)
print("OK ->",OUT)
