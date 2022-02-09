import pandas as pd
import numpy as np
from fuzzywuzzy import fuzz, process



def get_most_likely_neighbourhoods(df,column,threshold):
    '''This function takes as input a dataframe, a column name and a threshold
    it filters the string in the column that have a value counts above the threshold'''
    list_neighbourhoods = df[column].value_counts()
    df_neighbourhoods = pd.DataFrame(list_neighbourhoods)
    df_neighbourhoods = df_neighbourhoods.reset_index()
    df_neighbourhoods.columns = ['neighbourhood', 'counts']
    df_neighbourhoods = df_neighbourhoods.loc[df_neighbourhoods['counts']>threshold,:]
    output = df_neighbourhoods['neighbourhood'].values
    return output

def deduplicate_list_string(list_input,threshold):
    '''This function takes as input a list and a threshold
    and deduplicate name in the list based on the threshold'''
    list_output = list(process.dedupe(list_input, threshold=threshold, scorer=fuzz.token_sort_ratio))
    return list_output

def get_all_unique_names(df,column):
    '''This function takes as input a dataframe and a column name
    and return all unique string in this column removing NaN'''
    output = list(df[column].unique())
    if np.nan in output:
        output.remove(np.nan)
    return output

def get_match_score(list_all,list_unique):
    '''This function takes as input 2 lists list_all and list_unique
    and return a dataframe with match and score for each names within list_all
    with a match from list_unique'''

    match = []
    score = []

    for w in list_all:

        result = process.extractOne(w, list_unique,     scorer=fuzz.token_sort_ratio)

        match.append(result[0])
        score.append(result[1])

    df = pd.DataFrame({'names': list_all,'best_match': match,'score': score})

    return df

def get_new_names(df,threshold):
    '''This function takes as input a dataframe and a threshold
    and it update names in a new column new_names when the matching score is above the threshold'''
    df['new_names'] = df['names']
    df.loc[df['score']>=threshold,'new_names'] = df.loc[df['score']>=threshold,'best_match']
    return df

def update_table_with_new_name(df,df_match,column):
    '''This function takes as input 2 dataframe and a column name
    it update the column from first dataframe with new_names in the second dataframe'''
    df = df.merge(df_match[['names','new_names']], left_on=column,right_on='names', how='left')
    df[column] = df['new_names']
    df = df.drop(columns=['names','new_names'])
    return df


def unify_names(df,column,threshold_count=850, threshold_dedup = 80, threshold_match = 80):
    '''This function takes as input a dataframe and a column name as well as threshold parameters
    and it applies several functions in order to unify names in the column of the dataframe'''

    unique_names = get_most_likely_neighbourhoods(df,column=column,threshold=threshold_count)
    unique_names = deduplicate_list_string(unique_names,threshold=threshold_dedup)

    all_names = get_all_unique_names(df, column=column)

    df_match = get_match_score(all_names,unique_names)

    df_match = get_new_names(df_match,threshold=threshold_match)

    df = update_table_with_new_name(df,df_match,column = column)

    return df
