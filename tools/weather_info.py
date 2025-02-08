import requests
from bs4 import BeautifulSoup


def get_local_today_weather():
    # 获取不同城市天气信息，可替换城市代码 例如南京：101190101
    url = "http://www.weather.com.cn/weather/101190101.shtml"  # 南京市的天气信息页面
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}

    response = requests.get(url, headers=headers)
    response.encoding = "utf-8"

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        today = soup.find("ul", class_="t clearfix").find("li")

        weather = today.find("p", class_="wea").text  # 天气情况
        temperature = today.find("p", class_="tem").get_text(strip=True)  # 温度

        # 生活指数（仅提取感冒指数、穿衣指数、紫外线指数）
        live_index = soup.find("div", class_="livezs")
        target_indices = {"感冒指数", "穿衣指数", "紫外线指数"}
        indices = {}
        for item in live_index.find_all("li"):
            index_value = item.find("p").text.strip()
            index_name = item.find("em").text.strip()
            if index_name in target_indices:
                indices[index_name] = index_value

        return {
            "天气": weather,
            "温度": temperature,
            "生活指数": indices
        }
    else:
        # 防止爬取失败导致整个程序运行不了
        print("获取天气信息失败")
        return {
            "天气": '天气信息获取失败',
            "温度": '温度信息获取失败',
            "生活指数": '生活指数信息获取失败'
        }
