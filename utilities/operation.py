import db

def get_sms_captcha(mobile):
    # 获取短信验证码
    sms_captcha = db.execute('select code from send_sms_code where mobile=%s order by id desc', params=(mobile))
    return sms_captcha['code']

def delete_user(mobile):
    # 删除用户
    db.execute('delete from user where mobile=%s', params=(mobile))