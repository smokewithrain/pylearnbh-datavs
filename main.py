"""
数据分析案例，面向对象
两个月的销售数据，数据内容都是订单日期、订单ID、销售金额、省份
但是一个月是csv格式，一个月是json格式

制作每日销售额的图表

1. 设计一个类，完成数据的封装
2. 设计一个抽象类，定义文件读取的相关功能，并使用子类实现具体功能
3. 读取文件，生产数据对象
4. 进行数据需求的逻辑计算
"""

from file_define import FileReader, TextFileReader, JsonFileReader
from data_define import Record
from pyecharts.charts import Bar
from pyecharts.options import *
from pyecharts.globals import ThemeType

from pymysql import Connection
import json

text_file_reader = TextFileReader(r"E:\python黑马学习\第13章资料\2011年1月销售数据.txt")
json_file_reader = JsonFileReader(r"E:\python黑马学习\第13章资料\2011年2月销售数据JSON.txt")

jan_data: list[Record] = text_file_reader.read_data()
feb_data: list[Record] = json_file_reader.read_data()
# 将2个月份的数据合并为1个list存储
all_data: list[Record] = jan_data + feb_data


# 数据写入mysql数据库
# 构建mysql链接对象
# conn = Connection(
#     host="localhost",
#     port=3306,
#     user="root",
#     password="123456",
#     autocommit=True
# )
# # 获得游标对象
# cursor = conn.cursor()
# # 选择数据库
# conn.select_db("py_sql")
# # 组织sql语句
# for record in all_data:
#     sql = f"insert into orders(order_date, order_id, money, province) " \
#         f"values('{record.date}', '{record.order_id}', {record.money}, '{record.province}')"
#     cursor.execute(sql)

# conn.close()


# 将数据从mysql库中读取，并写入txt
# conn = Connection(
#     host="localhost",
#     port=3306,
#     user="root",
#     password="123456"
# )
# # 获得游标对象
# cursor = conn.cursor()
# # 选择数据库
# conn.select_db("py_sql")
# cursor.execute("select * from orders where month(order_date) = '02'; ")

# results: tuple = cursor.fetchall()
# data_list = []
# for r in results:  
#     data_dict = {}  # 将读出的数据组成json格式（字典）
#     data_dict["date"] = str(r[0])
#     data_dict["order_id"] = r[1]
#     data_dict["money"] = r[2]
#     data_dict["province"] = r[3] 
#     # ensure_ascii=False,确保非ASCII字符，如中文正常显示
#     json_str = json.dumps(data_dict, ensure_ascii=False)  # 字典转换为json格式
#     data_list.append(json_str)

# # print(data_list)
# file_path = r"E:\python黑马学习\第13章资料\2011年2月销售数据JSON-副本.txt"
# with open(file_path, 'w', encoding='UTF-8') as f:
#     for line in data_list:
#         f.write(line+'\n')


# 开始进行数据计算, 求出每天的销售额总和
# {"2011-01-01": 1234, "2011-01-02": 300, "2011-01-03": 650}
data_dict = {}
for record in all_data:
    if record.date in data_dict.keys():
        # 当前日期已有记录，和老记录做累加即可
        data_dict[record.date] += record.money
    else:
        data_dict[record.date] = record.money

# 可视化图表开发
bar = Bar(init_opts=InitOpts(theme=ThemeType.LIGHT))

bar.add_xaxis(list(data_dict.keys()))  # 添加x轴数据
bar.add_yaxis("销售额", list(data_dict.values()), label_opts=LabelOpts(is_show=False)) # 添加y轴数据
bar.set_global_opts(
    title_opts=TitleOpts(title="每日销售额")
)

bar.render(r"E:\python黑马学习\第13章资料\每日销售额柱状图.html")
