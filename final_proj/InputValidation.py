'''
Created on Nov 28, 2015

@author: Rafael rgc292 & Kristen kk3175
'''

import sys
from datetime import datetime

class InputValidation(object):
    '''
    This class obtains and validates the three user inputs needed to explore NYC housing complaints data.
    The three user inputs needed are:
    (1) housing complaint type ID
    (2) start date
    (3) end date
    
    Accepts a HousingComplaintsData master dataset in the form of a pandas dataframe as an argument.
    
    Contains a public function that prompts the user for the necessary inputs and validates them.
    
    Creates validated versions of the three user inputs and then returns them. 
    '''
    # Class attributes constructed from the dataset argument
    category_options = None
    valid_categories = None
    lowerbound_date = None
    upperbound_date = None
    

    def __init__(self, dataset):
        self.category_options = dataset.complaint_categories
        self.__build_valid_categories()
        self.lowerbound_date = dataset.all_dates.iloc[0]
        self.upperbound_date = dataset.all_dates.iloc[-1]
            
    '''
    Private function for constructing Class attributes
    '''    
    # Builds a list of housing complaint type IDs used for validating user input.    
    def __build_valid_categories(self):
        self.valid_categories = self.category_options['Complaint Type ID'].tolist()
        
            
    '''
    Private helper functions for validating the three user inputs (complaint type, start date, and end date).
    '''
    # Asks for the user to enter a complaint type ID and validates the input. If the input is valid, it is returned as an int. 
    def __validate_category_input(self):
        print ("\nHousing complaint types that you can explore are: ")
        print self.category_options.to_string(index=False)
        
        while True:
        
            try:
                raw_category_input = raw_input("\nPlease select a Complaint Type ID or type quit to exit: >>>")
                if raw_category_input == "quit":
                    sys.exit(0)
                
                # Casting the input to an integer throws a ValueError exception if the input is not an integer
                raw_category_input = int(raw_category_input)                   
                                                
                if raw_category_input in self.valid_categories:
                    return raw_category_input
                    break
                else:
                    print ('You entered an invalid complaint type ID. Please try again.')

            except (ValueError):
                print ('Complaint type IDs are numerical values! Please try again.')
                
             
    # Asks for user to enter a start date and validates the input. If the input is valid, it is returned as a datetime object in the format (yyyymmdd)
    def __validate_start_date_input(self):
        print ("\nNow we need a start date. We have housing complaints for the following date ranges: ")
        print ("%s through %s"%(str(self.lowerbound_date)[0:10], str(self.upperbound_date)[0:10]))
                
        while True:
            
            try:
                raw_start_date_input = raw_input("\nPlease enter a start date in the format of (yyyymmdd) or type quit to exit: ")
                if raw_start_date_input == "quit":
                    sys.exit(0)
                
                # Casting the input to an integer throws a ValueError if the input is not an integer
                raw_start_date_input = int(raw_start_date_input)  
                
                raw_start_date_input = datetime.strptime(str(raw_start_date_input), '%Y%m%d')      
                if self.__is_valid_start_date(raw_start_date_input):
                    return raw_start_date_input
                    break
                else:
                    print('You entered an invalid start date. Please try again.')
                   
            except ValueError:
                print ('You entered the date in an invalid format. Please try again.')
    
    
    # Accepts a start date in datetime format as an argument. Returns true if the start date is between the date ranges in the data set.                
    def __is_valid_start_date(self, raw_start_date_input):
        if (raw_start_date_input >= self.lowerbound_date) and (raw_start_date_input <= self.upperbound_date): return True
        else: return False
    
        
    # Asks for user to enter an end date and validates the input. If the input is valid, it is returned as a datetime object in the format (yyyymmdd) 
    def __validate_end_date_input(self, validated_start_date_input):
        print ("\nNow we need an end date. We have housing complaints for the following date ranges: ")
        print ("%s through %s"%(str(self.lowerbound_date)[0:10], str(self.upperbound_date)[0:10]))
                
        while True:
    
            try:
                raw_end_date_input = raw_input("\nPlease enter an end date in the format of (yyyymmdd) or type quit to exit: ")
                if raw_end_date_input == "quit":
                    sys.exit(0)
                
                # Casting the input to an integer throws a ValueError if the input is not an integer
                raw_end_date_input = int(raw_end_date_input)  
                
                raw_end_date_input = datetime.strptime(str(raw_end_date_input), '%Y%m%d')      
                if self.__is_valid_end_date(raw_end_date_input, validated_start_date_input):
                    return raw_end_date_input
                    break
                else:
                    print('You entered an invalid end date. Please try again.')            
            
            except ValueError:
                print ('You entered the date in an invalid format. Please try again.')
    
    
    # Accepts an end date in datetime format as an argument. Returns true if the end date is between the user selected start date and the last date in the data set.            
    def __is_valid_end_date(self, raw_end_date_input, validated_start_date_input):
        if (raw_end_date_input >= validated_start_date_input) and (raw_end_date_input <= self.upperbound_date): return True
        else: return False
                    
                 
      
    '''
    Public function
    
    Prompts the user for a housing complaint type ID, a start date, and an end date. Validates these inputs and then returns:
    (1) housing complaint type ID as an int
    (2) start date as a datetime object in the format (yyyymmdd)
    (3) end date as a datetime object in the format (yyyymmdd)
    '''     
    def validate_user_inputs(self):
        print 'In order to get started, we need to know what you are interested in looking at! You will be prompted to enter a housing complaint type, a start date, and an end date.'
        validated_category_id_input = self.__validate_category_input()
        validated_start_date_input = self.__validate_start_date_input()
        validated_end_date_input = self.__validate_end_date_input(validated_start_date_input)
        
        return validated_category_id_input, validated_start_date_input, validated_end_date_input