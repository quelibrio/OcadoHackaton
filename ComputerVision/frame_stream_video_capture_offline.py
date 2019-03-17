# Demo of homeheed.com


import time
import traceback
from threading import Thread
import mxnet as mx
import cv2 as cv
import numpy as np
import ctypes


# Min matches to look for homography
#MIN_MATCH_COUNT = 10
from keras.applications.resnet50 import ResNet50
from keras.preprocessing import image
from keras.applications.resnet50 import preprocess_input, decode_predictions
import numpy as np
from keras.models import load_model
from keras.models import model_from_json
import tensorflow as tf


from gluoncv import model_zoo, data, utils
from matplotlib import pyplot as plt

import pyttsx3
engine = pyttsx3.init()


######################################################################
# Load a pretrained model
# -------------------------
#
# Let's get an YOLOv3 model trained with on Pascal VOC
# dataset with Darknet53 as the base model. By specifying
# ``pretrained=True``, it will automatically download the model from the model
# zoo if necessary. For more pretrained models, please refer to
# :doc:`../../model_zoo/index`.

net = model_zoo.get_model('yolo3_darknet53_coco', pretrained=True)

#model = ResNet50(weights='input/best.hdf5', include_top=False)
#json_file = open('input/model.json', 'r')
#loaded_model_json = json_file.read()
#json_file.close()
#model = tf.keras.models.load_model('input/model.hdf5')

#model.summary()
print("")
# load weights into new model
#model.load_weights("input/model.hdf5")
print("Loaded model from disk")

def main():
  #img1 = cv.imread('banana.jpg')
  #img1 = cv.resize(img1, (0,0), fx=0.5, fy=0.5)
  #orb = cv.ORB_create(
  #  nfeatures=5000, edgeThreshold=20, patchSize=20, scaleFactor=1.3, nlevels=20)
  #kp1, des1 = orb.detectAndCompute(img1, None)

  frame_count = 0
  
  cap = cv.VideoCapture(0)
  while(True):
      # Capture frame-by-frame
      ret, frame = cap.read()
      frame_count += 1
      try:
        if frame_count % 30 == 0:
            print(ret)
            #frame = cv.resize(frame, (224,224))
            get_match_image(frame)
        # Display the resulting frame
        #cv.imshow('frame', img3)
      except:
        traceback.print_exc()
        time.sleep(0.5)
      if cv.waitKey(1) & 0xFF == ord('q'):
          break

  # When everything done, release the capture
  cap.release()
  cv.destroyAllWindows()

def get_match_image(img):
    #img_path = 'banana.jpg'
    #img = image.load_img(img_path, target_size=(224, 224))
    #x = image.img_to_array(img)
    #x = np.expand_dims(x, axis=0)
    #x = preprocess_input(x)
    #print(x.shape)
    # preds = model.predict(x)
    # decode the results into a list of tuples (class, description, probability)
    # (one such list for each sample in the batch)
    #print(preds)
    #print('Predicted:', decode_predictions(preds, top=3)[0])
    #im_fname = utils.download('https://raw.githubusercontent.com/zhreshold/' +
    #                      'mxnet-ssd/master/data/demo/dog.jpg',
    #                     path='dog.jpg')
    #x, img = data.transforms.presets.yolo.load_test(img, short=512)
    #print('Shape of pre-processed image:', x.shape)

    ######################################################################
    # Inference and displaym
    # ---------------------
    #
    # The forward function will return all detected bounding boxes, and the
    # corresponding predicted class IDs and confidence scores. Their shapes are
    # `(batch_size, num_bboxes, 1)`, `(batch_size, num_bboxes, 1)`, and
    # `(batch_size, num_bboxes, 4)`, respectively.
    #
    # We can use :py:func:`gluoncv.utils.viz.plot_bbox` to visualize the
    # results. We slice the results for the first image and feed them into `plot_bbox`:
    #scale = 0.00392
    #blob = cv.dnn.blobFromImage(img, scale, (416,416), (0,0,0), True, crop=False)
    #x, img = data.transforms.presets.yolo.transform_test(img)
    #img_array = np.asarray(img)
    # set input blob for the network
    #net.setInput(blob)
    from PIL import Image
    im = Image.fromarray(img)
    im.save("frame.jpeg")
    x, img1 = data.transforms.presets.yolo.load_test("frame.jpeg", short=512)

    class_IDs, scores, bounding_boxs = net(x)

    lables, scores = plot_bbox1(img, bounding_boxs[0], scores[0],
                           class_IDs[0], class_names=net.classes)
    print(lables)
    print(scores)
    for label in lables:
        engine.say(label)
        engine.runAndWait()
        #engine.say(scores[0])
        #engine.runAndWait()
    
    plt.show()
    print(net.classes)
    #print(scores[0])
    #print(class_IDs[0])
    #time.sleep(100)
    #plt.close()
    #cls_prob = mx.nd.softmax(scores, axis=-1)
    #for k, v in zip([net.classes], cls_prob):
    #  print(k, v)
   # print(net.classes[class_IDs[0]])

