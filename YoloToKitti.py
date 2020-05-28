# ---------------------------------------------------------------------
# Converts Yolo output .txt detections to Kitti (label, x1, y1, x2, y2)
#
# (C) 2020 Carlos Caetano, Belo Horizonte, Brazil
# Released under GNU Public License (GPL)
# ---------------------------------------------------------------------


import os
import glob
import argparse
import cv2 as cv
import multiprocessing as mp
from typing import List


def get_arguments(parser: argparse.ArgumentParser) -> argparse.Namespace:
	"""Get the arguments passed by command line.

	Args:
	    parser (argparse.ArgumentParser): the command line arguments

	Returns:
	    args (argparse): parsed command lines by argparse
	"""
	parser.add_argument(
		'-d',
		'--detections',
		type = str,
		required = True,
		help = 'directory containing the .txt Yolo detections')

	parser.add_argument(
		'-i',
		'--images',
		type=str,
		required=True,
		help='directory containing the corresponding .jpg images')

	parser.add_argument(
		'-o',
		'--output',
		type = str,
		help = 'directory to save the converted files',
		default = 'files_converted')

	args = parser.parse_args()
	print(args)
	return args


def get_label(label_num: int) -> str:
	"""Get the label name.

	Args:
	    label_num (int): the command lines

	Returns:
	    label_name (str): the label name (e.g., 0: 'person')
	"""
	labels_to_names = {0: 'person', 1: 'bicycle', 2: 'car', 3: 'motorcycle', 4: 'airplane', 5: 'bus', 6: 'train',
					   7: 'truck', 8: 'boat', 9: 'traffic light', 10: 'fire hydrant', 11: 'stop sign',
					   12: 'parking meter', 13: 'bench', 14: 'bird', 15: 'cat', 16: 'dog', 17: 'horse', 18: 'sheep',
					   19: 'cow', 20: 'elephant', 21: 'bear', 22: 'zebra', 23: 'giraffe', 24: 'backpack',
					   25: 'umbrella', 26: 'handbag', 27: 'tie', 28: 'suitcase', 29: 'frisbee', 30: 'skis',
					   31: 'snowboard', 32: 'sports ball', 33: 'kite', 34: 'baseball bat', 35: 'baseball glove',
					   36: 'skateboard', 37: 'surfboard', 38: 'tennis racket', 39: 'bottle', 40: 'wine glass',
					   41: 'cup', 42: 'fork', 43: 'knife', 44: 'spoon', 45: 'bowl', 46: 'banana', 47: 'apple',
					   48: 'sandwich', 49: 'orange', 50: 'broccoli', 51: 'carrot', 52: 'hot dog', 53: 'pizza',
					   54: 'donut', 55: 'cake', 56: 'chair', 57: 'couch', 58: 'potted plant', 59: 'bed',
					   60: 'dining table', 61: 'toilet', 62: 'tv', 63: 'laptop', 64: 'mouse', 65: 'remote',
					   66: 'keyboard', 67: 'cell phone', 68: 'microwave', 69: 'oven', 70: 'toaster', 71: 'sink',
					   72: 'refrigerator', 73: 'book', 74: 'clock', 75: 'vase', 76: 'scissors', 77: 'teddy bear',
					   78: 'hair drier', 79: 'toothbrush'}

	label_name = labels_to_names[label_num]
	return label_name


def convert_to_kitti(txt_file: str, img_file: str) -> List[str]:
	"""Converts from Yolo to Kitti

	Converts each line of the file from Yolo format to
	Kitti bounding box format (label, x1, y1, x2, y2).

	Args:
	    txt_file (str): file path to convert
	    img_file (str): corresponding img file path

	Returns:
	    converted_lines (List[str]): a list with lines converted to Kitti format
	"""
	fr = open(txt_file, 'r')
	converted_lines = []

	img = cv.imread(img_file)
	img_height, img_width, img_chanels = img.shape

	for line in fr:
		line_split = line.split(' ')
		label = get_label(int(line_split[0]))
		coords = list(map(float, list(map(float, line_split[1:5]))))

		x1 = float(img_width) * (2.0 * float(coords[0]) - float(coords[2])) / 2.0
		y1 = float(img_height) * (2.0 * float(coords[1]) - float(coords[3])) / 2.0
		x2 = float(img_width) * (2.0 * float(coords[0]) + float(coords[2])) / 2.0
		y2 = float(img_height) * (2.0 * float(coords[1]) + float(coords[3])) / 2.0

		line_to_write = '{} {} {} {} {}\n'.format(label, int(x1), int(y1), int(x2), int(y2))
		converted_lines.append(line_to_write)
	fr.close()

	return converted_lines


def check_path(path_to_check: str) -> bool:
	"""Check if path exists

	Check if path exists. If not, it creates the
	path. Raises an OSError exception if it is
	not possible to create

	Args:
	    path_to_check (str): path to check/create

	Returns:
	    ret (bool): returns True if path is ok
	"""
	ret = True
	try:
		if not os.path.exists(path_to_check):
			print('Creating path: {}'.format(path_to_check))
			os.makedirs(path_to_check)
			print('Path {} OK'.format(path_to_check ))

	except OSError:
		print('Error: Creating directory {}'.format( path_to_check))
		ret = False

	return ret


def worker(args: tuple)-> bool:
	"""Worker for parallel processing

	The worker function is for parallel processing
	of the many .txt files for conversion.

	Args:
	    args (tuple): a tuple composed by the file path to convert,
	    the corresponding image fpath and the output path to save
	    the converted file.

	Returns:
	     ret (bool): returns True if file successfully converted
	"""
	file_path = args[0]
	img_path = args[1]
	output_path = args[2]
	ret = True

	try:
		converted_lines = convert_to_kitti(file_path, img_path)
		file_name = os.path.basename(file_path)
		fw = open(os.path.join(output_path, file_name), 'w')
		fw.writelines(converted_lines)
		fw.close()
		print('{} converted...'.format(file_name))

	except Exception as exception:
		extraction = 'ERROR: {}'.format(str(exception))
		print(extraction)
		ret = False

	return ret


def main(parser: argparse.ArgumentParser) -> None:
	"""The main function for Yolo to Kitti conversion.

	Args:
	    parser (argparse.ArgumentParser): the command line arguments

	Returns:
	    no value
	"""
	args = get_arguments(parser)

	if not check_path(args.output):
		return

	files_to_convert =  glob.glob(os.path.join(args.detections, '*.txt'))
	files_to_convert.sort()
	img_files = glob.glob(os.path.join(args.images, '*.jpg'))
	img_files.sort()

	pool = mp.Pool(mp.cpu_count())
	out_list = pool.map(worker, ((txt_file, img_file, args.output) for txt_file, img_file in zip(files_to_convert, img_files)))
	pool.close()
	pool.join()
	pool.terminate()
	print('{} files converted!'.format(out_list.count(True)))


if __name__ == '__main__':
	main(argparse.ArgumentParser())