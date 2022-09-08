"""
Image White Balancing using CV2 and COlor Correction Cards with ArUCo Markers
Author: https://pyimagesearch.com/2021/02/15/automatic-color-correction-with-opencv-and-python/

Modify Stephan Krol 
G-Mail: Stephan.Krol.83[at]
Website: https://CouchBoss.de

"""



from imutils.perspective import four_point_transform
from skimage import exposure
import numpy as np
import argparse
import imutils
import cv2
import sys
from os.path import exists
import os.path as pathfile
from PIL import Image


def find_color_card(image):
    # load the ArUCo dictionary, grab the ArUCo parameters, and
    # detect the markers in the input image
    arucoDict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_ARUCO_ORIGINAL)
    arucoParams = cv2.aruco.DetectorParameters_create()
    (corners, ids, rejected) = cv2.aruco.detectMarkers(image,
                                                       arucoDict, parameters=arucoParams)

    # try to extract the coordinates of the color correction card
    try:
        # otherwise, we've found the four ArUco markers, so we can
        # continue by flattening the ArUco IDs list
        ids = ids.flatten()

        # extract the top-left marker
        i = np.squeeze(np.where(ids == 923))
        topLeft = np.squeeze(corners[i])[0]

        # extract the top-right marker
        i = np.squeeze(np.where(ids == 1001))
        topRight = np.squeeze(corners[i])[1]

        # extract the bottom-right marker
        i = np.squeeze(np.where(ids == 241))
        bottomRight = np.squeeze(corners[i])[2]

        # extract the bottom-left marker
        i = np.squeeze(np.where(ids == 1007))
        bottomLeft = np.squeeze(corners[i])[3]

    # we could not find color correction card, so gracefully return
    except:
        return None

    # build our list of reference points and apply a perspective
    # transform to obtain a top-down, bird’s-eye view of the color
    # matching card
    cardCoords = np.array([topLeft, topRight,
                           bottomRight, bottomLeft])
    card = four_point_transform(image, cardCoords)
    # return the color matching card to the calling function
    return card


def _match_cumulative_cdf_mod(source, template, full):
    """
    Return modified full image array so that the cumulative density function of
    source array matches the cumulative density function of the template.
    """
    src_values, src_unique_indices, src_counts = np.unique(source.ravel(),
                                                           return_inverse=True,
                                                           return_counts=True)
    tmpl_values, tmpl_counts = np.unique(template.ravel(), return_counts=True)

    # calculate normalized quantiles for each array
    src_quantiles = np.cumsum(src_counts) / source.size
    tmpl_quantiles = np.cumsum(tmpl_counts) / template.size

    interp_a_values = np.interp(src_quantiles, tmpl_quantiles, tmpl_values)

    # Here we compute values which the channel RGB value of full image will be modified to.
    interpb = []
    for i in range(0, 256):
        interpb.append(-1)

    # first compute which values in src image transform to and mark those values.

    for i in range(0, len(interp_a_values)):
        frm = src_values[i]
        to = interp_a_values[i]
        interpb[frm] = to

    # some of the pixel values might not be there in interp_a_values, interpolate those values using their
    # previous and next neighbours
    prev_value = -1
    prev_index = -1
    for i in range(0, 256):
        if interpb[i] == -1:
            next_index = -1
            next_value = -1
            for j in range(i + 1, 256):
                if interpb[j] >= 0:
                    next_value = interpb[j]
                    next_index = j
            if prev_index < 0:
                interpb[i] = (i + 1) * next_value / (next_index + 1)
            elif next_index < 0:
                interpb[i] = prev_value + ((255 - prev_value) * (i - prev_index) / (255 - prev_index))
            else:
                interpb[i] = prev_value + (i - prev_index) * (next_value - prev_value) / (next_index - prev_index)
        else:
            prev_value = interpb[i]
            prev_index = i

    # finally transform pixel values in full image using interpb interpolation values.
    wid = full.shape[1]
    hei = full.shape[0]
    ret2 = np.zeros((hei, wid))
    for i in range(0, hei):
        for j in range(0, wid):
            ret2[i][j] = interpb[full[i][j]]
    return ret2


