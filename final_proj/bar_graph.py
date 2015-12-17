'''
Created on Nov 13, 2015

@author: Rafael rgc292 & Kristen kk3175
'''

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class BarGraph(object):
    '''
    This class is intended to plot bar graphs as part of the housing data visual analyses
    '''


    def __init__(self):
        pass
    
    '''
    Public function that plots a bar graph having the number of complaints over time 
    '''    
    def plot_bar_graph(self, complaint_dataset):
        self.complaint_dataset = pd.DataFrame()
        self.complaint_dataset = complaint_dataset
        
        # Adjust dataset for plotting
        category = self.complaint_dataset['MajorCategory'].unique()[0]
        self.complaint_dataset = self.rows_violation_1(self.complaint_dataset)
        self.complaint_dataset = self.keep_needed_columns(self.complaint_dataset)
        self.complaint_dataset = self.agregate_by_minor_category(self.complaint_dataset)
        
        # Create figure for plotting  
        ax = self.complaint_dataset.plot(kind='bar')
        fig = ax.get_figure()
        
        # Set graph labels and graph size on the figure
        plt.legend('', title=category, fontsize='xx-small', loc='best')
        plt.title('Distribution Of Violations Per Minor Category')
        plt.ylabel('Number Of Violations')
        plt.xlabel('Minor Category')
        plt.xticks(rotation=14, fontsize='xx-small')
        plt.subplots_adjust(top=.9, left=.09, right=.99, bottom=.15 )
        
        # Save graph to .pdf file
        fig.savefig('figures/bargraph.pdf')
        
        # Close figure
        plt.close('all')
        plt.clf()
        
    '''
    Helper functions
    '''        
        
    # Take rows having ViolationIssued == 1    
    def rows_violation_1(self, complaint_dataset):
        self.complaint_dataset = pd.DataFrame()
        self.violation_1_dataset = pd.DataFrame()
        self.complaint_dataset = complaint_dataset
        self.violation_1_dataset = self.complaint_dataset[self.complaint_dataset['ViolationIssued'] != 0]
        
        return self.violation_1_dataset
    
    
    # Drop unneeded columns for plotting
    def keep_needed_columns(self, violation_1_dataset):
        self.violation_1_dataset = pd.DataFrame()
        self.needed_columns = pd.DataFrame()
        self.violation_1_dataset = violation_1_dataset
        self.needed_columns = self.violation_1_dataset.drop(['TypeID', 'Type', 'MajorCategoryID', 
                                       'MajorCategory', 'MinorCategoryID', 'StatusDate',
                                       'CodeID', 'Code'], axis=1)
        
        return self.needed_columns
    
    
    # Group the dataset by date for plotting
    def agregate_by_minor_category(self, needed_columns_dataset):
        self.agregate_minor = pd.DataFrame()
        self.needed_columns = pd.DataFrame()
        self.needed_columns = needed_columns_dataset
        self.agregate_minor = self.needed_columns.groupby('MinorCategory').agg({
                                                        'ViolationIssued': np.sum}) 
        
        return self.agregate_minor