import json
import tempfile
import unittest
from pathlib import Path

from app.legislation import connect, bootstrap, search
from app.official_ingest import ingest, review
from app.audit import audit


SAMPLE = """<?xml version="1.0" encoding="UTF-8"?>
<atto xmlns="urn:fake-nir-for-test">
 <articolato>
  <articolo><num>Art. 1</num>
    <comma><num>1.</num><corpo>Questo e' un testo artificiale di prova,
    usato esclusivamente per collaudare la pipeline senza dichiarare
    che sia una disposizione normativa autentica.</corpo></comma>
  </articolo>
 </articolato>
</atto>"""


class IngestionTests(unittest.TestCase):
    def setUp(self):
        self.t = tempfile.TemporaryDirectory()
        self.path = Path(self.t.name)
        self.db = connect(str(self.path / "test.sqlite"))
        bootstrap(self.db, "app/seed.json")

    def tearDown(self):
        self.db.close()
        self.t.cleanup()

    def test_import_and_audit(self):
        xml = self.path / "sample.xml"
        xml.write_text(SAMPLE, encoding="utf-8")
        result = ingest(self.db, "L68-1999", xml, "TEST-SYNTHETIC",
                        "test-version", "2026-11-08",
                        "https://dati.normattiva.it/")
        self.assertEqual(result["articles_extracted"], 1)
        report = audit(self.db, "2026-11-08")
        record = next(x for x in report["records"] if x["id"] == "L68-1999")
        self.assertEqual(record["status"], "testo_importato_da_validare")
        self.assertEqual(record["versions"], 1)
        self.assertEqual(self.db.execute(
            "SELECT reviewed FROM official_versions WHERE act_id=? AND number=?",
            ("L68-1999", "1")).fetchone()[0], 0)

    def test_conflict_rejected(self):
        xml = self.path / "sample.xml"
        xml.write_text(SAMPLE, encoding="utf-8")
        args = ("L68-1999", xml, "TEST-SYNTHETIC", "test-version",
                "2026-11-08", "https://dati.normattiva.it/")
        ingest(self.db, *args)
        xml.write_text(SAMPLE.replace("artificiale", "sintetico"), encoding="utf-8")
        with self.assertRaises(ValueError):
            ingest(self.db, *args)

    def test_review_requires_reason_and_document(self):
        with self.assertRaises(ValueError):
            review(self.db, "L68-1999", "1", "2026-11-08",
                   "test", "https://www.normattiva.it/", "vigente_verificato", "breve")

    def test_reinitialize_does_not_destroy_documents(self):
        xml = self.path / "sample.xml"
        xml.write_text(SAMPLE, encoding="utf-8")
        ingest(self.db, "L68-1999", xml, "TEST-SYNTHETIC", "test-version",
               "2026-11-08", "https://dati.normattiva.it/")
        bootstrap(self.db, "app/seed.json")
        n = self.db.execute("SELECT COUNT(*) FROM official_documents").fetchone()[0]
        self.assertEqual(n, 1)
        self.assertTrue(search(self.db, "collocamento"))


if __name__ == "__main__":
    unittest.main()
