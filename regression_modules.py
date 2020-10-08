## import libraries
import sklearn, scipy
import os
import numpy as np
import pandas as pd
from sklearn import linear_model
from scipy import stats
import statsmodels 
import matplotlib.pyplot as plt
import statsmodels.stats.api as sms
from statsmodels.compat import lzip 
import statsmodels.formula.api as smf 

# build regression modeling process
# Load data
url = 'https://raw.githubusercontent.com/vincentarelbundock/Rdatasets/master/csv/HistData/Guerry.csv'
dat = pd.read_csv(url)

# Fit regression model (using the natural log of one of the regressors)
results = smf.ols('Lottery ~ Literacy + np.log(Pop1831)', data=dat).fit()
residuals = results.resid
exogVars = results.model.exog
# Inspect the results
print(results.summary())
# test assumptions for linear regression
# test for normality

## Q-Q plot
## Input array. Should be 1-dimensional
def qqPlot(array):
    modelFit = statsmodels.OLS(array).fit
    residuals = modelFit.resid
    fig = statsmodels.qqplot(residuals)
    plt.show()

## shapiro wilk test
## returns test statistic and p value
def shapiroWilk(array):
    swTest = stats.shapiro(array)
    print(swTest)
    
## Jarque-Bera test for normality of residuals
def jarqueBeraTest(residuals):
    name = ['Jarque-Bera', 'Chi^2 two-tail prob.', 'Skew', 'Kurtosis']
    test = sms.jarque_bera(residuals)
    lzip(name, test)
    
## omni test for normality of residuals
def omniTest(residuals):
    name = ['Chi^2', 'Two-tail probability']
    test = sms.omni_normtest(residuals)
    lzip(name, test)

# transform the data if not normal
# Input array. Should be 1-dimensional
def boxCox(array):
    bcTest = stats.boxcox(array)
    print(bcTest)
    fig = plt.figure()
    ax = fig.add_subplot(212)
    stats.probplot(bcTest, dist=stats.norm, plot=ax)
    ax.set_title('Probplot after Box-Cox transformation')
    plt.show()

# test for multicolinearity
## Variance Inflation Factor - center the data or remove independent variables with high VIF
from statsmodels.stats.outliers_influence import variance_inflation_factor    

def calculate_vif_(X, thresh=5.0):
    variables =  list(range(X.shape[1]))
    dropped=True
    while dropped:
        dropped=False
        vif = [variance_inflation_factor(X.iloc[:,variables].values, ix) for ix in range(X.iloc[:,variables].shape[1])]

        maxloc = vif.index(max(vif))
        if max(vif) > thresh:
            print('dropping \'' + X.iloc[:,variables].columns[maxloc] + '\' at index: ' + str(maxloc))
            del variables[maxloc]
            dropped=True

    print('Remaining variables:')
    print(X.columns[variables])
    return X.iloc[:,variables]


### test for auto-correlation - assume that observations are ordered by time
## Durbin-Watson test
def durbinWatson(array):
    modelFit = statsmodels.OLS(array).fit
    residuals = modelFit.resid
    statsmodels.stats.stattools.durbin_watson(residuals, axis=0)

### test for homoscedasticity
##  Goldfeld-Quandt Test
def goldfeldQuandtTest(residuals,exogVars):
    name = ['F statistic', 'p-value']
    test = sms.het_goldfeldquandt(residuals, exogVars)
    lzip(name, test)

## test for linearity
## Harvey-Collier multiplier test for Null hypothesis that the linear specification is correct
def harveyCollier(results):
    name = ['t value', 'p value']
    test = sms.linear_harvey_collier(results)
    lzip(name, test)

