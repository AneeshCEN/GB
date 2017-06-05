'''
Created on May 12, 2017

@author: aneesh.c
'''

import os.path
import sys
import yaml
from config import *
import pandas as pd
import MySQLdb


try:
    import apiai
except ImportError:
    sys.path.append(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)
    )
    import apiai

CLIENT_ACCESS_TOKEN = '494d85ef41a84920ab4744cf11dda13d'

def connect_to_db():
    db = MySQLdb.Connection(host=host_inventory,
                         user=user_inventory,
                         passwd=passwd_inventory,
                         db=db_inventory)
    return db



def db_query(out_dict, db, search_string):
    print 'out_dict', out_dict
    results = []
    query = "select Model, Capacity, Caliber, \
Barrel_Length from gun_bro.gun_genius where user_type = '%s' and user_subtype = '%s' and \
Capacity is not null and Caliber is \
not null and Barrel_Length is not null limit 16;" %(out_dict['purpose'], out_dict[search_string])
    print query 
    try:
        df_type = pd.read_sql(query, db)
        results = df_type.to_dict(orient='records')
    except Exception as e:
        print e
    return results


def db_query_shooter(ent_dict, db):
    results = []
    user_sub_types = targets_guns[ent_dict['targets_shooter']]
    print user_sub_types
    query = "select Model, Capacity, Caliber, \
Barrel_Length from gun_bro.gun_genius where user_type = 'shooter' and \
user_subtype = '"
    user_sub_types_list = user_sub_types.split(', ')
    string_query = ''
    string_begning = ''
    if len(user_sub_types_list) >= 2:
        if len(string_query) == 0:
            string_begning += string_query + user_sub_types_list[0] + "'"
            print 'first', string_begning
        user_sub_types_list = user_sub_types_list[1::]
        print 'user', user_sub_types_list
        string_query =  ''.join([string_query+' or user_subtype= '+"'"+i+"'" for i in user_sub_types_list])
        query = query  + string_begning + string_query
    else:
        string_query = user_sub_types_list[0]+"'"
        query = query + string_query
    print 'final', query
    try:
        df_type = pd.read_sql(query, db)
        results = df_type.to_dict(orient='records')
    except Exception as e:
        print e
    return results


def check_for_shooter(ent_dict, dict_input, out_dict, db):
    if ent_dict['purpose'] == 'shooter' and ent_dict['targets_shooter'] == '':
        out_dict['messageText'] = []
        out_dict['messageText'].append(type_of_shooting)
        out_dict['messageText'].append(objects)
    elif ent_dict['targets_shooter'] != '':
        out_dict['messageText'] = []
        ent_dict['purpose'] = 'shooting'
        results = db_query_shooter(ent_dict, db)
        if len(results) != 0:
            if ent_dict['targets_shooter'].endswith('Shooting'):
                out_dict['messageText'].append(first_end_note +[ent_dict['targets_shooter']])
            else:
                out_dict['messageText'].append(first_end_note +[' '+ent_dict['targets_shooter']+' shooting'])
            out_dict['messageText'].append(end_note)
            out_dict['ResultBuyer'] = results
        else:
            out_dict['messageText'].append(no_recommendation)
    return out_dict


def check_for_prepper(ent_dict, dict_input, out_dict, db):
    if ent_dict['purpose'] == 'prepper' and ent_dict['target_prepper'] == '':
        out_dict['messageText'] = []
        out_dict['messageText'].append(type_of_shooting_prepper)
        out_dict['messageText'].append(type_of_shooting_prepper_category)
    elif ent_dict['target_prepper'] != '':
        out_dict['messageText'] = []
        ent_dict['purpose'] = 'prepper'
        search_string = 'target_prepper'
        results = db_query(ent_dict, db, search_string)
        if len(results) != 0 :
            out_dict['messageText'].append(first_end_note +[ent_dict['purpose']])
            out_dict['messageText'].append(end_note)
            out_dict['ResultBuyer'] = results
        else:
            out_dict['messageText'].append(no_recommendation)
    return out_dict


def military_guns(ent_dict, dict_input, out_dict, db):
    if ent_dict['purpose'] == 'LEO/MILITARY/TACTICAL' and ent_dict['target_military'] == '':
        out_dict['messageText'] = []
        out_dict['messageText'].append(military)
    elif ent_dict['target_military'] != '':
        out_dict['messageText'] = []
        ent_dict['purpose'] = 'LEO/MILITARY/TACTICAL'
        out_dict['messageText'].append([ent_dict['target_military'] +' guns' +military_second[0]])
        search_string = 'target_military'
        results = db_query(ent_dict, db, search_string)
        if len(results) != 0 :
            out_dict['messageText'].append(first_end_note +[ent_dict['purpose']+' '+ent_dict['targets_shooter']])
            out_dict['messageText'].append(end_note)
            out_dict['ResultBuyer'] = results
        else:
            out_dict['messageText'].append(no_recommendation)
    return out_dict


