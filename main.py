import cv2
import numpy as np


# checks the pixel in the given direction belongs to the region or not:
def check(image, no_rows, no_cols, point, direction):
    # if (check direction) and (check if the new pixel is not outside the image) and (check the pixel is wight)

    if direction == 3 and point[0]+1 <= no_rows-1 and image[point[0] + 1] [point[1]] [0] > 200:
        p = [point[0]+1, point[1]]

    elif direction == 2 and point[1]-1 >= 0 and image[point[0]] [point[1] - 1] [0] > 200:
        p = [point[0], point[1]-1]

    elif direction == 1 and point[0]-1 >= 0 and image[point[0] - 1] [point[1]] [0] > 200:
        p = [point[0]-1, point[1]]

    elif direction == 0 and point[1]+1 <= no_cols-1 and image[point[0]] [point[1] + 1] [0] > 200:
        p = [point[0], point[1]+1]

    else:
        # return index of -1 if the pixel next to the given one in the given direction does not belong to the region
        p = [-1, -1]

    return p


# checks if the pixel belong to a letter surrounded by red loop (inside an detected letter):
def in_boundary (point, out_img, no_row, no_col):
    North = False
    South = False
    East = False
    West = False

    if out_img[point[0]][point[1]][0] <= 200:
        return True

    # check if there is red pixel above the given one.
    for r in range(point[0]):
        if out_img[r][point[1]][0] == 0 and out_img[r][point[1]][1] == 0 and out_img[r][point[1]][2] == 255:
            North = True

    # check if there is red pixel below the given one.
    for r in range(point[0],no_row):
        if out_img[r][point[1]][0] == 0 and out_img[r][point[1]][1] ==0 and out_img[r][point[1]][2] == 255:
            South = True

    # check if there is red pixel at the left of the given one.
    for c in range(point[1]):
        if out_img[point[0]][c][0] == 0 and out_img[point[0]][c][1] == 0 and out_img[point[0]][c][2] == 255 :
            West = True

    # check if there is red pixel at the right of the given one.
    for c in range(point[1],no_col):
        if out_img[point[0]][c][0] == 0 and out_img[point[0]][c][1] == 0 and out_img[point[0]][c][2] == 255:
            East = True

    return (North and South) and (East and West)


# Find the starting pixel of new letter:
def find_start (out_img,no_row,no_col):
    for r in range(no_row):
        for c in range(no_col):
            # return the point if it does not belong to a detected letter.
            if not (in_boundary([r, c], out_img, no_row, no_col)):
                return [r, c]
    # return index of -1 if there is no undetected letters.
    return[-1, -1]


if __name__ == '__main__':
    dir = 3
    img = cv2.imread("hello.jpeg", 1)
    img = cv2.resize(img, (650, 310))
    ####################################################
    ###############################################

    output_img = np.copy(img)
    no_rows = np.shape(img)[0]
    no_cols = np.shape(img)[1]
    start = find_start(output_img, no_rows, no_cols)

    while start[0] != -1:
        # This loop iterates over the letters to detect each one of them
        print(start)
        edge_points = []
        row = start[0]
        column = start[1]
        output_img[row][column] = np.array([0, 0, 255])
        edge_points.append([row, column])

        while True:
            # This loop is to find all the pixels that forms the frame of the letter
            dir = (dir + 3) % 4
            while True:
                # This loop is to find the next valid point in the letter frame
                checked_point = check(img, no_rows, no_cols, edge_points[-1], dir)
                if checked_point[0] != -1:
                    output_img[checked_point[0]][checked_point[1]] = np.array([0, 0, 255])
                    edge_points.append(checked_point)
                    break
                else:
                    dir = (dir+1) % 4

            if (edge_points[0] == edge_points[-2]) and (edge_points[1] == edge_points[-1]) and (len(edge_points) > 2):
                start = find_start(output_img, no_rows, no_cols)
                break

    cv2.imshow("Original", img)
    cv2.imshow("Output", output_img)
    cv2.waitKey(0)