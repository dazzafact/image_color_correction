# White-Balance with Color Cards 
A python function to correct image White-Balance using Color Cards, detecting with [CV2 Aruco](https://docs.opencv.org/4.x/d5/dae/tutorial_aruco_detection.html).
Base Idea: https://pyimagesearch.com/2021/02/15/automatic-color-correction-with-opencv-and-python/

You just need an already optimized color input image and another image which is not color optimized. Both images with Color Card, using ArUCo Marker (you can glue them on the Corners of every imageCard to for detecting)

`python color_correction.py --reference ref.jpg  --input test.jpg --out output.jpg`

## Image Inputs

**First you need a color optimized Image as Reference using a Color Card with [Aruco Markers](https://docs.opencv.org/4.x/d5/dae/tutorial_aruco_detection.html) (or follow the Link to [purchase the Panton Color Card](https://www.pantone.com/eu/de/pantone-color-match-card)).**


![image](https://user-images.githubusercontent.com/67874406/187918735-78967b36-ce77-47cc-8a17-773ea856d988.png)

**1.) A ReferenceImage used as the basis for all further image processes. The colors of this Card image should be optimized to your liking.**

`--reference ref.jpg`

![image](https://user-images.githubusercontent.com/67874406/187906176-23303477-0dd7-4ef8-ae05-1e36f3e82de7.png)


 **2.) you have to choose a none color optimized Image with the a Color card, to detect the Color Difference between both images**

`--input test.jpg`

![image](https://user-images.githubusercontent.com/67874406/187906327-8a42dcf2-c312-4ce7-b336-6f8d4f310788.png)

**3.) As result you get the Final color optimized Output Image based on the reference Histogram Colors**

![image](https://user-images.githubusercontent.com/67874406/187906458-244286b9-70c5-4b6f-8f35-bdee9908573a.png)


## Python command

### **Output File**
`python color_correction.py --reference raw.jpg  --input test.jpg --out output.jpg`


### **Special output File width**
`python color_correction.py --reference raw.jpg  --input test.jpg --out output.jpg  --width 1280`


### **with output Preview**
`python color_correction.py --reference raw.jpg  --input test.jpg --view`

### **with an output Preview and file output**
`python color_correction.py --reference raw.jpg  --input test.jpg --out output.jpg --view`


Blog: https://pyimagesearch.com/2021/02/15/automatic-color-correction-with-opencv-and-python/

Stackoverflow: https://stackoverflow.com/questions/70233645/color-correction-using-opencv-and-color-cards/73566972#73566972
