from sklearn.datasets import load_boston
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

import pandas as pd
import numpy as np


# Gather Data
boston_dataset = load_boston()
data=pd.DataFrame(data=boston_dataset.data,columns=boston_dataset.feature_names)
features= data.drop(['INDUS','AGE'],axis=1)
#features.head()
log_prices=np.log(boston_dataset.target)
target=pd.DataFrame(log_prices,columns=['PRICE'])
#target.shape


CRIME_IDX=0
ZN_IDX=1
CHAS_IDX=2
RM_IDX=4
PTRATIO_IDX=8


ZILLOW_MEDIAN_PRICE=583.3
SCALE_FACTOR=ZILLOW_MEDIAN_PRICE/np.median(boston_dataset.target)

property_stats = features.mean().values.reshape(1,11)

reg=LinearRegression().fit(features,target)
fitted_vals=reg.predict(features)


#Challenge : calculate the MSE and RMSE using sklearn

MSE= mean_squared_error(target,fitted_vals)
RMSE = np.sqrt(MSE)


def get_log_estimate(nr_rooms,students_per_classroom,next_to_river=False,high_confidence=True):
    
    #Configure Property
    property_stats[0][RM_IDX]= nr_rooms
    property_stats[0][PTRATIO_IDX]=  students_per_classroom
    
    
    if next_to_river:
        property_stats[0][CHAS_IDX]=1
    else :
        property_stats[0][CHAS_IDX]=0
    
    
    # Make perdiction
    
    log_estimate=reg.predict(property_stats)[0][0]
    
    # Calc Range
    
    if high_confidence:
        upper_bound=log_estimate + 2*RMSE
        lower_bound= log_estimate-2*RMSE
        interval=95
    else:
        upper_bound=log_estimate+RMSE
        lower_bound=log_estimate-RMSE
        interval=68
        
    return log_estimate,upper_bound,lower_bound,interval


def get_dollor_estimate(rm,ptratio,chas=False,large_range=True):
    ''' Estimate the price of property in Boston
    
    Keywords agruments:
    rm-- number oof rooms in the property
    ptratio-- no of stdents per teachers in tthe classroom for the school in the area
    chas-- True if the property is next to river, False otherwise
    large_range-- True for a 95% predection intervel, False for a 68% interval
    '''
    
    
    
    
    if rm<1 or ptratio<1:
        print('This is unrealistic try with another ')
        return
    
    # Convert to today's dollors
    log_est,upper,lower,conf=get_log_estimate(rm,ptratio,next_to_river=chas,high_confidence=large_range)
    
    
    dollor_est=np.e**log_est * 1000 * SCALE_FACTOR

    dollor_hi=np.e**upper * 1000 * SCALE_FACTOR

    dollor_low=np.e**lower * 1000 * SCALE_FACTOR

    # Round the dollor values to nearest thousand

    rounded_est=np.around(dollor_est,-3)
    rounded_hi=np.around(dollor_hi,-3)
    rounded_low=np.around(dollor_low,-3)

    print('Estimated Value',rounded_est)
    print('Upper range',rounded_hi)
    print('Lower range',rounded_low)







