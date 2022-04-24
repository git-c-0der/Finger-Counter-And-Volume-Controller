# Finger-Counter-And-Volume-Controller
#### Some projects I learned on youtube based on computer vision.

I watched a YouTube tutorial by __Murtaza Hassan__ [FreeCodeCamp](https://www.youtube.com/watch?v=01sAkU_NvOY&list=WL&index=6) and learned to build these amazing computer vision projects.

These projects are heavily based on the mediapipe solutions provided by Google which are easy to use by just few lines of code and highly accuracte for example facemesh module which predict around 378 landmarks on a person's face.

## Project 1:
### Finger Counter
<hr>
In this projects I developed a realtime finger counter in which you just have to show the number of fingers and the code will automatically understand how many fingers are there in the video.

By using the hand module present in teh mediapipe solutions which has been trained on millions of images we can predict 20 landmarks for different points of our fingers then we can use these landmarks to develop a little bit of logic to identify how many fingers are up.

![image](https://user-images.githubusercontent.com/77848178/164980686-ed1d82b8-0275-44e9-b8ac-8d981e2faf20.png)


## Project 2:
### Volume Controller
<hr>
Here based on the distance between the thumbs tip and the index fingers tip volume of the device can be controlled. This distance between the two tips will be calculated by leveraging the landmarks predicted by the mediapipe solutions module.

Code for the Pose detection and Face Mesh has been provided in this repository for real time predictions.

![image](https://user-images.githubusercontent.com/77848178/164981127-0d9364c2-9a7f-40b5-8017-41c7c9e8fc86.png)
![image](https://user-images.githubusercontent.com/77848178/164981070-bda456a9-aad5-402a-8412-4d0994327cf1.png)


In this project I learned how to use OpenCV to handle images easily and make desired changes in them. MediaPipe Solutions are amazing as they are predicting the landmarks in realtime with such a high accuracy without any GPU requirements. Above images has been taken from the [Mediapipe Website](https://google.github.io/mediapipe/) for your better understanding.

Thank You! for Reading.
