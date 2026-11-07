import tempfile
import unittest
from pathlib import Path
from app.legislation import connect,bootstrap
from app.official_ingest import ingest,review
from app.legal_critic import evaluate

XML="""<atto><articolo><num>Art. 2</num><comma>
Il collocamento mirato e l'inserimento lavorativo sono temi qui riportati
in un documento di prova, senza valore normativo.</comma></articolo></atto>"""

class CriticTests(unittest.TestCase):
    def test_never_certifies_without_review(self):
        with tempfile.TemporaryDirectory() as t:
            db=connect(str(Path(t)/"x.db"))
            bootstrap(db,"app/seed.json")
            file=Path(t)/"test.xml"
            file.write_text(XML,encoding="utf-8")
            ingest(db,"L68-1999",file,"test","test","2026-11-08",
                   "https://dati.normattiva.it/")
            results=evaluate(db,"collocamento mirato","2026-11-08")
            self.assertTrue(results)
            self.assertTrue(all(x["legal_status"]=="non_certificato" for x in results))
            self.assertFalse(evaluate(db,"collocamento mirato","2026-11-07"))
            db.close()

if __name__=="__main__":
    unittest.main()
