# coding=utf-8
# 加载必要的库
import random
import numpy as np
import sys
import os
# import pickle

caffe_root = '/home/siudong/Deep_Learning/caffe/'
caffe_root = '/root/Deep_Learning/caffe'
# caffe_root = '/home/xsd/Deep_Learning/caffe/'

sys.path.insert(0, caffe_root + 'python')
import caffe
os.chdir(caffe_root)

# 设置当前目录
net_file = caffe_root + '/src/model/AlxNet/alxnet_deploy.prototxt'
caffe_model = caffe_root + '/src/model/AlxNet/alexNet_0.98.caffemodel'
mean_file = caffe_root + '/src/model/mean.npy'

net = caffe.Net(net_file, caffe.TEST, weights=caffe_model)

transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})
transformer.set_transpose('data', (2, 0, 1))
transformer.set_mean('data', np.load(mean_file).mean(1).mean(1))
transformer.set_raw_scale('data', 255)
transformer.set_channel_swap('data', (2, 1, 0))

# 计算欧式距离，输入为两个一千维的列表
def getEuc(imgFeature1, imgFeature2):
    dis = 0
    assert len(imgFeature1) == len(imgFeature2), 'Wrong Vector Dimension!'
    for i in xrange(len(imgFeature1)):
        dis += (imgFeature1[i]-imgFeature2[i])*(imgFeature1[i]-imgFeature2[i])
    dis = np.sqrt(dis)
    return dis

# 写文件，将一个列表中的数据写入到目标文件
def writeFile(feature_list, feature_file):
    # 将1000维浮点型特征数据保存到文件中
    with open(feature_file, 'w') as write_file:
        for i in xrange(len(feature_list)):
            write_file.write(str(feature_list[i]) + '\n')

# 读文件，将一个文件中的内容读入一个列表, 返回一个浮点型特征列表
def readFile(feature_file):
    feature = list()
    with open(feature_file, 'r') as read_file:
        code_all = read_file.readlines()
        for i in xrange(len(code_all)):
            feature.append(float(code_all[i].strip('\n')))
    return feature

def write_pair(pair, pair_path):
    print pair
    print pair_path
    pair_wt = open(pair_path, 'w')
    try:
        for i in pair:
            print i
            pair_wt.write(i.encode('utf-8'))
            # print i.encode('utf-8')
            pair_wt.write(':')
            pair_wt.write(pair[i].encode('utf-8'))
            pair_wt.write('\n')
    finally:
        pair_wt.close()


    print 'complete writing pair file!'

def read_from_pair(pair_path):
    pair = {}
    pair_read = open(pair_path, 'r')
    try:
        for line in pair_read.readlines():
            str = line.split('\n')[0].split(':')
            pair[str[0]] = str[1]
    finally:
        pair_read.close()
    return pair

# extract feature of images in a certain folder and write them to the files
def extract_feature(base_dir, feature_path):

    # net, transformer = load_model()  # 加载caffe model
    assert net is not None, 'load caffe model error!'
    assert transformer is not None, 'load caffe model error!'
    pair = {}
    items = os.listdir(base_dir)

    for i in range(0, len(items)):
        path = os.path.join(base_dir, items[i])

        file_name = os.path.split(path)[1]
        pair[file_name] = {}

        im = caffe.io.load_image(path)
        net.blobs['data'].data[...] = transformer.preprocess('data', im)
        _ = net.forward()

        encode = net.blobs['pool10'].data[0].flatten()

        float_code = list()
        for k in xrange(encode.size):
            float_code.append(round(encode[k], 5))  # 截断特征位数

        code = []
        total = 0
        for k in np.arange(encode.size):
            total += encode[k]
        avg = total / encode.size

        for j in np.arange(encode.size):
            if encode[j] >= avg:
                code.append('1')
            else:
                code.append('0')

        #     # print code[j],
        # pair[file_name]['code'] = ''.join(code)

        pair[file_name]['code'] = code

        to_path = os.path.join(feature_path, items[i].split('.')[0] + '.txt')

        pair[file_name]['txt_name'] = os.path.split(to_path)[1]

        writeFile(float_code, to_path)  # 将SqueezeNet提取出的1000维浮点型特诊存储在txt文件中

        # feature = open(to_path, 'w')
        # try:
        #     feature.write(''.join(code))
        #     print('Write feature!')
        #     feature.write('\n')
        # finally:
        #     feature.close()
        # print to_path

    return pair

