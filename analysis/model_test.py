########################
#
# 模型调用过程
# 2019/7/1 v1.0
#
########################
import gensim
import jieba
import os
from target import Target
from OtherTargets import OtherTargets

global MODEL_NAME, TARGET_LIST, WORD_LIST, TIME_TARGET, OTHER_TARGET, RESULT
MODEL_NAME = 'models\CitiCup_2000.model.bin'  # 模型名
WORD_LIST = []  # 待分析词列表
TIME_TARGET = [[]]
OTHER_TARGET = []
RESULT = []
TARGET_LIST = [
    # 充分性
    [
        Target('1公司年报是否披露主要的财务指标', [
            ['资产', '负债率'],
            ['流动', '比率'],
            ['速动', '比率'],
            ['应收', '账款', '周转率'],
            ['存货', '周转率'],
            ['资本金', '利润率'],
            ['销售', '利润率'],
            ['营业', '收入', '利润率'],
            ['成本', '费用', '利润率']
        ], 'struct', [
            [5.00, 5.53],
            [0.69, 0.76],
            [2.56, 2.24],
            [9.58, 9.11, 2.29],
            [2.44, 1.84],
            [3.62, 2.60],
            [2.60, 2.04],
            [5.11, 5.49, 2.16],
            [1.53, 1.49, 1.02]
        ]),
        Target('2公司年报是否披露其他应收、应付款等带"其他"字样的项目的详细情况', [
            ['其他', '应收款'],
            ['其他', '应付款'],
            ['赔款'],
            ['罚款'],
            ['出租', '包装物', '租金'],
            ['职工', '水电费'],
            ['职工', '医药费'],
            ['租入', '包装物', '押金'],
            ['暂付']
        ], 'struct', [
            [20.64, 30.07],
            [18.51, 17.64],
            [10.00],
            [4.44],
            [0.44, 1.64, 0.78],
            [5.07, 6.04],
            [3.00, 12.73],
            [1.80, 1.87, 4.33],
            [14.09]
        ]),
        Target('3公司是否披露营业外收支的详细情况', [
            ['罚款', '支出'],
            ['捐赠', '支出'],
            ['非常', '损失']
        ], 'struct', [
            [3.02, 2.27],
            [2.40, 2.27],
            [1.42, 2.96]
        ]),
        Target('4公司是否披露披露募集资金有关项目的进展', [
            ['合同', '完工', '进度'],
            ['累计', '实际', '发生']
        ], 'struct', [
            [4.11, 3.09, 2.62],
            [0.89, 1.11, 0.98]
        ]),
        Target('5投资项目未达到计划进度和收益的，公司是否披露原因', [
            ['项目', '受挫', '原因'],
            ['项目', '失败', '原因'],
            ['未到', '计划', '原因']
        ], 'union', [
            [9.16, 9.38, 2.8]
        ]),
        Target('6公司募集资金投资项目变更的是否披露变更原因', [
            ['投资', '变更', '原因'],
            ['放弃', '项目', '原因']
        ], 'union', [
            [5.84, 1.80, 1.11]
        ]),
        Target('7公司年报是否说明关联交易的必要性、持续性', [
            ['关联', '交易'],
            ['经营', '租赁'],
            ['融资', '租赁'],
            ['代理', '销售'],
            ['代理', '签订'],
            ['研发', '转移'],
            ['许可', '协议']
        ], 'union', [
            [26.62, 24.4]
        ]),
        Target('8公司若不存在重大诉讼、仲裁事项，是否在年报中明确声明', [
            ['没有', '诉讼'],
            ['没有', '仲裁'],
            ['申诉', '仲裁'],
            ['权利', '仲裁'],
            ['利益', '仲裁'],
            ['合约', '仲裁']
        ], 'union', [
            [7.44, 6.22]
        ]),
        Target('9公司是否披露支付的审计费用金额', [
            ['审计', '费用']
        ], 'struct', [
            [3.38, 1.69]
        ]),
        Target('10若不存在任何重大担保合同，公司是否在年报中声明', [
            ['担保', '合同']
        ], 'struct', [
            [11.16, 3.71]
        ]),
        Target('11公司年报是否披露更换会计事务所的原因', [
            ['会计', '事务所', '变更', '原因']
        ], 'struct', [
            [0.71, 1.27, 0.42, 0.22]
        ]),
        Target('12公司是否披露社会责任报告书', [
            ['社会', '责任', '报告']
        ], 'struct', [
            [2.42, 1.93, 1.93]
        ]),
        Target('13公司年报中是否披露重要的会计政策', [
            ['会计', '政策']
        ], 'struct', [
            [5.38, 2.96]
        ])
    ],
    # 可比性
    [
        Target('1是否未发生会计变更', [
            ['未发生', '会计', '政策', '变更'],
            ['未发生', '会计', '估计', '变更'],
            ['未发生', '会计', '差错', '更正']
        ], 'union', [
            [0, 0, 0, 0]
        ]),
        Target('2是否披露发生会计变更原因', [
            ['会计', '变更', '原因']
        ], 'struct', [
            [2.89, 2.04, 0.87]
        ])
    ],
    # 准时性
    [
        Target('2公司第一季报是否按法定时间披露', [], 'time_target', []),
        Target('3公司中报是否按法定时间披露', [], 'time_target', []),
        Target('4公司中报是否一个月内披露', [], 'time_target', []),
        Target('5公司第三季报是否按法定时间披露', [], 'time_target', []),
        Target('6年报是否在法定时间披露', [], 'time_target', []),
        Target('7年报是否在会计年度结束后两个月内披露', [], 'time_target', []),
        Target('1是否及时披露董事会、监事会和股东大会的决议报告', [
            ['决议', '刊登', '日期']
        ], 'struct', [
            [15.6, 16.89, 2.71]
        ])
    ],
    # 真实性
    [
        Target('11证监会对于信息披露不按期行为给予公开谴责', [], 'other', []),
        Target('12证监会对于信息披露不真实行为给予公开谴责', [], 'other', []),
        Target('13注册会计师出具的审计报告体现了被审单位信息披露的质量，标准无保留意见', [], 'other', []),
        Target('6两职分离能有效地提高监督和控制经理层的能力、维护董事会的独立性、保证会计信息披露质量。', [
            ['两职', '分离'],
            ['两权', '分离']
        ], 'union', [
            [0.0, 0.0]
        ]),
        Target('7是否有独立董事', [
            ['独立', '董事']
        ], 'struct', [
            [25.84, 47.02]
        ]),
        Target('8是否有审计委员会', [
            ['审计', '委员会']
        ], 'struct', [
            [5.0, 8.87]
        ]),
        Target('9公司是否披露内部控制', [
            ['组织', '控制'],
            ['人员', '控制'],
            ['职务', '控制'],
            ['业务', '控制'],
            ['授权', '控制']
        ], 'struct', [
            [1.42, 4.67],
            [1.58, 2.56],
            [6.33, 2.18],
            [5.36, 6.51],
            [0.84, 2.31]
        ]),
        Target('10是否有审计委员会', [
            ['内部', '控制', '鉴证', '报告']
        ], 'struct', [
            [0.78, 0.67, 0.44, 1.02]
        ])
    ],
    # 相关性
    [
        Target('1公司是否根据风险情况，披露拟采取的对策', [
            ['风险', '预防']
        ], 'struct', [
            [1.36, 0.87]
        ]),
        Target('2公司是否自愿披露经审核的新年度盈利预测', [
            ['盈利', '预测']
        ], 'struct', [
            [8.73, 7.93]
        ]),
        Target('3公司年报是否披露新年度的经营计划或经营目标', [
            ['经营', '目标']
        ], 'struct', [
            [3.31, 2.47]
        ]),
        Target('4公司是否对公司战略进行描述', [
            ['战略']
        ], 'struct', [
            [10.13]
        ]),
        Target('5公司是否进行行业未来的发展趋势分析', [
            ['公司', '未来'],
            ['行业', '未来']
        ], 'union', [
            [19.6, 2.6]
        ]),
        Target('6公司是否对面临的市场竞争格局进行分析', [
            ['市场', '格局'],
            ['市场', '规模'],
            ['市场', '分析'],
            ['竞争', '格局']
        ], 'union', [
            [4.96, 14.09]
        ]),
        Target('7公司是否对未来公司发展机遇和挑战进行分析', [
            ['机会', '挑战']
        ], 'struct', [
            [10.89, 32.47]
        ]),
        Target('8公司是否对面临的风险因素进行分析', [
            ['面临', '风险'],
            ['潜在', '威胁']
        ], 'union', [
            [7.71, 8.98]
        ])
    ],
    # 易得性
    [
        Target('1年报中是否披露公司建有网站', [
            ['本', '公司', '网址']
        ], 'struct', [
            [23.33, 39.16, 17.02]
        ])
    ]
]


