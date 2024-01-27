from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from twilio.twiml.messaging_response import MessagingResponse

@csrf_exempt
def sms_response(request):
    resp = MessagingResponse()
    msg = resp.message("Check out this sweet out!")
    return HttpResponse(str(resp))
