import unittest
from unittest.mock import patch
from app.fetch_official import download_xml

class SourceValidationTests(unittest.TestCase):
    def test_rejects_official_looking_spoof(self):
        with self.assertRaises(ValueError):
            download_xml("https://normattiva.it.evil.example/atto.xml")

    def test_rejects_http(self):
        with self.assertRaises(ValueError):
            download_xml("http://dati.normattiva.it/atto.xml")

    def test_rejects_non_xml_response(self):
        class Response:
            def __enter__(self):return self
            def __exit__(self,*_):pass
            def geturl(self):return "https://dati.normattiva.it/download.xml"
            def read(self,n):return b"not XML"
        with patch("app.fetch_official.ensure_public_dns"):
            with patch("app.fetch_official.build_opener") as opener:
                opener.return_value.open.return_value=Response()
                with self.assertRaises(ValueError):
                    download_xml("https://dati.normattiva.it/download.xml")

if __name__=="__main__":
    unittest.main()
