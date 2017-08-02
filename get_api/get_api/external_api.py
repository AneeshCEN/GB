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
from fetch_msrp import get_msrp

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
    print 'search', search_string
    general_use = out_dict['purpose']
    best_use = out_dict[search_string]
    specific_use = out_dict['third_level_persona_hunter']
    parent_category = out_dict['guns_category']
    query_first_part = 'select Model, MfgPartNumber, Caliber, BarrelLength, \
Manufacturer, MSRP, Category, Series, BestUse, ParentCategory, \
Image1 from gun_bro.MDL_API_DATA_SUBSET_NEW where '
    if parent_category != '':
        query_first_part = query_first_part + "ParentCategory = '%s' and" % (parent_category)
    if general_use != '':
        query_first_part = query_first_part + " GeneralUse = '%s' and" % (general_use)
    if best_use != '':
        query_first_part = query_first_part + " BestUse = '%s' and" % (best_use)
    if specific_use != '':
        query_first_part = query_first_part + " SpecificUse = '%s'" % (specific_use)
    if query_first_part.endswith('and'):
        query_first_part = query_first_part.rsplit(' ',1)[0]
    #query_first_part = query_first_part +' group by MfgPartNumber order by LifeTimeNumberSold desc'
    #print query_first_part
    try:
        df_type = pd.read_sql(query_first_part, db)
        #results = get_msrp(df_type)
        results = df_type.to_dict(orient='records')
        #print results
    except Exception as e:
        print e
    return results, query_first_part


def db_query_shooter(ent_dict, db):
    results = []
    user_sub_types_list = []
    general_use = 'Shooter'
    best_use = ent_dict['targets_shooter']
    specific_use = ent_dict['third_level_persona_shooter']
    parent_category = ent_dict['guns_category']
    if ent_dict['targets_shooter'] != '':
        try:
            user_sub_types = targets_guns[ent_dict['targets_shooter']]
        except:
            return [], 'invalid'
        user_sub_types_list = user_sub_types.split(', ')
    string_query = ''
    query_first_part = 'select Model, MfgPartNumber, Caliber, BarrelLength, \
Manufacturer, MSRP, Series, Category, BestUse, ParentCategory, \
Image1 from gun_bro.MDL_API_DATA_SUBSET_NEW where '
    if parent_category != '':
        query_first_part = query_first_part + "ParentCategory = '%s' and" % (parent_category)
    if general_use != '':
        query_first_part = query_first_part + " GeneralUse = '%s' and" % (general_use)
    if specific_use != '':
        query_first_part = query_first_part + " SpecificUse = '%s' and" % (specific_use)
    if len(user_sub_types_list) == 0:
        query_first_part = query_first_part.rsplit(' ',1)[0]
        print 'first part', query_first_part
        try:
            #query_first_part = query_first_part +' group by MfgPartNumber order by LifeTimeNumberSold desc'
            df_type = pd.read_sql(query_first_part, db)
            #results = get_msrp(df_type)
            results = df_type.to_dict(orient='records')
            return results, query_first_part
        except Exception as e:
            print e
    elif len(user_sub_types_list) >= 2:
        query = query_first_part + " BestUSe = '%s'"%(user_sub_types_list[0])
        user_sub_types_list = user_sub_types_list[1::]
        string_query = ''.join([string_query+" or BestUse='%s' "%(i) for i in user_sub_types_list])
        print 'query is ', query
        query = query + string_query
        #query = query +' group by MfgPartNumber order by LifeTimeNumberSold desc'
    else:
        string_query = user_sub_types_list[0]
        query = query_first_part + " BestUse = '%s'"%(string_query)
        #query = query +' group by MfgPartNumber order by LifeTimeNumberSold desc'
        #print 'final', query
    try:
        df_type = pd.read_sql(query, db)
        #results = get_msrp(df_type)
        results = df_type.to_dict(orient='records')
        return results, query
    except Exception as e:
        print e


def check_for_shooter(ent_dict, dict_input, out_dict, db):
    if ent_dict['purpose'] == 'shooter' and ent_dict['targets_shooter'] == '' and ent_dict['third_level_persona_shooter'] == '':
        out_dict['messageText'] = []
        out_dict['messageText'].append(type_of_shooting)
        out_dict['messageText'].append(objects)
        out_dict["plugin"] = {'name': 'autofill', 'type': 'Targets', 'data': target_lists}
    elif ent_dict['targets_shooter'] != '' or ent_dict['third_level_persona_shooter'] !='':
        out_dict['messageText'] = []
        ent_dict['purpose'] = 'Shooter'
        results, query = db_query_shooter(ent_dict, db)
        if len(results) != 0:
            if ent_dict['targets_shooter'].endswith('Shooting'):
                out_dict['messageText'].append(first_end_note +[ent_dict['targets_shooter']])
            else:
                out_dict['messageText'].append(first_end_note +[' '+ent_dict['targets_shooter']+ent_dict['third_level_persona_shooter']+' shooting'])
            out_dict['messageText'].append(end_note)
