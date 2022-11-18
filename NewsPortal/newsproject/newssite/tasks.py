
from accounts.models import subscription
from django.core import mail
from django.shortcuts import redirect, render, reverse
from newsproject.newssite.models import New, Category
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from datetime import datetime, date, timedelta
from newsproject.accounts.models import User, UsersSubscriptions




def send_message(pk_, id_categories_):
    new = New.objects.get(id=pk_)
    emails = User.objects.filter(category__in=id_categories_).values('email').distinct()
    email_list = [item['email'] for item in emails]
    html_content = render_to_string(
        'subscribe_created.html',
        {
            'usersubscribtions': new
        }
    )
    msg = EmailMultiAlternatives(
        subject=f'{mail.title}',
        body=f'{mail.text}',
        from_email='demopython@yandex.ru',
        to=[subscription.user.email],
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def week_news():
    start = datetime.now() - timedelta(7)
    finish = datetime.now()
    categories = Category.objects.all()

    for category_ in categories:
        new_list = New.objects.filter(date_time__range = (start, finish), category=category_.pk)
        print(new_list)
        email_list = []
        print(category_)
        for user_ in User.objects.all():
            user_email = UsersSubscriptions.objects.filter(category=category_.pk, user=user_.pk)
            if user_email and user_email not in email_list:
                email_list.append(user_.email)
        print(email_list)

        if new_list:
            html_content = render_to_string(
                'week_news.html',
                {
                    'news': new_list,
                    'category': category_.category_name
                }
            )
            msg = EmailMultiAlternatives(
                subject=f'{mail.title}',
                body=f'{mail.text}',
                from_email='demopython@yandex.ru',
                to=[subscription.user.email],
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()