class Model_Test:
##########################################
# get_result(company_id)
# company_id: 公司代码
# 返回：int：-1 报错，1 正常，result：报错信息（-1），正常结果（1）
# 验证过程入口函数
##########################################
    def get_result(self, company_id):
        try:
            global TIME_TARGET, OTHER_TARGET, RESULT
            other_target = OtherTargets(company_id=company_id)
            TIME_TARGET, OTHER_TARGET = other_target.get_targets()
            file_name_lists = os.listdir('dds\\' + company_id)
            dir_path = 'dds\\' + company_id
            for index, file_name in enumerate(file_name_lists):
                path = os.path.join(dir_path, file_name)
                self.cut_txt(path)
                self.check_grade(index)
                self.save_grade(file_name)
            return 1, RESULT
        except BaseException as e:
            print(str(e))
            return -1, e


##########################################
# cut_txt(self, path)
# path 路径
# 将待验证文件分词，存入WORD_LIST
##########################################
    def cut_txt(self, path):
        global WORD_LIST
        try:
            old_file = open(path, 'r', encoding='utf-8')
            section_list = old_file.read().split('$')  # 分段
            for section in section_list:  # 将段落分词，存入WORD_LIST
                cut_text = jieba.cut(section, cut_all=False)
                new_text = ' '.join(cut_text)
                new_list = new_text.split(' ')
                WORD_LIST.append(new_list)
            old_file.close()
        except BaseException as e:
            print(Exception, ":", e)


