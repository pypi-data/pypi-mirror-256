import numpy as np
import matplotlib.pyplot as plt
from skimage import exposure, filters
from readrr import read_img , gray_img
from features import lpq , sharpness , lbpv , fractal_dimension , texture_analysis


from Sift_keypoints import visualize_keypoints
# img = read_img("b.jpg",gray=True)
# print(sharpness(img))

# img = read_img("asd.jpg")/

img = read_img("129.PNG")
a=lpq(gray_img(img))

# img = read_img("A.jpg",gray=True)
# print(img.shape)

# img = read_img("A.jpg",gray=False)
# dim=fractal_dimension(img,plot=True)
# print(dim)


# img = read_img("A.jpg",gray=True)
# dim=texture_analysis(img)
# print(dim)

# img = read_img("b.jpg",gray=True)
# dim=lbpv(img)
# print(dim)

visualize_keypoints(img)