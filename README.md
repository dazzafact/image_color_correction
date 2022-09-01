# White-Balance with Color Cards 
A python function to correct image White-Balance using Color Cards, detecting with [CV2 Aruco](https://docs.opencv.org/4.x/d5/dae/tutorial_aruco_detection.html).


You just need an already optimized color input image and another image which is not color optimized. Both images with Color Card, using ArUCo Marker (you can glue them on the Corners of every imageCard to for detecting)

## Image Inputs

**First you need a color optimized Image as Reference using a Color Card with Aruco Markers (See Link).**

![image](https://user-images.githubusercontent.com/67874406/187918735-78967b36-ce77-47cc-8a17-773ea856d988.png)

**ReferenceImage with correct Colors. It is quite sufficient if only the card can be seen.**

![image](https://user-images.githubusercontent.com/67874406/187906176-23303477-0dd7-4ef8-ae05-1e36f3e82de7.png)


 **As second Paramter you have to choose a none color optimized Image with the a Color card, to detect the Color Difference between both images**

![image](https://user-images.githubusercontent.com/67874406/187906327-8a42dcf2-c312-4ce7-b336-6f8d4f310788.png)

**As result you get the Final color optimized Output Image based on the reference Histogram Colors**

![image](https://user-images.githubusercontent.com/67874406/187906458-244286b9-70c5-4b6f-8f35-bdee9908573a.png)


## Python command

use the Script with this arguments

### **Output File**
`python color_correction.py --reference raw.jpg  --input test1.jpg --out output.jpg`

### **with an output Preview**
`python color_correction.py --reference raw.jpg  --input test1.jpg --view`

### **with an output Preview and file output**
`python color_correction.py --reference raw.jpg  --input test1.jpg --out output.jpg --view`