##########################################
# check_grade(self, time_target_index)
# time_target_index行数
# 相似度检测
##########################################
    def check_grade(self, time_target_index):
        global MODEL_NAME, TARGET_LIST, WORD_LIST, TIME_TARGET, OTHER_TARGET
        model = gensim.models.KeyedVectors.load_word2vec_format(MODEL_NAME, binary=True)  # 加载已训练好的模型
        for sub_target_list in TARGET_LIST:  # 计算两个词的相似度/相关程度
            for sub_target_index, target in enumerate(sub_target_list):
                if target.type == "struct":
                    for value_list in target.value_list:
                        max_time_list = []
                        for index, lists in enumerate(WORD_LIST):
                            time_list = []
                            for key_word in value_list:
                                time = 0
                                for word in lists:
                                    try:
                                        grade = model.wv.similarity(key_word, word)
                                        if grade > 0.7:
                                            time += 1
                                    except KeyError:
                                        pass
                                time_list.append(time)
                            if len(max_time_list) == 0:
                                max_time_list = time_list
                            else:
                                for i in range(len(max_time_list)):
                                    if max_time_list[i] >= time_list[i]:
                                        break
                                    if i == len(max_time_list) - 1 and max_time_list[i] < time_list[i]:
                                        max_time_list = time_list
                        target.append_time_list(max_time_list)
                        target.is_check_func()
                    target.get_grade()
                elif target.type == "union":
                    max_time_list = []
                    for value_list in target.value_list:
                        for index, lists in enumerate(WORD_LIST):
                            time_list = []
                            for key_word in value_list:
                                time = 0
                                for word in lists:
                                    try:
                                        grade = model.wv.similarity(key_word, word)
                                        if grade > 0.7:
                                            time += 1
                                    except KeyError:
                                        pass
                                time_list.append(time)
                            if len(max_time_list) == 0:
                                max_time_list = time_list
                            else:
                                for i in range(len(max_time_list)):
                                    if max_time_list[i] >= time_list[i]:
                                        break
                                    if i == len(max_time_list) - 1 and max_time_list[i] < time_list[i]:
                                        max_time_list = time_list
                    target.append_time_list(max_time_list)
                    target.is_check_func()
                    target.get_grade()
                elif target.type == 'time_target':
                    target.is_check = TIME_TARGET[time_target_index][sub_target_index]
                    target.grade = target.is_check
                else:
                    target.is_check = OTHER_TARGET[sub_target_index]
                    target.grade = target.is_check
        WORD_LIST = []


##########################################
# save_grade(self, file_name)
# file_name 文件名
# 将分析结果存入结构RESULT
##########################################
    def save_grade(self, file_name):
        global TARGET_LIST, RESULT
        value_list = []
        for index, targets in enumerate(TARGET_LIST):
            for target in targets:
                value = {
                    'type': target.get_family(index),
                    'name': target.name,
                    'grade': target.grade,
                    'is_check': target.is_check
                }
                value_list.append(value)
                target.time_list = []
                target.grade = 0
                target.is_check = True
                target.family = ''

        temp_value = {
            'year': file_name[-19:-15],
            'value': value_list
        }
        RESULT.append(temp_value)


def main():
    test_model = Model_Test()
    test_model.get_result('000001')


if __name__ == '__main__':
    main()
