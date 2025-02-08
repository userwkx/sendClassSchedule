from tools.handle_data import excel_format
from tools.send_subject_table import send_email

if __name__ == '__main__':

    # 目的是将excel表格数据转换成目标数据格式，执行一次即可，下次可以注释掉
    # 填写课表和收件人的excel路径
    course_path = 'excel_files/course_excel.xlsx'
    receiver_path = 'excel_files/receiver_excel.xlsx'
    excel_format(course_path, receiver_path)

    # 填写发送邮件的账号
    SENDER_EMAIL = '###########@qq.com'
    # 填写STMP授权码
    PASSWORD = '#################'

    send_email(SENDER_EMAIL, PASSWORD)
    print('SUCCESS!')
