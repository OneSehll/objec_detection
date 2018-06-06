from skimage import io,transform 
import tensorflow as tf
import numpy as np
import time 
objects_dic = {
        0:'康师傅冰红茶',
        1:'可比克薯片',
        2:'猪',
        3:'猴子',
        4:'鲨鱼',
        5:'好丽友派',
        6:'双汇肉花肠',
        7:'食人鱼',
        8:'鹰',
        9:'兔子',
        10:'狗',
        11:'友臣肉松饼',
        12:'眼镜蛇',
        13:'蜜蜂',
        14:'益达口香糖',
        15:'旺旺碎冰冰',
        16:'狮子',
        17:'康师傅红烧牛肉面',
        18:'老干妈',
        19:'农夫山泉'
}

w=299
h=299
c=3

def read_one_image(path):
    img = io.imread(path)
    img = transform.resize(img,(w,h))
    return np.asarray(img)

with tf.Session() as sess:
    #读入模型的参数过程
    print("Session define OK")
    print(time.asctime(time.localtime(time.time())))
    saver = tf.train.import_meta_graph('./model/-780.meta')
    print("Saver initial OK")    
    print(time.asctime(time.localtime(time.time())))
    saver.restore(sess,tf.train.latest_checkpoint('./model'))
    print("Restore model OK")
    print(time.asctime(time.localtime(time.time())))
    graph = tf.get_default_graph()
    print("Graph OK")
    print(time.asctime(time.localtime(time.time())))
    #每次必须初始化一张无关的图片
    image_data = []
    for i in range(4):
        initial_image = read_one_image("./data/train/initial.jpg")
        image_data.append(initial_image)
    print("Initial OK!!!") 
        #从路径输入一张图片
    while True: 
        image_path = input("Input image path:")#输入图片，后期可以改动
        data = read_one_image(image_path)
        image_data.append(data)
    
        images = graph.get_tensor_by_name("input_images:0")
        feed_dict = {images:image_data}
        logits = graph.get_tensor_by_name("InceptionV3/Logits/SpatialSqueeze:0")
        classification_result = sess.run(logits,feed_dict)

        #打印出预测矩阵
        #print(classification_result)
        #打印出预测矩阵每一行最大值的索引
        print(tf.argmax(classification_result,1).eval())
        #根据索引通过字典对应图片的分类
        output = []
        output = tf.argmax(classification_result,1).eval()
        print(objects_dic[output[4]])
        del image_data[4]
