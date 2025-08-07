# test_scrapper.py
import unittest
from unittest.mock import patch, MagicMock
from src.scrapper import is_leap_year, scrapper_req

class TestScrapper(unittest.TestCase):

    def test_is_leap_year(self):
        self.assertTrue(is_leap_year("2016"))
        self.assertFalse(is_leap_year("2015"))

    @patch("src.scrapper.requests.get")
    def test_scrapper_req_download_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.iter_content = lambda chunk_size: [b'data']
        mock_get.return_value = mock_response

        scrapper_req(["01to15"], "jan", years_list=["2016"])

        mock_get.assert_called_once()
        called_url = mock_get.call_args[0][0]
        self.assertIn("ocm2_ndvi_filt_01to15_jan2016", called_url)


    @patch("src.scrapper.requests.get")
    def test_scrapper_req_download_failure(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        scrapper_req(["01to15"], "jan")

        mock_get.assert_called()
        called_url = mock_get.call_args[0][0]
        self.assertIn("ocm2_ndvi_filt_01to15_jan", called_url)

if __name__ == "__main__":
    unittest.main()
