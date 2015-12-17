'''
Created on Nov 13, 2015

@author: Kristen kk3175 & Rafael rgc292


This program was developed for offering visual analyses for use in understanding data 
collected from housing complaints by the NYC Department of Housing Preservation and Development.

'''

from HousingComplaintsData import HousingComplaintsData
from VisualAnalyses import make_visual_analyses
import InputValidation as vl
import sys

'''
Main program that produces NYC housing complaint visual analyses by the complaint type and date range
selected by the user.

Visual analyses are saved in the figures folder.
'''

if __name__ == '__main__':
    pass

    print '\nThis program lets you explore NYC housing complaints by the type of complaint and the date range you select.'
    print '\nLoading NYC housing complaints data set. This will take a few seconds...'
    
    housing_complaints_data = HousingComplaintsData()
    validation = vl.InputValidation(housing_complaints_data)
    
    # Loop until user wants to quit
    while True:
        try:
            user_response = raw_input('\nWould you like to explore a housing complaint? (yes/no)  ')
            user_response = user_response.lower()
            
            # If the user wants to quit, the loop breaks and the program is done.
            if user_response == 'no':
                print 'Okay, good bye!'
                break
            
            # If the user wants to continue, the user is prompted for inputs. Visual analyses are
            # generated from these inputs.
            elif user_response =='yes':
                category_id, start_date, end_date = validation.validate_user_inputs()
                complaint_data = housing_complaints_data.construct_complaint_dataset(category_id, start_date, end_date)
                make_visual_analyses(complaint_data)
                
            else:
                print 'That is not a valid answer. Please try again.'
                    
        except (EOFError, IOError, KeyboardInterrupt, SystemExit):
            print 'Interrupted. Good bye!'
            sys.exit(1)