"""
Street object detection with YOLOv5.

Loads a pretrained YOLOv5 model, runs it on a street photo, draws a box and
label around every detected object, prints what was found, and saves the
annotated image as output_result.png.

Built by Prodipta Acharjee for Introduction to Open Source Software.
"""

import torch
import cv2

# settings I changed from the class demo
INPUT_FILE = "input_image.jpg"
OUTPUT_FILE = "output_result.png"
CONF_THRESHOLD = 0.40          # demo used 0.50, I lowered it to catch more objects
BOX_COLOR = (0, 200, 0)        # demo drew red boxes, I switched to green
BOX_THICKNESS = 2


def load_model():
    # pull yolov5s (small, fast) with its pretrained COCO weights
    model = torch.hub.load("ultralytics/yolov5", "yolov5s", pretrained=True, trust_repo=True)
    model.conf = CONF_THRESHOLD
    print("Model loaded. Confidence threshold set to", CONF_THRESHOLD)
    return model


def detect(model, image):
    # YOLO returns one row per object as x1, y1, x2, y2, confidence, class id
    results = model(image)
    detections = results.xyxy[0].cpu().numpy()
    return detections, model.names


def annotate(image, detections, names):
    output = image.copy()

    # collect names so I can print a summary after drawing
    found = []
    for x1, y1, x2, y2, conf, class_id in detections:
        label = names[int(class_id)]
        found.append(label)

        top_left = (int(x1), int(y1))
        bottom_right = (int(x2), int(y2))
        cv2.rectangle(output, top_left, bottom_right, BOX_COLOR, BOX_THICKNESS)
        cv2.putText(
            output,
            f"{label} {conf:.2f}",
            (int(x1), int(y1) - 6),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            BOX_COLOR,
            1,
        )
    return output, found


def main():
    image = cv2.imread(INPUT_FILE)
    if image is None:
        print("Could not read", INPUT_FILE)
        return

    model = load_model()
    detections, names = detect(model, image)
    output, found = annotate(image, detections, names)

    # print the result the assignment asks for
    print("\nTotal objects detected:", len(found))
    print("Detected objects:")
    for x1, y1, x2, y2, conf, class_id in detections:
        print(f"  {names[int(class_id)]}: {conf:.2f}")

    cv2.imwrite(OUTPUT_FILE, output)
    print("\nSaved annotated image as", OUTPUT_FILE)


if __name__ == "__main__":
    main()
