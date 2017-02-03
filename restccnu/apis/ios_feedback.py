#coding: utf-8

from . import api
from .decorators import admin_required, tojson
from flask import request, jsonify
from restccnu.models import connection, Feedback
# from restccnu.workers.workers import send_async_mail

ADMIN_EMAIL = "muxistudio@qq.com"
MAIL_DEFAULT_SENDER = "muxistudio@163.com"
MAIL_SUBJECT_PREFIX = "[feedback]"

# def send_mail(to, subject, template, **kwargs):
#     """
#     kwargs: {'feedback', 'contact'}
#     """
#     msg = Message(
#         MAIL_SUBJECT_PREFIX+ subject,
#         sender = MAIL_DEFAULT_SENDER,
#         recipients = [to]
#     )
#     msg.html = render_template(template, **kwargs)
#     send_async_email.delay(msg)  # delay


@api.route('/feedback/', methods=['GET', 'POST'])
def ios_post_feedback():
    if request.method == 'POST':
        feedobj = connection.Feedback()
        feedback = request.get_json().get('feedback')
        contact = request.get_json().get('contact')
        # 发邮件服务 => 直接发管理后台
        # send_mail(  # a celery async task
        #     ADMIN_EMAIL, 'ccnubox~ios: there is a new feedback',
        #     'mail.html',
        #     feedback=feedback, contact=contact
        # )
        feedobj['contact'] = contact # 存储用户反馈: 联系方式+反馈信息
        feedobj['feedback'] = feedback
        feedobj.save()
        return jsonify({}), 201


@api.route('/feedbacks/', methods=['GET'])
@admin_required
@tojson
def ios_get_feedback():
    feedbacks_list = []
    feedbacks = connection.Feedback.find()
    for feedback in feedbacks:
        feedbacks_list.append({
            feedback['contact']:feedback['feedback']
        })
    return feedbacks_list
    