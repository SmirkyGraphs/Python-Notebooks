import pandas as pd

def bin_date(date):
    if date >= pd.Timestamp('2008-08-13') and date <= pd.Timestamp('2009-06-30'):
        return '2009'
    if date >= pd.Timestamp('2009-08-13') and date <= pd.Timestamp('2010-06-30'):
        return '2010'
    if date >= pd.Timestamp('2010-08-13') and date <= pd.Timestamp('2011-06-30'):
        return '2011'
    if date >= pd.Timestamp('2011-08-13') and date <= pd.Timestamp('2012-06-30'):
        return '2012'
    if date >= pd.Timestamp('2012-08-13') and date <= pd.Timestamp('2013-06-30'):
        return '2013'
    if date >= pd.Timestamp('2013-08-13') and date <= pd.Timestamp('2014-06-30'):
        return '2014'
    if date >= pd.Timestamp('2014-08-13') and date <= pd.Timestamp('2015-06-30'):
        return '2015'
    if date >= pd.Timestamp('2015-08-13') and date <= pd.Timestamp('2016-06-30'):
        return '2016'
    if date >= pd.Timestamp('2016-08-13') and date <= pd.Timestamp('2017-06-30'):
        return '2017'
    if date >= pd.Timestamp('2017-08-13') and date <= pd.Timestamp('2018-06-30'):
        return '2018'
    if date >= pd.Timestamp('2018-08-13') and date <= pd.Timestamp('2019-06-30'):
        return '2019'
    if date >= pd.Timestamp('2019-08-13') and date <= pd.Timestamp('2020-06-30'):
        return '2020'
    else:
        return 'out of season'