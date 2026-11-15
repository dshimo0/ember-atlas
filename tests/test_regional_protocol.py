import calendar,copy,json,sys,tempfile,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from evaluate_regions import evaluate,comparison_document
from stream_region import stream_inputs

class RegionalProtocolTests(unittest.TestCase):
 def daily(self,outer_modis=50):
  result=[]
  for year in range(2020,2027):
   for month in range(1,13 if year<2026 else 8):
    for day in range(1,calendar.monthrange(year,month)[1]+1):
     for product in ['MODIS_SP','VIIRS_NOAA20_SP']:
      value=(50 if year<=2022 else outer_modis)if product=='MODIS_SP'else 100
      result.append({'day':f'{year}-{month:02}-{day:02}','area':'all','product':product,'native':value,'cells':value})
  return result
 def test_selection_is_inner_only_and_publication_checks_separate_periods(self):
  a=evaluate(self.daily(),'california');b=evaluate(self.daily(100),'california')
  self.assertEqual(a['selected_method'],'scalar');self.assertEqual(b['selected_method'],a['selected_method']);self.assertTrue(a['accepted']);self.assertFalse(b['accepted'])
  self.assertEqual(a['partitions']['outer']['scalar']['n'],24);self.assertEqual(a['partitions']['outer_excluding_known']['scalar']['n'],23);self.assertEqual(a['partitions']['external']['scalar']['n'],19)
  self.assertTrue(all(r['adjusted']is None for r in b['monthly']))
 def test_missing_day_cannot_become_a_complete_publication_month(self):
  daily=self.daily();daily.pop();r=evaluate(daily,'siberia');self.assertFalse(r['support_complete']);self.assertFalse(r['accepted']);self.assertIn('2026-07',r['excluded_months'])
 def test_incomplete_inner_period_cannot_be_reported_as_a_selected_fit(self):
  rows=[r for r in self.daily()if not(r['day'].startswith('2020')and r['product']=='MODIS_SP')];v=evaluate(rows,'california');self.assertIsNone(v['selected_method']);self.assertFalse(v['accepted']);self.assertEqual(v['adjusted']['n'],0);self.assertTrue(all(f is None for f in v['factors'].values()))
 def test_original_pantanal_stays_frozen_despite_comparison_gates(self):
  r=evaluate(self.daily(),'pantanal');self.assertFalse(r['accepted']);self.assertIn('19 fresh months',r['reason']);self.assertIsNone(r['publication_domain'])
 def test_streamed_zero_and_duplicate_rules(self):
  import hashlib
  with tempfile.TemporaryDirectory()as t:
   root=Path(t);path=root/'source';path.mkdir();spool=root/'spool';spool.mkdir();payload=b'latitude,longitude,acq_date,acq_time,satellite\n38,-120,2020-01-01,0030,Terra\n38,-120,2020-01-01,0030,Terra\n';(path/'a.csv').write_bytes(payload)
   (path/'a.json').write_text(json.dumps({'source':'MODIS_SP','processing_class':'SP','bbox':'-125,32,-114,42.5','start':'2020-01-01','end':'2020-01-02','sha256':hashlib.sha256(payload).hexdigest(),'rows':2,'retrieved_at':'2026-11-15T00:00:00Z'}))
   daily,manifests,covered,total=stream_inputs([path],[-125,32,-114,42.5],'SP',spool)
   self.assertEqual(stream_inputs([path],[-125,32,-114,42.5],'SP',None),(daily,manifests,covered,total));self.assertEqual(total,1);self.assertEqual([r['native']for r in daily],[1,0]);self.assertEqual(len((spool/'2020-01.jsonl').read_text().splitlines()),1)
 def test_covering_query_preserves_original_fields_and_filters_only_analysis_mask(self):
  from source_masks import subset
  payload=b'latitude,longitude,acq_date,acq_time,satellite,frp\n38,-120,2020-01-01,0030,Terra,12.50\n10,-60,2020-01-01,0030,Terra,8.2\n'
  content,n=subset(payload,[-125,32,-114,42.5],'2020-01-01','2020-01-01')
  self.assertEqual(n,1);self.assertIn(b'12.50',content);self.assertNotIn(b'8.2',content)
if __name__=='__main__':unittest.main()
