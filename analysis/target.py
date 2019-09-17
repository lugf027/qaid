########################
#
# Target类，定义指标节点
# 2019/7/9 v1.0
#
########################
class Target:
    ########################
    #
    # __init__()
    # Target类构造函数
    #
    ########################
    def __init__(self, name: str, value_list: list, type: str, avg_time: list):
        self.name = name                # 指标名
        self.value_list = value_list    # 指标关键词内容
        self.type = type                # 指标类型（struct，union，time_target，other）
        self.avg_time = avg_time        # 指标匹配标准
        self.time_list = []             # 指标真实匹配次数
        self.grade = 0                  # 成绩
        self.is_check = True            # 是否匹配成功
        self.family = ''                # 指标所属类别（充分性，可比性，准时性，真实性，相关性，易得性）


    ###################################
    #
    # append_time_list(time_list: list)
    # 获取匹配次数
    # time_list:从主程序中传入的
    #           经相似度检测匹配成功次数
    #
    ###################################
    def append_time_list(self, time_list: list):
        self.time_list.append(time_list)


    ###################################
    #
    # append_time_list(time_list: list)
    # 获取匹配次数
    # time_list:从主程序中传入的
    #           经相似度检测匹配成功次数
    #
    ###################################
    def is_check_func(self):
        for list in self.time_list:
            if min(list) == 0:
                self.is_check = False


    ###################################
    #
    # get_grade()
    # 计算成绩
    # 计算匹配次数占匹配标准比例，得出加权平均
    # 大于1补正为1
    #
    ###################################
    def get_grade(self):
        grade = 0
        for list_index, list in enumerate(self.time_list):
            for index, time in enumerate(list):
                if self.avg_time[list_index][index] == 0:
                    self.avg_time[list_index][index] += 0.5
                grade += ((time/(self.avg_time[list_index][index] * 2))/len(list))/len(self.time_list)
                if grade > 1:
                    grade =1
        self.grade = grade


    ###################################
    #
    # get_family()
    # 获得指标类型
    #
    ###################################
    def get_family(self, index: int):
        if index == 0:
            self.family = '充分性'
        elif index == 1:
            self.family = '可比性'
        elif index == 2:
            self.family = '准时性'
        elif index == 3:
            self.family = '真实性'
        elif index == 4:
            self.family = '相关性'
        elif index == 5:
            self.family = '易得性'
        else:
            self.family = '未知属性'
        return self.family
