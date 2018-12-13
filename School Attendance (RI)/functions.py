import pandas as pd

def bin_date(date):
    
    if date >= pd.Timestamp('2008-09-03') and date <= pd.Timestamp('2009-06-26'):
        return '2009'

    if date >= pd.Timestamp('2009-09-03') and date <= pd.Timestamp('2010-06-26'):
        return '2010'

    if date >= pd.Timestamp('2010-09-01') and date <= pd.Timestamp('2011-06-24'):
        return '2011'

    if date >= pd.Timestamp('2011-08-31') and date <= pd.Timestamp('2012-06-22'):
        return '2012'

    if date >= pd.Timestamp('2012-08-30') and date <= pd.Timestamp('2013-06-23'):
        return '2013'

    if date >= pd.Timestamp('2013-08-27') and date <= pd.Timestamp('2014-06-20'):
        return '2014'

    if date >= pd.Timestamp('2014-08-28') and date <= pd.Timestamp('2015-06-24'):
        return '2015'

    if date >= pd.Timestamp('2015-08-31') and date <= pd.Timestamp('2016-06-23'):
        return '2016'

    if date >= pd.Timestamp('2016-08-30') and date <= pd.Timestamp('2017-06-23'):
        return '2017'

    if date >= pd.Timestamp('2017-08-29') and date <= pd.Timestamp('2018-06-22'):
        return '2018'

    if date >= pd.Timestamp('2018-08-29') and date <= pd.Timestamp('2019-06-21'):
        return '2019'
    
    else:
        return 'out of season'