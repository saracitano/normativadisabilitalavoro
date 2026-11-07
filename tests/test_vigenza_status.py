import unittest
from critic.vigenza_status import load_report, interpret

class VigenzaAuditTests(unittest.TestCase):
    def test_all_records_have_noncertified_article_status(self):
        audit=load_report()
        self.assertEqual(audit["risultati"]["totale"],63)
        self.assertEqual(audit["risultati"]["articoli_certificati"],0)
        self.assertTrue(all(not interpret(x)["can_claim_current_article"]
                            for x in audit["records"]))
    def test_unverified_not_misrepresented_as_repealed(self):
        audit=load_report()
        unknown=[x for x in audit["records"]
                 if x["stato_atto"]=="non_verificato_singolarmente"]
        self.assertTrue(unknown)
        self.assertTrue(all(x["stato_articoli"]=="non_verificato" for x in unknown))

if __name__=="__main__": unittest.main()
