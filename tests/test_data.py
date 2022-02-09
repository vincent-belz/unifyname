# -*- coding: utf-8 -*-
import pandas as pd
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.append('..')
from unifyname.utils import unify_names, deduplicate_list_string


def test_output_unify_name():
    """ test that unify_names is working as expected"""

    data = pd.read_csv("./data/sample_data_nlp.csv",index_col=0)

    input_size = len(data['BAIRRO DO IMOVEL'].value_counts())

    data = unify_names(data,column='BAIRRO DO IMOVEL',threshold_count=500)

    output_size = len(data['BAIRRO DO IMOVEL'].value_counts())


    assert output_size < input_size
    assert data['BAIRRO DO IMOVEL'].unique()[0] == 'SANTA EFIGENIA'

def test_deduplication():
    """ test that deduplicate_list_string is working as expected"""

    list_in = ['SANTA EFIGENIA','SANTA IFIGENIA']
    list_ou = deduplicate_list_string(list_in,threshold=80)


    assert list_ou < list_in
    assert list_ou[0] == 'SANTA EFIGENIA'
