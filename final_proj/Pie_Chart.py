'''
Created on Dec 12, 2015

@author: Kristen kk3175 & Rafael rgc292
'''

import pandas as pd
import matplotlib.pyplot as plt

class Pie_Chart(object):
    '''
    Class that constructs pie charts to visualize NYC Housing Complaint Data.
    Class attribute is a dataframe containing data for one housing complaint type.     
    Performs the necessary data wrangling to generate pie charts.        
    '''
    dataset = None

    def __init__(self, complaint_dataset):
        self.dataset = complaint_dataset
    
    
    '''
    Private helper functions
    '''
    def __construct_complaints_breakdown(self):
        '''
        Constructs the dataframe necessary to plot a specific housing complaint by complaint breakdown in violation and non-violation categories.
        '''
        # Only use columns relevant to this data visualization
        complaints_breakdown = self.dataset[['MinorCategory', 'ViolationIssued']]
        
        # Filters for complaints that resulted in a violation
        complaints_breakdown_violations = complaints_breakdown[complaints_breakdown['ViolationIssued'] == 1]
        complaints_breakdown_violations = self.__construct_complaints_by_count(complaints_breakdown_violations)
        complaints_breakdown_violations.columns = ['Violation Issued']
                
        # Filters for complaints that resulted in no violation
        complaints_breakdown_no_violations = complaints_breakdown[complaints_breakdown['ViolationIssued'] == 0]
        complaints_breakdown_no_violations = self.__construct_complaints_by_count(complaints_breakdown_no_violations)
        complaints_breakdown_no_violations.columns = ['Violation Not Issued']
        
        # Concatenates the violation and no violation dataframes into one dataframe that is pie chart plot-friendly
        complaints_breakdown = pd.concat([complaints_breakdown_violations, complaints_breakdown_no_violations], axis=1)
        
        return complaints_breakdown
        
        
    def __construct_complaints_by_count(self, complaints_dataset):
        '''
        Takes a complaint dataset, merges the complaint descriptions into one description, and then counts the number of times the
        complaint description occurred.
        
        Returns this dataframe.
        '''
        # Explicitly declares the dataset as a copy to prevent ambiguity that the dataset could be a slice.
        complaints_dataset = complaints_dataset.copy()
                
        # Reduce column to just the complaint type    
        complaints_dataset = complaints_dataset[['MinorCategory']] 
        
        # Rename the column so it is more user friendly
        complaints_dataset.columns = ['Complaint Description']      
        
        # Group by complaint description and count the number of times this complaint description occurs
        complaints_dataset = complaints_dataset.groupby(['Complaint Description']).size().reset_index()
        
        # Order in ascending order
        complaints_dataset = complaints_dataset.sort_values(['Complaint Description'], ascending=True)            
        complaints_dataset = complaints_dataset.set_index(['Complaint Description'])                  
            
        return complaints_dataset
        
      
    '''
    Public function
    '''       
    def plot_by_violation_type(self):
        '''
        Displays the specific subtypes of a housing complaint that resulted in violations and no violations.
        '''
        # Construct dataframe for pie charts
        complaints_breakdown = self.__construct_complaints_breakdown()
           
        # Make pie charts
        colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'yellow', 'skyblue', 'rosybrown']
        
        fig, axes = plt.subplots(1,2, figsize=(12,8))
        for ax, col in zip(axes, complaints_breakdown.columns):
            ax.pie(complaints_breakdown[col], labels=complaints_breakdown.index, colors=colors, startangle=30)
            ax.set(ylabel='', title=col, aspect='equal')
       
        plt.rcParams['font.size'] = 9.0
        
        fig.savefig('figures/piechart.pdf', bbox_inches='tight')
        
        plt.close('all')