#             out_dict['messageText'].append(second_level_text)
            out_dict['ResultBuyer'] = results
#             out_dict['messageSource'] = 'secondLevel'
            out_dict['entities'][0].update({'query':query})
        else:
            out_dict['messageText'].append(no_recommendation)
    return out_dict


def check_for_prepper(ent_dict, dict_input, out_dict, db):
    if ent_dict['purpose'] == 'prepper' and ent_dict['target_prepper'] == '':
        out_dict['messageText'] = []
        out_dict['messageText'].append(type_of_shooting_prepper)
        out_dict['messageText'].append(type_of_shooting_prepper_category)
        out_dict["plugin"] = {'name': 'autofill', 'type': 'collections', 'data': prepper_objects}
    elif ent_dict['target_prepper'] != '':
        out_dict['messageText'] = []
        ent_dict['purpose'] = 'prepper'
        search_string = 'target_prepper'
        results, query = db_query(ent_dict, db, search_string)
        if len(results) != 0 :
            out_dict['messageText'].append(first_end_note +[ent_dict['purpose']])
            out_dict['messageText'].append(end_note)
            out_dict['messageText'].append(second_level_text)
            out_dict['ResultBuyer'] = results
            out_dict['messageSource'] = 'secondLevel'
            out_dict['entities'][0].update({'query':query})
        else:
            out_dict['messageText'].append(no_recommendation)
    return out_dict


def military_guns(ent_dict, dict_input, out_dict, db):
    if ent_dict['purpose'] == 'LEO/MILITARY/TACTICAL' and ent_dict['target_military'] == '':
        out_dict['messageText'] = []
        out_dict['messageText'].append(military)
        out_dict["plugin"] = {'name': 'autofill', 'type': 'items', 'data': military_objects}
    elif ent_dict['target_military'] != '':
        out_dict['messageText'] = []
        ent_dict['purpose'] = 'LEO/MILITARY/TACTICAL'
        out_dict['messageText'].append([ent_dict['target_military'] +' guns' +military_second[0]])
        search_string = 'target_military'
        results, query = db_query(ent_dict, db, search_string)
        if len(results) != 0 :
            out_dict['messageText'].append(first_end_note +[ent_dict['purpose']+' '+ent_dict['targets_shooter']])
            out_dict['messageText'].append(end_note)
            out_dict['messageText'].append(second_level_text)
            out_dict['ResultBuyer'] = results
            out_dict['messageSource'] = 'secondLevel'
            out_dict['entities'][0].update({'query':query})
        else:
            out_dict['messageText'].append(no_recommendation)
    return out_dict


def personal_protection(ent_dict, dict_input, out_dict, db):
    if ent_dict['purpose'] == 'Personal Protection' and ent_dict['perosnal_protection_sub'] == '':
        out_dict['messageText'] = []
        out_dict['messageText'].append(personal_protection_text)
        out_dict["plugin"] = {'name': 'autofill', 'type': 'items', 'data': personal_protection_objects}
    elif ent_dict['perosnal_protection_sub'] != '':
        out_dict['messageText'] = []
        ent_dict['purpose'] = 'Personal Protection'
        #out_dict['messageText'].append(end_note)
        search_string = 'perosnal_protection_sub'
        results, query = db_query(ent_dict, db, search_string)
        if len(results) != 0 :
            out_dict['messageText'].append([first_end_note[0] +' '+ent_dict['perosnal_protection_sub'] + ' category'])
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
        out_dict["plugin"] = {'name': 'autofill', 'type': 'items', 'data': collector_objects}
    elif ent_dict['collector_sub'] != '':
        out_dict['messageText'] = []
        ent_dict['purpose'] = 'Collectors'
        #out_dict['messageText'].append(end_note)
        search_string = 'collector_sub'
        results, query = db_query(ent_dict, db, search_string)
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
        out_dict["plugin"] = {'name': 'autofill', 'type': 'Sporting guns', 'data': sporting_objects}
    elif ent_dict['sporting_arms_sub'] != '':
        out_dict['messageText'] = []
        ent_dict['purpose'] = 'Modern sporting arms'
        search_string = 'sporting_arms_sub'
        results, query = db_query(ent_dict, db, search_string)
        if len(results) != 0 :
            out_dict['messageText'].append(end_note[0] + ' for '+ ent_dict['sporting_arms_sub'])
            out_dict['ResultBuyer'] = results
        else:
            out_dict['messageText'].append(no_recommendation)
    return out_dict


