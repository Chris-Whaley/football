# -*- coding: utf-8 -*-
"""
This module will read the html tables on ESPN QBR webpages. There are a two
mandatory parameters and 2 optional parameters. Data is available from 2006
to 2020.

Mandatory parameters:
    1. Year(s): requested years for seasons. 
        - either single year (integer) or multiple years (list of integers)
    2. Week(s): requested weeks for seasons.
        - either single year (integer) or multiple years (list of integers)
        
Optional parameters:
    1. Season type: regular season, postseason, or all. Same table format, 
        so can be unioned.         
    2. Stat type: weekly stats or season leaders. Different formats, so can
        only request either one.
        
This module relies on pandas module for reading the html tables, and creating
    the data manipulation for dataframes.

@author: cwhaley. 2021-02-17
"""

import pandas as pd    # reading ESPN webpages, creating dataframes



class Qbr:
    """
    Load ESPN's QBR data from their website. Able to get regular season or
    postseason, weekly stats or season leaders.
    """
    
    def __init__(self, years, weeks, season_type='regular', stat_type='weekly'):
         """ Initialize attributes to describe QBR stats from seasons and weeks."""
         self.years = years
         self.weeks = weeks
         self.season_type = season_type.lower().strip()
         self.stat_type = stat_type.lower().strip()
        
        
    def load_qbr(self):
        """
        Parameters
        ----------
        years : integer or list of integers
            years for seasons.
        weeks : integer or list of integers
            weeks of the season.
        season_type : string
            regular, postseason, or all seasons.
        stat_type: string
            'weekly' or 'leaders'.
            
        Returns
        -------
        Dataframe of quarterbacks and their repsective QBR stats.
        """
                
        # convert season values to url identifiers
        self.season_type = self.convert_season_identifiers(self.season_type)
        
        # if years entered is not integer or list of integers, throw exception
        self.years = self.convert_to_list(self.years)
        self.weeks = self.convert_to_list(self.weeks)

         
        # Stat Type: Return weekly or season leaders stats, or both
        if self.stat_type == 'weekly':
           final_df = self.load_weekly_qbr(self.years, self.weeks, self.season_type)
        
        elif self.stat_type == 'leaders':
            final_df = self.load_season_leaders_qbr(self.years, self.season_type)
            
        else:
            print("Please enter an appropriate choice for stat types: "
                  "weekly or leaders.")
        
        return final_df


    def load_weekly_qbr(self, years, weeks, season_type):
        """
        Parameters
        ----------
        years : int or list
            years for seasons.
        weeks : int or list
            weeks of the season.
        season_type : string
            regular, postseason, or all seasons.
            
        Returns
        -------
        Dataframes of quarterbacks and repsective QBR stats.
        """
        # initialize empty dataframe
        df = []
        
        # Loop through season type-year-month        
        try:
            for season_id in season_type:
                for year in years:
                    for week in weeks:
                        # no postseason week 4, so skip
                        if season_id == 3 and week == 4:
                            continue
                        else:
                            # pull data by season
                            url = f"https://www.espn.com/nfl/qbr/_/view/weekly/season/{year}/seasontype/{season_id}/week/{week}"
                
                            # webpage has 2 tables: one for QB, other for stats
                            dfs = pd.read_html(url)
                
                            # join both dataframes together by binding columns
                            stg_df = pd.concat(dfs, axis=1)
                    
                            # add a column for the year
                            stg_df['year'] = year
                            
                            # add column for season_type
                            stg_df['season_type'] = season_id
                            stg_df['season_type'] = ['regular' if x == 2 else 'postseason' for x in stg_df['season_type']]
                    
                            # append to other weeks
                            df.append(stg_df)
        except ImportError:
            print("No data to output. Check variables entered. "
                  "Note: there is no 'Week 4' webpage for postseason stats. "
                  "It is skipped, with Week 3 as Conference Championships, and "
                  "Week 5 as the Super Bowl.")
            
        except TypeError:
            print("Please enter valid parameters.")
        
        # row bind all years, weeks data together    
        try:
            weekly_df = pd.concat(df, ignore_index=True)
            
        # Raise exception when final dataframe is empty
        except ValueError:
            print("No data to output.")
            weekly_df = []
        
        return weekly_df
        
    
    def load_season_leaders_qbr(self, years, season_type):
        """
        Parameters
        ----------
        years : integer or list of integers
            Years for seasons.
        season_type : string
            'regular', 'postseason', or 'all'.
            
        Returns
        -------
        Dataframes of quarterbacks and repsective QBR stats.
        """
        # initialize empty dataframe
        df = []
        
        try:
            for season_id in season_type:
                for year in years:
                    # pull data by season
                    url = f"https://www.espn.com/nfl/qbr/_/season/{year}/seasontype/{season_id}"
        
                    # webpage has 2 tables: one for QB, other for stats
                    dfs = pd.read_html(url)
        
                    # join both dataframes together by binding columns
                    stg_df = pd.concat(dfs, axis=1)
            
                    # add a column for the year
                    stg_df['year'] = year
            
                    # append to other weeks
                    df.append(stg_df)
        except ValueError:
            print("No tables found.")
            leaders_df = []
            
        # row bind all years, weeks data together.     
        try:
            leaders_df = pd.concat(df, ignore_index=True)
        
        # Raise exception when final dataframe is empty
        except ValueError:
            print("No data to output.")
            leaders_df = []
            
        return leaders_df
    
    
    def convert_season_identifiers(self, season_type):
        """
        Convert the seasons needed to identifiers for url.
        
        Parameters
        ----------
        season_type : string
            Takes input of season types, and converts values to the identifiers
            ESPN uses in the QBR urls.
            string: 'regular', 'postseason', 'all'
            
        Returns
        -------
        List of identifiers for data requested.
            regular identifier: [2]
            postseason identifier: [3]
            all: [2,3]
        """
        # Create url identifiers based on seasons requested
        if self.season_type == 'regular':
            season_espn_identifiers = [2]
         
        elif self.season_type == 'postseason':
            season_espn_identifiers = [3]
        
        elif self.season_type == 'all':
            season_espn_identifiers = [2,3]
        
        else:
            season_espn_identifiers = print("Please enter either: 'regular', "
                                            "'postseason', or 'all'.")

        return season_espn_identifiers

    
    def convert_to_list(self, weeks_or_years):
        """
        Take user input of interger or list of integers, converts to list.
        Parameters
        ----------
        weeks_or_years : int, list
            Takes input of weeks or years for seasons, 
            and adds values to a list to be used in loops.
            
        Returns
        -------
        List of weeks or years for seasons of data requested.
        """
        # initialize an empty list
        out_list = []
        
        # if one number entered, verify variable is an int. if so, append to empty list
        if isinstance(weeks_or_years, int):
            out_list.append(weeks_or_years)
        
        # if list, check to see that all elements are integers.
        elif isinstance(weeks_or_years, list):
            out_list = weeks_or_years[:]
            for num in out_list:
                if not isinstance(num,int):
                    return None
                
        # neither integer or list of integers, give user feedback.            
        else:
            return None
        
        return out_list
        
    
  