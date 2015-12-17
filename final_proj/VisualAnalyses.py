'''
Created on Dec 12, 2015

@author: Kristen kk3175 & Rafael rgc292
'''

import line_graph as lg 
import bar_graph as bg
from Pie_Chart import Pie_Chart


'''
Module to perform visual analyses of a specific NYC housing complaint.

Takes a complaint dataset as an argument.

Makes pie charts, line graphs, and bar graphs so the user can understand the housing
complaint data from different viewpoints.
'''
def make_visual_analyses(complaint_dataset):
    print 'Making visual analysis tools...'
    
    try:    
        pie_chart = Pie_Chart(complaint_dataset)
        pie_chart.plot_by_violation_type()
    
        line_graph = lg.LineGraph()
        line_graph.plot_line_graph(complaint_dataset)

        bar_graph = bg.BarGraph()
        bar_graph.plot_bar_graph(complaint_dataset) 
    
        print '\nFigures are now saved in the figures folder.'
        
    except (ValueError, TypeError):
        print "\nYour range of dates does not contain information for your choice of ID."
        print "Please, choose a different combination."
        
 