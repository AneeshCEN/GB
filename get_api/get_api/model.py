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
brain_file_medical = "C:\Users\\aneesh.c\workspace\get_api\get_api\gunbroker_modified.brn"



def write_to_db(user_input, reply, date_time, user_id):
    try:
        db = MySQLdb.connect("192.168.0.28", "user", "kreara@1", "ggc")
        cursor = db.cursor()
        user_input = user_input.encode('utf-8').translate(None, string.punctuation)
        reply = string.join(reply)
        reply = reply.encode('utf-8').translate(None, string.punctuation)
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
        print e
        print 'Db is not getting connected'
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
    print 'kernel ores',kernel_reply
    if "Sorry, I didn't get you.." in kernel_reply or 'See you later' in kernel_reply:
        response = call_api(response)
        return response
    else:
        response['entities'] = []
        response['messageText'] = []
        response['messageText'].append(kernel_reply)
        print 'response', response
        return response
    