def personal_protection(ent_dict, dict_input, out_dict, db):
    if ent_dict['purpose'] == 'Personal Protection' and ent_dict['perosnal_protection_sub'] == '':
        out_dict['messageText'] = []
        out_dict['messageText'].append(personal_protection_text)
        out_dict['messageText'].append(personal_protection_text2)
    elif ent_dict['perosnal_protection_sub'] != '':
        out_dict['messageText'] = []
        ent_dict['purpose'] = 'Personal Protection'
        #out_dict['messageText'].append(end_note)
        search_string = 'perosnal_protection_sub'
        results = db_query(ent_dict, db, search_string)
        if len(results) != 0 :
            out_dict['messageText'].append([first_end_note[0] +' '+ent_dict['purpose']])
            out_dict['messageText'].append(end_note)
            out_dict['ResultBuyer'] = results
        else:
            out_dict['messageText'].append(no_recommendation)
    return out_dict


def collector(ent_dict, dict_input, out_dict, db):
    if ent_dict['purpose'] == 'Collectors' and ent_dict['collector_sub'] == '':
        out_dict['messageText'] = []
        out_dict['messageText'].append(collector_text)
        out_dict['messageText'].append(collector_text2)
        out_dict['messageText'].append(collector_text3)
    elif ent_dict['collector_sub'] != '':
        out_dict['messageText'] = []
        ent_dict['purpose'] = 'Collectors'
        #out_dict['messageText'].append(end_note)
        search_string = 'collector_sub'
        results = db_query(ent_dict, db, search_string)
        if len(results) != 0 :
            out_dict['messageText'].append(end_note[0] + ' for '+ ent_dict['collector_sub'])
            out_dict['ResultBuyer'] = results
        else:
            out_dict['messageText'].append(no_recommendation)
    return out_dict


def sporting(ent_dict, dict_input, out_dict, db):
    if ent_dict['purpose'] == 'Modern sporting arms' and ent_dict['sporting_arms_sub'] == '':
        out_dict['messageText'] = []
        out_dict['messageText'].append(sporting_arms)
        out_dict['messageText'].append(sporting_arms2)
    elif ent_dict['sporting_arms_sub'] != '':
        out_dict['messageText'] = []
        ent_dict['purpose'] = 'Modern sporting arms'
        search_string = 'sporting_arms_sub'
        results = db_query(ent_dict, db, search_string)
        if len(results) != 0 :
            out_dict['messageText'].append(end_note[0] + ' for '+ ent_dict['sporting_arms_sub'])
            out_dict['ResultBuyer'] = results
        else:
            out_dict['messageText'].append(no_recommendation)
    return out_dict


def check_for_hunter(ent_dict, dict_input, out_dict, db):
    if ent_dict['purpose'] == 'hunter' and ent_dict['target_hunter'] == '':
        out_dict['messageText'] = []
        out_dict['messageText'].append(hunter_text)
        out_dict['messageText'].append(hunter_text2)
        out_dict['messageText'].append(hunter_text3)
    elif ent_dict['target_hunter'] != '':
        print 'passed'
        out_dict['messageText'] = []
        ent_dict['purpose'] = 'hunter'
        #out_dict['messageText'].append(end_note)
        search_string = 'target_hunter'
        results = db_query(ent_dict, db, search_string)
        if len(results) != 0 :
            out_dict['messageText'].append(end_note[0] + ' for '+ ent_dict['target_hunter'])
            out_dict['ResultBuyer'] = results
            out_dict['messageSource'] = 'secondLevel'
        else:
            out_dict['messageText'].append(no_recommendation)
    return out_dict

def call_api(dict_input):
    db = connect_to_db()
    out_dict = {}
    out_dict['entities'] = []
    out_dict['messageText'] = []
    out_dict['messageSource'] = dict_input['messageSource']
    ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)
    request = ai.text_request()
    request.lang = 'de'
    request.resetContexts = True
    request.session_id = dict_input['user_id']
    request.query = dict_input['messageText']
    response = yaml.load(request.getresponse())
    print 'response', response
    out_dict['messageText'].append(response['result']['fulfillment']['speech'])
    out_dict['entities'].append(response['result']['parameters'])
    ent_dict = out_dict['entities'][0]
    print ent_dict
    if ent_dict.has_key('purpose'):
        out_dict = check_for_shooter(ent_dict, dict_input, out_dict, db)
        out_dict = check_for_hunter(ent_dict, dict_input, out_dict, db)
        out_dict = check_for_prepper(ent_dict, dict_input, out_dict, db)
        out_dict = military_guns(ent_dict, dict_input, out_dict, db)
        out_dict = personal_protection(ent_dict, dict_input, out_dict, db)
        out_dict = collector(ent_dict, dict_input, out_dict, db)
        out_dict = sporting(ent_dict, dict_input, out_dict, db)
    return out_dict


