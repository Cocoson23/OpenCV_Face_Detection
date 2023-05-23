import cv2

from tools import read_images

# 创建人脸检测级联
face_cascade = cv2.CascadeClassifier(r"./cascades/haarcascade_frontalface_default.xml")

# 数据集根路径
path_to_training_images = './datasets/face'
# 训练时设置的人脸图像大小
training_image_size = (200, 200)
# 读取人名、训练图像以及标签
names, training_images, training_labels = read_images(path_to_training_images, training_image_size)

model = cv2.face.EigenFaceRecognizer_create()
model.read('./model.xml')

# 创建电脑自带摄像头对象
camera = cv2.VideoCapture(0)
key = 'nothing'
# 按'q'退出
while True:
    # 读取摄像头每一帧
    success, frame = camera.read()
    if success:
        # 对每一帧检测人脸
        faces = face_cascade.detectMultiScale(frame, 1.3, 5)
        # 检测结果若有人脸则将其裁剪出来放入模型进行检测
        # 若无人脸则跳过
        for (x, y, w, h) in faces:
            # 画人脸框
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 4)
            roi = frame[x:x+w, y:y+h]
            if roi.size == 0:
                continue
            # 调整检测人脸至训练时人脸图像大小
            roi = cv2.resize(roi, training_image_size)
            # 转换至灰色图像
            roi = cv2.cvtColor(roi, cv2.COLOR_RGBA2GRAY)
            # 检测结果
            label, confidence = model.predict(roi)
            # 在人脸框左上角标注人名及置信度
            text = '%s, confidence=%.2f' % (names[label], confidence)
            cv2.putText(frame, text, (x, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        cv2.imshow('Face Recognition', frame)
        key = cv2.waitKey(1)
        if key == ord('q'):
            break
        else:
            continue


camera.release()
cv2.destroyAllWindows()