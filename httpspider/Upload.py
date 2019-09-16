# !/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import os.path
import paramiko
import datetime
import re
import time


class Upload():
    def __init__(self, company_id):
        # 配置属性
        self.config = {
            # 本地项目路径
            'local_path': 'C:\\pdfs\\'+str(company_id),
            # 服务器项目路径
            'ssh_path': '/root/'+str(company_id)+'/',
            # 项目名
            'project_name': '',
            # 忽视列表
            'ignore_list': [],
            # ssh地址、端口、用户名、密码
            'hostname': '',
            'port': 22,
            'username': '',
            'password': '',
            # 是否强制更新
            'mandatory_update': True,
            # 更新完成后是否重启tomcat
            'restart_tomcat': False,
            # tomcat bin地址
            'tomcat_path': '',
            # 被忽略的文件类型
            'ignore_file_type_list': []
        }

        # ssh控制台
        self.ssh = paramiko.SSHClient()

        self.sftp = None

    def start_upload(self):
        # 上传流程开始
        print('上传开始')
        begin = datetime.datetime.now()

        # 文件夹列表
        folder_list = []
        # 文件列表
        file_list = []
        # ssh上文件列表
        ssh_file_list = []

        for parent, dirnames, filenames in os.walk(self.config['local_path'] + self.config['project_name']):
            # 初始化文件夹列表
            for dirname in dirnames:
                p = os.path.join(parent, dirname)
                folder_list.append(p[p.find(self.config['project_name']):])
            # 初始化文件列表
            for filename in filenames:
                if self.config['ignore_list'].count(filename) == 0:
                    p = os.path.join(parent, filename)
                    file_list.append(p[p.find(self.config['project_name']):])

        print('共有文件夹%s个，文件%s个' % (len(folder_list), len(file_list)))


        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(hostname=self.config['hostname'], port=self.config['port'], username=self.config['username'],
                    password=self.config['password'])
        # ssh传输
        transport = paramiko.Transport((self.config['hostname'], self.config['port']))
        transport.connect(username=self.config['username'], password=self.config['password'])

        self.sftp = paramiko.SFTPClient.from_transport(transport)

        # 检查根目录是否存在
        root_path = self.config['ssh_path'] + self.config['project_name']
        stdin, stdout, stderr = self.ssh.exec_command('find ' + root_path)
        result = stdout.read().decode('utf-8')
        if len(result) == 0:
            print('目录 %s 不存在，创建目录' % root_path)
            self.ssh.exec_command('mkdir -p ' + root_path)
            print('%s 创建成功' % root_path)
        else:
            print('目录 %s 已存在，获取所有文件' % root_path)
            ssh_file_list = re.split('\n', result)

        # 检查文件夹
        create_folder_num = 0
        for item in folder_list:
            target_folder_path = self.config['ssh_path'] + item
            create_folder_num = create_folder_num + self.check_folder(target_folder_path)

        # 可能由于发送新目录创建命令时，反应不过来，故需要在此停顿数秒再上传文件
        time.sleep(5)
        print("Sleeped")

        # 检查文件
        update_file_num = 0
        for item in file_list:
            print(item)
            if self.config['ignore_file_type_list'].count(os.path.splitext(item)[1]) == 0:
                local_file_path = item
                target_file_path = self.config['ssh_path'] + item.split('\\')[-1]
                if self.config['mandatory_update']:
                    if os.path.isfile(local_file_path):

                        self.sftp.put(local_file_path, target_file_path)
                    else:
                        print("abc")
                        raise IOError('找不到本地路径：%s !!' % local_file_path)
                    print('%s 强制更新成功' % (target_file_path))
                    update_file_num = update_file_num + 1
                else:
                    update_file_num = update_file_num + self.check_file(local_file_path, target_file_path)
            else:
                print('%s 在被忽略文件类型中，所以被忽略' % item)

        # 检查ssh是否有需要删除的文件
        '''
        delete_file_num = 0
        for item in ssh_file_list:
            temp = item[item.find(config['project_name']):]
            if folder_list.count(temp) == 0 and file_list.count(temp) == 0 and temp != config['project_name'] and temp != '':
                print('%s 在本地不存在，删除' % item)
                ssh.exec_command('rm -rf ' + item)
                delete_file_num = delete_file_num + 1
        '''

        end = datetime.datetime.now()
        print('本次上传结束：创建文件夹%s个，更新文件%s个，耗时：%s' % (create_folder_num, update_file_num, end - begin))

        if self.config['restart_tomcat']:
            print('关闭tomcat')
            self.ssh.exec_command('sh ' + self.config['tomcat_path'] + 'shutdown.sh')
            print('启动tomcat')
            self.ssh.exec_command('sh ' + self.config['tomcat_path'] + 'startup.sh')

        # 关闭连接
        self.sftp.close()
        self.ssh.close()





    # 检查文件夹是否存在，不存在则创建
    def check_folder(self, path):
        stdin, stdout, stderr = self.ssh.exec_command('find ' + path)
        result = stdout.read().decode('utf-8')
        if len(result) == 0:
            print('目录 %s 不存在，创建目录' % path)
            self.ssh.exec_command('mkdir ' + path)
            print('%s 创建成功' % path)
            return 1
        else:
            print('目录 %s 已存在' % path)
            return 0


    # 检查文件是否存在，不存在直接上传，存在检查大小是否一样，不一样则上传
    def check_file(self, local_path, ssh_path):
        # 检查文件是否存在，不存在直接上传
        stdin, stdout, stderr = self.ssh.exec_command('find ' + ssh_path)
        result = stdout.read().decode('utf-8')
        if len(result) == 0:
            self.sftp.put(local_path, ssh_path)
            print('%s 上传成功' % (ssh_path))
            return 1
        else:
            # 存在则比较文件大小
            # 本地文件大小
            lf_size = os.path.getsize(local_path)
            # 目标文件大小
            stdin, stdout, stderr = self.ssh.exec_command('du -b ' + ssh_path)
            result = stdout.read().decode('utf-8')
            tf_size = int(result.split('\t')[0])
            print('本地文件大小为：%s，远程文件大小为：%s' % (lf_size, tf_size))
            if lf_size == tf_size:
                print('%s 大小与本地文件相同，不更新' % (ssh_path))
                return 0
            else:
                self.sftp.put(local_path, ssh_path)
                print('%s 更新成功' % (ssh_path))
                return 1


'''
# 测试
upload = Upload(600000)
upload.start_upload()
'''
