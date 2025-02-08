## 目录结构：

```
├── data/                         # 存放由handle_data.py转换excel后写入的信息
│   ├── course_data.py            # 存放课程表的信息 
│   ├── receiver_data.py          # 存放收件人信息
├── excel_files/                  # 该目录下存放excel，下面是两个	示例可替换
│   ├── course_excel.xlsx					
│   ├── receiver_excel.xlsx					
├── log/                          # 存放运行产生的日志
│   ├── email_log.log
├── tools/													
│   ├── handle_data.py            # 将excel转换为目标格式
│   ├── send_subject_table.py     # 发送的信息以及配置信息
│   ├── weather_info.py           # 实时获取天气
├── main.py                       # 主程序入口
├── LICENSE                       # 许可证文件
├── requirements.txt              # 依赖项列表
├── README.MD                     # 项目说明文件
```

## 效果展示：

**没有课时的页面：**

<img src="https://github.com/user-attachments/assets/e020fec6-c313-43b1-882d-5749ede2485b" alt="image-20250208172816326" width="300" />


**有课时的页面：**

<img src="https://github.com/userwkx/sendClassSchedule/blob/main/image/image-20250208172816326.png" alt="image-20250208172816326" width="300" />

## 使用说明：

1. `main.py`这里的密码不是邮箱密码,而是`STMP`服务的授权码，开启服务后会获取。

<img src="https://github.com/userwkx/sendClassSchedule/blob/main/image/image-20250208170702700.png" alt="image-20250208172816326" width="300" />

3. 导入的`excel`表格时注意事项：

   课程信息大概格式如下（略有不同的是，`excel`多了`姓名`这一列，~~如果是选修课的话要在姓名列填入选修者姓名~~，具体可参见第四条）：

   <img src="https://github.com/userwkx/sendClassSchedule/blob/main/image/image-20250208190314.png" alt="image-20250208172816326" width="300" />

   - 课程表表头必须包含`['姓名','课程名', '上课周次', '上课星期', '开始节次', '结束节次', '上课教师', '教室名称','课程性质']`

   - 收件人表头必须包含`['姓名', '邮箱']`

4. 群发邮件时，~~如果是公共课，姓名那一栏可以为空，如果是选修课，要在姓名栏备注其姓名，多人重复的选修课要列多行，即每人一行~~。谁的课前面姓名就填写谁，如果有公共的课，每个人都要对应一条，即有几个人就重复写几条，前面姓名不同，可参考`excel_files/`下的表格

5. 群发邮件时，如果是同班级的话，可以参考`handle_data.py`下`Courses_data_return()`方法和`send_subject_table.py`下`subject_table_list()`方法被注释掉的内容，公共课的`courser`设为空，非空则为选修课，可以节省空间和时间，以及`excel`制作的时间（可以看看学校官网有没有，一般会有的（：）

3. 发送的内容可以自己在`tools/send_subject_table.py`中编辑`course_not_none()`和`course_none()`函数中的`html`代码

4. 可根据自己的开学时间修改`tools/send_subject_table.py`下的`semester_day_start()`函数，默认是`2025年2月17日`

5. 运行`main.py`

6. 可部署到服务器上每天定时发送邮件
