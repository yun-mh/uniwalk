from pusher import pusher
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

# configure pusher object
pusher = pusher.Pusher(
    app_id="947136",
    key="768af5bb1417be83adc3",
    secret="3463dc60f6fe87264630",
    cluster="ap3",
    ssl=True,
)


@csrf_exempt
def guestUser(request):
    data = json.loads(request.body)
    pusher.trigger(
        u"general-channel", u"new-guest-details", {"email": data["email"]},
    )
    return JsonResponse(data)


@csrf_exempt
def pusher_authentication(request):
    auth = pusher.authenticate(
        channel=request.POST["channel_name"], socket_id=request.POST["socket_id"]
    )
    return JsonResponse(auth)
