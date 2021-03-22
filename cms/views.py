from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.views.generic.list import ListView

from cms.models import Quest, Record, Weapon, Issue
from cms.forms import QuestForm, RecordForm, IssueForm

# for list sort
from operator import itemgetter, attrgetter
from datetime import timedelta
# Create your views here.

from django.urls import reverse

# to get client ipaddress
from ipware import get_client_ip

# for login_required
from django.contrib.auth.decorators import login_required

from django.views.generic import DetailView

def quest_list(request):
    """クエストの一覧"""
    # return HttpResponse('List of Quest')
    quests = Quest.objects.all().order_by('priority')
    return render(request, 'cms/quest_list.html',  # 使用するテンプレート
                           {'quests': quests, 'nav': 'Q'})     # テンプレートに渡すデータ


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

# party, weapon などの選択情報を保持するクラス
class PageStatus:
    party = 'solo'
    party_name = ''
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

class PartyInfo:
    def __init__(self, name, urlname, modelname):
        self.name = name
        self.urlname = urlname
        self.modelname = modelname

class RuleInfo:
    def __init__(self, name, urlname, modelname):
        self.name = name
        self.urlname = urlname
        self.modelname = modelname

class PlatformInfo:
    def __init__(self, name, urlname, modelname):
        self.name = name
        self.urlname = urlname
        self.modelname = modelname


weapon_list = [
                WeaponInfo('All', 'all', ''),
                WeaponInfo('Great Sword', 'great-sword', 'Great Sword'),
                WeaponInfo('Long Sword', 'long-sword', 'Long Sword'),
                WeaponInfo('Sword & Shield', 'sword-and-shield', 'Sword & Shield'),
                WeaponInfo('Dual Blades', 'dual-blades', 'Dual Blades'),
                WeaponInfo('Hammer', 'hammer', 'Hammer'),
                WeaponInfo('Hunting Horn', 'hunting-horn', 'Hunting Horn'),
                WeaponInfo('Lance', 'lance', 'Lance'),
                WeaponInfo('Gunlance', 'gunlance', 'Gunlance'),
                WeaponInfo('Switch Axe', 'switch-axe', 'Switch Axe'),
                WeaponInfo('Charge Blade', 'charge-blade', 'Charge Blade'),
                WeaponInfo('Insect Glaive', 'insect-glaive', 'Insect Glaive'),
                WeaponInfo('Light Bowgun', 'light-bowgun', 'Light Bowgun'),
                WeaponInfo('Heavy Bowgun', 'heavy-bowgun', 'Heavy Bowgun'),
                WeaponInfo('Bow', 'bow', 'Bow'),
                WeaponInfo('Mixed', 'mix', 'Mixed'),
              ]
  
party_list = [
                PartyInfo('All', 'all', r'.*'),
                PartyInfo('Solo', 'solo', 'S'),
                PartyInfo('Pair', 'pair', 'P'),
                PartyInfo('3or4', 'multi', 'M'),
             ]

rule_list = [
                RuleInfo('Freestyle', 'all', r'.*'),
                RuleInfo('TAwiki', 'ta-wiki', 'TW'),
                RuleInfo('Production', 'production', 'PD'),
            ]

platform_list = [
                PlatformInfo('All', 'all', r'.*'),
                PlatformInfo('Switch', 'switch', 'SW'),
                PlatformInfo('PC', 'pc', 'PC'),
                ]
 
class RecordList(ListView):
    """クエストのTA記録の一覧"""
    context_object_name = 'records'
    template_name = 'cms/record_list.html'
    # paginate_by = 2 # 1ページは最大2件

    def get(self, request, *args, **kwargs):
        quest = get_object_or_404(Quest, pk=kwargs['quest_id'])

        num = quest.records.all().count()
        quest.recordnum = num
        quest.save()

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
        
        # make regular expression for DB from URL path
        party_qr = kwargs['party']
        for itr in party_list:
            if party_qr == itr.urlname:
                party_re = itr.modelname
                st.party_name = itr.name
                break
        
        weapon_qr = kwargs['weapon']
        weapon_re = ''
        for itr in weapon_list:
            if weapon_qr == itr.urlname:
                weapon_re = itr.modelname
                if itr.name != 'All':
                    st.weapon_name = itr.name
                else:
                    st.weapon_name = 'Weapon'
                break

        rule_qr = kwargs['rule']
        for itr in rule_list:
            if rule_qr == itr.urlname:
                rule_re = itr.modelname
                break
        
        platform_qr = kwargs['platform']
        for itr in platform_list:
            if platform_qr == itr.urlname:
                platform_re = itr.modelname
                break

        records = quest.records.filter(party__regex=party_re, weapon__name__regex=weapon_re, rules__regex=rule_re, platform__regex=platform_re).order_by('cleartime')