def extract_feature_of_target(image):
    im = caffe.io.load_image(image)
    net.blobs['data'].data[...] = transformer.preprocess('data', im)
    out = net.forward()

    encode = net.blobs['pool10'].data[0].flatten()

    print encode

    code = []
    total = 0
    for k in np.arange(encode.size):
        total += encode[k]
    avg = total / encode.size

    for j in np.arange(encode.size):
        # print encode[j]
        if (encode[j] >= avg):
            code.append('1')
        else:
            code.append('0')
    return code


def get_prob_of_target(image):
    im = caffe.io.load_image(image)
    net.blobs['data'].data[...] = transformer.preprocess('data', im)
    _ = net.forward()

    encode = net.blobs['prob'].data[0].flatten()

    print encode

    code = []

    for k in np.arange(encode.size):
        code.append(encode[k])

    return code


def extract_feature_of_mat(im):
    # net, transformer = load_model()
    im = caffe.io.load_image(im)
    net.blobs['data'].data[...] = transformer.preprocess('data', im)
    _ = net.forward()

    encode = net.blobs['pool10'].data[0].flatten()
    # print(encode)
    code = []
    total = 0
    for k in np.arange(encode.size):
        total += encode[k]
    avg = total / encode.size

    for j in np.arange(encode.size):
        # print encode[j]
        if encode[j] >= avg:
            code.append('1')
        else:
            code.append('0')
    return code


def extract_single_img_float_feature(img):
    # net, transformer = load_model()
    img = caffe.io.load_image(img)
    net.blobs['data'].data[...] = transformer.preprocess('data', img)
    _ = net.forward()

    encode = net.blobs['pool10'].data[0].flatten()

    float_code = list()

    for k in xrange(encode.size):
        float_code.append(encode[k])  # 截断特征位数

    return float_code


def printTopk(topk, sort):
    result = {}
    # print 'The result of top ' + str(topk) + ' is: '
    i = 0
    for item in sort:
        if i < topk:
            # print item[0], item[1]
            result[i] = {}
            result[i]['name'] = item[0]
            result[i]['distance'] = item[1]
            i += 1
    return result


def calculate_hamming_distance(feature_path, code, topk):
    feature_dic = {}
    items2 = os.listdir(feature_path)
    for i in range(0, len(items2)):

        # path2为遍历特征文件夹中txt文件的所有路径
        path2 = os.path.join(feature_path, items2[i])
        feature_read = open(path2, 'r')
        try:
            temp = feature_read.readlines()
            dif = 0
            for line in temp:
                # print path2.split('/')[len(path2.split('/')) - 1],
                # print line
                for k in range(0, len(code)):
                    if code[k] != line[k]:
                        dif += 1
            feature_dic[path2] = dif
        finally:
            feature_read.close()
    sort = sorted(feature_dic.iteritems(), key = lambda asd:asd[1], reverse = False)
    result = printTopk(topk, sort)
    return result


def getHamming(a, b):
    dif = 0
    if len(a) == len(b):
        for i in range(len(a)):
            if a[i] != b[i]:
                dif += 1
        return dif
    else:
        return "Error: len(a)!=len(b)!"


def getRandomFeature():
    feature = ""
    for i in range(0, 1000):
        ran = random.random()
        if ran > 0.5:
            feature += '1'
        else:
            feature += '0'

    return feature
