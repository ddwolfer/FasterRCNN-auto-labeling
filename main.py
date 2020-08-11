import argparse
import os
from videoLabel import AutoLabel

parser = argparse.ArgumentParser(description='')

parser.add_argument('--model_path', dest='model_path', default='inference_graph', help='Model you trained from fasterRCNN')
parser.add_argument('--save_path', dest='save_path', default='output', help='the folder of label result(output with .jpg + .xml file) ')
parser.add_argument('--video_frame', dest='video_frame', type=int, default=30, help='the video fps you want to labeling')
parser.add_argument('--video_name', dest='video_name', default='', help='video filename')
parser.add_argument('--video_group_folder', dest='video_group_folder', default='', help='if you wnat to label in muti video, type the video folder, and be sure they are all video')
parser.add_argument('--num_classes', dest='num_classes', type=int, default=1, help='Number of classes the object detector can identify')
parser.add_argument('--model_threshold', dest='model_threshold', type=float, default=0.8, help='set detect threshold')

args = parser.parse_args()

#main function
def main():
	if args.video_group_folder !='':
		videoList = os.listdir(args.video_group_folder)
		for videoName in videoList:
			args.video_name = videoName
			print(args)
			start = AutoLabel(args)
			start.run()
		pass
	elif args.video_name !='':
		start = AutoLabel(args)
		start.run()
		pass
	else:
		print("use --video_name to set video name")

if __name__ == '__main__':
	main()