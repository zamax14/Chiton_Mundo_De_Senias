import tensorflow as tf
from object_detection.utils import config_util
import os
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as viz_utils
from object_detection.builders import model_builder
import cv2 
import numpy as np
import time

WORKSPACE_PATH = 'Tensorflow\\workspace'
ANNOTATION_PATH = WORKSPACE_PATH+'\\annotations'
MODEL_PATH = WORKSPACE_PATH+'\\models'
CONFIG_PATH = MODEL_PATH+'\\my_ssd_mobnet\\pipeline.config'
CHECKPOINT_PATH = MODEL_PATH+'\\my_ssd_mobnet\\'

def config_init():
    # Load pipeline config and build a detection model
    configs = config_util.get_configs_from_pipeline_file(CONFIG_PATH)
    detection_model = model_builder.build(model_config=configs['model'], is_training=False)

    # Restore checkpoint
    ckpt = tf.compat.v2.train.Checkpoint(model=detection_model)
    ckpt.restore(os.path.join(CHECKPOINT_PATH, 'ckpt-31')).expect_partial()

    return detection_model


@tf.function
def detect_fn(image, detection_model):
    image, shapes = detection_model.preprocess(image)
    prediction_dict = detection_model.predict(image, shapes)
    detections = detection_model.postprocess(prediction_dict, shapes)
    return detections


def start_detection():
    detection_model = config_init()
    category_index = label_map_util.create_category_index_from_labelmap(ANNOTATION_PATH+'/label_map.pbtxt')

    # Setup capture
    cap = cv2.VideoCapture(0)

    print("get ready")
    time.sleep(1)
    print("3")
    time.sleep(1)
    print("2")
    time.sleep(1)
    print("1")
    time.sleep(1)
    ret, frame = cap.read()
    print("Done!")
    cap.release()
    image_np = frame

    input_tensor = tf.convert_to_tensor(np.expand_dims(image_np, axis=0), dtype=tf.float32)
    detections = detect_fn(input_tensor, detection_model)

    num_detections = int(detections.pop('num_detections'))
    detections = {key: value[0, :num_detections].numpy()
                    for key, value in detections.items()}
    detections['num_detections'] = num_detections

    # detection_classes should be ints.
    detections['detection_classes'] = detections['detection_classes'].astype(np.int64)

    label_id_offset = 1
    image_np_with_detections = image_np.copy()

    image, res = viz_utils.visualize_boxes_and_labels_on_image_array(
                image_np_with_detections,
                detections['detection_boxes'],
                detections['detection_classes']+label_id_offset,
                detections['detection_scores'],
                category_index,
                use_normalized_coordinates=True,
                max_boxes_to_draw=5,
                min_score_thresh=.5,
                agnostic_mode=False)

    return res

start_detection()