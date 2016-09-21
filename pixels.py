##############################################################################
### pixels.py                                                              ###
### Author: Alistair Campbell                                              ###
### except for averagePixel and blur, written by                           ###
### Oliver Keh                                                             ###
###                                                                        ###
### Date: 1/11/2016                                                        ###
###                                                                        ###
### This program reads an image file, extracts a 2D array of pixels (as    ###
### defined in the pixel class here), blurs the pixels, replaces them in   ###
### the image, and writes the image to another file.                       ###
###                                                                        ###
##############################################################################

from PIL import Image

class pixel:
    def __init__(self, r=0, g=0, b=0):
        """save given red, green, and blue values"""
        assert(type(r)==type(0) and type(g)==type(0) and type(b)==type(0))
        assert(0 <= r and r <= 255)
        assert(0 <= g and g <= 255)
        assert(0 <= b and b <= 255)
        self._r = r
        self._g = g
        self._b = b

    def getR(self):
        """ return red component of this pixel """
        return self._r

    def getG(self):
        """ return green component of this pixel """
        return self._g

    def getB(self):
        """ return blue component of this pixel """
        return self._b

    def __repr__(self):
        return "(" + str(self.getR()) + ", " + str(self.getG()) + ", " + \
                str(self.getB()) + ")"

def averagePixel(pixelList):
    """ @param pixelList: a list of pixels, compute the average pixel:  
        a pixel with average red, average green, and average blue components
        of the given pixels.
        @return the computed pixel """

    #these 3 lists contain the color values of each pixel
    red_pixels = []
    blue_pixels = []
    green_pixels = []

    #goes through all of the pixels and appends the color values to the appropriate list
    for c in pixelList:
        red_pixels.append(c._r)
        blue_pixels.append(c._b)
        green_pixels.append(c._g)

    #finds average using round function to round to lowest whole number
    avg_red = int(round(sum(red_pixels) / len(red_pixels)))
    avg_blue = int(round(sum(blue_pixels) / len(blue_pixels)))
    avg_green = int(round(sum(green_pixels) / len(green_pixels)))

    #returns a new pixel color value
    return pixel(avg_red, avg_green, avg_blue)

def blur(data):
    """ @param data: 2D array (list of lists) of pixels from an image.
        Replace each pixel in data with a new pixel computed as the average
        of the pixel and each of its original neighbors. 
        @return None """
    if data == [] or len(data) == 1: #checks that a given array is not empty and longer 
    #than one
        return
    data_copy = [c[:] for c in data] #makes a deep copy of the original data
    row = len(data) #finds the length of a given row
    column = len(data[0]) #finds the number of columns in a given list
    values = []

    for i in range(row):
        for c in range(column):
            values.append(data_copy[i][c])
            if (i-1 >= 0): #finds pixel immediately above a given pixel
                values.append(data_copy[i-1][c])

            if (i+1 < row): #finds pixel immediately below a given pixel
                values.append(data_copy[i+1][c])

            if (c-1 >= 0): #finds pixel immediately to the left of a given pixel
                values.append(data_copy[i][c-1])

            if (c+1 < column): #finds pixel immediately to the right of a given pixel
                values.append(data_copy[i][c+1])

            if (i-1 >= 0) and (c-1 >= 0): #finds pixel diagonally left of a pixel (up)
                values.append(data_copy[i-1][c-1])

            if (i+1 < row) and (c+1 < column): #finds pixel diagonally right of a pixel (down)
                values.append(data_copy[i+1][c+1])

            if (i-1 >= 0) and (c+1 < column): #finds pixel diagonally right of a pixel (up)
                values.append(data_copy[i-1][c+1])

            if (i+1 < row) and (c-1 >= 0): #finds pixel diagonally left of a pixel (down)
                values.append(data_copy[i+1][c-1])

            data[i][c] = averagePixel(values) #replaces original data with new values
            values = [] #empties the list before moving onto next pixel
    

    return

def rc(data):
    """ Return a pair: the number of rows and columns of a 2D array """
    rows = len(data)
    cols = 0
    if (rows > 0):
        cols = len(data[0])
    return rows, cols

def get_pixels(im):
    """ Return a 2D array (list of lists) of pixels from a Python image """
    cols, rows = im.size
    data = [[None] * cols for _ in range(rows)]
    raw = im.getdata()
    i = 0
    for row in range(rows):
        for col in range(cols):
            data[row][col] = pixel(raw[i][0], raw[i][1], raw[i][2])
            i = i + 1
    return data

def put_pixels(im, data):
    """Replace the pixels of a Python image with those from a 2D array"""
    rows, cols = rc(data)
    raw = [None] * (rows * cols)
    i = 0
    for r in range(rows):
        for c in range(cols):
            raw[i] = (data[r][c].getR(), data[r][c].getG(), data[r][c].getB())
            i = i + 1
    im.putdata(raw)

def main():
    """Main program: open an image, blur it a certain number of times,
       write to another file."""
    blur_times = 5
    im = Image.open("small_logo.png")
    pixels = get_pixels(im)
    for i in range(blur_times):
        blur(pixels)
    put_pixels(im, pixels)
    im.save("small_logo_blurred.png", "PNG")

# Don't modify this at all:
if __name__ == "__main__":
    main()
