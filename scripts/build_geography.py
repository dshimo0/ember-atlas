"""Build the local map fallback from committed Natural Earth inputs."""
import hashlib,json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
INPUT=ROOT/'data/reference'
EXTENT=(-66,-28,-47,-9)

def coordinates(value):
    if not value:return
    if isinstance(value[0],(int,float)):yield value
    else:
        for child in value:yield from coordinates(child)

def intersects(feature):
    points=list(coordinates(feature['geometry']['coordinates']))
    if not points:return False
    xs,ys=zip(*[p[:2] for p in points])
    w,s,e,n=EXTENT
    return min(xs)<=e and max(xs)>=w and min(ys)<=n and max(ys)>=s

def main():
    sources=[]
    def load(name,description):
        path=INPUT/(name+'.geojson');payload=path.read_bytes()
        sources.append({'name':description,'url':'https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/'+path.name,'sha256':hashlib.sha256(payload).hexdigest(),'license':'Public domain','terms':'https://www.naturalearthdata.com/about/terms-of-use/'})
        return json.loads(payload)['features']
    countries=load('ne_110m_admin_0_countries','Natural Earth Admin 0 countries, 1:110m')
    rivers=load('ne_50m_rivers_lake_centerlines','Natural Earth rivers and lake centerlines, 1:50m')
    places=load('ne_50m_populated_places_simple','Natural Earth populated places, 1:50m')
    def collection(features,keys):
        return {'type':'FeatureCollection','features':[{'type':'Feature','properties':{k:f['properties'].get(k) for k in keys},'geometry':f['geometry']} for f in features if intersects(f)]}
    result={'extent':EXTENT,'sources':sources,
            'countries':collection(countries,['ADMIN','LABEL_X','LABEL_Y']),
            'rivers':collection(rivers,['name','name_en']),
            'places':collection(places,['name'])}
    payload=json.dumps(result,separators=(',',':'))
    (INPUT/'local-geography.json').write_text(payload)
    (ROOT/'web/assets/local-geography.json').write_text(payload)
    print({key:len(result[key]['features']) for key in ['countries','rivers','places']})
if __name__=='__main__':main()
