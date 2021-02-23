from django.db import models

from datetime import timedelta

class Quest(models.Model):
    """クエスト"""
    questname = models.CharField('Quest Name', max_length=255)
    rank = models.CharField('Quest Rank', max_length=255)
    target = models.CharField('Target', max_length=255)
    # publisher = models.CharField('出版社', max_length=255, blank=True)
    # page = models.IntegerField('ページ数', blank=True, default=0)

    def __str__(self):
        return self.questname


class Record(models.Model):
    """記録"""
    quest = models.ForeignKey(Quest, verbose_name='Quest', related_name='records', on_delete=models.CASCADE)
    runner = models.CharField('Player Name', max_length=255)
    party = models.CharField('Party', max_length=255, choices=[('S','1'), ('P','2'), ('M', '3or4'),])
    # cleartime = models.DurationField(default=timedelta(minutes=12, seconds=7, milliseconds=780))
    cleartime = models.DurationField()
    link = models.URLField(max_length=2047)
    weapon = models.CharField('Weapon', max_length=255,
                               choices=[('GS', 'great-sword'), ('LS', 'long-sword'), ('SNS', 'sword-and-shield'), ('DB', 'dual-blades'),
                                        ('HM', 'hammer'), ('HH', 'hunting-horn'), ('LN', 'lance'), ('GL', 'gunlance'),
                                        ('SA', 'switch-axe'), ('CB', 'charge-blade'), ('IG', 'insect-glaive'), ('LBG', 'light-bowgun'),
                                        ('HBG', 'heavy-bowgun'), ('BOW', 'bow'), ('MIX', 'mixed'), 
                                        ])
    rules = models.CharField('Rules', max_length=255, choices=[('FR','FreeStyle'), ('TW','TA wiki'), ('PD','Production'), ])
    platform = models.CharField('PlatForms', max_length=255, choices=[('SW','Switch'), ('PC','PC'),])
    problems = models.IntegerField('Problem report', blank=True, default=0)

    def __str__(self):
        return self.runner