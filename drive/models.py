from datetime import date

from django.db import models

from django.contrib.auth.models import User

서울 = '서울'
경기 = '경기'
인천 = '인천'
강원 = '강원'
대전 = '대전'
충남 = '충남'
충북 = '충북'
광주 = '광주'
전남 = '전남'
전북 = '전북'
부산 = '부산'
경남 = '경남'
대구 = '대구'
경북 = '경북'
AREA = (
    (서울, '서울'),
    (경기, '경기'),
    (인천, '인천'),
    (강원, '강원'),
    (대전, '대전'),
    (충남, '충남'),
    (충북, '충북'),
    (광주, '광주'),
    (전남, '전남'),
    (전북, '전북'),
    (부산, '부산'),
    (경남, '경남'),
    (대구, '대구'),
    (경북, '경북'),
)

class Drive(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    departure_area = models.CharField(max_length=10, choices=AREA)
    arrive_area = models.CharField(max_length=10, choices=AREA)
    departure_date = models.DateField(default=date.today)
    departure_time = models.CharField(max_length=20)
    detail_plan = models.CharField(max_length=100)
    fee = models.CharField(max_length=30)
    connect = models.CharField(max_length=50)
    memo = models.CharField(max_length=300)
    #
    # def save(self, force_insert=False, force_update=False, using=None,
    #          update_fields=None):
    #     self.connect = self.user.phone
    #     return super(Drive,self).save(force_insert,force_update,using,update_fields)
    #
