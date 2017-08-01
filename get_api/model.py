'''
Created on Mar 31, 2017

@author: aneesh.c
'''
import aiml
import dill
from .models import RequestCache
from external_api import call_api
from get_api.models import UserCache
import string
import MySQLdb
from config import manufacturers
import re
manufacturers = [i.lower() for i in manufacturers]
from external_api import connect_to_db
import pandas as pd
from config import end_note
from config import no_recommendation
brain_file_medical = "C:\\Users\\aneesh.c\workspace\get_api\get_api\gunbroker_modified_v2.brn"



def write_to_db(user_input, reply, date_time, user_id):
    try:
        db = MySQLdb.connect("192.168.0.28", "user", "kreara@1", "ggc")
        cursor = db.cursor()
        user_input = user_input.encode('utf-8').translate(None, string.punctuation)
        try:
            reply = string.join(reply)
            reply = reply.encode('utf-8').translate(None, string.punctuation)
        except:
            reply = 'failed to decode'
        
        sql = """INSERT INTO ggc.chat_logs_gunbrocker(user_input,bot_response,date_time,\
user_id) VALUES ('%s','%s', '%s', '%s')""" % (
                                              user_input,
                                              reply,
                                              date_time,
                                              user_id
                                              )
        # print sql
        cursor.execute(sql)
        db.commit()
    except Exception as e:
        print (e)
        print ('Db is not getting connected')
        pass


def create_cache(CACHE_ID):
    import base64
    try:
        req_cache = RequestCache.objects.get(cache_id=CACHE_ID)
    except RequestCache.DoesNotExist:
        kern_medical = aiml.Kernel()
        kern_medical.bootstrap(brainFile=brain_file_medical)
        kernel_str = dill.dumps(kern_medical)
        kernel_str = base64.b64encode(kernel_str)
        req_cache = RequestCache.objects.create(cache_id=CACHE_ID, cache=[],
                                                user=UserCache.objects
                                                .create(aiml_kernel=kernel_str)
                                                )
    return req_cache


def generate_reply(question, kernel, cache_list):
    #question['messageSource'] = 'messageFromBot'
    response = question
    kernel_reply = kernel.respond(str(question['messageText']))
    print ('kernel ores', kernel_reply)
    if "Sorry, I didn't get you.." in kernel_reply or 'See you later' in kernel_reply:
        response = call_api(response)
        return response
    else:
        response['entities'] = []
        response['messageText'] = []
        response['messageText'].append(kernel_reply)
        return response


# def extract_manufacturer(response):
#     #print response['messageText']
#     string_input = "".join(response['messageText']).lower()
#     #print 'st', string_input
#     manufactr = ''
#     manufactr = re.findall(r"(?=("+'|'.join(manufacturers)+r"))", str(string_input))
#     manufactr = ''.join(manufactr)
#     return manufactr

# def create_response(question, kernel, cache_list):
#     response = question
#    
#     response['entities'] = cache_list
#     #print 'final', cache_list
#     label = text_classify(response)
#     if label == 0 and response["messageSource"] != "classified":
#         response['messageText'] = []
#         response['messageText'].append(['OK, See you again'])
#         response["messageSource"] = "messengerUser"
#         return response
#     elif label == 1 and response["messageSource"] != "classified":
#         response['messageText'] = []
#         response['messageText'] = ['Which manufacturer you would prefer?']
#         response["messageSource"] = "classified"
#         return response
#     if response["messageSource"] == "classified":
#         Manufacturer = extract_manufacturer(response)
#         print (Manufacturer)
#         ent_dict = response['entities'][0]
#         if Manufacturer !='':
#             results = []
#             query = ent_dict['query']
#             query = query.split('where', 1)[0] + "where Manufacturer='%s' and "%(Manufacturer)+ query.split('where', 1)[1]
#             print ('end', query)
#             db = connect_to_db()
#             try:
#                 table = pd.read_sql("%s"%query,db)
#                 results = table.to_dict(orient='records')
#             except Exception as e:
#                 print (e)
#             if len(results) !=0:
#                 response['messageText'] = []
#                 response['ResultBuyer'] = results
#                 response["messageSource"] = "messengerUser"
#                 response['messageText'].append(end_note[0])
#             else:
#                 response['messageText'] = []
#                 response["messageSource"] = "messengerUser"
#                 response['messageText'].append(no_recommendation)
#         else:
#             response['messageText'] = []
#             response["messageSource"] = "messengerUser"
#             response['messageText'].append(no_recommendation)
#     return response
