# coding=gbk
# encoding: utf-8
# xml������
import xml.etree.ElementTree as ET
import os

classes = ['door']


# ���й�һ������
def convert(size, box):  # size:(ԭͼw,ԭͼh) , box:(xmin,xmax,ymin,ymax)
    dw = 1. / size[0]  # 1/w
    dh = 1. / size[1]  # 1/h
    x = (box[0] + box[1]) / 2.0  # ������ͼ�е����ĵ�x����
    y = (box[2] + box[3]) / 2.0  # ������ͼ�е����ĵ�y����
    w = box[1] - box[0]  # ����ʵ�����ؿ��
    h = box[3] - box[2]  # ����ʵ�����ظ߶�
    x = x * dw  # �������ĵ�x�������(�൱�� x/ԭͼw)
    w = w * dw  # �����ȵĿ�ȱ�(�൱�� w/ԭͼw)
    y = y * dh  # �������ĵ�y�������(�൱�� y/ԭͼh)
    h = h * dh  # �����ȵĿ�ȱ�(�൱�� h/ԭͼh)
    return (x, y, w, h)  # ���� �����ԭͼ���������ĵ��x�����,y�����,��ȱ�,�߶ȱ�,ȡֵ��Χ[0-1]


def convert_annotation(image_id):
    '''
    ����Ӧ�ļ�����xml�ļ�ת��Ϊlabel�ļ���xml�ļ������˶�Ӧ��bunding���Լ�ͼƬ�����С����Ϣ��
    ͨ�����������Ȼ����й�һ�����ն���label�ļ���ȥ��Ҳ����˵
    һ��ͼƬ�ļ���Ӧһ��xml�ļ���Ȼ��ͨ�������͹�һ�����ܹ�����Ӧ����Ϣ���浽Ψһһ��label�ļ���ȥ
    labal�ļ��еĸ�ʽ��calss x y w h����ͬʱ��һ��ͼƬ��Ӧ������ж�������Զ�Ӧ�ģ�����������ϢҲ�ж��
    '''
    # ��Ӧ��ͨ��year �ҵ���Ӧ���ļ��У����Ҵ���Ӧimage_id��xml�ļ������Ӧbund�ļ�
    in_file = open('../data/Annotations/%s.xml' % (image_id), encoding='utf-8')
    # ׼���ڶ�Ӧ��image_id ��д���Ӧ��label���ֱ�Ϊ
    # <object-class> <x> <y> <width> <height>
    out_file = open('../data/prelabels/%s.txt' % (image_id), 'w', encoding='utf-8')
    # ����xml�ļ�
    tree = ET.parse(in_file)
    # ��ö�Ӧ�ļ�ֵ��
    root = tree.getroot()
    # ���ͼƬ�ĳߴ��С
    size = root.find('size')
    # ��ÿ�
    w = int(size.find('width').text)
    # ��ø�
    h = int(size.find('height').text)
    # ����Ŀ��obj
    for obj in root.iter('object'):
        # ���difficult ����
        difficult = obj.find('difficult').text
        # ������ =string ����
        cls = obj.find('name').text
        # �������Ƕ�Ӧ������Ԥ���õ�class�ļ��У���difficult==1������
        if cls not in classes or int(difficult) == 1:
            continue
        # ͨ����������ҵ�id
        cls_id = classes.index(cls)
        # �ҵ�bndbox ����
        xmlbox = obj.find('bndbox')
        # ��ȡ��Ӧ��bndbox������ = ['xmin','xmax','ymin','ymax']
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text),
             float(xmlbox.find('ymax').text))
        print(image_id, cls, b)
        # ������й�һ������
        # w = ��, h = �ߣ� b= bndbox������ = ['xmin','xmax','ymin','ymax']
        bb = convert((w, h), b)
        # bb ��Ӧ���ǹ�һ�����(x,y,w,h)
        # ���� calss x y w h ��label�ļ���
        out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')


if not os.path.exists("../data/prelabels"):
    os.mkdir("../data/prelabels")

file_ids = os.listdir("../data/Annotations/")
for file_id in file_ids:
    convert_annotation(file_id[:-4])
