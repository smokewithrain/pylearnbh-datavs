"""
和文件相关的类定义
"""

from data_define import Record
import json

# 先定义一个抽象类用来做顶层设计，确定有哪些功能需要设计
class FileReader:
    def read_data(self) -> list[Record]:
        """
        读取文件的数据，每一条数据都转换为Record对象，将它们都封装到list内返回
        """
        pass


class TextFileReader(FileReader):
    def __init__(self, path):
        self.path = path      # 定义成员变量记录文件的路径

    def read_data(self) -> list[Record]:
        f = open(self.path, "r", encoding="UTF-8")
        
        record_list: list[Record] = []
        for line in f.readlines():
            line = line.strip()   # 消除读取到的每一行数据中的\n
            data_list = line.split(",")

            record = Record(data_list[0], data_list[1], int(data_list[2]), data_list[3])
            record_list.append(record)
        
        f.close()
        return record_list
    
class JsonFileReader(FileReader):
    def __init__(self, path):
        self.path = path      # 定义成员变量记录文件的路径

    def read_data(self) -> list[Record]:
        f = open(self.path, "r", encoding="UTF-8")
        
        record_list: list[Record] = []
        for line in f.readlines():
            data_dict = json.loads(line)
            record = Record(data_dict["date"], data_dict["order_id"], int(data_dict["money"]), data_dict["province"])
            record_list.append(record)
        
        f.close()
        return record_list


if __name__ == "__main__":
    text_file_reader = TextFileReader(r"E:\python黑马学习\第13章资料\2011年1月销售数据.txt")
    record_list = text_file_reader.read_data()
    for record in record_list:
        print(record)

    # json_file_reader = JsonFileReader(r"E:\python黑马学习\第13章资料\2011年2月销售数据JSON.txt")
    # record_list = json_file_reader.read_data()
    # for record in record_list:
    #     print(record)
