from django.shortcuts import render
from django.views.generic.base import TemplateView
from agora_token_builder import RtcTokenBuilder
from django.http import JsonResponse
import random
import time
import json


from .models import RoomMember

from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def get_token(request):
    appId = '794e613ca09a48b98db0a33d64fda1c3'
    appCertificate = '3aaf2b66eba04405b03d7c1db7ce464b'
    channelName = request.GET.get('channel')
    uid = random.randint(1, 230)
    expirationTimeInSeconds = 3600 * 24
    currentTimeStamp = time.time()
    privilegeExpiredTs = currentTimeStamp + expirationTimeInSeconds
    role = 1

    token = RtcTokenBuilder.buildTokenWithUid(appId, appCertificate, channelName, uid, role, privilegeExpiredTs)
    
    return JsonResponse({'token': token, 'uid':uid}, safe=False)


def lobby(request):
    return render(request, 'lobby.html')

def room(request):
    return render(request, 'room.html')

@csrf_exempt
def create_member(request):
    data = json.loads(request.body)

    member, created = RoomMember.objects.get_or_create(
        name=data['name'],
        uid=data['UID'],
        room_name=data['room_name'],
    )

    return JsonResponse({'name':data['name']}, safe=False)

def get_member(request):
    uid = request.GET.get('uid')
    room_name = request.GET.get('room')

    member = RoomMember.objects.get(
        uid=uid,
        room_name=room_name,
    )

    name = member.name
    return JsonResponse({'name':member.name}, safe=False)

@csrf_exempt
def delete_member(request):
    data = json.loads(request.body)
    member = RoomMember.objects.get(
        name=data['name'],
        uid=data['UID'],
        room_name=data['room_name']
    )
    member.delete()
    return JsonResponse('Member deleted', safe=False)