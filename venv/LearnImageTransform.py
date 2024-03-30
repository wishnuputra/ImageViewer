# Imports PIL module
import numpy as np
from PIL import Image
import time

start = time.time()



# open method used to open different extension image file
im = Image.open(r"C:\Users\wishn\Downloads\pexels-micheile-oliviestrauss-11823968.jpg")
im_arr = np.asarray((im))
# This method will show image in any image viewer
#im.show()

def cropImageAt(x, y, r, mat):
    x_start = x - r
    x_end = x + r
    y_start = y - r
    y_end = y + r
    return mat[x_start:x_end, y_start:y_end]

def getPixelsInsideCircle(x, y, r, mat):
    x_start = x - r
    x_end = x + r
    y_start = y - r
    y_end = y + r
    for i in range(x_start, x_end):
        for j in range(y_start, y_end):
            a = i - x
            b = j - y
            if a*a + b*b <= r*r:
                mat[i][j] = [0, 0, 0]

# img = cropImageAt(2050, 3100, 100, im_arr)
# img_pil = Image.fromarray(img)
# img_pil.show()
# im_arr[0,0] = 0
# print(im_arr[0][0])

#img_circled= getPixelsInsideCircle(2050, 3100, 100, im_arr)
# img_circled_pil = Image.fromarray(im_arr)
# img_circled_pil.show()

end = time.time()
print(end - start)
#print(type(im_arr))