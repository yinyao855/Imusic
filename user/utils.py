from django.contrib.sessions.models import Session
from django.core.mail import send_mail


def sendMessage(email):  # 发送邮件并返回验证码
    # 生成验证码
    import random
    str1 = '0123456789'
    rand_str = ''
    for i in range(0, 6):
        rand_str += str1[random.randrange(0, len(str1))]
    # 发送邮件：
    # send_mail的参数分别是  邮件标题，邮件内容，发件箱(settings.py中设置过的那个)，收件箱列表(可以发送给多个人),失败静默(若发送失败，报错提示我们)
    pre_message = "欢迎加入imusic!\n"
    message = pre_message + "您的验证码是" + rand_str + "，10分钟内有效，请尽快填写"
    emailBox = []
    emailBox.append(email)
    send_mail('imusic开发团队', message, from_email='yinyao5312021@163.com', recipient_list=emailBox, fail_silently=False)
    return rand_str


from datetime import datetime


def validate_verification_code(request, verification_code):
    sessionId = request.POST.get("sessionId")
    if not sessionId:
        return False

    # 解密获取会话数据
    try:
        session = Session.objects.get(session_key=sessionId)
        session_data = session.get_decoded()
    except Session.DoesNotExist:
        return False

    # 获取验证码和过期时间
    session_verification_code = session_data.get("verification_code", None)
    expire_date = session.expire_date

    # 判断验证码是否正确
    if session_verification_code and session_verification_code == verification_code:
        # 判断验证码是否过期
        if expire_date:
            current_time = datetime.now()
            if current_time <= expire_date:
                # 清除已验证的验证码
                del request.session['verification_code']
                return True
            else:
                # 验证码已过期
                return False
        else:
            # 没有过期时间，无法判断是否过期
            return False
    else:
        return False

