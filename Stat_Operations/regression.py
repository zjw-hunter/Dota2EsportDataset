from enum import Enum

import DatabaseConnector
import os
import numpy as np
import statsmodels.formula.api as smf
import statsmodels.api as sm
import pandas as pd
from matplotlib import pyplot as plt

class regression():

    def __init__(self, dependent, independents, groupType, description, xLabels, yLabel, title):
        self.dbc = DatabaseConnector.DatabaseConnector(os.environ['LOCALMONGOSTR'])
        self.dependent = dependent # array of the dependent variable (results)
        self.independents = independents # array of independent variables (causes)
        self.groupType = groupType #a grouptype from regressionGroupType
        self.description = description #a description of the regression
        # self.regressionType = regressionType #the type of regression to perform

        self.xLabels = xLabels # for graphing
        self.yLabel = yLabel
        self.title = title

        self.linearRegression()

        

    def linearRegression(self):
        dataFrameArgs = {
           self.yLabel: self.dependent 
        }
        
        myFormula = (self.yLabel) + " ~ " 

        i = 0
        for IV in self.independents:
            dataFrameArgs[self.xLabels[i]] = IV
            if( i == 0):
                myFormula += (self.xLabels[i])
            else:
                myFormula += " + " + (self.xLabels[i])
            i+=1
        df = pd.DataFrame(dataFrameArgs)

        mod = smf.ols(formula=myFormula, data=df).fit()
        print(mod.summary())
        fig =  plt.figure(figsize=(12,6))
        fig = sm.graphics.plot_regress_exog(mod, (self.xLabels[0]), fig=fig)
        plt.show()
    

#Roster, role, individual, team
class regressionGroupType(Enum):
    ROSTER = 'roster'
    TEAM = 'team'
    INDIVIDUAL = 'individual'
    ROLE = 'role'
