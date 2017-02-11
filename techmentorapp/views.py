from django.shortcuts import render, redirect
from .models import Mentor, Skill_Detail, Profile, Review, Skill, Available, Infomation
from django.utils import dateformat
from django.contrib.auth.decorators import login_required
from .forms import MentorForm, ProfileForm, SkillForm, AddSkillForm, ScheduleForm, ContactForm
from datetime import datetime as dt
import string, random, datetime
import urllib.parse
from django.db.models import Q
from django.core.mail import send_mail
from django.core.paginator import (
    Paginator,  # ページネーター本体のクラス
    EmptyPage,  # ページ番号が範囲外だった場合に発生する例外クラス
    PageNotAnInteger  # ページ番号が数字でなかった場合に発生する例外クラス
)


# def _get_page(list_, page_no, count=1):
#     """ページネーターを使い、表示するページ情報を取得する"""
#     paginator = Paginator(list_, count)
#     try:
#         page = paginator.page(page_no)
#     except (EmptyPage, PageNotAnInteger):
#         # page_noが指定されていない場合、数値で無い場合、範囲外の場合は
#         # 先頭のページを表示する
#         page = paginator.page(1)
#     return page


# Create your views here.
def home(request):
    return render(request, 'home.html', {})

def mentor_detail(request, id):

    if request.method == "POST" and \
        not request.user.is_anonymous() and \
        'content' in request.POST and \
        request.POST['content'].strip() != '':
        Review.objects.create(content=request.POST['content'], mentor_id=id, user=request.user)

    try:
        mentor = Mentor.objects.get(id=id)
    except Mentor.DoesNotExist:
        return redirect('/')

    d = mentor.create_time
    create = dateformat.format(d, 'Y年 n月 d日')
    u = mentor.update_time
    update = dateformat.format(u, 'Y年 n月 d日')
    m = mentor.mentor_time
    mentime = dateformat.format(m, 'Y年 n月 d日')
    documents = Skill_Detail.objects.filter(status=True)

    url = request.get_full_path()
    parsed = urllib.parse.urlparse(url)
    params = urllib.parse.parse_qs(parsed.query)

    if not params:
        if mentor.user == request.user:
            return redirect('/mentor_list/')

    # mentor.mentor_time = 1
    # mentor.save()

    if request.user.is_anonymous() or \
        Review.objects.filter(mentor=mentor, user=request.user).count() > 0:
        show_post_review = False
    else:
        show_post_review = True #後で直す

    reviews = Review.objects.filter(mentor=mentor)
    return render(request, 'mentor_detail.html', {
        "mentor": mentor,
        "documents": documents,
        "create": create,
        "update": update,
        "mentime": mentime,
        "reviews": reviews,
        "show_post_review": show_post_review,
        "params": params,
    })


def mentor_list(request):
    info = Infomation.objects.all().order_by('-id')[:4]
    if not request.user.is_anonymous():
        mentors = Mentor.objects.all().exclude(user=request.user).exclude(status=False)
    else:
        mentors = Mentor.objects.all().exclude(status=False)
    page = request.GET.get('page')

    paginator = Paginator(mentors, 10)
    try:
        # mentors = _get_page(
        #     Mentor.objects.order_by('-id'),  # 投稿を新しい順に並び替えて取得する
        #     request.GET.get('page')  # GETクエリからページ番号を取得する
        # )

        paged_list = paginator.page(page)
    except PageNotAnInteger:
        paged_list = paginator.page(1)
    except EmptyPage:
        paged_list = paginator.page(paginator.num_pages)


    return render(request, 'mentor_list.html', {'mentors': paged_list, 'info': info})

@login_required(login_url="/")
def edit_mentor(request):
    try:
        mentor = Mentor.objects.get(user=request.user)
        error = ''
        if request.method == 'POST':
            mentor_form = MentorForm(request.POST, instance=mentor)
            if mentor_form.is_valid():
                mentor.save()
                success = "更新しました"
                # return redirect('/edit_mentor/')
                return render(request, 'edit_mentor.html', {'mentor': mentor, "error": error, "success": success})
            else:
                error = mentor_form.errors #"Data is not valid"

        return render(request, 'edit_mentor.html', {'mentor': mentor, "error": error})
    except Mentor.DoesNotExist:
        return redirect('/')

