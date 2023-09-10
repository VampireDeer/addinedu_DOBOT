import sys
import os
import pandas as pd
import cv2, imutils
import time
import datetime
import urllib.request
import numpy as np
import threading


# Yolo import
from detect import run_yolo_detection




class DobotController:
    def __init__(self):
        self.do_composit = 'default'
        print(self.do_composit)

# DOBOT 행동하는 변수를 self.do_composit으로 지정하겠습니다.
# self.do_composit == [default, screenshot, first_act, second_act, third_act]

    # image screenshot and save
    def image_screenshot(self): # 이미지 저장 1장만 저장된다
        self.video = cv2.VideoCapture(0)
        print(self.do_composit)

        while True:
            ret, frame = self.video.read()
            if (self.do_composit == "screenshot"): #로봇이 처음 시작하고 시작 자리로 위치시 Home으로 바뀌고 스크린샷
                #now = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = "/home/seokwon/dev_ws/dobot/project/image_files/" + "image1" + ".png"
                cv2.imwrite(filename, frame)
                self.do_composit = "yolo_detect"
                print(self.do_composit)
            break

    









    # dobot_acting
    def dobot_acting(self):
        self.do_composit = "screenshot"
        
        print(self.do_composit)



    def main(self):
        # 필요한 옵션을 설정합니다.
        weights = '/home/seokwon/dev_ws/yolo/src/yolov3/runs/train/yolov3_cl215/weights/best.pt'
        source = '/home/seokwon/dev_ws/dobot/project/image_files/image.png' # "0"
        data = 'data/mydata.yaml'
        imgsz = (640,640)
        conf_thres = 0.70
        iou_thres = 0.45
        max_det = 1000
        device = ''
        view_img = False
        save_txt = True
        save_conf = False
        save_crop = False
        nosave = False
        classes = None
        agnostic_nms = False
        augment = False
        visualize = False
        update = False
        project = 'runs/detect'  # 저장 경로
        name = 'exp' # 저장할 이름 파일 
        exist_ok = False
        line_thickness = 3
        hide_labels = False
        hide_conf = False
        half = False
        dnn = False
        vid_stride = 1


        run_yolo_detection(weights, source, data, imgsz, conf_thres, iou_thres, max_det, device, view_img, save_txt,
                                save_conf, save_crop, nosave, classes, agnostic_nms, augment, visualize, update, project,
                                name, exist_ok, line_thickness, hide_labels, hide_conf, half, dnn, vid_stride)









