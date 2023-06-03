from ctypes import *
import random
import os
import cv2
import time
from darknet import darknet
import argparse
from threading import Thread, enumerate
from queue import Queue

CONFIG_FILE='yolov7-darknet.cfg'
OBJ_FILE='obj.data'
WEIGHTS_FILE='yolov7-darknet_best.weights'
INPUT_FILE='test.mp4'

def parser():
    parser = argparse.ArgumentParser(description="YOLO Object Detection")
    parser.add_argument("--input", type=str, default=INPUT_FILE,
                        help="video source. If empty, uses webcam 0 stream")
    parser.add_argument("--out_filename", type=str, default="",
                        help="inference video name. Not saved if empty")
    parser.add_argument("--weights", default=WEIGHTS_FILE,
                        help="yolo weights path")
    parser.add_argument("--dont_show", action='store_true',
                        help="windown inference display. For headless systems")
    parser.add_argument("--ext_output", action='store_true',
                        help="display bbox coordinates of detected objects")
    parser.add_argument("--config_file", default=CONFIG_FILE,
                        help="path to config file")
    parser.add_argument("--data_file", default=OBJ_FILE,
                        help="path to data file")
    parser.add_argument("--thresh", type=float, default=.4,
                        help="remove detections with confidence below this value")
    return parser.parse_args()



def check_arguments_errors(args):
    assert 0 < args.thresh < 1, "Threshold should be a float between zero and one (non-inclusive)"
    if not os.path.exists(args.config_file):
        raise(ValueError("Invalid config path {}".format(os.path.abspath(args.config_file))))
    if not os.path.exists(args.weights):
        raise(ValueError("Invalid weight path {}".format(os.path.abspath(args.weights))))
    if not os.path.exists(args.data_file):
        raise(ValueError("Invalid data file path {}".format(os.path.abspath(args.data_file))))
    if str(args.input) == str and not os.path.exists(args.input):
        raise(ValueError("Invalid video path {}".format(os.path.abspath(args.input))))






frame_queue = Queue()
darknet_image_queue = Queue(maxsize=1)
detections_queue = Queue(maxsize=1)
fps_queue = Queue(maxsize=1)
args = parser()
check_arguments_errors(args)
network, class_names, class_colors = darknet.load_network(
        args.config_file,
        args.data_file,
        args.weights,
        batch_size=1
    )

darknet_width = darknet.network_width(network)
darknet_height = darknet.network_height(network)


def str2int(video_path):
    """
    argparse returns and string althout webcam uses int (0, 1 ...)
    Cast to int if needed
    """
    try:
        return int(video_path)
    except ValueError:
        return video_path



def set_saved_video(input_video, output_video, size):
    fourcc = cv2.VideoWriter_fourcc(*"MJPG")
    fps = int(input_video.get(cv2.CAP_PROP_FPS))
    video = cv2.VideoWriter(output_video, fourcc, fps, size)
    return video


def convert2relative(bbox):
    """
    YOLO format use relative coordinates for annotation
    """
    x, y, w, h  = bbox
    _height     = darknet_height
    _width      = darknet_width
    return x/_width, y/_height, w/_width, h/_height


def convert2original(image, bbox):
    x, y, w, h = convert2relative(bbox)

    image_h, image_w, __ = image.shape

    orig_x       = int(x * image_w)
    orig_y       = int(y * image_h)
    orig_width   = int(w * image_w)
    orig_height  = int(h * image_h)

    bbox_converted = (orig_x, orig_y, orig_width, orig_height)

    return bbox_converted


def convert4cropping(image, bbox):
    x, y, w, h = convert2relative(bbox)

    image_h, image_w, __ = image.shape

    orig_left    = int((x - w / 2.) * image_w)
    orig_right   = int((x + w / 2.) * image_w)
    orig_top     = int((y - h / 2.) * image_h)
    orig_bottom  = int((y + h / 2.) * image_h)

    if (orig_left < 0): orig_left = 0
    if (orig_right > image_w - 1): orig_right = image_w - 1
    if (orig_top < 0): orig_top = 0
    if (orig_bottom > image_h - 1): orig_bottom = image_h - 1

    bbox_cropping = (orig_left, orig_top, orig_right, orig_bottom)

    return bbox_cropping


def video_capture(frame_queue, darknet_image_queue):
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_resized = cv2.resize(frame_rgb, (darknet_width, darknet_height),
                                   interpolation=cv2.INTER_LINEAR)
        frame_queue.put(frame)
        img_for_detect = darknet.make_image(darknet_width, darknet_height, 3)
        darknet.copy_image_from_bytes(img_for_detect, frame_resized.tobytes())
        darknet_image_queue.put(img_for_detect)
    cap.release()


