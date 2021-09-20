from enum import Enum

import DatabaseConnector
import os
import numpy as np
import statsmodels.formula.api as smf
import pandas as pd
from matplotlib import pyplot as plt

class regression():

    def __init__(self, dependent, independents, groupType, description, xLabels, yLabel, title):
        self.dbc = DatabaseConnector(os.environ['LOCALMONGOSTR'])
        self.dependent = dependent # array of the dependent variable (results)
        self.independents = independents # array of independent variables (causes)
        self.groupType = groupType #a grouptype from regressionGroupType
        self.description = description #a description of the regression
        # self.regressionType = regressionType #the type of regression to perform

        self.xLabels = xLabels # for graphing
        self.yLabel = yLabel
        self.title = title


        self.beta = None
        self.alpha = None
        self.linearRegression()

    @classmethod
    def fromDict():
        pass

    def linearRegression(self):
        dataFrameArgs = {
           self.yLabel: self.dependent 
        }
        myFormula = self.yLabel + " ~ " 

        i = 0
        for IV in self.independents:
            dataFrameArgs[self.xLabels[i]] = IV
            if( i == 0):
                myFormula += self.xLabels[i] 
            else:
                myFormula += " + " + self.xLabels[i]
            i+=1
        df = pd.DataFrame(dataFrameArgs)

        mod = smf.ols(formula=myFormula, data=df)
        res = mod.fit()
        plt.figure(figsize=(12,6))
        plt.plot(df[self.xLabels[0]], df[self.yLabel], 'o')
        plt.plot(df[self.xLabels[0]], mod.predict(), 'r', linewidth=2)
        plt.xlabel = self.xLabels[0]
        plt.ylabel = self.yLabel
        plt.title = self.title
        plt.show()
        pass



class regressionAttributes(Enum):
    pass

#Roster, role, individual, team
class regressionGroupType(Enum):
    ROSTER = 'roster'
    TEAM = 'team'
    INDIVIDUAL = 'individual'
    ROLE = 'role'

# class regressionType(Enum):
#     LINEAR = True
#     NONLINEAR = False

