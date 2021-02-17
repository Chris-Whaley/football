# -*- coding: utf-8 -*-
"""
This script can be used to try the different datasets that can be retrieved
using the espn module.

Years: integer or list of integers of available years. Currently, 2006-2020
Weeks: integer or list of integers of available years. Currently, 1-17, for
        years 2006-2020.
Season_type: string. 'regular', 'postseason', or 'all'.
Stat_type: string. 'weekly' or 'leaders' (i.e., season leaders).
      
@author: cwhaley. 2021-02-17
"""
# Load packages
from espn import Qbr
import sys

# add folder to path list for python to look for module
sys.path.append(input("Please enter file path that espn.py is installed: "))

# check to see if path is now included
for path in sys.path:
    print(path)


#---- Weekly Stats
#-- Regular Season
# 1 year, 1 week
df = Qbr(years=2020, weeks=1)
df1 = df.load_qbr()
    
# 1 year, multiple weeks 
df2 = Qbr(years=2020, weeks=[1,2])
df3 = df2.load_qbr()

# multiple years, 1 week
df4 = Qbr(years=[2019,2020], weeks=1)
df5 = df4.load_qbr()

# multiple years, multiple weeks
df6 = Qbr(years=[2019, 2020], weeks=[1,2])
df7 = df6.load_qbr()


#-- Postseason
# 1 year, 1 week
df8 = Qbr(years=2020, weeks=1, season_type='postseason')
df9 = df8.load_qbr()
    
# 1 year, multiple weeks 
df10 = Qbr(years=2020, weeks=[1,2], season_type='postseason')
df11 = df10.load_qbr()

# multiple years, 1 week
df12 = Qbr(years=[2019,2020], weeks=1, season_type='postseason')
df13 = df12.load_qbr()

# multiple years, multiple weeks
df14 = Qbr(years=[2019, 2020], weeks=[1,2], season_type='postseason')
df15 = df14.load_qbr()




#---- Season Leaders
#-- Regular Season
# 1 year
df16 = Qbr(years=2020, weeks=1, stat_type='leaders')
df17 = df16.load_qbr()
    
# multiple years
df18 = Qbr(years=[2019,2020], weeks=1, stat_type='leaders')
df19 = df18.load_qbr()


#-- Postseason
# 1 year
df20 = Qbr(years=2020, weeks=1, season_type='postseason', stat_type='leaders')
df21 = df20.load_qbr()
    
# multiple years 
df22 = Qbr(years=[2019,2020], weeks=1, season_type='postseason', stat_type='leaders')
df23 = df22.load_qbr()








