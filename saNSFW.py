#“Donated under Volatility Foundation, Inc. Individual Contributor Licensing Agreement”;
import argparse
import os
import numpy as np
from PIL import Image
import cv2
import shutil

parser = argparse.ArgumentParser(description='Process some images')
parser.add_argument("input_directory", help="The input directory to scan")
parser.add_argument("output_directory", help="The output directory to move positive hits")
args = parser.parse_args()

input_directory = args.input_directory
output_directory = args.output_directory

# Caffe model paths
model_path = "deploy.prototxt"
weights_path = "resnet_50_1by2_nsfw.caffemodel"

net = cv2.dnn.readNetFromCaffe(model_path, weights_path)

try:
    for filename in os.listdir(input_directory):
        if filename.endswith(".jpg.dat") or filename.endswith(".png.dat") or filename.endswith(".jpg") or filename.endswith(".png"):
            filepath = os.path.join(input_directory, filename)

            try:
                image = Image.open(filepath)
            except (IOError, OSError) as e:
                print(f"Error opening file '{filepath}': {e}")
                continue

            try:
                # Image pre-processing based on your Caffe model requirements
                image = image.resize((224, 224))
                image = np.asarray(image)
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                image = image.transpose((2, 0, 1))  # Adapt to Caffe BGR image format
                image = image.astype(np.float32)
                image /= 255.0  # Normalize between 0 and 1

                # Set input and perform inference
                net.setInput(np.expand_dims(image, axis=0))
                prediction = net.forward()

                # Interpret prediction based on your model's output format
                confidence = prediction[0][1]

                if confidence > 0.50:
                    output_filename = os.path.join(output_directory, filename)
                    print(f"Image is NSFW with confidence: {confidence:.2f}. Copied to: {output_filename}")
                    shutil.copy(filepath, output_filename)
                else:
                    print(f"Image is not NSFW with confidence: {confidence:.2f}") 
            except Exception as e:
                print(f"Error processing file '{filepath}': {e}")

except Exception as e:
    print(f"Fatal error: {e}")