def inference(darknet_image_queue, detections_queue, fps_queue):
    while cap.isOpened():
        darknet_image = darknet_image_queue.get()
        #print(type(darknet_image))
        prev_time = time.time()
        detections = darknet.detect_image(network, class_names, darknet_image, thresh=args.thresh)
        detections_queue.put(detections)
        fps = int(1/(time.time() - prev_time))
        fps_queue.put(fps)
        #print(f"FPS: {fps}")
        darknet.print_detections(detections, args.ext_output)
        darknet.free_image(darknet_image)
    cap.release()


def drawing(frame_queue, detections_queue, fps_queue, saving_video_name):
    random.seed(3)  # deterministic bbox colors
    video = set_saved_video(cap, saving_video_name, (video_width, video_height))
    while cap.isOpened():
        frame = frame_queue.get()
        detections = detections_queue.get()
        fps = fps_queue.get()
        detections_adjusted = []
        if frame is not None:
            for label, confidence, bbox in detections:
                bbox_adjusted = convert2original(frame, bbox)
                detections_adjusted.append((str(label), confidence, bbox_adjusted))
            image = darknet.draw_boxes(detections_adjusted, frame, class_colors)
            #if not args.dont_show:
            #    cv2.imshow('Inference', image)
            if saving_video_name is not None:
                video.write(image)
            #if cv2.waitKey(fps) == 27:
            #    break
    cap.release()
    video.release()
    cv2.destroyAllWindows()

def detect_on_frame(frame):
    width = darknet.network_width(network)
    height = darknet.network_height(network)
    darknet_image = darknet.make_image(width, height, 3)


    image = frame
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image_resized = cv2.resize(image_rgb, (width, height),
                               interpolation=cv2.INTER_LINEAR)

    darknet.copy_image_from_bytes(darknet_image, image_resized.tobytes())
    detections = darknet.detect_image(network, class_names, darknet_image, thresh=.25)
    darknet.free_image(darknet_image)
    image = darknet.draw_boxes(detections, image_resized, class_colors)
    return cv2.cvtColor(image, cv2.COLOR_BGR2RGB), detections
    #frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    #frame_resized = cv2.resize(frame_rgb, (darknet_width, darknet_height),
    #                           interpolation=cv2.INTER_LINEAR)
    #img_for_detect = darknet.make_image(darknet_width, darknet_height, 3)
    #darknet.copy_image_from_bytes(img_for_detect, frame_resized.tobytes())
    #detections = darknet.detect_image(network, class_names, img_for_detect, thresh=0.25)
    #print('detections: ', detections)
    #detections_adjusted = []
    #if img_for_detect is not None:
    #    for label, confidence, bbox in detections:
    #        bbox_adjusted = convert2original(img_for_detect, bbox)
    #        detections_adjusted.append((str(label), confidence, bbox_adjusted))
    #    new_frame = darknet.draw_boxes(detections_adjusted, frame, class_colors)
    #    return new_frame
    
    
def detect_on_video(saving_video_name:str = None):
    global cap,args
    global darknet_width,darknet_height
    global video_width,video_height
    global network, class_names, class_colors
    input_path = str2int(args.input)
    cap = cv2.VideoCapture(input_path)
    video_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    video_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    Thread(target=video_capture, args=(frame_queue, darknet_image_queue)).start()
    Thread(target=inference, args=(darknet_image_queue, detections_queue, fps_queue)).start()
    Thread(target=drawing, args=(frame_queue, detections_queue, fps_queue, saving_video_name)).start()


def video_prediction(input_video:str, out_video:str):
    cap = cv2.VideoCapture(input_video)
    width  = cap.get(cv2.CAP_PROP_FRAME_WIDTH)   
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    fps = cap.get(cv2.CAP_PROP_FPS)
    print(width, height, fps)
    #fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    out = cv2.VideoWriter(out_video,  cv2.VideoWriter_fourcc(*'MJPG'), float(fps),(int(width), int(height)), True)
    print(out_video)
    while(True):
      ret, frame = cap.read()
    
      if ret == True: 
        new_frame, detections = detect_on_frame(frame)
        # Write the frame into the file 'output.avi
        new_frame = cv2.resize(new_frame, (frame.shape[1], frame.shape[0]))
        out.write(new_frame)
    
        # Press Q on keyboard to stop recording
        if cv2.waitKey(1) & 0xFF == ord('q'):
          break
      
      # Break the loop
      else:
        break 
    
    # When everything done, release the video capture and video write objects
    cap.release()
    out.release()
    
    # Closes all the frames