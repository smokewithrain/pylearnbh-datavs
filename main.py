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

text_file_reader = TextFileReader(r"E:\python黑马学习\第13章资料\2011年1月销售数据.txt")
json_file_reader = JsonFileReader(r"E:\python黑马学习\第13章资料\2011年2月销售数据JSON.txt")

jan_data: list[Record] = text_file_reader.read_data()
feb_data: list[Record] = json_file_reader.read_data()
# 将2个月份的数据合并为1个list存储
all_data: list[Record] = jan_data + feb_data

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
