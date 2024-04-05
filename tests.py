import unittest
import time
from pprint import pprint
import cereal
import pandas as pd

class Testdataframe(unittest.TestCase):
    def setUp(self) -> None:
        self.columns = ['name', 'mfr', 'type', 'calories', 'protein', 'fat', 
                        'sodium', 'fiber', 'carbo', 'sugars', 'potass', 
                        'vitamins', 'shelf', 'weight', 'cups']
        file = 'data/Cereal.csv'
        self.df = pd.read_csv(file, sep = ';', header = 0, skiprows = [1], on_bad_lines = 'skip')
        self.df = self.df.drop('rating', axis = 1)
        
    def testSimpleFilter(self):
        series = cereal.filter_df('name', 'eq', 'Smacks')
        
        l = ['Smacks', 'K','C', 110, 2, 1, 70, 1.0, 9.0, 15, 40, 25 ,2, 1.0, 0.75]
        new_df = pd.DataFrame(dict(map(lambda k, v : (k,v), self.columns, l)), index = [0])
        
        for c in self.columns:
            self.assertEqual(series[c].values, new_df[c].values)
        
        series = cereal.filter_df('type', 'eq', 'H')
        
        self.assertEqual(len(series), 3)

    def testMultipleFilter(self):
        series = cereal.filter_df(['mfr', 'calories', 'sugars', 'weight'], ['eq', 'lt', 'le', 'ge'], ['K', 90, 10, 1])

        self.assertEqual(len(series), 2)

    def testUpdate(self):
        almond_name = self.df.loc[4]['name']
        cereal.update(4, 'name', 'Almond Delight. Now with ekstra sugar')
        series = cereal.filter_df('name', 'eq', 'Almond Delight. Now with ekstra sugar')
        
        self.assertFalse(almond_name == series['name'].values)
        
        cereal.update(5, ['calories', 'sugars'], [1000, 900])
        series = cereal.filter_df('sugars', 'ge', 800)
        
        self.assertEqual(series['calories'].values, 1000)

    def testAddDeleteRow(self):
        df = cereal.add_row('Bread', 'J', 'B', 20, 1, 3, 50, 0.1, 0.2, 5, 20, 10, 4, 0.9, 0)
        content = ['Bread', 'J', 'B', 20, 1, 3, 50, 0.1, 0.2, 5, 20, 10, 4, 0.9, 0]

        series = cereal.filter_df('name', 'eq', 'Bread')
        
        for i,c in enumerate(self.columns):
            self.assertEqual(series[c].values, content[i])
            
        self.assertEqual(len(df), 78)
        
        series = cereal.delete(df, 76)
        
        self.assertEqual(len(series), 77)

    def testGetImage(self):
        r = cereal.get_image(5)

        self.assertTrue(r)
        
        with self.assertRaises(KeyError):
            cereal.get_image(100)

class CustomTestResult(unittest.TextTestResult):
    def printErrors(self):
        self.stream.writeln("Passed: {}".format(self.testsRun - len(self.failures) - len(self.errors)))
        self.stream.writeln("Failed: {}".format(len(self.failures)))
        self.stream.writeln("Errors: {}".format(len(self.errors)))
        super().printErrors()

class CustomTestRunner(unittest.TextTestRunner):
    resultclass = CustomTestResult

if __name__ == '__main__':
    unittest.main(testRunner=CustomTestRunner())
