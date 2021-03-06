from django.db import models

from datetime import timedelta
from django.utils import timezone
from django.core.validators import RegexValidator
from django.contrib.auth.models import User

import ast
class ListField(models.TextField):
	description = "Stores a python list"

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

	def from_db_value(self, value, expression, connection):
		if value is None:
			return value
		if isinstance(value, str):
			return value.split(',')

	def to_python(self, value):
		if not value:
			value = []
		if isinstance(value, list):
			return value
		if isinstance(value, str):
			return ast.literal_eval(value)

	def get_prep_value(self, value):
		if value is None:
			return value
		if value is not None and isinstance(value, str):
			return value
		if isinstance(value, list):
			return ','.join(value)

	def value_to_string(self, obj):
		value = self.value_from_object(obj)
		return self.get_prep_value(value)


class Target(models.Model):
    """クエストターゲットになるモンスター"""
    monstername = models.CharField('Monster Name', max_length=255)
    imagepath = models.CharField('Image Path', max_length=511)

    def __str__(self):
        return self.monstername


class Weapon(models.Model):
    name = models.CharField('Weapon Name', max_length=255)
    imagepath = models.CharField('Image Path', max_length=511)

    def  __str__(self):
        return self.name



class Quest(models.Model):
    """クエスト"""
    questname = models.CharField('Quest Name', max_length=255)
    questname_j = models.CharField('Quest Name japanese', max_length=255)
    #target = models.CharField('Quest Rank', max_length=255)
    rank = models.CharField('Quest Rank', max_length=255)
    priority = models.PositiveIntegerField('Priority in quest page', default=0)
    target = models.ForeignKey(Target, verbose_name='Target', related_name='quests', on_delete=models.SET_NULL, null=True)
    recordnum = models.IntegerField('Number of record of this quest', default=0)

    def __str__(self):
        return self.questname


class Record(models.Model):
    """記録"""
    quest = models.ForeignKey(Quest, verbose_name='Quest', related_name='records', on_delete=models.CASCADE)
    runner = models.CharField('Player Name', max_length=255)
    party = models.CharField('Party', max_length=255, choices=[('S','1'), ('P','2'), ('M', '3or4'),])
    # cleartime = models.DurationField(default=timedelta(minutes=12, seconds=7, milliseconds=780))
    cleartime = models.DurationField()
    link_regex = RegexValidator(regex=r'^https://www.youtube.com/watch|https://www.nicovideo.jp/watch/|https://www.bilibili.com/video/', 
                                message='aaaaaaaaaaaa!!!')
    link = models.URLField(validators=[link_regex], max_length=2047, unique=True, help_text="A Video from Youtube, niconico, bilibili is available.", error_messages={'required': 'aa', 'invalid': 'invalid'})
    weapon = models.ForeignKey(Weapon, verbose_name='Weapon', on_delete=models.SET_NULL, null=True)
    """
    weapon = models.CharField('Weapon', max_length=255,
                               choices=[('GS', 'great-sword'), ('LS', 'long-sword'), ('SNS', 'sword-and-shield'), ('DB', 'dual-blades'),
                                        ('HM', 'hammer'), ('HH', 'hunting-horn'), ('LN', 'lance'), ('GL', 'gunlance'),
                                        ('SA', 'switch-axe'), ('CB', 'charge-blade'), ('IG', 'insect-glaive'), ('LBG', 'light-bowgun'),
                                        ('HBG', 'heavy-bowgun'), ('BOW', 'bow'), ('MIX', 'mixed'), 
                                        ])
    """
    rules = models.CharField('Rules', max_length=255, choices=[('FR','FreeStyle'), ('TW','TA wiki'), ('PD','Production'), ])
    platform = models.CharField('PlatForms', max_length=255, choices=[('SW','Switch'), ('PC','PC'),])
    problems = models.IntegerField('Problem report', blank=True, default=0)
    regist_date = models.DateTimeField(default=timezone.now)
    ipaddr = models.GenericIPAddressField(verbose_name="client-ipaddress", default="127.0.0.1")
    submitter = models.ForeignKey(User, verbose_name='record_submitter', related_name='records', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.runner
    

class Issue(models.Model):
    record = models.ForeignKey(Record, verbose_name='Record', related_name='issues', on_delete=models.CASCADE)
    open = models.BooleanField(verbose_name='open', default=True)
    request = models.CharField('request', max_length=10, choices=[('M', 'modify'), ('D', 'delete')])
    reason = models.CharField('reason', max_length=10, choices=[('C/B', 'cheat/bug'), ('M', 'miss input'), ('AR', 'against rule'), ('O', 'other')])
    detail = models.TextField(verbose_name='issue detail', max_length=1000, null=True, blank=True)

    def __str__(self):
        return self.request
 