class DobotController:
    def __init__(self):
        detect = ObjectDetect()
        
        self.ip = "192.168.1.6"
        self.gripper_port = 1
        self.speed_value = 30

        self.center_values =[]
        # e
        self.center_value = detect.yolo_main() # detect.read_txt()
        
    
        self.center_values.append(self.center_value[0][0])
        
        self.center_values.append(self.center_value[0][1].item())
        self.center_values.append(self.center_value[0][2].item())
        
        # self.center_values.append(self.center_value[1][0])
        
        # self.center_values.append(self.center_value[1][1].item())
        # self.center_values.append(self.center_value[1][2].item())

        #print(self.center_value)
        self.center_value = self.center_values

        # 측정값은 -51.697025이지만 안전을 위해  0.5 추가 한다. 50.5    2층 3층도 동일하게 한다.
        # 1층
        self.z_1f = -50.5    
        # 2층
        self.z_2f = -35
        # 3층
        self.z_3f = -18.566692


        self.point_home = []

        self.what_dobot_do = 'default'



        
        self.x_1 = float(self.center_value[1]/640)  # 좌표값 계산전
        self.y_1 = float(self.center_value[2]/480)  # 좌표값 계산전
        self.z_1f = -51.5      # 1층 
        self.z_2f = -36 # 2층
        self.z_3f = -19.5 # 3층
        self.z_top = -10  # 살짝 들고 옮기기


        self.x = 171.020358+215.442479*self.y_1-11.0505039*self.x_1+5 # 계산한 좌표값
        self.y = -152.89923+16.342308*self.y_1+295.8404935*self.x_1+8 # 계산한 좌표값
        
        # 이 주석은 일단 치우치는 값 설정하려고 대강 만든것
        if self.y < 0:
            self.y = self.y + 3
        elif self.y > 0:
            self.y = self.y - 3

        # home -> default 위치
        self.point_home = [197.074762,8.888062,0,18.034557]

        # 객체 인식한 좌표의 중간값
        self.point_block_1f = [self.x, self.y, self.z_1f,18.034557]
        self.point_block_3f = [self.x, self.y, self.z_3f,18.034557]
        self.point_block_2f = [self.x,self.y, self.z_2f,18.034557]

        self.point_block_top = [self.x,self.y, self.z_top,18.034557]


        # 노란색 놓는 좌표 값 1 
        self.point_yellow1 = [227.285320,44.915774,self.z_1f,18.034557]
        self.point_yellow_2f1 = [227.285320,44.915774,self.z_2f,18.034557]
        self.point_yellow_3f1 = [227.285320,44.915774,self.z_3f,18.034557]

        self.point_yellow_top1 = [227.285320,44.915774,self.z_top,18.034557]
         # 노란색 놓는 좌표 값 2
        self.point_yellow2 = [280.120363,122.300497,self.z_1f,18.034557]
        self.point_yellow_2f2 = [280.120363,122.300497,self.z_2f,18.034557]
        self.point_yellow_3f2 = [280.120363,122.300497,self.z_3f,18.034557]

        self.point_yellow_top2 = [280.120363,122.300497,self.z_top,18.034557]

        # 초록색 놓는 좌표 값 1
        self.point_green1 = [309.103498,-28.172209,self.z_1f,18.034557]
        self.point_green_2f1 = [309.103498,-28.172209,self.z_2f,18.034557]
        self.point_green_3f1 = [309.103498,-28.172209,self.z_3f,18.034557]

        self.point_green_top1 = [309.103498,-28.172209,self.z_top,18.034557]
        # 초록색 놓는 좌표 값 2
        self.point_green2 = [305.613676,46.616053,self.z_1f,18.034557]
        self.point_green_2f2 = [305.613676,46.616053,self.z_2f,18.034557]
        self.point_green_3f2 = [305.613676,46.616053,self.z_3f,18.034557]

        self.point_green_top2 = [305.613676,46.616053,self.z_top,18.034557]

        # 빨간색 놓는 좌표 값 1
        self.point_red1 = [214.260258,-63.759681,self.z_1f,18.034557]
        self.point_red_2f1 = [214.260258,-63.759681,self.z_2f,18.034557]
        self.point_red_3f1 = [214.260258,-63.759681,self.z_3f,18.034557]

        self.point_red_top1 = [214.260258,-63.759681,self.z_top,18.034557]
        # 빨간색 놓는 좌표 값 2
        self.point_red2 = [275.626315,-104.114694,self.z_1f,18.034557]
        self.point_red_2f2 = [275.626315,-104.114694,self.z_2f,18.034557]
        self.point_red_3f2 = [275.626315,-104.114694,self.z_3f,18.034557]

        self.point_red_top2 = [275.626315,-104.114694,self.z_top,18.034557]










    # 로봇 파란불에서 초록불로 켜는 함수
    def dobot_turn_on(self):
        


        
        dashboard, move, feed = connect_robot(self.ip)
        dashboard.EnableRobot()
        robot_clear(dashboard)
        robot_speed(dashboard, self.speed_value)
        # get_feed()
        # wait_arrive()
        
    # dobot_acting
    def dobot_acting(self):
        

        self.do_composit = "screenshot"
       
        pass



    def dobot_act_home(self):
        run_point(move, self.point_home)

    # 처음 카메라가 블럭을 볼 수 있도록 위치 이동( 위치 : 홈 이라고 지정)
    def dobot_act1(self):
        
        # 탑이 초록색판 위에 위치하고 카메라 화면 기준 오른쪽에 위치할 때 
        if (self.center_value[0] == 'Green') & (self.center_value[2] > 240):
            self.what_dobot_do = 'green up'
            gripper_DO(dashboard, gripper_port, 1)
            run_point(move, self.point_block_top)
            sleep(0.5)
            run_point(move, self.point_block_3f)
            print("1")
            sleep(1)
            run_point(move, self.point_block_top)
            sleep(0.3)
            run_point(move, self.point_green_top)
            sleep(0.5)
            run_point(move, self.point_green)
            sleep(0.5)
            gripper_DO(dashboard, gripper_port, 0)
            sleep(0.5)
        elif (self.center_value[0] == 'Green') & (self.center_value[2] <= 240):
            self.what_dobot_do = 'green down'
            gripper_DO(dashboard, gripper_port, 1)
            run_point(move, self.point_block_top)
            sleep(0.5)
            run_point(move, self.point_block_3f)
            print("1")
            sleep(1)
            run_point(move, self.point_block_top)
            sleep(0.3)
            run_point(move, self.point_green_top)
            sleep(0.5)
            run_point(move, self.point_green)
            sleep(0.5)
            gripper_DO(dashboard, gripper_port, 0)
            sleep(0.5)



        if (self.center_value[0] == 'Yellow') & (self.center_value[2] > 240):
            self.what_dobot_do = 'yellow up'
            gripper_DO(dashboard, gripper_port, 1)
            run_point(move, self.point_block_top)
            sleep(0.5)
            run_point(move, self.point_block_3f)
            print("1")
            sleep(1)
            run_point(move, self.point_block_top)
            sleep(0.3)
            run_point(move, self.point_green_top)
            sleep(0.5)
            run_point(move, self.point_green)
            sleep(0.5)
            gripper_DO(dashboard, gripper_port, 0)
            sleep(0.5)
        elif (self.center_value[0] == 'Yellow') & (self.center_value[2] <= 240):
            self.what_dobot_do = 'yellow down'
            gripper_DO(dashboard, gripper_port, 1)
            run_point(move, self.point_block_top)
            sleep(0.5)
            run_point(move, self.point_block_3f)
            print("1")
            sleep(1)
            run_point(move, self.point_block_top)
            sleep(0.3)
            run_point(move, self.point_green_top)
            sleep(0.5)
            run_point(move, self.point_green)
            sleep(0.5)
            gripper_DO(dashboard, gripper_port, 0)


        if (self.center_value[0] == 'Red') & (self.center_value[2] > 240):
            self.what_dobot_do = 'Red up'
            gripper_DO(dashboard, gripper_port, 1)
            run_point(move, self.point_block_top)
            sleep(0.5)
            run_point(move, self.point_block_3f)
            print("1")
            sleep(1)
            run_point(move, self.point_block_top)
            sleep(0.3)
            run_point(move, self.point_green_top)
            sleep(0.5)
            run_point(move, self.point_green)
            sleep(0.5)
            gripper_DO(dashboard, gripper_port, 0)
            sleep(0.5)
        elif (self.center_value[0] == 'Red') & (self.center_value[2] <= 240):
            self.what_dobot_do = 'Red down'
            gripper_DO(dashboard, gripper_port, 1)
            run_point(move, self.point_block_top)
            sleep(0.5)
            run_point(move, self.point_block_3f)
            print("1")
            sleep(1)
            run_point(move, self.point_block_top)
            sleep(0.3)
            run_point(move, self.point_green_top)
            sleep(0.5)
            run_point(move, self.point_green)
            sleep(0.5)
            gripper_DO(dashboard, gripper_port, 0)
            sleep(0.5)


    def dobot_act2(self):


            # if (self.center_value[1][0] == "Yellow"):
            #     self.x = self.center_value[1][1]
            #     self.y = self.center_value[1][2]
            #     run_point(move, self.point_green_top)
            #     sleep(0.5)
            #     gripper_DO(dashboard, self.gripper_port, 1)
            #     sleep(0.3)
            #     run_point(move, self.point_block_top)
            #     sleep(0.5)
            #     run_point(move, self.point_block_2f)
            #     sleep(1)
            #     print("2")
            #     run_point(move, self.point_block_top)
            #     sleep(0.5)
            #     run_point(move, self.point_yellow_top)
            #     sleep(0.5)
            #     run_point(move, self.point_yellow)
            #     sleep(0.3)
            #     gripper_DO(dashboard, gripper_port, 0)
            #     sleep(0.5)
            #     run_point(move, self.point_yellow_top)
            #     sleep(0.5)
            #     gripper_DO(dashboard, gripper_port, 1)
            #     sleep(0.5)
            #     run_point(move, self.point_block_top)
            #     sleep(0.5)
            #     run_point(move, self.point_block_1f)
            #     sleep(1)
            #     run_point(move, self.point_block_top)
            #     sleep(0.5)
            #     run_point(move, self.point_red_top)
            #     sleep(0.5)
            #     run_point(move, self.point_red)
            #     sleep(0.5)
            #     gripper_DO(dashboard, gripper_port, 0)
            #     sleep(0.5)
            #     run_point(move, self.point_red_top)
            #     sleep(0.5)
            #     gripper_DO(dashboard, gripper_port, 1)
            #     sleep(0.5)
            #     run_point(move, self.point_yellow_top)
            #     sleep(0.5)
            #     run_point(move, self.point_yellow)
            #     sleep(1)
            #     run_point(move, self.point_yellow_top)
            #     sleep(0.5)
            #     run_point(move, self.point_red_top)
            #     sleep(0.3)
            #     run_point(move, self.point_red_2f)
            #     sleep(0.5)
            #     gripper_DO(dashboard, gripper_port, 0)
            #     sleep(0.5)
            #     run_point(move, self.point_red_top)
            #     sleep(0.3)
            #     run_point(move, self.point_green_top)
            #     sleep(0.3)
            #     gripper_DO(dashboard, gripper_port, 1)
            #     sleep(0.5)
            #     run_point(move, self.point_green)
            #     sleep(1)
            #     run_point(move, self.point_green_top)
            #     sleep(0.3)
            #     run_point(move, self.point_red_top)
            #     sleep(0.3)
            #     run_point(move, self.point_red_3f)
            #     sleep(0.3)
            #     gripper_DO(dashboard, gripper_port, 0)
            #     sleep(0.5)
            #     print("2")
            #     # "캡쳐 실행"
            # elif (self.center_value[1][0] == "Red"):
            #     self.x = self.center_value[1][1]
            #     self.y = self.center_value[1][2]
            #     run_point(move, self.point_green_top)
            #     sleep(0.5)
            #     gripper_DO(dashboard, gripper_port, 1)
            #     sleep(0.3)
            #     run_point(move, self.point_block_top)
            #     sleep(0.5)
            #     run_point(move, self.point_block_2f)
            #     sleep(1)
            #     print("3")
            #     run_point(move, self.point_block_top)
            #     sleep(0.5)
            #     run_point(move, self.point_red_top)
            #     sleep(0.5)
            #     run_point(move, self.point_red)
            #     sleep(0.3)
            #     gripper_DO(dashboard, gripper_port, 0)
            #     sleep(0.5)
            #     run_point(move, self.point_red_top)
            #     sleep(0.5)
            #     gripper_DO(dashboard, gripper_port, 1)
            #     sleep(0.5)
            #     run_point(move, self.point_block_top)
            #     sleep(0.5)
            #     run_point(move, self.point_block_1f)
            #     sleep(1)
            #     run_point(move, self.point_block_top)
            #     sleep(0.5)
            #     run_point(move, self.point_yellow_top)
            #     sleep(0.5)
            #     run_point(move, self.point_yellow)
            #     sleep(0.5)
            #     gripper_DO(dashboard, gripper_port, 0)
            #     sleep(0.5)
            #     run_point(move, self.point_yellow_top)
            #     sleep(0.5)
            #     gripper_DO(dashboard, gripper_port, 1)
            #     sleep(0.5)
            #     run_point(move, self.point_red_top)
            #     sleep(0.5)
            #     run_point(move, self.point_red)
            #     sleep(1)
            #     run_point(move, self.point_red_top)
            #     sleep(0.5)
            #     run_point(move, self.point_yellow_top)
            #     sleep(0.3)
            #     run_point(move, self.point_yellow_2f)
            #     sleep(0.5)
            #     gripper_DO(dashboard, gripper_port, 0)
            #     sleep(0.5)
            #     run_point(move, self.point_yellow_top)
            #     sleep(0.3)
            #     run_point(move, self.point_green_top)
            #     sleep(0.3)
            #     gripper_DO(dashboard, gripper_port, 1)
            #     sleep(0.5)
            #     run_point(move, self.point_green)
            #     sleep(1)
            #     run_point(move, self.point_green_top)
            #     sleep(0.3)
            #     run_point(move, self.point_yellow_top)
            #     sleep(0.3)
            #     run_point(move, self.point_yellow_3f)
            #     sleep(0.3)
            #     gripper_DO(dashboard, gripper_port, 0)
            #     sleep(0.5)
            #     print("3")
                
