import sys
import cv2 # 安装 https://www.jianshu.com/p/922dca81ffa8
import os
import pytesseract # 安装 https://zhuanlan.zhihu.com/p/110647131
import time

if os.path.exists('frames') == False:

  os.mkdir('frames')
 
def video2frame(videos_path,frames_save_path):
  '''
  :param videos_path: 视频的存放路径
  :param frames_save_path: 视频切分成帧之后图片的保存路径
  :return:
  '''
  vidcap = cv2.VideoCapture(videos_path)
  frames = vidcap.get(cv2.CAP_PROP_FRAME_COUNT)
  success, image = vidcap.read()
  count = 0
  now=time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
  f = open(sys.argv[1]+now+".csv",'w')
  fstr=''
  while success:
    success, image = vidcap.read()
    if(success==False):
      print('read end.')
      break
    count += 1
    # pro21配置 左上角原点，速度矩形坐标是左上角[1666,26]，右下角[1887,132] 可以用ps量一下
    image_speed=image[26:132,1666:1887]
    image_time=image[145:196,1645:1887]
    image_both=image[26:196,1645:1887]

    str_speed=pytesseract.image_to_string(image_speed).strip()
    str_time=pytesseract.image_to_string(image_time).replace('00:','').strip()
    fstr+=str_speed+', '+str_time+'\n'
    # cv2.imencode('.jpg', image_speed)[1].tofile(frames_save_path + "/frame%d_speed.jpg" % count)
    # cv2.imencode('.jpg', image_time)[1].tofile(frames_save_path + "/frame%d_time.jpg" % count)
    cv2.imencode('.jpg', image_both)[1].tofile(frames_save_path + "/frame%d.jpg" % count)
    if count%30 == 0:
      print(str(count)+'/'+str(frames))
  f.write(fstr)
  f.close()
 
if __name__ == '__main__':
   videos_path = sys.argv[1]
   frames_save_path = r'frames'
   time_interval = 1#每帧都计算
   video2frame(videos_path, frames_save_path, time_interval)