def plot_bbox1(img, bboxes, scores=None, labels=None, thresh=0.5,
              class_names=None, colors=None, ax=None,
              reverse_rgb=False, absolute_coordinates=True):
    all_names = []
    probs = []
    from matplotlib import pyplot as plt

    if labels is not None and not len(bboxes) == len(labels):
        raise ValueError('The length of labels and bboxes mismatch, {} vs {}'
                         .format(len(labels), len(bboxes)))
    if scores is not None and not len(bboxes) == len(scores):
        raise ValueError('The length of scores and bboxes mismatch, {} vs {}'
                         .format(len(scores), len(bboxes)))

    #ax = plot_image(img, ax=ax, reverse_rgb=reverse_rgb)

    if len(bboxes) < 1:
        return ax

    if isinstance(bboxes, mx.nd.NDArray):
        bboxes = bboxes.asnumpy()
    if isinstance(labels, mx.nd.NDArray):
        labels = labels.asnumpy()
    if isinstance(scores, mx.nd.NDArray):
        scores = scores.asnumpy()

    if not absolute_coordinates:
        # convert to absolute coordinates using image shape
        height = img.shape[0]
        width = img.shape[1]
        bboxes[:, (0, 2)] *= width
        bboxes[:, (1, 3)] *= height

    # use random colors if None is provided
    if colors is None:
        colors = dict()
    for i, bbox in enumerate(bboxes):
        if scores is not None and scores.flat[i] < thresh:
            continue
        if labels is not None and labels.flat[i] < 0:
            continue
        cls_id = int(labels.flat[i]) if labels is not None else -1
        if cls_id not in colors:
            if class_names is not None:
                colors[cls_id] = plt.get_cmap('hsv')(cls_id / len(class_names))
            else:
                colors[cls_id] = (random.random(), random.random(), random.random())
        xmin, ymin, xmax, ymax = [int(x) for x in bbox]
        rect = plt.Rectangle((xmin, ymin), xmax - xmin,
                             ymax - ymin, fill=False,
                             edgecolor=colors[cls_id],
                             linewidth=3.5)
        #ax.add_patch(rect)
        if class_names is not None and cls_id < len(class_names):
            class_name = class_names[cls_id]
        else:
            class_name = str(cls_id) if cls_id >= 0 else ''
        score = '{:.3f}'.format(scores.flat[i]) if scores is not None else ''
        # if class_name or score:
        #     ax.text(xmin, ymin - 2,
        #             '{:s} {:s}'.format(class_name, score),
        #             bbox=dict(facecolor=colors[cls_id], alpha=0.5),
        #             fontsize=12, color='white')
        all_names.append(class_name)
        probs.append(score)
    return all_names, probs

if __name__ == "__main__":
  main()
