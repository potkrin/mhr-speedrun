from django.contrib import admin
from cms.models import Target, Quest, Record

# Register your models here.

class TargetAdmin(admin.ModelAdmin):
    list_display = ('id', 'monstername', 'imagepath',)
    list_display_links = ('id', 'monstername', 'imagepath')

admin.site.register(Target, TargetAdmin)


class QuestAdmin(admin.ModelAdmin):
    list_display = ('id', 'questname', 'rank', )
    list_display_links = ('id', 'questname', 'rank',) 
    
admin.site.register(Quest, QuestAdmin)

class RecordAdmin(admin.ModelAdmin):
    list_display = ('id', 'quest', 'runner', 'party', 'cleartime', 'weapon', 'rules', 'platform',)
    list_display_links = ('id', 'quest', )
    raw_id_fields = ('quest',)


admin.site.register(Record, RecordAdmin)