# for issue num update (but maybe don't need)
        for itr in records:
            itr.problems = Issue.objects.filter(record=itr, open=True).count()

        self.object_list = records
        context = self.get_context_data(object_list=self.object_list, quest=quest, st=st, weapon_list=weapon_list, party_list=party_list, rule_list=rule_list)
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

        party_qr = kwargs['party']
        #party_re
        for itr in party_list:
            if party_qr == itr.urlname:
                party_re = itr.modelname
 

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
        st.weapon_name = 'Weapon'
        st.party_name = 'Solo'

        rule_qr = kwargs['rule']
        for itr in rule_list:
            if rule_qr == itr.urlname:
                rule_re = itr.modelname
                break
        
        platform_qr = kwargs['platform']
        for itr in platform_list:
            if platform_qr == itr.urlname:
                platform_re = itr.modelname
                break
        
        records = []
        summary_list = []
        for j in range(0, 14):
            summary_list.append([])

        for i in range(1, 15):
            #print(weapon_list[i].modelname)
            wrecords = quest.records.filter(party__regex='S', weapon__name=weapon_list[i].modelname, rules__regex=rule_re, platform__regex=platform_re).order_by('cleartime')
            if not wrecords:
                #print("no rec")
                top = Record(runner="NO ENTRY YET", cleartime=timedelta(seconds=3599), weapon=Weapon.objects.filter(name=weapon_list[i].modelname)[0])
                records.append(top)
            else:
                #print("found")
                records.append(wrecords[0])
                for j in range(0, len(wrecords)):
                    summary_list[i-1].append(wrecords[j])

        #for i in records:
            #print(i.weapon)
        records = sorted(records, key=attrgetter('cleartime'))
        ### add for ranking end

        self.object_list = records
        context = self.get_context_data(object_list=self.object_list, quest=quest, st=st, weapon_list=weapon_list, party_list=party_list, summary_list=summary_list)
        return self.render_to_response(context)


@login_required
def usersub_list(request):
    # quests = Quest.objects.all().order_by('priority')
    user = request.user
    records = Record.objects.filter(submitter=user).order_by('regist_date')
    return render(request, 'cms/usersub_list.html',  # 使用するテンプレート
                           {'records': records, 'nav': 'U', 'user': user})     # テンプレートに渡すデータ



@login_required
def record_edit(request, quest_id, record_id=None, conf=None):
    """記録の編集"""
    quest = get_object_or_404(Quest, pk=quest_id)
    user = request.user
    print(user.username)
    if record_id:
        record = get_object_or_404(Record, pk=record_id)
        if record.submitter != user:
            print("permission denyed")
            return redirect('cms:record_list', quest_id=quest_id, party='solo', weapon='all', rule='all', platform='switch')
    else:
        record = Record()

    if request.method == 'POST':
        form = RecordForm(request.POST, instance=record)
        if conf == 1 or not form.is_valid():
            return render(request, 'cms/record_edit.html', dict(form=form, quest_id=quest_id, record_id=record_id, noconf=1, quest=quest))

        if form.is_valid():
            record = form.save(commit=False)
            client_addr, _ = get_client_ip(request)
            record.ipaddr = client_addr
            record.quest = quest
            record.submitter = user
            record.save()
            return redirect('cms:record_list', quest_id=quest_id, party='solo', weapon='all', rule='all', platform='switch')
    else: # GET
        record.quest = quest
        form = RecordForm(instance=record)
    
    return render(request, 'cms/record_edit.html', dict(form=form, quest_id=quest_id, record_id=record_id, quest=quest, user=user))


def record_del(request, quest_id, record_id):
    """記録の削除"""
    record = get_object_or_404(Record, pk=record_id)
    if record.submitter.username == request.user.username:
        record.delete()
    return redirect('cms:record_list', quest_id=quest_id, party='solo', weapon='all', rule='all', platform='switch')


def issue_edit(request, quest_id, record_id, accept=None):
    """問題報告の編集"""
    record = get_object_or_404(Record, pk=record_id)
    issue = Issue()

    if request.method == 'POST':
        form = IssueForm(request.POST, instance=issue)
        if form.is_valid():
            issue = form.save(commit=False)
            issue.record = record 
            issue.save()
            record.problems = record.problems + 1
            record.save()
            #return redirect('cms:record_list', quest_id=quest_id, party='solo', weapon='all', rule='all', platform='switch')
            context = dict(accept=1)
            # return redirect('cms:issue_submit', {quest_id=quest_id, record_id=record_id, accept=1} context=context ) 
            return render(request, 'cms/issue_edit.html', {'record': record, 'form': form, 'quest_id': quest_id, 'record_id': record_id, 'accept': 1} )

    else: # GET
        issue.record = record 
        form = IssueForm(instance=issue)
    
    return render(request, 'cms/issue_edit.html', {'record': record, 'form': form, 'quest_id': quest_id, 'record_id': record_id, } )

def about_site(request, nav):
    if nav=="rules":
        nav = 'R'
    elif nav=="submit":
        nav = 'S'
    elif nav=="site":
        nav = 'A'
    
    client_addr, _ = get_client_ip(request)
    print(client_addr)

    """サイト概要"""
    return render(request, 'cms/about.html', {'nav_site': 1, 'nav': nav,})

def about_rules(request):
    """ルールについてヘルプ画面"""
    return render(request, 'cms/about.html', {'nav_rules': 1})

def about_submit(request):
    """提出方法についてのヘルプ画面"""
    return render(request, 'cms/about.html', {'nav_submit': 1})

