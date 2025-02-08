import logging
import random
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from tools.weather_info import get_local_today_weather
from data.course_data import COURSES
from data.receiver_data import RECEIVERS
from datetime import datetime, date

# 日志记录
logging.basicConfig(level=logging.INFO, filename='log/email_log.log', filemode='a', encoding='utf-8',
                    format='%(asctime)s - %(levelname)s - %(message)s')


# 返回已经开学的天数，假设是 2025年2月17日开学
def semester_day_start():
    data = date(2025, 2, 17)
    diff = datetime.now().date() - data
    return diff.days


# 返回距离某日还有多少天，当前假设距离5月1日的天数
def semester_day_end():
    data = date(2025, 5, 1)
    diff = data - datetime.now().date()
    return diff.days

# 返回课程列表
def subject_table_list(receiver):
    weekday = week_handel()
    semester_week = (semester_day_start() // 7) + 1
    # weekday = '星期二'
    # semester_week = 1
    course_contents = []
    select_contents = []
    for course in COURSES[weekday]:
        if course['courser'] == receiver:
            if semester_week in course['weeks']:
                if course['nature'] == "必修":
                    course_content = f"""
                        <tr>
                            <td>{course['course']}</td>
                            <td>{course['time']}</td>
                            <td>{course['location']}</td>
                            <td>{course['teacher']}</td>
                        </tr>"""
                    course_contents.append(course_content)
                else:
                    select_content = f"""
                        <tr>
                            <td>{course['course']}</td>
                            <td>{course['time']}</td>
                            <td>{course['location']}</td>
                            <td>{course['teacher']}</td>
                        </tr>"""
                    select_contents.append(select_content)

    data_list = [course_contents, select_contents]
    return data_list
# 如果选修课为空 表格显示'暂无选修课'不然显得空旷
def check_select_list(content_list):
    # 检查content_list是否为空
    if not content_list:
        table_body = "<tr><td colspan='4' style='text-align: center;'>暂无选修课</td></tr>"
    else:
        table_body = ''.join(content_list)
    return table_body


# 如果必修课为空 表格显示'暂无必修课'不然显得空旷
def check_course_list(content_list):
    # 检查content_list是否为空
    if not content_list:
        table_body = "<tr><td colspan='4' style='text-align: center;'>暂无必修课</td></tr>"
    else:
        table_body = ''.join(content_list)
    return table_body


# 当有课时返回的数据
def course_not_none(receiver):
    # 天气信息
    weather_info = get_local_today_weather()
    living_index = []
    for key, value in weather_info["生活指数"].items():
        living_index.append(value)

    data_list = subject_table_list(receiver)
    # 必修课的数据
    check_course = check_course_list(data_list[0])
    # 选修课的数据
    check_select = check_select_list(data_list[1])
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{
                font-family: 'Arial', sans-serif;
                margin: 0;
                padding: 20px;
                background: #f5f7fa;
            }}
            table {{
                border-collapse: collapse;
                width: 100%;
                margin: 20px 0;
                animation: fadeIn 1s ease-in;
            }}
            th, td {{
                border: 1px solid #dddddd;
                text-align: center;
                padding: 8px;
                transition: background-color 0.3s ease;
            }}
            th {{
                background-color: #f2f2f2;
            }}
            tr:nth-child(even) {{
                background-color: #f9f9f9;
            }}
            tr:hover {{
                background-color: #f1f1f1;
            }}
            h2 {{
                text-align: center;
            }}
            @media screen and (max-width: 600px) {{
                table {{
                    border: 0;
                }}
                table thead {{
                    display: none;
                }}
                table tr {{
                    border-bottom: 1px solid #ddd;
                    display: block;
                    margin-bottom: .625em;
                }}
                table td {{
                    border-bottom: 1px solid #ddd;
                    justify-content: center;
                    display: block;
                    font-size: .8em;
                    text-align: center;
                    position: relative;
                }}
                table td::before {{
                    content: attr(data-label);
                    position: absolute;
                    left: 0;
                    width: 50%;
                    padding-left: 10px;
                    font-weight: bold;
                    text-align: left;
                    text-transform: uppercase;
                }}
                table td:last-child {{
                    border-bottom: 0;
                }}
            }}
            @keyframes fadeIn {{
                from {{
                    opacity: 0;
                    transform: translateY(-20px);
                }}
                to {{
                    opacity: 1;
                    transform: translateY(0);
                }}
            }}
        </style>
    </head>
    <body>
        <div class="text-content">
        <p style="text-align: left">👋 Hi, {receiver} - 早安！</p>
        <p style="text-align: left">今天南京市的天气：{weather_info['天气']} 气温：{weather_info['温度']}</p>
        <p style="text-align: left">🌬️😷{living_index[0]}</p>
        <p style="text-align: left">🧥🧣{living_index[1]}</p>
        <p style="text-align: left">☀️🧴{living_index[2]}</p>
        <p style="text-align: left">今天是第{(semester_day_start() // 7) + 1}周，{week_handel()}📅。</p>
        <p style="text-align: left">已经开学{semester_day_start() + 1}天🎒，距离五一劳动节还有{semester_day_end()}天🏖️⏳。</p>
        </div>
        <p style="text-align: left"> 让我们来看看今天的课表吧！📖✨</p>
        <p style="text-align: center;font-weight: bold">班级课程表</p>
        <table>
            <thead>
                <tr>
                    <th>课程名</th>
                    <th>上课时间</th>
                    <th>教室</th>
                    <th>任课教师</th>
                </tr>
            </thead>
            <tbody>
                {check_course}
            </tbody>
        </table>
        <p style="text-align: center;font-weight: bold">个人选修课</p>
        <table>
            <thead>
                <tr>
                    <th>课程名</th>
                    <th>上课时间</th>
                    <th>教室</th>
                    <th>任课教师</th>
                </tr>
            </thead>
            <tbody>
                {check_select}
            </tbody>
        </table>
        
        <div class="text-content">
            <br>
            <br>
            <p style="text-align: left">如果有选修课别忘记去了哦！🌟🕸️</p>
            <p style="font-size: 0.9em; color: #888;text-align: center">【自动拒收】回复REFUSE自动拒收</p>
            <p style="font-size: 0.85em; color: #999;text-align: center">-- 课表展示模块为小屏幕做了适配，隐藏了表头</p>
        </div>
    </body>
    </html>
    """
    return html_content


# 当没课时返回的数据
def course_none(receiver):
    # 天气信息
    weather_info = get_local_today_weather()
    living_index = []
    for key, value in weather_info["生活指数"].items():
        living_index.append(value)

    html_content = f"""
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
        <title>今日没课</title>
        <style>
            * {{
                box-sizing: border-box;
            }}

            body {{
                margin: 0;
                padding: 20px;
                min-height: 100vh; /* 替换固定高度 */
                background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
                font-family: 'Arial', sans-serif;
                display: flex;
                flex-direction: column;
                align-items: center;
            }}

            /* 通用文本样式 */
            .text-content {{
                width: 100%;
                max-width: 500px;
                margin: 10px 0;
                padding: 0 15px;
                text-align: center;
            }}

            .container {{
                background: rgba(255, 255, 255, 0.8);
                text-align: center;
                padding: 25px;
                border-radius: 15px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
                animation: fadeIn 2s ease-in-out;
                width: 100%;
                max-width: 500px;
                margin: 20px 0;
            }}

            h1 {{
                font-size: 2.2em;
                margin: 15px 0;
                color: #333;
                line-height: 1.3;
            }}

            p {{
                color: #666;
                margin: 12px 0;
                line-height: 1.5;
            }}

            .icon {{
                font-size: 3.5em;
                margin: 15px 0;
                animation: bounce 2s infinite;
            }}

            /* 移动端优先的响应式设计 */
            @media (min-width: 600px) {{
                h1 {{ font-size: 2.5em; }}
                p {{ font-size: 1.1em; }}
                .icon {{ font-size: 4em; }}
            }}

            @media (max-width: 480px) {{
                body {{
                    padding: 10px;
                }}

                .container {{
                    padding: 20px;
                    margin: 15px 0;
                }}

                h1 {{
                    font-size: 1.8em;
                    margin: 12px 0;
                }}

                p {{
                    font-size: 0.95em;
                    margin: 10px 0;
                }}

                .icon {{
                    font-size: 3em;
                }}
            }}

            @keyframes fadeIn {{
                from {{ opacity: 0; transform: translateY(-20px); }}
                to {{ opacity: 1; transform: translateY(0); }}
            }}

            @keyframes bounce {{
                0%, 20%, 50%, 80%, 100% {{ transform: translateY(0); }}
                40% {{ transform: translateY(-20px); }}
                60% {{ transform: translateY(-10px); }}
            }}
        </style>
    </head>
    <body>
        <div class="text-content">
        <p style="text-align: left">👋 Hi, {receiver} - 早安！</p>
        <p style="text-align: left">今天南京市的天气：{weather_info['天气']} 气温：{weather_info['温度']}</p>
        <p style="text-align: left">🌬️😷{living_index[0]}</p>
        <p style="text-align: left">🧥🧣{living_index[1]}</p>
        <p style="text-align: left">☀️🧴{living_index[2]}</p>
        <p style="text-align: left">今天是第{(semester_day_start() // 7) + 1}周，{week_handel()}📅。</p>
        <p style="text-align: left">已经开学{semester_day_start() + 1}天🎒，距离五一劳动节还有{semester_day_end()}天🏖️⏳。</p>
        </div>

        <div class="container">
            <div class="icon">🎉</div>
            <h1>今日没课</h1>
            <p>今天是个放松的好日子！<br>享受你的休闲时光吧！</p>
        </div>

        <div class="text-content">
            <p style="font-size: 0.9em; color: #888;">【自动拒收】回复REFUSE自动拒收</p>
            <p style="font-size: 0.85em; color: #999;">-- 课表展示模块为小屏幕做了适配，隐藏了表头</p>
        </div>
    </body>
    </html>
        """
    return html_content

# 转换为中文星期
def week_handel():
    WEEKDAYS_CN = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
    return WEEKDAYS_CN[datetime.now().weekday()]




def send_email(sd,pw):
    # 配置信息
    global count_send
    smtp_server = "smtp.qq.com"
    smtp_port = 465
    sender_email = sd
    password = pw

    receivers = RECEIVERS
    for receiver in receivers:
        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = receivers[receiver]
        msg["Subject"] = f"{receiver} - 早安"

        subject_table_list_return = subject_table_list(receiver)
        if len(subject_table_list_return[0]) == 0 and len(subject_table_list_return[1]) == 0:
            body = course_none(receiver)
        else:
            body = course_not_none(receiver)

        msg.attach(MIMEText(body, 'html'))
        try:
            with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
                server.login(sender_email, password)
                server.sendmail(sender_email, receivers[receiver], msg.as_string())
                logging.info(f"邮件发送成功: 收件人={receiver}, 邮箱={receivers[receiver]}")

        except Exception as e:
            logging.error(f"邮件发送失败: 收件人={receiver}, 邮箱={receivers[receiver]},{str(e)}")
            print(f"邮件发送成功: 收件人={receiver}, 邮箱={receivers[receiver]}")


if __name__ == '__main__':
    pass

