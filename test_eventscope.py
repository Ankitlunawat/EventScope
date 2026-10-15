import unittest,json,csv,tempfile
from pathlib import Path
from eventscope import parse,export,ROOT
class EventTests(unittest.TestCase):
 def setUp(self):self.source=(ROOT/'source/python-events.html').read_text();self.rows,self.issues=parse(self.source)
 def test_real_snapshot(self):self.assertEqual(len(self.rows),6);self.assertFalse(self.issues)
 def test_unique_and_sorted(self):self.assertEqual(len({r['event_url'] for r in self.rows}),6);self.assertEqual(self.rows,sorted(self.rows,key=lambda r:(r['start_iso'],r['event'])))
 def test_duplicate_listing(self):self.assertEqual(len(parse(self.source+self.source)[0]),6)
 def test_missing_time(self):self.assertEqual(parse('<ul class="list-recent-events"><li><h3 class="event-title"><a href="/events/1/">Event</a></h3></li></ul>')[0],[])
 def test_exports(self):
  with tempfile.TemporaryDirectory() as t:
   out=Path(t);export(self.rows,out);self.assertEqual(json.loads((out/'events.json').read_text()),self.rows)
   with (out/'events.csv').open(encoding='utf-8-sig') as f:self.assertEqual(len(list(csv.DictReader(f))),6)
   self.assertTrue((out/'events.xlsx').stat().st_size>0)
 def test_no_empty_export(self):
  with tempfile.TemporaryDirectory() as t:
   with self.assertRaises(ValueError):export([],Path(t))
if __name__=='__main__':unittest.main()
