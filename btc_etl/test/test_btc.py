import unittest
from pathlib import Path

import pandas as pd

import btc_etl.app.btc as btc


class TestReader(unittest.TestCase):

    def setUp(self) -> None:
        self.btc_file_csv = btc.Reader('btc-test.csv', 'date', '%Y-%m-%d')
        self.btc_file_xlsx = btc.Reader('file.xlsx', 'date', None)

    def testExtractionOfFileType(self):
        self.assertEqual(self.btc_file_csv.file_type, '.csv',
                         msg=f'Wrong extracted file_type: {self.btc_file_csv.file_type}')
        self.assertEqual(self.btc_file_xlsx.file_type, '.xlsx',
                         msg=f'Wrong extracted file_type: {self.btc_file_xlsx.file_type}')

    def testReadFile(self):
        # unittest.mock could be used, but it's not elegant to store multiline data here - better to read test file
        data_from_csv = self.btc_file_csv.read_file()
        self.assertIsInstance(data_from_csv, pd.DataFrame)

    def tearDown(self) -> None:
        pass


class TestMyDataFrame(unittest.TestCase):

    def setUp(self):
        self.testDataFrame_forFilterTest = btc.MyDataFrame(btc.Reader('btc-test.csv', 'date', '%Y-%m-%d'))
        self.testDataFrame_leaveColumns = btc.MyDataFrame(btc.Reader('btc-test.csv', 'date', '%Y-%m-%d'))
        self.testDataFrame_convertCurr = btc.MyDataFrame(btc.Reader('btc-test.csv', 'date', '%Y-%m-%d'))
        self.testDataFrame_createStats = btc.MyDataFrame(btc.Reader('btc-test.csv', 'date', '%Y-%m-%d'))

    def testFilterDays(self):
        self.testDataFrame_forFilterTest.filter_days(2)
        self.assertEqual(self.testDataFrame_forFilterTest.df.shape[0], 2)

    def testLeaveColumns(self):
        self.testDataFrame_leaveColumns.leave_columns({'date', 'price(USD)', 'exchangeVolume(USD)'})
        self.assertEqual(self.testDataFrame_leaveColumns.df.shape[1], 3)

    def testConvertCurrency(self):
        self.testDataFrame_convertCurr.convert_currency({'price(EUR)': 'price(USD)'}, 2.23)
        self.assertEqual(self.testDataFrame_convertCurr.df['price(EUR)'].iloc[0],
                         self.testDataFrame_convertCurr.df['price(USD)'].iloc[0] * 2.23)

        # TODO: implement same methods for max and mean; maybe divide the original method into 3? And call from 1 above them

    def testCreateStatsMin(self):
        self.testDataFrame_createStats.create_stats('price(USD)', 10)
        self.assertEqual(self.testDataFrame_createStats.cols_stats[0], 'price(USD)')
        self.assertEqual(float(self.testDataFrame_createStats.min[0]),
                         float(self.testDataFrame_createStats.df['price(USD)'].min() / 10))

        self.testDataFrame_createStats.create_stats('generatedCoins')
        self.assertEqual(self.testDataFrame_createStats.cols_stats[1], 'generatedCoins')
        self.assertEqual(float(self.testDataFrame_createStats.min[1]),
                         float(self.testDataFrame_createStats.df['generatedCoins'].min()))

    # a test for printing stats makes not much sense, for me. Although it is possible with sys.stdout
    # Except: col_stats, min etc, could be checked for data type.

    # a test for the export_file() can be done via os.walk, for example.
    # Also via reading the file and comparing it with a prepared dataframe / mock (from unittest.mock)

    # unit test for plotting the graph makes not much sense for me, because creation of visualization of data
    # happens during the data exploration phase (which occurs under human direct control).

