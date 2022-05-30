
import numpy as np
import cv2

# set boundary for the first object
# delete object from original image
# repeat


def search_for_first_pixel(img):
    no_row, no_col = img.shape
    for r in range(no_row):
        for c in range(no_col):
            if img[r][c] != 0:
                return r, c  # coordinate of first nonzero pixel
    return -1, -1  # if the image was totally black , termination condition


def set_boundary(img):
    height, width = img.shape  # get the shape of the img
    new_img = np.zeros(shape=(height, width), dtype=np.uint8)  # create new blank image with the same size

    while True:
        print("give me some time ...")  # debugging
        boundary_locations = []  # list to store the  location of the boundary pixels
        direction = 3  # initialization
        top, left = search_for_first_pixel(img)  # get the first nonzero pixel in the original img
        if top == -1:  # termination condition
            break
        new_img[top][left] = 255  # assign it with white in the new image
        boundary_locations.append((top, left))  # store the location in the boundary locations list
        current_pixel_x = top
        current_pixel_y = left

        #  search for new boundary pixel
        while True:
            direction = (direction + 3) % 4
            coordinates = {0: (current_pixel_x, current_pixel_y + 1),  # mapping each direction to its coordinates
                           1: (current_pixel_x + 1, current_pixel_y),
                           2: (current_pixel_x, current_pixel_y - 1),
                           3: (current_pixel_x - 1, current_pixel_y)
                           }

            for coordinate in coordinates:  # loop through the coordinates and finding the nonzero pixel anti-clockWise
                if img[coordinates[direction]] != 0:
                    break  # break from the for loop
                else:
                    direction = (direction + 1) % 4  # get next element in the coordinates dictionary

            new_pixel = coordinates[direction]  # coordinate of the new pixels
            new_img[new_pixel] = 255  # assign it with white in the new image
            boundary_locations.append(new_pixel)  # store the location in the boundary locations list
            current_pixel_x = new_pixel[0]  # update current_pixel_x
            current_pixel_y = new_pixel[1]  # update current_pixel_y

            if (boundary_locations[0] == boundary_locations[-2]) and\
                    (boundary_locations[1] == boundary_locations[-1]) and \
                    (len(boundary_locations) > 2):  # termination condition
                break

        x_min = min(boundary_locations)[0]     # delete the object from the original image
        x_max = max(boundary_locations)[0]
        y_min = min(boundary_locations)[1]
        y_max = max(boundary_locations)[1]
        for x in range(x_min, x_max+1):
            for y in range(y_min, y_max+1):
                img[x][y] = 0

    return new_img


if __name__ == '__main__':

    blank = 255 * np.zeros(shape=[512, 512, 3], dtype=np.uint8)  # create blank image

    cv2.rectangle(blank, pt1=(50, 50), pt2=(150, 150), color=(255, 255, 255), thickness=-1)  # draw squares
    cv2.rectangle(blank, pt1=(200, 200), pt2=(300, 300), color=(255, 255, 255), thickness=-1)  # draw squares
    cv2.rectangle(blank, pt1=(350, 350), pt2=(450, 450), color=(255, 255, 255), thickness=-1)  # draw squares

    gray = cv2.cvtColor(blank, cv2.COLOR_BGR2GRAY)  # convert to grey scale

    ret, binary_image = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)  # binary image
    my_new_image = set_boundary(binary_image)  # apply algorithm

    cv2.imshow('Original', gray)
    cv2.imshow('HOPE', my_new_image)

    cv2.waitKey()
    cv2.destroyAllWindows()
