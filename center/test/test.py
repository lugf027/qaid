1  #!/usr/bin/env python
2  # -*- coding: utf-8 -*-
3  # @Time  : 17:09
4  # @File  : test.py
5  # @Author: Ch
6  # @Date  : 2019/7/11
from util import web_util
import json

def test():
    # 获取补充数据
    company='000001'
    analysis=1
    # msg = {'analysis_id': analysis, 'company_id': company}
    other_info = json.loads('''{"time_result": [[1, 1, 0, 1, 1, 0], [1, 1, 0, 2, 1, 0], [1, 1, 0, 1, 1, 0], [1, 1, 0, 1, 1, 0], [1, 1, 0, 1, 1, 0]], "other_result": [1, 1, 1]}''')
    time_target = other_info.get('time_result')
    other_target = other_info.get('other_result')

    # 调用分析
    msg = {'analysis_id': analysis, 'company_id': company, 'time_target': time_target, 'other_target': other_target}
    web_util.startService('analysis', msg)

if __name__ == '__main__':
    test()