@login_required(login_url="/")
def edit_profile(request):
    try:
        profile = Profile.objects.get(user=request.user)
        error = ''
        if request.method == 'POST':
            profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
            if profile_form.is_valid():
                # photoが空白だった場合は既存のまま
                # if not photo:
                #     profile.photo = photo
                profile.save()
                # return redirect('/edit_profile/')
                success = "更新しました"
                return render(request, 'edit_profile.html', {'profile': profile, "error": error, "success": success})
            else:
                error = profile_form.errors

        return render(request, 'edit_profile.html', {'profile': profile, "error": error})
    except Mentor.DoesNotExist:
        return redirect('/')


@login_required(login_url="/")
def my_skills(request):
    try:
        mentor = Mentor.objects.get(user=request.user)
        skills = Skill_Detail.objects.filter(mentor=mentor)
    except Skill_Detail.DoesNotExist:
        return redirect('/add_skill/')

    if request.method == 'POST':
        delete_ids = request.POST.getlist('delete_ids')
        if delete_ids:
            Skill_Detail.objects.filter(id__in=delete_ids).delete()
            delete = "削除しました"
            return render(request, 'my_skill.html', {"skills": skills, "delete": delete})
        else:
            error = "削除項目を選択してください"
        return render(request, 'my_skill.html', {"skills": skills, "error": error})

    return render(request, 'my_skill.html', {"skills": skills})


@login_required(login_url="/")
def add_skill(request):
    mentor = Mentor.objects.get(user=request.user)
    skills = Skill_Detail.objects.filter(mentor=mentor)
    error = ''
    add_skill = Skill.objects.all()
    # add_skill = Skill.objects.filter(~Q(name=skills))
    # Skill.objects.all().exclude(name=skills)
    skill_list = []
    for all in add_skill:
        skill_list.append(all)
        for not_need in skills:
            if all.name == not_need.skill.name:
                skill_list.pop()


    if request.method == 'POST':
        add_skill_form = AddSkillForm(request.POST)
        if add_skill_form.is_valid():
            skill = add_skill_form.save(commit=False)
            skill.mentor = mentor
            skill.save()
            # return redirect('/my_skill/')
            success = "スキルを追加しました"
            return render(request, 'my_skill.html', {"skills": skills, "error": error, "success": success})
        else:
            error = "Data is not valid"
        return render(request, 'add_skill.html', {"error": error})
    add_skill_form = AddSkillForm()
    return render(request, 'add_skill.html', {"add_skill_form": add_skill_form, "error": error, "skill_list": skill_list})


@login_required(login_url="/")
def edit_skill(request, id):
    try:
        skill = Skill_Detail.objects.get(id=id)
        error = ''
        if request.method == 'POST':
            skill_form = SkillForm(request.POST, instance=skill)
            if skill_form.is_valid():
                skill.save()
                # return redirect('/my_skill/')
                success = "更新しました"
                return render(request, 'edit_skill.html', {'skill': skill, "error": error, "success": success})
            else:
                error = skill_form.errors

        return render(request, 'edit_skill.html', {'skill': skill, "error": error})
    except Mentor.DoesNotExist:
        return redirect('/')

def category(request, link):
    categories = {
        "html-css": "HTML & CSS",
        "javascript": "JavaScript",
        "php": "PHP",
        "python": "Python",
        "ruby-on-rails": "Ruby on Rails"
    }
    try:
        skill = Skill.objects.get(name=categories[link])
        # mentors = Mentor.objects.filter(skill=skill).exclude(user=request.user)
        if not request.user.is_anonymous():
            mentors = Mentor.objects.filter(skill=skill).exclude(user=request.user)
        else:
            mentors = Mentor.objects.filter(skill=skill)
        info = Infomation.objects.all().order_by('-id')[:4]
        # mentors = Mentor.objects.all()
    except Skill.DoesNotExist:
        return redirect('/')

    page = request.GET.get('page')

    paginator = Paginator(mentors, 10)
    try:
        paged_list = paginator.page(page)
    except PageNotAnInteger:
        paged_list = paginator.page(1)
    except EmptyPage:
        paged_list = paginator.page(paginator.num_pages)
    return render(request, 'mentor_list.html', {'mentors': paged_list, 'skill': skill, 'info': info})


