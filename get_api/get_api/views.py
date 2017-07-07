'''
Created on Mar 31, 2017

@author: aneesh.c
'''
from rest_framework import viewsets
from config import *
from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from datetime import datetime
from rest_framework import permissions
from model import *
import random
import dill
import base64

@permission_classes((permissions.AllowAny,))
class TestAPI(viewsets.ViewSet):
    def create(self, request):
        question = request.data
        #output_text = {'status': 'Hellow'}
        CACHE_ID = 'Constant45l54'
        if 'user_id' in question:
            CACHE_ID = question['user_id']
        print 'question', question
        req_cache = create_cache(CACHE_ID)
        user_input = question['messageText']
        if question['messageSource'] == 'userInitiatedReset':
            req_cache.delete()
            question['messageSource'] = 'messageFromBot'
            question['messageText'] = welcome_note
            question["plugin"] = {'name': 'autofill', 'type': 'items', 'data': top_level_persona}
            return Response(question)
        if 'Something else' in question['messageText']:
            question['messageSource'] = 'messageFromBot'
            question['messageText'] = reply_something_else
            return Response(question)
            
        kernel = dill.loads(base64.b64decode(req_cache.user.aiml_kernel))
        question = generate_reply(question, kernel, req_cache.cache)
        print question
        if 'entities' in question:
            req_cache.cache = question['entities']
            req_cache.user.aiml_kernel = \
                base64.b64encode(dill.dumps(kernel))
            req_cache.user.save()
            req_cache.save()

        date_time = str(datetime.now())
        write_to_db(user_input, question['messageText'], date_time, CACHE_ID)
        #question.pop("entities", None)
        return Response(question)
        