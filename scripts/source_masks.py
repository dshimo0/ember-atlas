"""Deterministic bbox/date subset of an unchanged original covering FIRMS CSV."""
import csv,io

def subset(payload,bbox,start,end):
 reader=csv.DictReader(io.StringIO(payload.decode('utf-8-sig')));out=io.StringIO(newline='');writer=csv.DictWriter(out,fieldnames=reader.fieldnames);writer.writeheader();count=0
 west,south,east,north=bbox
 for row in reader:
  if start<=row['acq_date']<=end and west<=float(row['longitude'])<=east and south<=float(row['latitude'])<=north:writer.writerow(row);count+=1
 return out.getvalue().encode(),count