def search(request):
    try:
        if not request.user.is_anonymous():
            mentors = Mentor.objects.filter(
                Q(specialty__contains=request.GET['title']) |
                # Q(skill__name__in=request.GET['title']) |
                Q(about__contains=request.GET['title']) |
                Q(job__contains=request.GET['title'])
            ).exclude(user=request.user)
        else:
            mentors = Mentor.objects.filter(
                Q(specialty__contains=request.GET['title']) |
                # Q(skill__name__in=request.GET['title']) |
                Q(about__contains=request.GET['title']) |
                Q(job__contains=request.GET['title'])
            )
    except KeyError:
        return redirect('/')

    info = Infomation.objects.all().order_by('-id')[:4]
    page = request.GET.get('page')

    paginator = Paginator(mentors, 10)
    try:
        paged_list = paginator.page(page)
    except PageNotAnInteger:
        paged_list = paginator.page(1)
    except EmptyPage:
        paged_list = paginator.page(paginator.num_pages)

    return render(request, 'mentor_list.html', {'mentors': paged_list, 'info': info})


@login_required(login_url="/")
def reserve(request, id):
    if not request.user.profile.email:
        error = "emailを設定してください"
        return redirect(request.META.get('HTTP_REFERER'), error=error)
    week = datetime.date.today()
    today = datetime.date.today()
    date_time = []
    available_format = []
    week_list = []
    date_format = []
    time_list = []
    hour = 11
    minutes = "00"
    int_minutes = 0
    for i in range(7):
        week = week + datetime.timedelta(days=1)
        week_list.append(week)
        date_format.append(week.strftime("%Y年%m月%d日"))

    for i in range(12):
        for j in range(2):
            time_list.append(str(hour) + ":" + minutes)
            if minutes == "00":
                minutes = "30"
            else:
                minutes = "00"
        hour = hour + 1

    for i in range(7):
        today = today + datetime.timedelta(days=1)
        hour = 11
        for j in range(9):
            for k in range(2):
                time = datetime.time(hour, int_minutes, 0)
                diff = datetime.datetime.combine(today, time)
                date_time.append(diff)
                available_format.append(diff)
                if int_minutes == 0:
                    int_minutes = 30
                else:
                    int_minutes = 0
            hour = hour + 1

    try:
        mentor = Mentor.objects.get(id=id)
        available = Available.objects.filter(mentor=mentor)

        show = []
        boolean = True
        tbody_list = []
        for time in time_list:
            thead = '<tr><th>' + time + '</th>'
            if available:
                for week in date_format:
                    for ava in available:
                        if ava.date == week and ava.time == time:
                            if ava.status == True:
                                status = "○"
                                tbody_list.append('''
                                <td><a href="/mentor/reserve_check/'''
                                + str(ava.id) +
                                '''/'''
                                + str(mentor.id) +
                                '''" class="btn btn-info schedule-btn"> '''
                                + status +
                                '''
                                </a>  
                                </td>''')
                            else:
                                status = "×"
                                tbody_list.append('''
                                <td> <p class="btn btn-success schedule-btn disabled">'''
                                + status +
                                '''
                                </p></td>''')
                            boolean = False
                            break
                    if boolean == False:
                        boolean = True
                    elif boolean == True:
                        tbody_list.append('''
                            <td> 
                            <p class="btn btn-success schedule-btn disabled">×</p>
                            </td> 
                            ''')
            else:
                for week in date_format:
                    tbody_list.append('''
                    <td> 
                    <p class="btn btn-success schedule-btn disabled">×</p>
                    </td> 
                    ''')
            close = '</tr>'
            result = thead
            for list in tbody_list:
                result += list
            result += close
            show.append(result)
            tbody_list.clear()



    except Mentor.DoesNotExist:
        return redirect('/')

    return render(request, 'reserve.html', {
        'week_list': week_list,
        'time_list': time_list,
        'available': available,
        'date_format': date_format,
        'available_format': available_format,
        'show': show
    })


