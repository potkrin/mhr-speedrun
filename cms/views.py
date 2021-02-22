from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.views.generic.list import ListView

from cms.models import Quest, Record
from cms.forms import QuestForm, RecordForm

# for list sort
from operator import itemgetter, attrgetter
from datetime import timedelta
# Create your views here.

def quest_list(request):
    """クエストの一覧"""
    # return HttpResponse('List of Quest')
    quests = Quest.objects.all().order_by('id')
    return render(request, 'cms/quest_list.html',  # 使用するテンプレート
                           {'quests': quests})     # テンプレートに渡すデータ


def quest_edit(request, quest_id=None):
    """クエストの編集"""
    # return HttpResponse('Edit Quest')
    if quest_id: # edit
        quest = get_object_or_404(Quest, pk=quest_id)
    else:        # add
        quest = Quest()
    
    if request.method == 'POST':
        form = QuestForm(request.POST, instance=quest)
        if form.is_valid():
            quest = form.save(commit=False)
            quest.save()
            return redirect('cms:quest_list')
    else:  # GET
        form = QuestForm(instance=quest)
    
    return render(request, 'cms/quest_edit.html', dict(form=form, quest_id=quest_id))


def quest_del(request, quest_id):
    """クエストの削除"""
    # return HttpResponse('Delete Quest')
    quest = get_object_or_404(Quest, pk=quest_id)
    quest.delete()
    return redirect('cms:quest_list')

class PageStatus:
    party = 'solo'
    weapon = 'all'
    weapon_name = 'All'
    rule = 'all'
    platform = 'switch'
    free = ''
    tawiki = ''
    product = ''
    plat_all = ''
    switch = ''
    pc = ''
    record_list = ''
    summary = ''


class WeaponInfo:
    def __init__(self, name, urlname, modelname):
        self.name = name
        self.urlname = urlname
        self.modelname = modelname


weapon_list = [
                WeaponInfo('All', 'all', r'.*'),
                WeaponInfo('Great Sword', 'great-sword', 'GS'),
                WeaponInfo('Long Sword', 'long-sword', 'LS'),
                WeaponInfo('Sword & Shield', 'sword-and-shield', 'SNS'),
                WeaponInfo('Dual Blades', 'dual-blades', 'DB'),
                WeaponInfo('Hammer', 'hammer', 'HM'),
                WeaponInfo('Hunting Horn', 'hunting-horn', 'HH'),
                WeaponInfo('Lance', 'lance', 'LN'),
                WeaponInfo('Gunlance', 'gunlance', 'GL'),
                WeaponInfo('Switch Axe', 'switch-axe', 'SA'),
                WeaponInfo('Charge Blade', 'charge-blade', 'CB'),
                WeaponInfo('Insect Glaive', 'insect-glaive', 'IG'),
                WeaponInfo('Light Bowgun', 'light-bowgun', 'LBG'),
                WeaponInfo('Heavy Bowgun', 'heavy-bowgun', 'HBG'),
                WeaponInfo('Bow', 'bow', 'BOW'),
                WeaponInfo('Mixed', 'mix', 'MIX'),
              ]
  

