import os
import cv2
import numpy as np
import tensorflow as tf
import sys
import time
from utils import label_map_util
from utils import visualization_utils as vis_util
import win32com.client

class AutoLabel(object):

	def __init__(self, args):
		super(AutoLabel, self).__init__()
		self.model_path = args.model_path
		self.save_path = args.save_path
		self.video_frame = args.video_frame
		self.video_name = args.video_name
		self.num_classes = args.num_classes
		self.video_group_folder = args.video_group_folder
		self.model_threshold = args.model_threshold
		self.resize_width = args.resize_width
		self.resize_height = args.resize_height

	def run(self):
		print("path:",self.model_path)
		print("path2:",self.save_path)
		print("video frame:",self.video_frame)
		#if output folder is not exist
		if self.FolderExist(self.save_path) == False:
			print("create "+str(self.save_path)+" folder")
			os.mkdir(self.save_path)
		self.ModelOpen()
		pass
	#open model trained from FasterRCNN 把FasterRCNN訓練好的模組掉出來用
	def ModelOpen(self):
		#設定路徑
		speaker = win32com.client.Dispatch("SAPI.SpVoice")
		MODEL_NAME = self.model_path
		#影片
		VIDEO_NAME = self.video_name
		print(VIDEO_NAME)
		#VIDEO_NAME = 'test1.mov'
		CWD_PATH = os.getcwd()
		# Path to frozen detection graph .pb file, which contains the model that is used
		# for object detection.
		PATH_TO_CKPT = os.path.join(CWD_PATH,MODEL_NAME,'frozen_inference_graph.pb')
		# Path to label map file
		PATH_TO_LABELS = os.path.join(CWD_PATH,'training','labelmap.pbtxt')
		# Path to video
		if(self.video_group_folder!=''):
			PATH_TO_VIDEO = os.path.join(CWD_PATH,self.video_group_folder,VIDEO_NAME)
		else:
			PATH_TO_VIDEO = os.path.join(CWD_PATH,VIDEO_NAME)
		# Number of classes the object detector can identify
		#設定有幾個東西要偵測
		NUM_CLASSES = self.num_classes
		#從training/labelmap.pbtx 抓資料
		label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
		categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
		category_index = label_map_util.create_category_index(categories)
		print("Loading Model...\n")
		# Load the Tensorflow model into memory.
		detection_graph = tf.Graph()
		print("Detecting start...\n")
		#Start counting times
		tStart = time.time()

		with detection_graph.as_default():
		    od_graph_def = tf.GraphDef()
		    with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
		        serialized_graph = fid.read()
		        od_graph_def.ParseFromString(serialized_graph)
		        tf.import_graph_def(od_graph_def, name='')

		    sess = tf.Session(graph=detection_graph)

		# Define input and output tensors (i.e. data) for the object detection classifier

		# Input tensor is the image
		image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')

		# Output tensors are the detection boxes, scores, and classes
		# Each box represents a part of the image where a particular object was detected
		detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')

		# Each score represents level of confidence for each of the objects.
		# The score is shown on the result image, together with the class label.
		detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
		detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')

		# Number of objects detected
		num_detections = detection_graph.get_tensor_by_name('num_detections:0')

		print(PATH_TO_VIDEO)
		# Open video file
		video = cv2.VideoCapture(PATH_TO_VIDEO)
		frameCount = 0 
		detectCount = 0 #拿來命名用的
		# 跑影片抓每一鎮圖片
		while(video.isOpened()):
			ret, frame = video.read()
			if ret == False:
				print("----video end----")
				break
			cv2.imshow("object detection", frame)
			cv2.waitKey(1)
			height, width = frame.shape[:2]
			frame_expanded = np.expand_dims(frame, axis=0)
		    
			if frameCount % self.video_frame ==0:
				frameCount = 0 
				frameCount += 1 
				pass
			else:
				frameCount += 1 
				continue
			if self.resize_height!=-1 and self.resize_width!=-1:
				frame = self.ResizeImg(frame,self.resize_width,self.resize_height)
				pass
			print("--[ Frame INFO]--")
			print("frame:",ret)
			print(frame.shape)
			print(width)
			print(height)
		    # Perform the actual detection by running the model with the image as input
			(boxes, scores, classes, num) = sess.run(
		        [detection_boxes, detection_scores, detection_classes, num_detections],
		        feed_dict={image_tensor: frame_expanded})
			boxesList = [] #之後拿來做成xml檔案用的
			classesList = [] #之後拿來做成xml檔案用的
			
			num = int(np.squeeze(num))
			# print("number of detect"+str(num))
		    #把>80%的資料抓出來START(預設80%)
			for i in range(0,num):
				if scores[0][i] >= self.model_threshold:
					print("find")
					print(height, width)
					y1, x1, y2, x2 = boxes[0][i]
    				#弄成int
					x1 = int(x1 * width)
					x2 = int(x2 * width)
					y1 = int(y1 * height)
					y2 = int(y2 * height)
					print("y1 x1 y2 x2:",y1, x1, y2, x2)
					sameFlag = 0
					for idx in range(0,len(boxesList)):
						#如果兩個框框有重疊就合併
						if self.ComputeIoU(boxesList[idx],[y1, x1, y2, x2]):
							boxesList[idx][0] = min( boxesList[idx][0], y1) #y1
							boxesList[idx][1] = min( boxesList[idx][1], x1) #x1 
							boxesList[idx][2] = max( boxesList[idx][2], y2) #y2
							boxesList[idx][3] = max( boxesList[idx][3], x2) #x2
							sameFlag = 1
							pass
					if sameFlag == 0:
						boxesList.append([y1, x1, y2, x2])
						classesList.append( category_index[classes[0][i]]['name'] )
			#把>80%的資料抓出來END
    		#存檔
			if len(boxesList)>0:
				print("-----[ "+str(detectCount)+" INFO]-----")
				print("boxes vlaue: ",boxesList)
				print("predicted_class : ",classesList) 

				jpgfileName = VIDEO_NAME.split('.')[0]+str(detectCount).zfill(5)+'.jpg'
				jpgfilepath = os.path.join('.',self.save_path,jpgfileName)
				print("save jpg file as "+jpgfileName)
				cv2.imwrite(jpgfilepath,frame)
				self.SaveXmlFile(jpgfileName, boxesList, classesList, width, height)
				detectCount += 1
				pass
			else:
				print("detect result: nothing here")
		# Clean up
		video.release()
		cv2.destroyAllWindows()	
	#convert xy value to xml file and save xml file 把偵測到的座標轉換成xml檔案然後存檔
	def SaveXmlFile(self, fileName: str, boxes: list, classes: list, width: int, height: int):
		#start
		content ='<annotation>\n'
		content+='    <folder>output</folder>\n'
		content+='    <filename>'+fileName+'</filename>\n'
		content+='    <size>\n'
		content+='        <width>'+str(width)+'</width>\n'
		content+='        <height>'+str(height)+'</height>\n'
		content+='        <depth>3</depth>\n'
		content+='    </size>\n'
		#boxes
		for i in range(0,len(boxes)):
			content+='    <object>\n'
			content+='        <name>'+str(classes[i])+'</name>\n'
			content+='        <pose>Unspecified</pose>\n'
			content+='        <truncated>0</truncated>\n'
			content+='        <difficult>0</difficult>\n'
			content+='        <bndbox>\n'
			content+='            <xmin>'+str(boxes[i][1])+'</xmin>\n'
			content+='            <ymin>'+str(boxes[i][0])+'</ymin>\n'
			content+='            <xmax>'+str(boxes[i][3])+'</xmax>\n'
			content+='            <ymax>'+str(boxes[i][2])+'</ymax>\n'
			content+='        </bndbox>\n'
			content+='    </object>\n'
			pass
		#end
		content+='</annotation>'
		#write file
		savefilename = str(fileName.split('.')[0])+'.xml'
		print(savefilename)
		xmlfilepath = os.path.join('.',self.save_path,savefilename)
		xmlfile = open(xmlfilepath,'w')
		xmlfile.write(content)
		xmlfile.close()
		pass
	#compute iou value 計算兩個矩形的iou值
	def ComputeIoU(self, rec1: list, rec2: list) -> float:
		S_rec1 = (rec1[2] - rec1[0]) * (rec1[3] - rec1[1])
		S_rec2 = (rec2[2] - rec2[0]) * (rec2[3] - rec2[1])
	
	    # computing the sum_area
		sum_area = S_rec1 + S_rec2
	
	    # find the each edge of intersect rectangle
		left_line = max(rec1[1], rec2[1])
		right_line = min(rec1[3], rec2[3])
		top_line = max(rec1[0], rec2[0])
		bottom_line = min(rec1[2], rec2[2])
	
	    # judge if there is an intersect
		if left_line >= right_line or top_line >= bottom_line:
			return 0.
		else:
			intersect = (right_line - left_line) * (bottom_line - top_line)
			return (intersect / (sum_area - intersect))*1.0
	def ResizeImg(self, img, width:int, height:int):
		print("resize img to "+str(width)+"*"+str(height))
		img = cv2.resize(img,(width,height),interpolation=cv2.INTER_CUBIC)
		return img
	#check folder exist 確認資料夾是否存在
	def FolderExist(self, folderName: str) -> bool:
		if os.path.isdir(folderName):
			return True
		else:
			return False
		pass

			