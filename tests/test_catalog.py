import json
import sqlite3
import tempfile
import unittest
from pathlib import Path
from app.legislation import connect, bootstrap, search
from monitor.monitor import trusted

class CatalogueTests(unittest.TestCase):
    def test_seed_contains_all_initial_sources(self):
        seed=json.loads(Path("app/seed.json").read_text(encoding="utf-8"))
        self.assertGreaterEqual(len(seed["acts"]),60)
        self.assertEqual(len({x["id"] for x in seed["acts"]}),len(seed["acts"]))
        self.assertEqual(sum(len(a["articles"]) for a in seed["acts"]),33)

    def test_search_returns_act_only_records(self):
        with tempfile.TemporaryDirectory() as t:
            db=connect(str(Path(t)/"test.sqlite"))
            bootstrap(db,"app/seed.json")
            rows=search(db,"diritti permessi")
            self.assertTrue(any(x["status"]=="solo_atto" for x in rows))
            db.close()

    def test_official_host_validation(self):
        self.assertTrue(trusted("https://www.normattiva.it/eli/stato/LEGGE/1999/03/12/68"))
        self.assertFalse(trusted("https://normattiva.it.evil.example/atto"))

if __name__=="__main__":
    unittest.main()
