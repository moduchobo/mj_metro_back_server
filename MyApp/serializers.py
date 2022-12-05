from rest_framework import serializers
from .models import *


class UserSerializer(serializers.ModelSerializer):
    #  validation을 여기서 진행
    # usrid = User.objects.get()
    # schedules = Schedule.objects.pk(user=usrid)
    class Meta:
        model = User
        fields = '__all__'

class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = '__all__'

class FavStationSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavStation
        fields = '__all__'
 
class FavRouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavRoute
        fields = '__all__'
  

class StationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Station
        fields = '__all__'

class UserScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = '__all__'

class UserStationSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavStation
        fields = '__all__'

class UserRouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavRoute
        fields = '__all__'

class SingleStationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Station
        fields = '__all__'