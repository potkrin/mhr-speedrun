from django.contrib import admin
from cms.models import Target, Weapon, Quest, Record, Issue

# Register your models here.

class TargetAdmin(admin.ModelAdmin):
    list_display = ('id', 'monstername', 'imagepath',)
    list_display_links = ('id', 'monstername', 'imagepath')

admin.site.register(Target, TargetAdmin)


class WeaponAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'imagepath',)
    list_display_links = ('id', 'name', 'imagepath')

admin.site.register(Weapon, WeaponAdmin)


class QuestAdmin(admin.ModelAdmin):
    list_display = ('id', 'questname', 'rank', )
    list_display_links = ('id', 'questname', 'rank',) 
    
admin.site.register(Quest, QuestAdmin)

class RecordAdmin(admin.ModelAdmin):
    list_display = ('id', 'quest', 'runner', 'party', 'cleartime', 'weapon', 'rules', 'platform', 'regist_date')
    list_display_links = ('id', 'quest', )
    raw_id_fields = ('quest',)

admin.site.register(Record, RecordAdmin)

class IssueAdmin(admin.ModelAdmin):
    list_display = ('id', 'record', 'open', 'request', 'reason', 'detail',)
    list_display_links = ('id', 'record', 'open', )
    raw_id_fields = ('record',)

admin.site.register(Issue, IssueAdmin)
 