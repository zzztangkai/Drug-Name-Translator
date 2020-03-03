import cv2
import numpy as np


# This method performs finishing work and removes the bounds that were not caught by the line thresh hold
# while merging. Although this method has three for loops but it is not very expensive because we have already
# merged the most of the bounds.
# This method does not cover all the cases of one bound being inside another bound. It only checks for top left
# corner and bottom right corner. This covers more than 90% for our purpose.
# Some of the potential cases could be checking if top left corner and top right corner is inside another bound
# or bottom left corner and bottom right corner is inside another bound or based on some proportion of area etc.
def remove_inside_bounds(b_list):
    processed_bounds = list()
    for b in b_list:
        top_in = False
        bot_in = False
        x1, y1, x2, y2 = b

        # check if top left corner is inside another bound
        for bdr in b_list:
            topx1, topy1, botx1, boty1 = bdr
            if topx1 < x1 < botx1:
                if topy1 <= y1 < boty1:
                    top_in = True
                    break

        # check if bottom right corner is inside another bound
        for bdr in b_list:
            topx1, topy1, botx1, boty1 = bdr
            if topx1 < x2 < botx1:
                if topy1 < y2 <= boty1:
                    bot_in = True
                    break

        inside = top_in and bot_in
        if not inside:
            processed_bounds.append(b)
    return processed_bounds


def read_text(im):

    # IMAGE PRE PROCESSING
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)  # convert image to gray scale
    gray_mask = cv2.inRange(gray, 100, 255)  # change all pixels below 100 to 0 and above 100 to 255
    mask = cv2.inRange(gray_mask, 0, 127)  # change white background to black and black text to white

    _, contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)  # find all the contours

    # this is the white background of the same size as original image. We will use this image to draw all the
    # contours on to it
    mask2 = np.ones(im.shape, np.uint8) * 255
    for cnt in contours:
        cv2.drawContours(mask2, [cnt], -1, (0, 0, 0), -1)  # draw all the contours in black color on white background

    kernel = np.ones((5, 5), np.uint8)  # kernel to perform morphological operation on contours

    opening = cv2.morphologyEx(mask2, cv2.MORPH_OPEN, kernel)  # close small openings in the contours by growing them

    gray_op = cv2.cvtColor(opening, cv2.COLOR_BGR2GRAY)  # convert to gray image to perform thresh holding

    # change all pixels below 150 to 0 and above 150 to 255. We are performing this operation because we want to find
    # all the contours in next step
    _, threshold_op = cv2.threshold(gray_op, 150, 255, cv2.THRESH_BINARY_INV)

    # find all the contours again. Because we have closed small gaps in contours with morphology. We hope to get
    # better results and we will get all the contours that are not broken
    _, contours_op, _ = cv2.findContours(threshold_op, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    bounds_list = list()

    # Go through all the contours. If the contour area is more than 10 then make a bounding box around the contour
    # and add top left corner x, y and bottom right corner x, y coordinates to the bounding list
    for cnt in contours_op:
        if cv2.contourArea(cnt) > 10:
            rect = cv2.minAreaRect(cnt)  # calculate rectangle around the contour
            box = cv2.boxPoints(rect)  # convert the rectangle into box
            a, b, c, d = np.int0(box)  # convert floating points to integers
            bound = [a, b, c, d]  # change the points to list

            # change list to numpy array for vectorize operations to avoid for loops to go through the points list
            bound = np.array(bound)

            x1, y1 = (bound[:, 0].min(), bound[:, 1].min())  # minimum x and y are the coordinates of top left corner
            x2, y2 = (bound[:, 0].max(), bound[:, 1].max())  # maximum x and y are the coordinates of bottom right
            bounds_list.append((x1, y1, x2, y2))  # collect those points into bounds_list for further processing

    # COMBINE BOUNDS THAT ARE ON SAME LINE
    same_line_threshold = 10.0  # y coordinate thresh hold to be considered on same line
    b_array = np.array(bounds_list)
    start_y = b_array[:, 1].min()
    line_list = list()

    # start with the minimum y coordinate that is supposed to be the first line and using vectorize operation of
    # numpy collect all the bounds that are on same line
    # This while loop is not very expensive because it just iterates equal to the number of lines in the image
    while start_y is not None:
        # The main task of iterating through the whole list of bounds is done by this line of code. Instead of
        # using for loop we are using vectorize operation which much faster than the for loop
        same_line_indices = np.where(b_array[:, 1] <= start_y + same_line_threshold)

        line_list.append(b_array[same_line_indices])  # collect all the bounds that are on one line in line_list
        b_array = np.delete(b_array, same_line_indices, axis=0)  # delete the collected bounds from the main list
        try:
            start_y = b_array[:, 1].min()  # set start_y for next line
        except ValueError:
            break

    # MERGE ALL THE BOUNDS OF SAME LINE INTO ONE
    processed_bounds = list()

    # This for loop is also not very expensive because it just iterates equal to the number of lines in the image
    for line in line_list:
        # The main task of iterating through the all the bounds of same line is done through vectorization
        x1, y1 = line[:, 0].min(), line[:, 1].min()
        x2, y2 = line[:, 2].max(), line[:, 3].max()
        processed_bounds.append((x1, y1, x2, y2))

    # REMOVE SMALL BOUNDS THAT ARE INSIDE BIGGER BOUNDS
    # This method performs finishing work and removes the bounds that were not caught by the line thresh hold
    # while merging
    processed_bounds = remove_inside_bounds(processed_bounds)
    return processed_bounds  # final list of bounds. Each bound encloses the each line of text on the image


# START THE PROGRAM
if __name__ == '__main__':
    img = cv2.imread('./img.png')  # read image
    original_img = np.copy(img)
    list_of_lines = read_text(img)  # detect text lines

    # draw a boundary in green color based on the detected text bounds
    for each_line in list_of_lines:
        topx, topy, botx, boty = each_line
        roi = img[topy + 1: boty, topx + 1: botx]  # region of interest on image
        cv2.rectangle(img, (topx, topy), (botx, boty), (0, 255, 0), 1)  # draw the boundary

    # display the image
    cv2.imshow('Original image (Left), Detected text (Right)', np.hstack((original_img, img)))
    cv2.waitKey(0)
    cv2.destroyAllWindows()
