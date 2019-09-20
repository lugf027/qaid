1  #!/usr/bin/env python
2  # -*- coding: utf-8 -*-
3  # @Time  : 9:38
4  # @File  : t_pyMysql.py
5  # @Author: Ch
6  # @Date  : 2019/7/5
import pymysql
from common import db_helper
from  config import db_config


if __name__ == '__main__':
    dbo=db_helper.init_db(db_config.DB_Admin)
    paReal = dbo.execute_query('SELECT user_id,email,'
            'COUNT(if(state=\'0\',true,null)) as countW,'
            'COUNT(if(state=\'1\',true,null))  as countF '
            'FROM user NATURAL JOIN analysis '
            'GROUP BY user_id')
    print(paReal)