import cv2
from darkflow.net.build import TFNet
import numpy as np
import time


# def main(user_video_path):
# os.chdir('./flask_deep/darkflow_yolo')
# print('-------------------------------------')
# print(user_video_path)
# user_video_name = user_video_path.split('/')[-1].split('.')[0]
# print('-------------------------------------')

option = {
	'model': 'cfg/yolo.cfg',
	'load': 'bin/yolo.weights',
	'threshold': 0.3,
	'gpu': 0.6
}

tfnet = TFNet(option)

capture = cv2.VideoCapture('test_video.mp4')
colors = [tuple(255 * np.random.rand(3)) for i in range(5)]

while (capture.isOpened()):
	stime = time.time()
	ret, frame = capture.read()
	if ret:
		results = tfnet.return_predict(frame)
		for color, result in zip(colors, results):
			tl = (result['topleft']['x'], result['topleft']['y'])
			br = (result['bottomright']['x'], result['bottomright']['y'])
			label = result['label']
			frame = cv2.rectangle(frame, tl, br, color, 5)
			frame = cv2.putText(frame, label, tl, cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 2)
		cv2.imshow('frame', frame)
		print('FPS {:.1f}'.format(1 / (time.time() - stime)))
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
	else:
		capture.release()
		cv2.destroyAllWindows()
		break