@login_required(login_url="/")
def my_schedule(request):
    week = datetime.date.today()
    today = datetime.date.today()
    date_time = []
    available_format = []
    week_list = []
    date_format = []
    time_list = []
    hour = 11
    minutes = "00"
    int_minutes = 0
    url = request.get_full_path()
    parsed = urllib.parse.urlparse(url)
    params = urllib.parse.parse_qs(parsed.query)
    if params:
        week = datetime.date.today() + datetime.timedelta(days=7)
    for i in range(7):
        week = week + datetime.timedelta(days=1)
        week_list.append(week)
        date_format.append(week.strftime("%Y年%m月%d日"))


    for i in range(12):
        for j in range(2):
            time_list.append(str(hour) + ":" + minutes)
            if minutes == "00":
                minutes = "30"
            else:
                minutes = "00"
        hour = hour + 1

    for i in range(7):
        today = today + datetime.timedelta(days=1)
        hour = 10
        for j in range(9):
            for k in range(2):
                time = datetime.time(hour, int_minutes, 0)
                diff = datetime.datetime.combine(today, time)
                date_time.append(diff)
                available_format.append(diff)
                if int_minutes == 0:
                    int_minutes = 30
                else:
                    int_minutes = 0
            hour = hour + 1

    try:
        mentor = Mentor.objects.get(user=request.user)
        available = Available.objects.filter(mentor=mentor)


        show = []
        boolean = True
        tbody_list = []
        for time in time_list:
            thead = '<tr><th>' + time + '</th>'
            if available:
                for week in date_format:
                    for ava in available:
                        if ava.date == week and ava.time == time:
                            status = ''
                            if ava.status == True:
                                status = "○"
                                tbody_list.append('''
                                <td> 
                                <a href="/edit_schedule/'''
                                + str(ava.id) +
                                '''" class="btn btn-info schedule-btn"> '''
                                + status +
                                '''
                                </a>  
                                </td>''')
                            else:
                                status = "×"
                                tbody_list.append('''
                                <td> 
                                <a href="/edit_schedule/'''
                                + str(ava.id) +
                                '''" class="btn btn-success schedule-btn"> '''
                                + status +
                                '''
                                </a>  
                                </td>''')
                            boolean = False
                            break
                    if boolean == False:
                        boolean = True
                    elif boolean == True:
                        tbody_list.append('''
                        <td> 
                            <a href="/create_schedule/?date='''
                            + week +
                            '''&time='''
                            + time +
                            '''" class="btn btn-success schedule-btn">
                                ×
                            </a> 
                        </td> 
                        ''')
            else:
                for week in date_format:
                    tbody_list.append('''
                    <td> 
                    <a href="/create_schedule/?date='''
                    + week +
                    '''&time='''
                    + time +
                    '''" class="btn btn-success schedule-btn">
                    ×
                    </a> 
                    </td> 
                    ''')
            close = '</tr>'
            result = thead
            for list in tbody_list:
                result += list
            result += close
            show.append(result)
            tbody_list.clear()

    except Mentor.DoesNotExist:
        return redirect('/')

    return render(request, 'my_schedule.html', {
        'week_list': week_list,
        'time_list': time_list,
        'available': available,
        'date_format': date_format,
        'available_format': available_format,
        'show': show,
        'params': params
    })

@login_required(login_url="/")
def create_schedule(request):
    try:
        mentor = Mentor.objects.get(user=request.user)
    except Mentor.DoesNotExist:
        return redirect('/')

    url = request.get_full_path()
    parsed = urllib.parse.urlparse(url)
    params = urllib.parse.parse_qs(parsed.query)
    date = ""
    time = ""
    for k, v in params.items():
        if k == "date":
            date = '%s' % v
        elif k == "time":
            time = v


    if request.method == 'POST':
        create_schedule_form = ScheduleForm(request.POST)
        if create_schedule_form.is_valid():
            schedule = create_schedule_form.save(commit=False)
            schedule.mentor = mentor
            schedule.save()
            return redirect('/my_schedule/')
        else:
            error = create_schedule_form.errors
        return render(request, 'create_schedule.html', {"error": error})

    schedule_form = ScheduleForm
    return render(request, 'create_schedule.html', {
        "schedule_form": schedule_form,
        "params": params,
        "date": date,
        "time": time
    })


@login_required(login_url="/")
def edit_schedule(request, id):
    try:
        mentor = Mentor.objects.get(user=request.user)
        avalilable = Available.objects.get(mentor=mentor, id=id)
    except Available.DoesNotExist:
        return redirect('/')
    if request.method == 'POST':
        schedule_form = ScheduleForm(request.POST, instance=avalilable)
        if schedule_form.is_valid():
            schedule = schedule_form.save(commit=False)
            schedule.mentor = mentor
            schedule.save()
            # return redirect('/my_schedule/')
            success = "更新しました"
            return render(request, 'edit_schedule.html', {"avalilable": avalilable, "success": success})
        else:
            error = "Data is not valid"
        return render(request, 'edit_schedule.html', {"avalilable": avalilable, "error": error})

    return render(request, 'edit_schedule.html', {"avalilable": avalilable})


