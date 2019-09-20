1  # !/usr/bin/env python
2  # -*- coding: utf-8 -*-
3  # @Time  : 14:32
4  # @File  : web_config.py
5  # @Author: Ch
6  # @Date  : 2019/7/7

# 爬虫
spider_host = 'http://101.132.108.235:8000'
# 爬取文件
spider_location = '/spider'
# 四个信息
search_location = '/search'
# 其他信息
other_location = '/analysis_other_targets'
# 股价信息
message_location='/stock'


# 转换
conversion_host = 'http://127.0.0.1:8080'
# conversion_host = 'http://47.93.40.32:8080'
conversion_location = '/conversion'

# 分析
analysis_host = 'http://47.102.110.84:8080'
analysis_location = '/analysis'


spider_next = 'conversion'
conversion_next = 'analysis'
WebConfig = {
    'spider': spider_host + spider_location,
    'conversion': conversion_host + conversion_location,
    'analysis': analysis_host + analysis_location
}
