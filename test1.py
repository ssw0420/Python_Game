import numpy as np
import cv2
import mediapipe as mp
import matplotlib.pyplot as plt

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

# 웹캠, 영상 파일의 경우 이것을 사용하세요.:
cap = cv2.VideoCapture(0)
w = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
h = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
a = w//3 
hi = h//3

# fourcc = cv2.VideoWriter_fourcc(*'DIVX')
# out = cv2.VideoWriter('output.avi', fourcc, 30.0, (int(w), int(h)))

# hands = mp_hands.Hands(
#     model_complexity=0,
#     min_detection_confidence=0.5,
#     min_tracking_confidence=0.5)

with mp_hands.Hands(
    model_complexity=0,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:
  while cap.isOpened():
    success, image = cap.read()
    if not success:
      print("카메라를 찾을 수 없습니다.")
      # 동영상을 불러올 경우는 'continue' 대신 'break'를 사용합니다.
      continue

    # 필요에 따라 성능 향상을 위해 이미지 작성을 불가능함으로 기본 설정합니다.
    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image)

    if results.multi_hand_landmarks is not None:

            for res in results.multi_hand_landmarks:   
                for j, lm in enumerate(res.landmark):
                    if j==0:
                        # print((lm.x*w, lm.y*h, lm.z))
                        if 0 <= lm.x*w and a >= lm.x*w:
                            if hi * 2 <= lm.y*h:
                                print("a")
                                text ="A"
                                cv2.putText(image,"A" , (300, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
            (0, 0, 255), 1, cv2.LINE_AA)   
                        elif a <lm.x*w and 2 * a >= lm.x*w:
                            if hi * 2 <= lm.y*h:
                               print("b")
                               text ="B"
                               cv2.putText(image, "B", (300,100), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
            (0, 0, 255), 1, cv2.LINE_AA)   
                      
                        else:
                            if hi * 2 <= lm.y*h:
                                print("c")
                                text ="C"
                                cv2.putText(image, "C", (300, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
            (0, 0, 255), 1, cv2.LINE_AA)   
            # cv2.putText(image, text, (a, hi), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
            # (0, 0, 255), 1, cv2.LINE_AA)      
                        
                        


    # 이미지에 손 주석을 그립니다.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    if results.multi_hand_landmarks:
      for hand_landmarks in results.multi_hand_landmarks:
        mp_drawing.draw_landmarks(
            image,
            hand_landmarks,
            mp_hands.HAND_CONNECTIONS,
            mp_drawing_styles.get_default_hand_landmarks_style(),
            mp_drawing_styles.get_default_hand_connections_style())
    #보기 편하게 이미지를 좌우 반전합니다.
    
    cv2.imshow('MediaPipe Hands', cv2.flip(image, 1))
    out.write(image)
    if cv2.waitKey(5) & 0xFF == 27:
      break
cap.release()