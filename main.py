from skimage import io,transform 
import tensorflow as tf
import numpy as np
import time 
import os 
from download_picture import get_present_picture 
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
pi_addr = "pi@10.42.0.150"
button_signal_path = "./signal/button_signal.sig"
result_signal_path = "./signal/result_signal.sig"
voice_path = "~/voice_response/"
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
    #每次必须初始化四张无关的图片
    image_data = []
    for i in range(5):
        initial_image = read_one_image("./data/train/initial.jpg")
        image_data.append(initial_image)
    print("Initial OK!!!") 
        #从路径输入一张图片
    
    while True:
        with open(button_signal_path, 'r+') as button_signal:
            flag = button_signal.read().strip()
            #print(flag)
            try:
                if int(flag) == 1:#当按钮按下，获取实时图片进行识别，否则继续等待
                    print("开始识别......")
                    image_path = get_present_picture()
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

                    print(objects_dic[output[5]])
                    del image_data[4]

                    button_signal.seek(0,0)
                    button_signal.truncate()
                    button_signal.write("0")
                    print("按钮信号清零")
                    with open(result_signal_path, 'r+') as result_signal:
                        result_signal.seek(0,0)
                        result_signal.truncate()
                        result_signal.write(objects_dic[output[5]])
                        print("结果已经写入文件")
                        #此处加入语音模块
                        cmd = "ssh " +pi_addr + " 'play " + voice_path + "21.mp3 " + voice_path + str(output[5]) + ".mp3'"
                        os.system(cmd)
                    continue 
                else:
                    #print("等待中......")
                    continue 
            except:
                continue
    
    ''' 
    while True: 
        flag = input("Picture Ready?")
        if flag == 'y':
            image_path = get_present_picture()
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
        else:
            continue
    '''
