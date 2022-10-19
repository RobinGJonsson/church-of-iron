from django.http import HttpResponse


class StripeWH_Handler:

    def __init__(self, request):
        self.request = request

    def handle_webhook(self, event):
        return HttpResponse(
            content=f'Webhook recived: {event["type"]}',
            status=200
        )

    def handle_payment_intent_succeeded(self, event):
        return HttpResponse(
            content=f'Webhook recived: {event["type"]}',
            status=200
        )

    def handle_payment_intent_failed(self, event):
        return HttpResponse(
            content=f'Webhook recived: {event["type"]}',
            status=200
        )
