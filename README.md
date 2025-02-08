## 目录结构：

```
├── data/								# 存放由handle_data.py转换excel后写入的信息
│   ├── course_data.py				# 存放课程表的信息 
│   ├── receiver_data.py			# 存放收件人信息
├── excel_files/						# 该目录下存放excel，下面是两个	示例可替换
│   ├── course_excel.xlsx					
│   ├── receiver_excel.xlsx					
├── log/								   # 存放运行产生的日志
│   ├── email_log.log
├── tools/													
│   ├── handle_data.py				# 将excel转换为目标格式
│   ├── send_subject_table.py		# 发送的信息以及配置信息
│   ├── weather_info.py				# 实时获取天气
├── main.py								# 主程序入口
├── LICENSE								# 许可证文件
├── requirements.txt					# 依赖项列表
├── README.MD						# 项目说明文件
```

## 效果展示：

**没有课时的页面：**

<img src="C:\Users\wkx32\AppData\Roaming\Typora\typora-user-images\image-20250208172604684.png" alt="image-20250208172604684" style="zoom:25%;" />

**有课时的页面：**

<img src="C:\Users\wkx32\AppData\Roaming\Typora\typora-user-images\image-20250208172816326.png" alt="image-20250208172816326" style="zoom:25%;" />

## 使用说明：

1. `main.py`这里的密码不是邮箱密码,而是`STMP`服务的授权码，开启服务后会获取。

   <img src="C:\Users\wkx32\AppData\Roaming\Typora\typora-user-images\image-20250208170702700.png" alt="image-20250208170702700" style="zoom:25%;" />

2. 导入的excel表格时注意事项：

   - 课程表表头必须包含`['姓名','课程名', '上课周次', '上课星期', '开始节次', '结束节次', '上课教师', '教室名称','课程性质']`

   - 收件人表头必须包含`['姓名', '邮箱']`

3. 群发邮件时，如果是公共课，姓名那一栏可以为空，如果是选修课，要在姓名栏备注其姓名，多人重复的选修课要列多行，即每人一行。可参考`excel_files/`下的表格

4. 发送的内容可以自己在`tools/send_subject_table.py`中编辑`course_not_none()`和`course_none()`函数中的`html`代码

5. 可根据自己的开学时间修改`tools/send_subject_table.py`下的`semester_day_start()`函数，默认是`2025年2月17日`

6. 可部署到服务器上每天定时发送邮件