class RecordList(ListView):
    """クエストのTA記録の一覧"""
    context_object_name = 'records'
    template_name = 'cms/record_list.html'
    # paginate_by = 2 # 1ページは最大2件

    def get(self, request, *args, **kwargs):
        quest = get_object_or_404(Quest, pk=kwargs['quest_id'])

        st = PageStatus()
        st.party = kwargs['party']
        st.weapon = kwargs['weapon']
        st.rule = kwargs['rule']
        st.platform = kwargs['platform']

        if st.rule == 'all':
            st.free = 'checked'
        elif st.rule == 'ta-wiki':
            st.tawiki = 'checked'
        elif st.rule == 'production':
            st.product = 'checked'

        if st.platform == 'all':
            st.plat_all= 'checked'
        elif st.platform == 'switch':
            st.switch = 'checked'
        elif st.platform == 'pc':
            st.pc = 'checked'
        
        st.record_list = 'checked'
        


        party_qr = kwargs['party']
        #party_re
        if party_qr=='all':
            party_re = r'.*'
        elif party_qr=='pair':
            party_re = r'P'
        elif party_qr=='multi':
            party_re = r'M'
        else:
            party_re = r'S'


        weapon_qr = kwargs['weapon']
        weapon_re = r'.*'
        for itr in weapon_list:
            if weapon_qr == itr.urlname:
                weapon_re = itr.modelname
                st.weapon_name = itr.name
                break

        rule_qr = kwargs['rule']
        if rule_qr=='free-style':
            rule_re = r'.*'
        elif rule_qr=='ta-wiki':
            rule_re = r'TW'
        elif rule_qr=='production':
            rule_re = r'PD'
        else:
            rule_re = r'.*'

        platform_qr = kwargs['platform']
        #platform_re
        if platform_qr=='all':
            platform_re = r'.*'
        elif platform_qr=='switch':
            platform_re = r'SW'
        elif platform_qr=='pc':
            platform_re = r'PC'
        else:
            platform_re = r'SW'
 
        records = quest.records.filter(party__regex=party_re, weapon__regex=weapon_re, rules__regex=rule_re, platform__regex=platform_re).order_by('cleartime')

        self.object_list = records
        context = self.get_context_data(object_list=self.object_list, quest=quest, st=st, weapon_list=weapon_list)
        return self.render_to_response(context)

class Summary(ListView):
    """武器ランキング と トップ3まとめ用"""
    context_object_name = 'records'
    template_name = 'cms/weapon_rank.html'

    def get(self, request, *args, **kwargs):
        quest = get_object_or_404(Quest, pk=kwargs['quest_id'])

        st = PageStatus()
        st.party = kwargs['party']
        st.rule = kwargs['rule']
        st.platform = kwargs['platform']
        st.weapon_name = 'All'

        if st.rule == 'all':
            st.free = 'checked'
        elif st.rule == 'ta-wiki':
            st.tawiki = 'checked'
        elif st.rule == 'production':
            st.product = 'checked'

        if st.platform == 'all':
            st.plat_all= 'checked'
        elif st.platform == 'switch':
            st.switch = 'checked'
        elif st.platform == 'pc':
            st.pc = 'checked'

        st.summary = 'checked'

        rule_qr = kwargs['rule']
        if rule_qr=='free-style':
            rule_re = r'.*'
        elif rule_qr=='ta-wiki':
            rule_re = r'TW'
        elif rule_qr=='production':
            rule_re = r'PD'
        else:
            rule_re = r'.*'

        platform_qr = kwargs['platform']
        if platform_qr=='all':
            platform_re = r'.*'
        elif platform_qr=='switch':
            platform_re = r'SW'
        elif platform_qr=='pc':
            platform_re = r'PC'
        else:
            platform_re = r'SW'
 
        ### add for ranking
        records = []
        for i in range(1, 15):
            wrecords = quest.records.filter(party__regex='S', weapon__regex=weapon_list[i].modelname, rules__regex=rule_re, platform__regex=platform_re).order_by('cleartime')
            if not wrecords:
                top = Record(runner="NO ENTRY YET", cleartime=timedelta(seconds=3599), weapon=weapon_list[i].modelname)
                records.append(top)
            else:
                records.append(wrecords[0])
        records = sorted(records, key=attrgetter('cleartime'))
        ### add for ranking end

        self.object_list = records
        context = self.get_context_data(object_list=self.object_list, quest=quest, st=st)
        return self.render_to_response(context)




def record_edit(request, quest_id, record_id=None):
    """記録の編集"""
    quest = get_object_or_404(Quest, pk=quest_id)
    if record_id:
        record = get_object_or_404(Record, pk=record_id)
    else:
        record = Record()

    if request.method == 'POST':
        form = RecordForm(request.POST, instance=record)
        if form.is_valid():
            record = form.save(commit=False)
            record.quest = quest
            record.save()
            return redirect('cms:record_list', quest_id=quest_id, party='solo', weapon='all', rule='all', platform='switch')
    else: # GET
        form = RecordForm(instance=record)
    
    return render(request, 'cms/record_edit.html', dict(form=form, quest_id=quest_id, record_id=record_id))

def record_del(request, quest_id, record_id):
    """記録の削除"""
    record = get_object_or_404(Record, pk=record_id)
    record.delete()
    return redirect('cms:record_list', quest_id=quest_id, party='solo', weapon='all', rule='all', platform='switch')
