# -*- coding: utf-8 -*-
"""
Created on Wed Jan  6 23:33:21 2021

@author: OZLEM
"""
import cv2                        #Görüntü okuma icin opencv kütüphanesi import islemi
import numpy as np                #dizi islemleri icin numpy kütüphanesi import islemi



cap = cv2.VideoCapture("drones.mp4")    ##video okundu

while True:         ##Video frameler seklinde okundu
    ret, frame = cap.read()    ##


    frame_width = frame.shape[1]      ##framelerin genislik degerleri
    frame_height = frame.shape[0]     ##framelerin yükseklik degerleri

    frame_blob = cv2.dnn.blobFromImage(frame , 1/255, (416,416), swapRB= True, crop=False)
      ##Görüntü modele verilebilmesi icin 4 boyutlu tensör formatına dönüstürüldü

    labels = ["drone"]

    colors = ["0,255,255"]   ##nesnelerin renklendirilmesi
    colors = [np.array(color.split(",")).astype("int") for color in colors] ##string alınan color degerleri int e cevrildi
    colors = np.array(colors)    ##colors list i matrise cevrildi
    colors = np.tile(colors,(18,1))  ##matris buyutuldu


    model = cv2.dnn.readNetFromDarknet("yolov4.cfg" , "yolov4.weights")
    ##model icine .cfg ve .weights dosyalari alindi
    layers = model.getLayerNames()   ##model icindeki katmanlar okundu
    output_layer = [layers[layer[0]-1] for layer in model.getUnconnectedOutLayers()]  ##cikti katmanlarina erisildi
    model.setInput(frame_blob)   ##blob formatimndaki frame modele verildi

    detection_layers = model.forward(output_layer)  ##cikti katmanlari tespit edildi



    ############## NON-MAXIMUM SUPPRESSION - OPERATION 1 ###################
    
    ids_list = []      
    boxes_list = []
    confidences_list = []
    
    ############################ END OF OPERATION 1 ########################



    for detection_layer in detection_layers:
        for object_detection in detection_layer:
            
            scores = object_detection[5:]          
            predicted_id = np.argmax(scores)    ##güven skoru en yüksek olan objelerin index i tutuldu
            confidence = scores[predicted_id]    ##güven skoru en yüksek olan objenin güven skoru belirlendi       
            
            if confidence > 0.20:      ##güven skoru 0.20den az olan objeler atildi
                
                label = labels[predicted_id]     
                bounding_box = object_detection[0:4] * np.array([frame_width,frame_height,frame_width,frame_height])
                (box_center_x, box_center_y, box_width, box_height) = bounding_box.astype("int")
                
                start_x = int(box_center_x - (box_width/2))   ##bounding box cizdirilmeye baslanacak nokta belirlendi
                start_y = int(box_center_y - (box_height/2))
                
                
                ############## NON-MAXIMUM SUPPRESSION - OPERATION 2 ###################
                
                ids_list.append(predicted_id)
                confidences_list.append(float(confidence))
                boxes_list.append([start_x, start_y, int(box_width), int(box_height)])
                
                ############################ END OF OPERATION 2 ########################
            
    ############## NON-MAXIMUM SUPPRESSION - OPERATION 3 ###################
                
    max_ids = cv2.dnn.NMSBoxes(boxes_list, confidences_list, 0.5, 0.4)   ##bounding boxlarin güven skoru en yüksek olanlarin idleri tutuldu
         
    for max_id in max_ids:
        
        max_class_id = max_id[0]
        box = boxes_list[max_class_id]
        
        start_x = box[0] 
        start_y = box[1] 
        box_width = box[2] 
        box_height = box[3] 
         
        predicted_id = ids_list[max_class_id]
        label = labels[predicted_id]
        confidence = confidences_list[max_class_id]
      
    ############################ END OF OPERATION 3 ########################
                
        end_x = start_x + box_width
        end_y = start_y + box_height
                
        box_color = colors[predicted_id]
        box_color = [int(each) for each in box_color]
                
                
        label = "{}: {:.2f}%".format(label, confidence*100)
        print("predicted object {}".format(label))
         
                
        cv2.rectangle(frame, (start_x,start_y),(end_x,end_y),box_color,2)
        cv2.putText(frame,label,(start_x,start_y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, box_color, 2)
    
    cv2.imshow("Detection Window", frame)
    
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
    
cap.release()
cv2.destroyAllWindows()

