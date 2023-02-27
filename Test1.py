# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import calendar
import os
from datetime import datetime
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)



########## Switches ###########
debug_mode = 0           # 0 , 1
plot_mode  = 'current'   # 'all' , 'current'



########## Functions ###########

# !Adding value labels on bar charts
def addlabels(x,y,pos):
    for i in range(len(x)):
        plt.text( y[i]//2, i+pos-0.1 ,y[i], ha = 'center')

    
########## Auxiliary variables ##########
# Thresholds for each costs
Threshold_food          = 30000 
Threshold_entertainment = 20000
Threshold_dress         = 10000
Threshold_work          = 5000
Threshold_fastfood      = 5000
Threshold_transport     = 30000
Threshold_workoutstuff  = 2000
Thresholds = np.array([Threshold_food,Threshold_entertainment,Threshold_dress,Threshold_work,Threshold_fastfood,Threshold_transport,Threshold_workoutstuff])

width  = 0.3
colors = ['g','grey','c','y', 'orange','b','m']

Month_Names  = list(calendar.month_name)
today        = datetime.now()  
Month_Number = today.month
CurrentMonth = calendar.month_name[Month_Number]

# Creating variables for the Excel file names
Format       = '.xlsx'
Folder       = '2023'
File_Names   = [x+Format  for x in Month_Names]

# Creating title strings for the plots
Title_string = ' Monthly Cost'
Title        = [x + Title_string  for x in Month_Names]

# Memory allocations
Savings         = np.zeros((len(colors),12), dtype=int)
Monthly_Savings = np.zeros(12, dtype=int)
if debug_mode == 1:
    
    print(File_Names)
    print(Title)



########## Monthly report ##########
for i in range(0,12):
    
    # Searching for the excel files
    path      = Folder + "\\" + File_Names[i+1]
    data_frame = pd.read_excel(path) 
    
    if debug_mode == 1:
    
        print(path)
        print(i)
    
    # Reading the excel files into arrays
    Values_Cost = np.array(data_frame.values.tolist())
    Names_Cost  = data_frame.columns.ravel()   
    Main_Names   = Names_Cost[1:8]
    
    # Memory allocation
    Sum_Costs   = np.zeros(len(Main_Names), dtype=int)
    y_pos       = np.arange(len(Main_Names))
    
    for j in range(0,7):
        Sum_Costs[j] = sum(Values_Cost[:,j+1])
    
    # Calculation of the different costs    
    Monthly_Sum    = sum(sum(Values_Cost[:,1:8]))   
    Available_Cost = Thresholds - Sum_Costs
    
    if plot_mode == 'all':
    
        # Bar Plot (Horizontal)    
        fig, ax = plt.subplots()
        ax.barh(y_pos+width, Sum_Costs, width, color = 'blue' )
        ax.barh(y_pos, Available_Cost, width, color = 'green')   
        ax.barh(y_pos-width, Thresholds, width, color = 'red')
        addlabels(y_pos, Sum_Costs, width)
        addlabels(y_pos, Available_Cost, 0)
        addlabels(y_pos, Thresholds, -width)
        plt.yticks(y_pos, Main_Names)
        plt.xlabel('HUF')
        plt.title(Title[i+1])
        plt.grid(axis='x')
        ax.set_axisbelow(True)
        plt.legend(['Current','Available','Threshold'])
        plt.show() 
        
        # Area Plot With percentage
        slice      = Sum_Costs
        activities = Main_Names
        plt.pie(slice, labels =activities, colors = colors, startangle = 90, shadow = True, explode =(0.1,0.1,0.1,0.1,0.1,0.1,0.1), autopct ='%1.1f%%')
        plt.title('Cost ratio/'+'Sum Cost : '+str(Monthly_Sum)+' Ft')
        plt.grid()
        plt.show() 
        
    
    elif plot_mode == 'current':
    
        if CurrentMonth == Month_Names[i+1]:
            
            # Bar Plot (Horizontal)
            fig, ax = plt.subplots()
            ax.barh(y_pos+width, Sum_Costs, width, color = 'blue' )
            ax.barh(y_pos, Available_Cost, width, color = 'green')   
            ax.barh(y_pos-width, Thresholds, width, color = 'red')
            addlabels(y_pos, Sum_Costs, width)
            addlabels(y_pos, Available_Cost, 0)
            addlabels(y_pos, Thresholds, -width)
            plt.yticks(y_pos, Main_Names)
            plt.xlabel('HUF')
            plt.title(Title[i+1])         
            plt.grid(axis='x')
            ax.set_axisbelow(True)
            plt.legend(['Current','Available','Threshold'])
            plt.show() 

            # Area Plot With percentage
            slice      = Sum_Costs
            activities = Main_Names
            plt.pie(slice, labels =activities, colors = colors, startangle = 90, shadow = True, explode =(0.1,0.1,0.1,0.1,0.1,0.1,0.1), autopct ='%1.1f%%')
            plt.title('Cost ratio/'+'Sum Cost : '+str(Monthly_Sum)+' Ft')
            plt.grid()
            plt.show()


########## Saving Calculations ##########
for i in range(Month_Number):
    
    # Searching for the excel files
    path      = Folder + "\\" + File_Names[i+1]
    data_frame = pd.read_excel(path) 
    
    if debug_mode == 1:
    
        print(path)
        print(i)
    
    # Reading the excel files into arrays
    Values_Cost = np.array(data_frame.values.tolist())
    Names_Cost  = data_frame.columns.ravel()   
    Main_Names   = Names_Cost[1:8]
    
    # Memory allocation
    Sum_Costs   = np.zeros(len(Main_Names), dtype=int)
    y_pos       = np.arange(len(Main_Names))
    
    for j in range(0,7):
        Sum_Costs[j] = sum(Values_Cost[:,j+1])
    
    # Calculation of savings    
    Monthly_Sum = sum(sum(Values_Cost[:,1:8]))   
    Savings[:,i] = Thresholds - Sum_Costs
    Monthly_Savings[i] = sum(sum(Savings))

