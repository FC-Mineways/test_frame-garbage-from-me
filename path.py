import os
import sys
import json

class Path():
    '''
    初始化时获得本文件的绝对路径
    back（返回上级方式）:
    '''
    def __init__(self):
        fp = os.path.abspath(__file__)
        ul_pos = fp[::-1].find('\\')
        self.fp = fp[:len(fp)-ul_pos]

    def back(self, n=1):
        if n == 0:
            fp = self.fp
            ul_pos = fp.find('\\')
            self.fp = fp[:ul_pos+1]
        else:
            for i in range(n):
                fp = self.fp
                ul_pos = fp[-2::-1].find('\\')
                self.fp = fp[:len(fp) - ul_pos-1]
        return self.fp

    # flag默认不移动，有值后将会使文件路径至目标位置，路径无文件夹时会新建
    def isHere(self, filename, flag=0):
        fp = self.fp + filename
        if not os.path.exists(fp):
            os.mkdir(fp)
            print('>新建文件夹：'+filename)
        if flag:
            self.fp = fp + '\\'

    # 新建文件
    def new_file(self, filename, data):
        with open(self.fp+filename, 'w+', encoding='utf-8') as ff:
            ff.write(data)

    # 返回被调用时所在文件的路径
    def now(self):
        return sys.argv[0]

class PathGod(Path):
    def ini(self, data):
        # 新建总目录及文件结构
        self.isHere(data['file']['name'], 1)
        for file in data['file']['data']:
            self.isHere(file)
        del data['file']['data'], data['file']['name']
        for file in data['file']:
            self.new_file(file, data['file'][file])
        del data['file']
        # 读取data.json，并根据内容对文件进行新建
        for i in data:
            self.isHere(data[i]['re_path'])
            re_path = data[i]['re_path'] + '\\' + i
            self.new_file(re_path, data[i]['msg'])
            # 对于依赖额外处理，自动执行安装
            if i == '所用依赖.txt':
                lis = data[i]['msg'].split(',')
                for j in lis:
                    os.system("pip install " + j)

        return self.fp

    # 请在PATH基础上增加额外路径，否则删库跑路，连自己都不放过
    def clear(self, path):
        if os.path.isdir(path):  # 判断是不是文件夹
            for file in os.listdir(path):  # 遍历文件夹里面所有的信息返回到列表中
                self.clear(os.path.join(path, file))  # 是文件夹递归自己
            if os.path.exists(path):  # 判断文件夹为空
                os.rmdir(path)  # 删除文件夹
                print("删除文件夹" + path)

        else:
            if os.path.isfile(path):  # 严谨判断是不是文件
                os.remove(path)  # 删除文件
                print("删除文件" + path)

    # def down(self):
    #     lis = [x for x in dir(a) if 'fp' in x]
    #     dic = {}
    #     for i in lis:
    #         dic[i] = self.i
    #     dic['head'] = self.fp_head
    #     dic['path'] = self.fp
    #     dit = json.dumps(dic, sort_keys=False, indent=4, separators=(',', ': '))
    #     with open('path.json', 'w', encoding='utf-8') as ff:
    #         ff.write(dit)
    #
    # def inin(self):
    #     with open('path.json', 'r', encoding='utf-8') as ff:
    #         dic = json.load(ff)


class Data():

    def __init__(self):
        self.data = {}

    # 从py文件读取代码 并将信息存入字典
    def data_on(self, fileway, filename):
        dic = {'re_path': fileway}
        # 拼装绝对路径
        abs_way = PATH + self.data['file']['name'] + '\\' + fileway + filename
        print(abs_way)

        with open(abs_way, 'r', encoding='utf-8') as ff:
            dic['msg'] = ff.read()
            self.data[filename] = dic

    # 书写为json格式保存
    def data_down(self):
        d = json.dumps(self.data, sort_keys=False, indent=4, separators=(',', ': '))
        with open('data.json', 'w+', encoding='utf-8') as ff:
            ff.write(d)

    # 从json格式读出
    def data_up(self):
        with open('data.json', 'r', encoding='utf-8') as ff:
            self.data = json.load(ff)
        return self.data

    # 目录结构
    def data_file(self, name, data):
        datas = {'name': name, 'data': data}
        self.data['file'] = datas

    def data_me(self):
        path = Path().now()
        with open(path, 'r', encoding='utf-8') as ff:
            name = path[path.rfind('\\')+1:]
            self.data['file'][name] = ff.read()

# 1-初始化文件通过data.json 2-更新存档信息至data.json 3-执行全流程
def operate(num=0):
    if int(num%2):
        '''读取数据并初始化文件结构与内容'''
        data = Data().data_up()
        PathGod().ini(data)
    if int(num/2):
        '''读取当前文件结构内容并输入至json文件'''
        os.system('python TEST\\data_lib.py')
        os.remove('TEST\\data_lib.py')

# # 绝对路径
PATH = Path().fp
if __name__ == "__main__":
    operate(3)