def match_histograms_mod(inputCard, referenceCard, fullImage):
    """
        Return modified full image, by using histogram equalizatin on input and
         reference cards and applying that transformation on fullImage.
    """
    if inputCard.ndim != referenceCard.ndim:
        raise ValueError('Image and reference must have the same number '
                         'of channels.')
    matched = np.empty(fullImage.shape, dtype=fullImage.dtype)
    for channel in range(inputCard.shape[-1]):
        matched_channel = _match_cumulative_cdf_mod(inputCard[..., channel], referenceCard[..., channel],
                                                    fullImage[..., channel])
        matched[..., channel] = matched_channel
    return matched


# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-r", "--reference", required=True,
                help="path to the input reference image")
ap.add_argument("-w", "--width0", required=False,
                help="Image Size")
ap.add_argument("-v", "--view", required=False, default=False, action='store_true',
                help="Image Preview?")
ap.add_argument("-o", "--output", required=False, default=False,
                help="Image Output Path")
ap.add_argument("-i", "--input", required=True,
                help="path to the input image to apply color correction to")
args = vars(ap.parse_args())

# load the reference image and input images from disk
print("[INFO] loading images...")
# raw = cv2.imread(args["reference"])
# img1 = cv2.imread(args["input"])
file_exists = pathfile.isfile(args["reference"])

if not file_exists:
    print('[WARNING] Referenz File not exisits '+str(args["reference"]))
    sys.exit()


raw = cv2.imread(args["reference"])
img1 = cv2.imread(args["input"])

height, width0, channels = raw.shape
height2, width1, channels = img1.shape


# resize the reference and input images

newWidth=width0//3
countStep=400
goOn=False
while goOn==False and newWidth<=width0:

    raw_ = imutils.resize(raw, newWidth)
    img1_ = imutils.resize(img1, newWidth)

  
    print("[INFO] Finding color matching cards width "+ repr(newWidth)+"px")
    rawCard = find_color_card(raw_)
    imageCard = find_color_card(img1_)
    
    if rawCard is None or imageCard is None:
        oldW =newWidth
        newWidth +=countStep
        print("[INFO] Could not find color with width "+ repr(oldW)+"px. Try width:"+ repr(newWidth)+"px")
        continue
    else:
        goOn=True
        break

if(goOn is False):
    print("[WARNING] Could not find color matching cards in both images. Try a highter/better Resolution")
       
    sys.exit()

if args['view']:
        cv2.imshow("Reference", raw_)
        cv2.imshow("Input", img1_)
# show the color matching card in the reference image and input image,
# respectively
if args['view']:
    cv2.imshow("Reference Color Card", rawCard)
    cv2.imshow("Input Color Card", imageCard)
# apply histogram matching from the color matching card in the
# reference image to the color matching card in the input image
print("[INFO] matching images...")

# imageCard2 = exposure.match_histograms(img1, ref,
# inputCard = exposure.match_histograms(inputCard, referenceCard, multichannel=True)

if args["width0"]:
    width=int(args["width0"])
    if width>1:    
        print('resize Final: '+repr(width))
        img1 = imutils.resize(img1, width)

result2 = match_histograms_mod(imageCard, rawCard, img1)




# show our input color matching card after histogram matching
#cv2.imshow("Input Color Card After Matching", inputCard)


if args['view']:
    cv2.imshow("Input Color Card After Matching", result2)

if args['output']:
    file_ok = exists(args['output'].lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')))

    if file_ok:
        cv2.imwrite(args['output'], result2)
        print("[SUCCESSUL] Your Image was written to: "+args['output']+"")
    else:
        print("[WARNING] Sorry, But this is no valid Image Name "+args['output']+"\nPlease Change Parameter!")

if args['view']:
    cv2.waitKey(0)

if not args['view']:
    if not args['output']:
        print('[EMPTY] You Need at least one Paramter "--view" or "--output".')
