# The main goal of the study

- Security breaches that drone swarms may create in the air defense system must be determined in advance.
- In this study, an intelligent drone detection system is proposed for the detection of drone swarm.
- Among the object detection methods, the YOLO algorithm was preferred as the optimum method.


# Drone Swarms Detection with YOLO

*Model Training*

80% of the tagged data set is grouped to be used as training data and 20% as test data. 
The dataset consists of 1379 images in total.
The model was run in the Google Colab environment as the training process provides free GPU support for performance and speed.
By using the YOLOv4 ready model, the hyperparameters in the configuration file were arranged appropriately and the model was trained with 416x416 images.
Classes values were determined as 1, filters number 18, max_batches number 2000, subdivisions 64 and batch value 64.



# RESULTS

- The initial learning rate and other parameters required for the system to work properly were taken the same as in the original YOLOv4 model. Only necessary hyperparameters have been modified to improve performance.
- The model was trained for approximately 8 hours. The training process took 2000 epochs and the weights of the model were backed up every 200 steps. These backed up weights were then run on the test data.


![drone_tespit](https://user-images.githubusercontent.com/58220997/124391796-e6614080-dcfa-11eb-90da-ffbaa4476708.gif)
