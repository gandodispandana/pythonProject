from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from django.contrib.auth.decorators import login_required
from rest_framework.authtoken.models import Token
from .serializers import *
from django.contrib.auth import login as django_login
from .utils import QuiteTime
from twilio.rest import Client
from django.conf import settings
from django.views.decorators.csrf import csrf_protect


class NotificationAPIView(APIView):
    # permission_classes = (IsAuthenticated,)
    # authentication_classes = (TokenAuthentication,)

    def get(self, request):
        data = {"summaryContent": [
            {"BC's Opt In": {
                "optInCount": 20,
                "totalCount": 100
            }},
            {"Members Opt In": {
                "optInCount": 50,
                "totalCount": 200
            }}
        ],
            "templates": [
                {
                    "type": "approvalStatus",
                    "approvedCount": "approvedCount"
                }
            ]}
        return Response(data, status=200)

    def post(self, request):
        try:
            import pdb
            pdb.set_trace()
            data = request.data
            serializer = NotificationSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=201)
            return Response(serializer.errors, status=400)
        except data.DoesNotExist:
            return Response({
                "message": "Data doesnt exist"
            }, status=400)


class NotificationTemplateAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    authentication_classes = (TokenAuthentication,)

    def get(self, request):
        try:
            notifications = NotificationTemplate.objects.all()
            serailizer = NotificationTemplateSerializer(notifications, many=True)
            return Response(serailizer.data, status=200)
        except notifications.DoesNotExist:
            return Response({
                "message": "Deal doesnt exist"
            }, status=400)

    def post(self, request):
        try:
            import pdb
            pdb.set_trace()
            data = request.data
            serializer = NotificationTemplateSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=201)
            return Response(serializer.erros, status=400)
        except data.DoesNotExist:
            return Response({
                "message": "Data doesnt exist"
            }, status=400)

    def patch(self, request, pk):
        try:
            data = request.data
            serializer = NotificationTemplateSerializer(data=data, partial=True)
            # set partial=True to update a data partially
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(code=201, data=serializer.data)
            return JsonResponse(code=400, data="wrong parameters")
        except data.DoesNotExist:
            return Response({
                "message": "Data doesnt exist"
            }, status=400)


class LoginView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        django_login(request, user)
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key}, status=200)


class ReRoute(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def post(self, request):
        try:
            if request.role != "Admin":
                return Response({"role is not admin"}, status=400)
            data = request.data
            print(data)
            phonetype_obj = PhoneType.objects.get_or_create(number=data["phone"], phone_type="mobile")

            member_obj = Member.objects.get_or_create(first_name=data["first_name"], last_name=data["last_name"],
                                                      phone=phonetype_obj[0])

            member_source_obj = MemberSourceIdentifier.objects.get_or_create(member=member_obj[0])

            obj = NotificationTemplate.objects.get(template_type=self.__class__.__name__)
            message = obj.notification_body.format(person_first_name=data["first_name"], trip_date=data["trip_date"],
                                                   member_name=data["first_name"], pu_address=data["pu_address"],
                                                   do_address=data["do_address"],
                                                   tp_name=data["tp_name"])
            print(message)

            broker_obj = BrokerClient.objects.get_or_create(code=data["broker_client_id"],
                                                            name=data["broker_client_name"])

            temp = {
                "id": data["id"],
                "sid": data["sid"],
                "source_app": data["source_app"],
                "status": "active",
                "notification_type": "sms",
                "phone_number": phonetype_obj[0].id,
                "trip_date": data["trip_date"],
                "trip_id": data["trip_id"],
                "tp_type": data["trip_type"],
                "trip_pu_time": data["trip_pu_time"],
                "pu_address": data["pu_address"],
                "do_address": data["do_address"],
                "tp_name": data["tp_name"],
                "tp_phone_number": data["tp_phone_number"],
                "tzone": data["timezone"],
                "member_source_identifier": member_source_obj[0].id,
                "broker_client": broker_obj[0].id,
                "account_id": data["account_id"],
                "payload_body": data,
                "message_body": message,
                "force_communication": data["force_communication"]
            }
            import pdb
            pdb.set_trace()
            serializer = NotificationSerializer(data=temp)

            if serializer.is_valid():
                serializer.save()
                print(serializer.data)
                quitetime = QuiteTime()
                if quitetime[1] is False:
                    account_sid = settings.ACCOUNT_ID
                    auth_token = settings.AUTH_TOKEN
                    client = Client(account_sid, auth_token)
                    message = client.messages.create(
                        from_='+13346059091',
                        to='+917019132253',
                        body=temp["message_body"]
                    )
                    print(message.sid)
                else:
                    import pdb
                    pdb.set_trace()

                    temp1 = {
                        "notification": serializer.data["id"],
                        "scheduled_time": quitetime[0],
                        "status": "scheduled"
                    }
                    scheduleserializer = ScheduledNotificationSerializer(data=temp1)

                    import pdb
                    pdb.set_trace()
                    if scheduleserializer.is_valid():
                        scheduleserializer.save()
                        print(scheduleserializer.data)

                return Response(serializer.data, status=201)
            return Response(serializer.errors, status=400)
        except Exception:
            return Response({
                "message": "Data doesnt exist"
            }, status=400)
