import time
import os
import picamera

def takePicture():
	with picamera.PiCamera() as camera:
		camera.resolution = (640, 480)
		camera.vflip = True
		time.sleep(0.1)
		camera.capture('foo.jpg')

# sshfs phi@192.168.1.22:/www/oliver_tv/stream mount
while True:
	print('picture')
	takePicture()
	os.system('mv foo.jpg ./static/image_stream.jpg')

