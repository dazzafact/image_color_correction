# White-Balance with Color Cards 
A python function to correct image White-Balance using Color Cards, detecting with [CV2 Aruco](https://docs.opencv.org/4.x/d5/dae/tutorial_aruco_detection.html).


You just need an already optimized color input image and another image which is not color optimized. Both images with Color Card, using ArUCo Marker (you can glue them on the Corners of every imageCard to for detecting)

##Image Inputs
**Input Reference, color optimized**

![image](https://user-images.githubusercontent.com/67874406/187906176-23303477-0dd7-4ef8-ae05-1e36f3e82de7.png)

**Input not color optimize**

![image](https://user-images.githubusercontent.com/67874406/187906327-8a42dcf2-c312-4ce7-b336-6f8d4f310788.png)


**Final color optimized Output Image**

![image](https://user-images.githubusercontent.com/67874406/187906458-244286b9-70c5-4b6f-8f35-bdee9908573a.png)

##Python command
use the Script with this arguments

`python color_correction.py --reference ref.jpg --input input.jpg`
