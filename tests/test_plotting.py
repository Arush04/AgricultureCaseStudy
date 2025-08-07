# test_plotting.py

import unittest
import tempfile
import shutil
import os
import pandas as pd
from unittest.mock import patch
from src.plot_graphs import (
    ndvi_vs_temp_n_rainfall,
    ndvi_conc_temp_n_rainfall,
    temp_n_rainfall
)

class TestPlottingFunctions(unittest.TestCase):

    def setUp(self):
        # Create a temporary folder with mock CSV files
        self.test_dir = tempfile.mkdtemp()
        self.mock_df = pd.DataFrame({
            'mean_ndvi': [0.3, 0.4, 0.6],
            'mean_temp': [25.0, 30.0, 28.0],
            'mean_rainfall(mm)': [100.0, 150.0, 200.0],
            'year': [2012, 2013, 2014],
            'season': ['summer', 'monsoon', 'winter']
        })
        self.mock_file = os.path.join(self.test_dir, "climate_2012.csv")
        self.mock_df.to_csv(self.mock_file, index=False)

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    @patch("matplotlib.pyplot.show")
    def test_ndvi_vs_temp_n_rainfall(self, mock_show):
        try:
            ndvi_vs_temp_n_rainfall(self.test_dir)
        except Exception as e:
            self.fail(f"ndvi_vs_temp_n_rainfall raised an exception: {e}")

    @patch("matplotlib.pyplot.show")
    def test_ndvi_conc_temp_n_rainfall(self, mock_show):
        try:
            with patch("builtins.print") as mock_print:
                ndvi_conc_temp_n_rainfall(self.test_dir)
                mock_print.assert_any_call("\nTop 5 temperature and rainfall ranges with highest average NDVI:\n")
        except Exception as e:
            self.fail(f"ndvi_conc_temp_n_rainfall raised an exception: {e}")

    @patch("matplotlib.pyplot.show")
    def test_temp_n_rainfall(self, mock_show):
        try:
            temp_n_rainfall(self.test_dir)
        except Exception as e:
            self.fail(f"temp_n_rainfall raised an exception: {e}")


if __name__ == "__main__":
    unittest.main()
