import uuid
import datetime
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect

from board.forms import *
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

from user_agents import parse

dev_url = 'http://127.0.0.1:8000'
# TODO 邮箱信息
sender_email = 'xxx.email'
sender_password = 'password'
# 作者接收匿名提问的邮箱
recipient_emails = ['xxx']

class QQEmailSender:
    def __init__(self, sender_email, sender_password, recipient_emails=[], smtp_server='smtp.qq.com', smtp_port=587):
        self.sender_email = sender_email
        self.sender_password = sender_password
        self.recipient_emails = recipient_emails
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port

    def send_email(self, subject='', body='', attachments=[]):
        try:
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.sender_email, self.sender_password)

            message = MIMEMultipart()
            message['From'] = self.sender_email
            message['To'] = ", ".join(self.recipient_emails)
            message['Subject'] = subject

            body_part = MIMEText(body, 'html')
            message.attach(body_part)

            for attachment in attachments:
                with open(attachment, 'rb') as f:
                    attachment_part = MIMEApplication(f.read(), Name=attachment.split('/')[-1])
                    attachment_part['Content-Disposition'] = f'attachment; filename="{attachment.split("/")[-1]}"'
                    message.attach(attachment_part)

            server.sendmail(self.sender_email, self.recipient_emails, message.as_string())
            server.quit()
            print("Email sent successfully!")
        except Exception as e:
            print(f"Error: {e}")


# Create your views here.
def ask_question(request):
    board_ifo = BoardIfo.objects.get(id=1)
    board_ifo.visitis += 1
    question = QuestionForm()
    ip = request.META.get('REMOTE_ADDR')
    user_agent = request.environ.get("HTTP_USER_AGENT")
    if request.method == 'POST':
        key = str(uuid.uuid4())
        mes = Question(question_key=key, question=request.POST.get('question'))

        board_ifo2 = BoardIfo.objects.get(id=1)
        print(22222)
        mes.topic = board_ifo2.topic
        mes.ip = ip
        mes.user_agent = user_agent
        mes.create_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        mes.save()
        board_ifo2.count += 1
        board_ifo2.save()
        email_sender = QQEmailSender(sender_email=sender_email, sender_password=sender_password,
                                     recipient_emails=recipient_emails)
        url = f'{dev_url}/board/host/answer?question_key={mes.question_key}'
        body = f'有新提问，回复地址：<a href="{url}">{url}</a>'
        email_sender.send_email(subject='你问我答', body=body)
        return HttpResponseRedirect('../../board/success?question_key=' + mes.question_key)
    else:
        board_ifo.save()
        return render(request, 'ask.html', {'Question': question,

                                            'title': board_ifo.title,
                                            'topic': board_ifo.topic,
                                            'count': board_ifo.count})


def answer(request):
    board_ifo = BoardIfo.objects.get(id=1)
    question = Question.objects.get(question_key=request.GET.get('question_key'))

    return render(request, 'answer.html', {'question': question.question,
                                           'answer': question.answer,
                                           'title': board_ifo.title,
                                           'topic': board_ifo.topic, })


@login_required()
def host_answer(request):
    board_ifo = BoardIfo.objects.get(id=1)
    question = Question.objects.get(question_key=request.GET.get('question_key'))
    if request.method == 'POST':
        question.answer = request.POST.get('answer')
        question.is_answer = 1
        question.save()
        if question.email:
            email_sender = QQEmailSender(sender_email=sender_email, sender_password=sender_password,
                                         recipient_emails=[question.email])
            url = f'{dev_url}/board/answer?question_key={question.question_key}'
            body = f'有新回复，回复地址：<a href="{url}">{url}</a>'
            email_sender.send_email(subject='你问我答',
                                    body=body)

        return HttpResponseRedirect('../../list')
    return render(request, 'host_answer.html', {'question': question.question,
                                                'answer': question.answer,
                                                'title': board_ifo.title,
                                                'topic': board_ifo.topic, })


def success(request):
    question_key = request.GET.get('question_key')
    answer_url = f'{dev_url}/board/answer/?question_key={question_key}'
    print("success")
    print(question_key)
    if request.method == 'POST':
        mes = Question.objects.get(question_key=request.GET.get('question_key'))
        mes.email = request.POST.get('email')
        mes.save()
        return HttpResponseRedirect('../../board/ask')

    else:
        return render(request, 'success.html', {'answer_url': answer_url})


def error():
    pass


@login_required()
def show_mes(request):
    tmpquestions = Question.objects.all()
    board_ifo = BoardIfo.objects.get(id=1)
    questions = []
    for q in tmpquestions:
        user_agent = parse(q.user_agent)
        q.user_agent = user_agent.device.family
        questions.append(q)
    return render(request, 'list.html', {'questions': questions,
                                         'visitis': board_ifo.visitis,
                                         'count': board_ifo.count})


@login_required()
def changeBoardIfo(request):
    board_ifo = BoardIfo.objects.get(id=1)
    if request.method == 'POST':
        board_ifo.topic = request.POST.get('topic')
        board_ifo.title = request.POST.get('title')
        board_ifo.save()
        return HttpResponseRedirect('../../board/changeBoardIfo')
    else:
        return render(request, 'changeTopic.html', {'title': board_ifo.title,
                                                    'topic': board_ifo.topic})


def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        user = authenticate(request, username=request.POST.get('username'), password=request.POST.get('password'))
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('../../board/list')

    form = CustomAuthenticationForm()
    return render(request, 'login.html', {'form': form})