def check_for_hunter(ent_dict, dict_input, out_dict, db):
    if ent_dict['purpose'] == 'hunter' and ent_dict['target_hunter'] == '' and ent_dict['third_level_persona_hunter'] =='':
        out_dict['messageText'] = []
        out_dict['messageText'].append(hunter_text)
        out_dict['messageText'].append(hunter_text2)
        out_dict['messageText'].append(hunter_text3)
    elif ent_dict['target_hunter'] != '' or ent_dict['third_level_persona_hunter'] !='':
        out_dict['messageText'] = []
        ent_dict['purpose'] = 'hunter'
        #out_dict['messageText'].append(end_note)
        search_string = 'target_hunter'
        results, query = db_query(ent_dict, db, search_string)
        if len(results) != 0 :
            out_dict['messageText'].append(end_note[0] + ' for '+ ent_dict['purpose'] +' category')
            #out_dict['messageText'].append(second_level_text)
            out_dict['ResultBuyer'] = results
            #out_dict['entities'][0].update({'query':query})
            #out_dict['messageSource'] = 'secondLevel'
        else:
            out_dict['messageText'].append(no_recommendation)
    return out_dict


def identify_entities(out_dict, db):
    ent_dict = out_dict['entities'][0]
    if 'Manufacturer' in ent_dict:
        #print 'Manufacture is there'
        Manufacturer = ent_dict['Manufacturer']
        out_dict.pop('Manufacturer', None)
    else:
        Manufacturer = ''
        return out_dict
    if 'series' in ent_dict:
        #print 'series is there'
        Series = ent_dict['series']
        out_dict.pop('series', None)
    else:
        Series = ''
        return out_dict
    if 'purpose'in ent_dict:
        #print 'series is there'
        GeneralUse = ent_dict['purpose']
        out_dict.pop('purpose', None)
    else:
        GeneralUse =''
    for element in second_category:
        if element in ent_dict:
            BestUse = ent_dict[element]
        else:
            BestUse =''
    query_first_part = 'select Model, Image1 from gun_bro.MDL_API_DATA where '
    #print query_first_part
    if Manufacturer != '':
        query_first_part = query_first_part + "Manufacturer = '%s' and" % (Manufacturer)
    if Series != '':
        query_first_part = query_first_part + " Series = '%s' and" % (Series)
    if BestUse != '':
        query_first_part = query_first_part + " BestUse = '%s' and" % (BestUse)
    if query_first_part.endswith('and'):
        query_first_part = query_first_part.rsplit(' ',1)[0]
    print query_first_part
    try:
        df_type = pd.read_sql(query_first_part, db)
        results = df_type.to_dict(orient='records')
        if len(results) != 0:
            out_dict['messageText'] = ['yes you can, Its a nice choice']
            return out_dict
        else:
            out_dict['messageText'] = ["No, you can't, not"]
            return out_dict
    except Exception as e:
        print e

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
    #print 'response', response
    out_dict['messageText'].append(response['result']['fulfillment']['speech'])
    out_dict['entities'].append(response['result']['parameters'])
    ent_dict = out_dict['entities'][0]
    #print ent_dict
    if response['result']['action'] == 'yes/no':
        #print 'returned', response['result']['parameters']
        out_dict = identify_entities(out_dict, db)
    if ent_dict.has_key('purpose') and response['result']['action'] !='negative' and response['result']['action'] !='yes/no':
        out_dict = check_for_shooter(ent_dict, dict_input, out_dict, db)
        out_dict = check_for_hunter(ent_dict, dict_input, out_dict, db)
        out_dict = check_for_prepper(ent_dict, dict_input, out_dict, db)
        out_dict = military_guns(ent_dict, dict_input, out_dict, db)
        out_dict = personal_protection(ent_dict, dict_input, out_dict, db)
        out_dict = collector(ent_dict, dict_input, out_dict, db)
        out_dict = sporting(ent_dict, dict_input, out_dict, db)
    return out_dict


