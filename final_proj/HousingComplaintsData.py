'''
Created on Nov 26, 2015

@author: Kristen kk3175 & Rafael rgc292
'''

import pandas as pd
import sys

class HousingComplaintsData(object):
    '''
    Class that handles the NYC housing complaints data set.
    '''
    # Path of housing complaints dataset, which was downloaded from NYC Open Data at https://data.cityofnewyork.us/Housing-Development/Complaint-Problems/a2nx-4u46
    complaints_file = 'complaint_problems.csv'

    # Class attributes
    master_dataset = None
    complaint_categories = None
    all_dates = None
    
    
    def __init__(self):
        self.__construct_master_dataset()
        self.__construct_complaint_categories()
        self.__construct_all_dates()


    '''
    Private functions to construct Class attributes
    '''
    # Constructs the master dataset to be used for data analysis
    def __construct_master_dataset(self):
        try:
            self.master_dataset = pd.read_csv(self.complaints_file, delimiter=',', low_memory=False)
        
        except IOError:
            print '\nA .csv dataset is needed!'
            print "\nPlease verify your dataset's source below and try again."
            print 'https://data.cityofnewyork.us/Housing-Development/Complaint-Problems/a2nx-4u46'
            sys.exit(1)
        
        self.__drop_duplicates()
        self.__drop_incomplete_records()
        self.__drop_open_complaints()
        self.__enumerate_complaint_outcome()
        self.__drop_irrelevant_columns()
        self.__convert_to_datetime()
        self.__sort_by_date()

            
    # Constructs a dataframe of unique complaint categories and IDs    
    def __construct_complaint_categories(self):
        self.complaint_categories = self.master_dataset[['MajorCategoryID', 'MajorCategory']].copy()
        self.complaint_categories.drop_duplicates(inplace=True)
        self.complaint_categories = self.complaint_categories.sort_values(by='MajorCategoryID')
        
        # Renames the columns so they are more user friendly
        self.complaint_categories.columns = ['Complaint Type ID', 'Complaint Type']

    
    # Constructs a dataframe of unique dates sorted in ascending order.        
    def __construct_all_dates(self):
        self.all_dates = self.master_dataset['StatusDate']
        self.all_dates.drop_duplicates(inplace=True)

               
    # Cleans the dataset so all of its rows are unique   
    def __drop_duplicates(self):
        self.master_dataset.drop_duplicates(inplace=True)


    # Cleans the dataset by keeping only rows with valid values 
    def __drop_incomplete_records(self):
        self.master_dataset = self.master_dataset[~(self.master_dataset.isnull().any(axis=1))]


    # Complaints that are still open are dropped since the outcome of the complaint is still pending.    
    def __drop_open_complaints(self):
        self.master_dataset = self.master_dataset[(self.master_dataset.Status != 'OPEN')]


    # Categorizes the complaint outcome into violation (represented as 1) or no violation (represented as 0).
    def __enumerate_complaint_outcome(self):
        valid_violations = self.__populate_valid_violations()

        new_violation_column = 'ViolationIssued'
        
        self.master_dataset[new_violation_column] = 0
        for index in range(len(valid_violations)):
            self.master_dataset.loc[self.master_dataset['StatusDescription'] == valid_violations[index], new_violation_column] = 1

               
    # Helper function that makes and returns a list containing complaint outcomes that resulted in a violation.
    def __populate_valid_violations(self):
        # Complaint outcomes that resulted in violations were manually selected after looking at all unique complaint outcomes 
        # in the 'StatusDescription' column.
        valid_violations_file = 'complaint_outcomes_violations.txt'
        
        try:
            valid_violations = open(valid_violations_file).readlines()
        
        except IOError:
            print 'The complaint_outcomes_violations.txt file is missing!'
            print 'Please, assure its existence in the main directory and try again.'
            print 'Good bye'
            sys.exit(1)
        
        for index, valid_violation in enumerate(valid_violations):
            valid_violations[index] = valid_violation.rstrip()
        
        return valid_violations
    
    
    # Filter the dataset keeping only needed columns for analysis
    def __drop_irrelevant_columns(self):
        
        '''Some dataset can have the 'Unnamed: 0' which need to be removed.'''
        
        irrelevant_columns = ['ProblemID', 'ComplaintID', 'UnitTypeID', 'UnitType', 'SpaceTypeID ', 'SpaceType', 'StatusID', 'Status', 'StatusDescription']
        irrelevant_columns_unnamed = ['Unnamed: 0', 'ProblemID', 'ComplaintID', 'UnitTypeID', 'UnitType', 'SpaceTypeID ', 'SpaceType', 'StatusID', 'Status', 'StatusDescription']
        
        try:     
            for irrelevant_column_unnamed in irrelevant_columns_unnamed:
                self.master_dataset.drop(irrelevant_column_unnamed, axis=1, inplace=True)
         
        except ValueError:
            for irrelevant_columns in irrelevant_columns:
                self.master_dataset.drop(irrelevant_columns, axis=1, inplace=True)

                    
    # Converts the 'StatusDate' column to datetime format.
    def __convert_to_datetime(self):  
        self.master_dataset['StatusDate'] = pd.to_datetime(self.master_dataset['StatusDate'])
        
        
    # Sorts the dataset in ascending order by 'StatusDate'.     
    def __sort_by_date(self):
        self.master_dataset = self.master_dataset.sort_values(['StatusDate'], ascending=True).reset_index()
                
            

    '''
    Public function
    
    Accepts three arguments: 
    (1) category_id: housing complaint type ID as an int
    (2) start_date: start date as a datetime object in the format (yyyymmdd)
    (3) end_date: end date as a datetime object in the format (yyyymmdd)
    
    Creates and returns a dataframe with the complaint category and date range of interest.
    '''
    def construct_complaint_dataset(self, category_id, start_date, end_date):
        # Filter dataset for the complaint category id of interest
        complaint_dataset = self.master_dataset[(self.master_dataset.MajorCategoryID == category_id)]
                   
        # Filter datset for the date ranges of interest
        complaint_dataset = complaint_dataset[(complaint_dataset['StatusDate'] >= start_date) & (complaint_dataset['StatusDate'] <= end_date)]
        complaint_dataset = complaint_dataset.sort_values(['StatusDate'], ascending=True).reset_index()
        
        # Drop unnecessary columns
        complaint_dataset.drop('level_0', axis=1, inplace=True)
        complaint_dataset.drop('index', axis=1, inplace=True)
        
        return complaint_dataset