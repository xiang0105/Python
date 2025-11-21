import cv2

# 透過官網的資料集去判別人臉，再透過製作長方形框住臉部達成找到臉的效果
def find_face(img):
    gray = cv2.cvtColor(img , cv2.COLOR_BGR2GRAY)

    face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    faces = face_cascade.detectMultiScale(gray)

    for(x , y , h , w ) in faces:
        cv2.rectangle(img , (x , y) , (x + w , y + h) , (255 , 0 , 0) , 2)
        
    mosaic_face(frame , faces)
        
    return img

# 將臉部單個像素放大15倍達成馬賽克的效果
def mosaic_face(frame , faces):
    
    for(x,y,w,h) in faces:
        mosaic = frame[y:y+h , x:x+w]
        # level = 15
        # mh = int(h // level)
        # mw = int(w // level)
        
        # mosaic = cv2.resize(mosaic, (mw,mh), interpolation=cv2.INTER_LINEAR)
        # mosaic = cv2.resize(mosaic, (w,h), interpolation=cv2.INTER_NEAREST)
        
        blurred = cv2.blur(mosaic, (51, 51))
        
        frame[y:y+h, x:x+w] = blurred
    
    return frame
        
# 開啟攝像機
cap = cv2.VideoCapture(0)

while True:
    
    # ret 是在說明成功與否(True/false) frame則是影像資料(視為單張圖片)
    ret , frame = cap.read()
    
    frame = find_face(frame)
    
    cv2.imshow('video' , frame)
    
    if cv2.waitKey(1) == ord('q'):
        break
    
cap.release()