if __name__ == "__main__":

# 설정 시나리오
# 1. 로봇 가동
# 2. 로봇팔 home 위치로 이동(카메라로 객체 인식하기 위함)
# 3. 카메라로 맨 위 큐브 객체 인식하고 객체 중앙값 전달 
# 4. 로봇팔로 첫 큐브 옮기기
# 5. 카메라로 중앙 큐브 객체 인식하고 객체 중앙값 전달 2번
# 6. 로봇팔로 중앙 큐브 옮기기
# 7. 카메라로 맨 아래 큐브 객체 인식하고 객체 중앙값 전달 3번
# 8. 로봇팔로 마지막 큐브 옮기기
# 9. 중앙 큐브 마지막 큐브 자리로 옮기기
# 10. 맨 위에 있었던 큐브 마지막 큐브 바리로 옮기기

# opencv , yolo class
    detect = ObjectDetect() 
  #class
    dobot = DobotController()

# dobot start
    dobot.dobot_turn_on() ############################### 1번 


    dobot.dobot_act_home() ############################## 2번 
# # open cv screenshot(capture)
    detect.image_screenshot() ########################### 3-1 번

# # yolo detect object , values return txt data
    detect.yolo_main()  ################################# 3-2 번

# dobot move first cube
    dobot.dobot_act1()  ################################# 4 번

# # open cv screenshot(capture)
    detect.image_screenshot() ########################### 5-1 번

# # yolo detect object , values return txt data
    detect.yolo_main()  ################################# 5-2 번

# dobot move second block
    dobot.dobot_act2()  ################################# 6 번

# # open cv screenshot(capture)
    detect.image_screenshot() ########################### 7-1 번

# # yolo detect object , values return txt data
    detect.yolo_main()  ################################# 7-2 번

# dobot move last block
    dobot.dobot_act3()  ################################# 8 번

# dobot move second block reverse
    dobot.dobot_act4()  ################################# 9 번

# dobot move first cube reverse
    dobot.dobot_act5()  ################################# 10 번
