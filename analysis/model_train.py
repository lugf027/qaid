########################
#
# 模型训练过程
# 2019/7/1 v1.0
#
########################
from gensim.models import word2vec
import gensim
import logging
import os

global MODEL_NAME, CUT_FILE
MODEL_NAME = 'CitiCup_2.model'    # 模型名
CUT_FILE = 'CitiCup_cut.txt'    # 词库文件名


##########################################
# train_step()
# 训练过程入口函数
##########################################
def train_step():
    global MODEL_NAME, CUT_FILE
    for i in range(2):
        cut_txt('train/'+str(i+1) + '.dd')
        print('正在处理第' + str(i+1) + '个文件')
    if not os.path.exists(MODEL_NAME):     # 判断文件是否存在
        model_train()
    else:
        print('此训练模型已经存在，不用再次训练')


##########################################
# cut_txt(old_file_name)
# 将待训练的初始文件进行分词存入CUT_FILE
# old_file_name 初始文件名
##########################################
def cut_txt(old_file_name):
    import jieba
    global CUT_FILE
    try:
        old_file = open(old_file_name, 'r', encoding='utf-8')
        text = old_file.read()                                  # 获取文本内容
        cut_text = jieba.cut(text, cut_all=False)               # 对文本内容进行分词
        new_text = ' '.join(cut_text)
        cut_file = open(CUT_FILE, 'a+', encoding='utf-8')       # 以非覆盖方式写入CUT_FILE
        cut_file.write(new_text)
        cut_file.close()
    except BaseException as e:
        print(Exception, ":", e)


##########################################
# model_train()
# 加载词库，训练模型
##########################################
def model_train():
    global MODEL_NAME, CUT_FILE
    print('正在训练模型......')
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    train_words = word2vec.Text8Corpus(CUT_FILE)                          # 加载词库
    model = gensim.models.Word2Vec(train_words, size=200, alpha=0.001, window=10, sg=1)  # 训练skip-gram模型; 默认window=5
    model.save(MODEL_NAME)
    model.wv.save_word2vec_format(MODEL_NAME + ".bin", binary=True)       # 以二进制类型保存模型以便重用


def main():
    train_step()


if __name__ == '__main__':
    main()
