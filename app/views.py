from django.shortcuts import render
# import jwt
import random
from rest_framework.decorators import api_view
from rest_framework.decorators import parser_classes
from rest_framework.parsers import MultiPartParser
from django.http import JsonResponse
import datetime
from .models import Token
from django.db.models import Count
import pytz
from django.utils import timezone

# this is for token generation 

@api_view(['GET'])
def gen(request):
    date = datetime.datetime.now()
    print(date)
    
    token = random.random()
    print("dateTime.now" , datetime.datetime.now())
    TokenObj = Token(Token = token,creationTime = datetime.datetime.now() ,Status = 'unassigned')
    TokenObj.save()

    
    context = {'token':token}

    return JsonResponse(context ,safe=False)


@api_view(['GET'])
def assign(request):
    try:
        value = Token.objects.order_by('id').filter(Status='unassigned')[0:1].get()
        token = value.Token
        print(value.id)
        value.Status = "assigned"
        value.creationTime == datetime.datetime.now()
        value.save()
        # MyModel.objects.filter(pk=some_value).update(field1='some value')
        context = {"token":token , "timeout_Duration":"5 Minutes"}
        return JsonResponse(context ,safe=False)
    except:
        context = {'msg':"No Un-assigned token is available Please release or generate more"}
        return JsonResponse(context ,safe=False)

# this is for checking if its available in db or not 
@api_view(['POST'])
def check(request):
    requestToken = request.data['token']
    print(requestToken)
    try:
        TokenObj = Token.objects.filter(Token = requestToken).get()
        if TokenObj.Status == 'unassigned':
            context = {"msg":"Requested token is Unassingned. Please!! assign it first"}
            return JsonResponse(context ,safe=False)

        status = tokenCheck(TokenObj)
        if status == True and TokenObj.Status == 'assigned':
            msg = "Token is still active"
        else:
            msg = "Sorry!!! Token has Expired and Deleted"
    except:
        msg = "Requested Token is not available"
    context = {"msg":msg}
    return JsonResponse(context ,safe=False)


# this api is for refreshing the token
@api_view(['POST'])
def tokenRefresh(request):
    try:
        requestToken = request.data['token']
        TokenObj = Token.objects.filter(Token = requestToken).get()
        if TokenObj.Status == 'unassigned':
            context = {"msg":"Requested token is Unassingned. Please!! assign it first"}
            return JsonResponse(context ,safe=False)
        status = tokenCheck(TokenObj)
        print(status)
        if status == False:
            context = {"msg":"Requested Token has Expired" }
            return JsonResponse(context ,safe=False)

        
            TokenObj = Token.objects.filter(Token = requestToken).get()
            TokenObj.creationTime = datetime.datetime.now()
            TokenObj.save()
            msg = "Token Has been refreshed"
            duration = "5 Minutes"
    except:
        msg = "Requested Token is not available"
        duration = 0
    

    context = {"msg":msg,"timeout_Duration":duration }
    return JsonResponse(context ,safe=False)



@api_view(['POST'])
def unassign(request):
    
    requestToken = request.data['token']
    try:
        TokenObj = Token.objects.filter(Token = requestToken).get()
        TokenObj.Status = "unassigned"
        TokenObj.save()
        msg = "token is been un-assingned"
        
    except:
        msg = "Requested Token is not available"    
    context = {"msg":msg,"token":requestToken}
    return JsonResponse(context ,safe=False) 


@api_view(['POST'])
def deleteToken(request):
    try:
        requestToken = request.data['token']
        TokenObj = Token.objects.filter(Token = requestToken).get()
        TokenObj.delete()
        msg="Requested Token has been deleted"
    except:
        msg = "Requested is not available"

    context = {"msg":msg}
    return JsonResponse(context ,safe=False)  



def tokenCheck(TokenObj):
    date_string = TokenObj.creationTime.strftime("%m/%d/%Y, %H:%M:%S")
    tt = datetime.datetime.strptime(date_string,"%m/%d/%Y, %H:%M:%S")
    
    mins = 5
    if datetime.datetime.now() > tt + datetime.timedelta(minutes= mins):
        print("True")
        status = True
    else:
        TokenObj.delete()
        status = False
    return status