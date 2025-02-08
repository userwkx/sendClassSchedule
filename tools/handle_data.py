import pandas as pd
import re


def weeks_data_return(s):
    matches = re.findall(r'(\d+-\d+|\d+)周', s)
    result = []
    for match in matches:
        if '-' in match:
            start, end = map(int, match.split('-'))
            result.extend(range(start, end + 1))
        else:
            result.append(int(match))
    return result


def time_data_return(s):
    my_dict = {
        '第1节第2节': '08:00-09:40',
        '第3节第4节': '10:00-11:40',
        '第5节第6节': '13:30-15:10',
        '第7节第8节': '15:30-17:10',
        '第9节第10节': '18:15-19:55'
    }
    return my_dict[s]


def courses_to_list(path):
    courses = ['姓名','课程名', '上课周次', '上课星期', '开始节次', '结束节次', '上课教师', '教室名称','课程性质']
    df = pd.read_excel(path, header=0, na_values=['nan', '暂无信息'])
    df.fillna('暂无信息', inplace=True)
    for course in courses:
        if course not in df.columns:
            raise ValueError(
                f"没找到叫'{course}'的列表名，尽量按此命名：['姓名','课程名', '上课周次', '上课星期', '开始节次', '结束节次', '上课教师', '教室名称','课程性质']")

    data_list = df[courses].to_dict(orient='records')
    return data_list


def receiver_to_list(path):
    receivers = ['姓名', '邮箱']
    df = pd.read_excel(path, header=0)
    for receiver in receivers:
        if receiver not in df.columns:
            raise ValueError(
                f"没找到叫'{receiver}'的列表名，尽量按此命名：['姓名' , '邮箱']")
    data_list = df[receivers].values.tolist()
    return data_list

def Courses_data_return(path):
    Course = {
        "星期一": [],
        "星期二": [],
        "星期三": [],
        "星期四": [],
        "星期五": [],
        "星期六": [],
        "星期日": []
    }
    data_list = courses_to_list(path)
    for data in data_list:
        course_data = data['课程名']
        time_data = time_data_return(data['开始节次'] + data['结束节次'])
        location_data = data['教室名称']
        weeks_data = weeks_data_return(data['上课周次'])
        teacher = data['上课教师']
        weekday = data['上课星期']
        if data['课程性质'] == '选修':
            courser = data['姓名']
        else:
            courser = ''
        concrete_course = {
            "courser": courser,
            "course": course_data,
            "time": time_data,
            "location": location_data,
            "weeks": weeks_data,
            "teacher": teacher
        }
        Course[weekday].append(concrete_course)
    return Course


def json_format_couerse(path):
    course_dict = Courses_data_return(path)
    json_str = "COURSES = {\n"
    for day, courses in course_dict.items():
        json_str += f'    "{day}": [\n'
        for course in courses:
            course_str = "        {\n"
            course_str += f'            "courser": "{course["courser"]}",\n'
            course_str += f'            "course": "{course["course"]}",\n'
            course_str += f'            "time": "{course["time"]}",\n'
            course_str += f'            "location": "{course["location"]}",\n'
            course_str += f'            "weeks": {course["weeks"]},\n'
            course_str += f'            "teacher": "{course["teacher"]}"\n'
            course_str += "        },\n"
            json_str += course_str
        json_str = json_str.rstrip(",\n") + "\n    ],\n"
    json_str = json_str.rstrip(",\n") + "\n}"
    return json_str


def json_format_receiver(path):
    data_list = receiver_to_list(path)
    json_str = "RECEIVERS = {\n"
    for item in data_list:
        json_str += f'    "{item[0]}": "{item[1]}",\n'
    json_str = json_str.rstrip(",\n") + "\n}"
    return json_str


def excel_format(course_path , receiver_path ):
    course_json = json_format_couerse(course_path)
    with open('data/course_data.py', "w", encoding="utf-8") as f:
        f.write(course_json)
    receiver_json = json_format_receiver(receiver_path)
    with open('data/receiver_data.py', "w", encoding="utf-8") as f:
        f.write(receiver_json)



if __name__ == '__main__':
    pass