@login_required(login_url="/")
def reserve_check(request, id, mentor):
    try:
        profile = Profile.objects.get(user=request.user)
        mentor = Mentor.objects.get(id=mentor)
        avalilable = Available.objects.get(mentor=mentor, id=id)
    except Available.DoesNotExist:
        return redirect('/')

    if request.method == 'POST':
        schedule_form = ScheduleForm(request.POST, instance=avalilable)
        if schedule_form.is_valid():
            schedule = schedule_form.save(commit=False)
            schedule.status = False
            schedule.save()

            tdatetime = avalilable.date + avalilable.time
            mentor.mentor_time = dt.strptime(tdatetime, '%Y年%m月%d日%H:%M')
            mentor.save()

            def random_string(length, seq=string.digits + string.ascii_lowercase):

                sr = random.SystemRandom()
                return ''.join([sr.choice(seq) for i in range(length)])

            num = random_string(random.randint(12, 22))
            apper_url = "https://appear.in/" + num
            contents =  request.POST["text"]

            from_addr = 'no-reply@coworkplace.jp'
            to_addrs = profile.email
            bcc_addrs = mentor.user.profile.email

            subject = "予約確認メール"
            body_text = '''
            ＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝
            　　　　　　ご予約は下記のとおりです。
            ＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝

            【予約者】
            {0}
            【メンター】
            {1}
            【予約日時】
            {2}
            【質問内容】
            {3}
            【URL】
            {4}

            ■■□―――――――――――――――――――□■■
            TechMentor運営事務局
            URL：http://techmentor.jp/
            ■■□―――――――――――――――――――□■■
            '''.format(profile.name, mentor.name, avalilable.date + avalilable.time, contents, apper_url)

            send_mail(subject, body_text, from_addr, [to_addrs], fail_silently=False)
            send_mail(subject, body_text, from_addr, [bcc_addrs], fail_silently=False)

            return redirect('/thanks_page/')
        else:
            error = schedule_form.errors
            return render(request, 'reserve_check.html', {"avalilable": avalilable, "mentor": mentor, "error": error})

    return render(request, 'reserve_check.html', {"avalilable": avalilable, "mentor": mentor})


def thanks_page(request):
    return render(request, 'thanks.html', {})


def infomation(request):
    try:
        info = Infomation.objects.all().order_by('-id')[:10]
    except Infomation.DoesNotExist:
        return redirect('/')
    return render(request, 'infomation.html', {"info": info})

def contact(request):
    if request.method == 'POST':
        contact_form = ContactForm(request.POST)
        if contact_form.is_valid():
            contact = contact_form.save(commit=False)
            contact.save()

            from_addr = 'no-reply@coworkplace.jp'
            to_addrs = 'kubota-kohei@coworkplace.jp'

            name = request.POST["name"]
            email = request.POST["email"]
            subject = request.POST["subject"]
            reply_subject = "お問い合わせが送信されました"
            text = request.POST["text"]

            body_text = '''
＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝
　　　　　　お問い合わせがありました
＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝

【名前】
{0}
【メールアドレス】
{1}
【件名】
{2}
【内容】
{3}

<お問い合わせ先>
http://techmentor.jp/contact

■■□―――――――――――――――――――□■■
TechMentor運営事務局
URL：http://techmentor.jp
■■□―――――――――――――――――――□■■
            '''.format(name, email, subject, text)

            reply_text = '''
＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝
                   お問い合わせを受付しました
＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝

TechMnetor運営事務局です。

以下の内容でお問い合わせが送信されましたので、ご確認ください。

【名前】
{0}
【メールアドレス】
{1}
【件名】
{2}
【内容】
{3}

※このメールはTechMentorをご利用中のお客様にお送りしております。
お心当たりのない場合やご不明な点などございましたら、以下のお問合せ先までご連絡ください。
※本メールに返信されてもご返答はいたしかねます。

<お問い合わせ先>
http://techmentor.jp/contact

＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝
※　このメールに見覚えのない場合はお手数ですが破棄してください。
＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝

■■□―――――――――――――――――――□■■
TechMentor運営事務局
URL：http://techmentor.jp
■■□―――――――――――――――――――□■■
            '''.format(name, email, subject, text)

            send_mail(reply_subject, body_text, from_addr, [to_addrs], fail_silently=False)

            send_mail(reply_subject , reply_text, from_addr, [email], fail_silently=False)

            return redirect('/thanks_page/')
        else:
            error = contact_form.errors
            return render(request, 'contact.html', {"error": error})


    return render(request, 'contact.html', {})

def company(request):
    return render(request, 'company.html', {})

def privacy_policy(request):
    return render(request, 'privacy_policy.html', {})

def policy(request):
    return render(request, 'policy.html', {})





