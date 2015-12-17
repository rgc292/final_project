'''
Created on Nov 28, 2015

@author: Rafael rgc292 & Kristen kk3175
'''
import unittest
import line_graph as lg
import bar_graph as bg
import HousingComplaintsData as hd
from Pie_Chart import Pie_Chart
import os.path


class Test(unittest.TestCase):
    # Tests that the housing complaints dataset was opened and cleaned properly
    def test_housing_data_loaded_properly(self):
        housing_data_test = hd.HousingComplaintsData()
        
        test_shape = housing_data_test.master_dataset.shape
        expected_shape = (84201, 11)
        
        self.assertEquals(test_shape, expected_shape)
    
    # Tests that the construct_complaint_dataset function in the HousingComplaintsData class correctly constructs a complaint-specific and date-specific dataframe
    def test_construct_complaint_dataset(self):
        housing_data_test = hd.HousingComplaintsData()
        complaint_dataset = housing_data_test.construct_complaint_dataset(65, '20150801', '20150930') 
        
        test_shape = complaint_dataset.shape
        expected_shape = (6991, 10) 
        
        self.assertEquals(test_shape, expected_shape)  
           
    # Tests that the plot_by_violation_type function in the Pie_Chart class correctly generates and saves the pie chart.  
    def test_pie_chart_plot_by_violation_type(self):
        housing_data_test = hd.HousingComplaintsData()
        complaint_dataset = housing_data_test.construct_complaint_dataset(65, '20150801', '20150930')
        
        test_pie = Pie_Chart(complaint_dataset)
        test_pie.plot_by_violation_type()
        
        self.assertTrue(os.path.isfile('figures/piechart.pdf'))
        
    # Tests that the plot function in the bar_graph class correctly generates and saves the graph.  
    def test_bar_graph_plot_by_category(self):
        housing_data_test = hd.HousingComplaintsData()
        complaint_dataset = housing_data_test.construct_complaint_dataset(65, '20150801', '20150930')
        
        test_bar = bg.BarGraph()
        test_bar.plot_bar_graph(complaint_dataset)
        
        self.assertTrue(os.path.isfile('figures/bargraph.pdf'))
        
    # Tests that the plot function in the line_graph class correctly generates and saves the graph.  
    def test_line_graph_plot_by_category(self):
        housing_data_test = hd.HousingComplaintsData()
        complaint_dataset = housing_data_test.construct_complaint_dataset(65, '20150801', '20150930')
        
        test_line = lg.LineGraph()
        test_line.plot_line_graph(complaint_dataset)
        
        self.assertTrue(os.path.isfile('figures/linegraph.pdf'))
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()