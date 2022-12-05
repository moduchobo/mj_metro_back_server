from django.db import models 
import random
# Create your models here.

class Schedule(models.Model):
    user = models.ForeignKey(
        "User",   
        on_delete=models.CASCADE
    )
    scheduleName = models.CharField(help_text = "Name of the Schedule", max_length=30, default="My Schedule")
    routeContent = models.JSONField(default={
        "start": "",
        "end": "",
        "waypoint": []
    })
    week = models.CharField(choices=(
        ("mon", "월요일"),
        ("tue", "화요일"),
        ("wed", "수요일"),
        ("thu", "목요일"),
        ("fri", "금요일"),
        ("sat", "토요일"),
        ("son", "일요일"),
    ), max_length=3, default="") # 몇요일에 있는 일정인지
    # time은 파이썬의 time객체를 전달한다. 그러나 편의를 위해 text로 변환해서 모델에 저장..
    time = models.CharField(default="00:00:00", max_length=10) # 몇시에 있는 일정인지.
    count = models.SmallIntegerField(default=30) # 기본값으로 열차 출발 30분 전에 알림을 줌


    def __str__(self):
        return str(self.user)

 
class FavStation(models.Model):
    favstationId = models.ForeignKey(
        "User",
        on_delete=models.CASCADE
    )
    favStationName = models.CharField(max_length=10, default="")
    
    def __str__(self):
        return self.favStationName


class FavRoute(models.Model):

    favRouteId = models.ForeignKey(
        "User",
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=30, default="My Favorite Route")
    content = models.JSONField(default={
        "start": "",
        "end": "",
        "waypoint": []
    })
    def __str__(self):
        return str(self.favRouteId)
 

# 역 정보들만 나오면 됨.
class Station(models.Model):
    lineNumber = models.CharField(max_length=1, default="1")
    stationName = models.CharField(max_length=10, default="")
    stationNum = models.CharField(max_length=3, default="000")
    latitude = models.FloatField()
    longitude = models.FloatField()
    transfer = models.CharField(max_length=1, default="0")
    address = models.CharField(max_length=100, default="")

    timeTable = models.JSONField(default={
        "departureTime": [],
        "arrivalTime": []
    }) 

    def getWeather():
        pass
    def getPopulation():
        pass

    def __str__(self):
        return self.stationName


class User(models.Model):

    # user 식별자를 랜덤으로 하되.. 겹치지 않는 것으로 하는 것이니..
     

    # userKey = models.AutoField(primary_key=True, unique=True)
    Username = models.CharField(max_length=20, default="홍길동")
    Password = models.CharField(max_length=20, default="password")
 
    # 나머지는 유저, 리스트, 항목의 계층구조 
    # 왜 부분 주석 해제하면 에러가 나올까...?
    # 리스트처럼 오는 것들을 모두 그냥 포진키로 ..!!

    Reported = models.IntegerField(default=0) # 개인이 몇번이나 신고했는지.
     
     # 이 메소드들을 View에서 처리해줘??

    def addScheduleList(self, Schedule):
        pass

    def addFavRouteList(self, FavRoute):
        pass

    def addFavStation(self, FavStation):
        pass

    def getScheduleList(self):
        pass 

    def getFavRouteList(self):
        pass

    def getFavStationList(self):
        pass

    def __str__(self):
        return str(self.id)
