#“Donated under Volatility Foundation, Inc. Individual Contributor Licensing Agreement”;
import argparse
import os
import cv2
import math
import shutil

def highlightFace(net, frame, conf_threshold=0.7):
    frameOpencvDnn=frame.copy()
    frameHeight=frameOpencvDnn.shape[0]
    frameWidth=frameOpencvDnn.shape[1]
    blob=cv2.dnn.blobFromImage(frameOpencvDnn, 1.0, (300, 300), [104, 117, 123], True, False)

    net.setInput(blob)
    detections=net.forward()
    faceBoxes=[]
    for i in range(detections.shape[2]):
        confidence=detections[0,0,i,2]
        if confidence>conf_threshold:
            x1=int(detections[0,0,i,3]*frameWidth)
            y1=int(detections[0,0,i,4]*frameHeight)
            x2=int(detections[0,0,i,5]*frameWidth)
            y2=int(detections[0,0,i,6]*frameHeight)
            faceBoxes.append([x1,y1,x2,y2])
            cv2.rectangle(frameOpencvDnn, (x1,y1), (x2,y2), (0,255,0), int(round(frameHeight/150)), 8)
    return frameOpencvDnn,faceBoxes
    
    
parser = argparse.ArgumentParser(description='Process some images')
parser.add_argument("input_directory", help="The input directory to scan")
parser.add_argument("output_directory", help="The output directory to move positive hits")
args = parser.parse_args()

input_directory = args.input_directory
output_directory = args.output_directory

#model paths
faceProto="opencv_face_detector.pbtxt"
faceModel="opencv_face_detector_uint8.pb"
ageProto="age_deploy.prototxt"
ageModel="age_net.caffemodel"
genderProto="gender_deploy.prototxt"
genderModel="gender_net.caffemodel"

#weights
MODEL_MEAN_VALUES=(78.4263377603, 87.7689143744, 114.895847746)

#Labels
ageList=['(0-2)', '(4-6)', '(8-12)', '(15-20)', '(25-32)', '(38-43)', '(48-53)', '(60-100)']
genderList=['Male','Female']

#Net's
faceNet=cv2.dnn.readNet(faceModel,faceProto)
ageNet=cv2.dnn.readNet(ageModel,ageProto)
genderNet=cv2.dnn.readNet(genderModel,genderProto)


try:
    for filename in os.listdir(input_directory):
        if filename.endswith(".jpg.dat") or filename.endswith(".png.dat") or filename.endswith(".jpg") or filename.endswith(".png"):
            filepath = os.path.join(input_directory, filename)

            try:
                video=cv2.VideoCapture(filepath)
                padding=20
                hasFrame,frame=video.read()
                #image = Image.open(filepath)
            except (IOError, OSError) as e:
                print(f"Error opening file '{filepath}': {e}")
                continue

            try:
                resultImg,faceBoxes=highlightFace(faceNet,frame)
                if not faceBoxes:
                    print("No face's detected")
                    
                ptcount = 0
                for faceBox in faceBoxes:
                    face=frame[max(0,faceBox[1]-padding):
                    min(faceBox[3]+padding,frame.shape[0]-1),max(0,faceBox[0]-padding)
                    :min(faceBox[2]+padding, frame.shape[1]-1)]

                    blob=cv2.dnn.blobFromImage(face, 1.0, (227,227), MODEL_MEAN_VALUES, swapRB=False)
                    genderNet.setInput(blob)
                    genderPreds=genderNet.forward()
                    gender=genderList[genderPreds[0].argmax()]
                    #print(f'Gender: {gender}')

                    ageNet.setInput(blob)
                    agePreds=ageNet.forward()
                    
                    #the magic
                    age = ageList[agePreds[0].argmax()]
                    first_3_labels = ageList[:3]  #(0-2),(4-6),(8-12)
                    if age in first_3_labels:
                        output_filename = os.path.join(output_directory, filename)
                        print(f'Age: {age[1:-1]} years')
                        ptcount += 1
                        #break
                    #else:
                        #print(f"Face is not pre teen, keep looking if in loop condition") 4
                if ptcount >= 1:
                    #print(f"Image contains pre teen {ptcount} faces")
                    #copy or move image
                    print(f" Image contains pre teen {ptcount} faces, Copied image to: {output_filename}")
                    shutil.copy(filepath, output_filename)
                        
            except Exception as e:
                print(f"Error processing file '{filepath}': {e}")

except Exception as e:
    print(f"Fatal error: {e}")

