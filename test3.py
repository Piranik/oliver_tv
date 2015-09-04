import time
import os
import picamera

def takePicture():
	with picamera.PiCamera() as camera:
		camera.resolution = (640, 480)
		camera.vflip = True
		time.sleep(5)
		camera.capture('foo.jpg')

# sshfs phi@192.168.1.22:/www/oliver_tv/stream mount
while True:
	print('picture')
	takePicture()
	os.system('mv foo.jpg ./static/image_stream.jpg')
	#os.system('raspistill -w 640 -h 480 -q 50 -o ./mount/image_stream.jpg -rot 180 -th 0:0:0')
	#os.system('rsync -avr ./stream/image_stream.jpg phi@192.168.1.22:/www/oliver_tv/stream/')

