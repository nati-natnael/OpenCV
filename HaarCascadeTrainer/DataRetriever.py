import os
import sys
import cv2
import numpy as np

from urllib import urlopen
from urllib import urlretrieve
from utils import Logger

# CRITICAL - 50
# ERROR - 40
# WARNING - 30
# INFO - 20
# DEBUG - 10
logger = Logger('log\Trainer')
logger.set_level(20)


class DataRetriever(object):
    def __init__(self):
        self.clicked = False
        self.start = None
        self.dimension = None

    def pull_files_link(*args):
        """
        Download files using the online image links included
        in img_path 'links'. when downloading images
        are converted to gray scale and sized to [100,100].

        PARAMS IN ORDER
        links: Path containing links of files
        dir: download destination directory
        file_type: file type being downloaded
        file_pos: file name start position
        :return:
        """

        logger.info("Pulling Files from link")

        if len(args) < 6:
            logger.error("Illegal Argument Count")
            raise Exception("Illegal Argument Count")

        links = args[1]
        dir_path = args[2]
        file_type = args[3]
        file_pos = args[4]
        img_size = args[5]
        if not isinstance(img_size, tuple):
            logger.error("pull_files_link: Illegal Argument Type - Size")
            raise Exception("Illegal Argument Type: Size")

        how_many = float("inf")

        # Parse Args
        if len(args) == 7:
            how_many = int(args[6])

        try:
            r = urlopen(links).read()

            count = 1
            file_num = file_pos
            links = r.split('\n')
            for link in links:
                try:
                    logger.info("Getting: " + link)

                    img_path = dir_path + "img" + str(file_num) + file_type
                    urlretrieve(link, img_path)
                    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

                    if img is not None:
                        img = cv2.resize(img, img_size)
                        cv2.imwrite(img_path, img)
                        file_num += 1
                    else:
                        logger.error("Image Read Failed: " + link)
                        continue
                except Exception as e:
                    logger.error(str(e))

                count += 1
                if count >= how_many:
                    break

        except IOError as io_e:
            logger.error(str(io_e))

    def remove_bad_imgs(self, from_dir, bad_imgs_dir):
        """
        Removing Bad images in directory defined 'from_dir' that are the
        equal as images in directory 'bad_imgs_dir'.

        :param from_dir: Directory containing images to be cleaned
        :param bad_imgs_dir: Directory containing sample of bad images
        :return:
        """

        logger.debug("Removing bad image from %s" % from_dir)
        # Images to be tested
        for current in os.listdir(from_dir):
            current_path = from_dir + '\\' + str(current)
            # Known Bad images
            for bad_img in os.listdir(bad_imgs_dir):
                try:
                    bad_img_path = bad_imgs_dir + '\\' + str(bad_img)
                    cur = cv2.imread(current_path)
                    bad = cv2.imread(bad_img_path)

                    try:
                        cur_shape = cur.shape
                        bad_shape = bad.shape

                        if bad_shape == cur_shape and not (np.bitwise_xor(cur, bad).any()):
                            logger.debug("Removing ..." + current_path)
                            os.remove(current_path)

                    except AttributeError:
                        logger.error("Removing ..." + current_path)
                        os.remove(current_path)

                except Exception as e:
                    logger.error("Error: " + str(e))

    def negative(self, descriptor_path, imgs_path, rel_path):
        """
        Make a descriptor txt file for haarcascade_xml sets

        :param descriptor_path: path to descriptor file
        :param imgs_path: path to neg images
        :param rel_path: relative path of images from descriptor path
        :return:
        """

        logger.info("Making Neg descriptor file: " + descriptor_path)

        f = open(descriptor_path, 'w+')
        logger.debug("File opened. Path: %s" % descriptor_path)

        for img in os.listdir(imgs_path):
            logger.debug('Writing file: ' + imgs_path + img)
            path = rel_path + img + '\n'
            f.write(path)

        f.close()

    def mouse_event(self, event, x, y, flags, param):
        """

        :param event:
        :param x:
        :param y:
        :param flags:
        :param param:
        :return:
        """

        # Unused params
        del flags, param

        if event == cv2.EVENT_LBUTTONDOWN:
            self.clicked = True
            self.start = (x, y)
            self.dimension = (x, y)
            logger.debug("Left Mouse Button clicked")
            logger.debug("\tStart: (x, y) => " + str(self.start))
            logger.debug("\tDimension: (x, y) => " + str(self.dimension))

        elif event == cv2.EVENT_LBUTTONUP:
            self.clicked = False
            logger.debug("Left Mouse Button Relesed")
            logger.debug("\tStart: (x, y) => " + str(self.start))
            logger.debug("\tDimension: (x, y) => " + str(self.dimension))

        elif event == cv2.EVENT_MOUSEMOVE and self.clicked:
            self.dimension = (x, y)
            logger.debug("Mouse Dragged")
            logger.debug("\tStart: (x, y) => " + str(self.start))
            logger.debug("\tDimension: (x, y) => " + str(self.dimension))

    def positive(self, descriptor_path, pos_images_path, rel_dir):
        """
        Purpose: Help create a descriptor file for positive images

        :param descriptor_path: file path to write description of images
        :param pos_images_path: path for positive image directory
        :param rel_dir: relative path of images to descriptor file
        :return: None
        """

        logger.info("Making Pos descriptor file: " + descriptor_path)

        save_key = ord('s')
        next_key = ord(' ')
        exit_key = 27
        crop_color = (0, 255, 0)

        # selected crops per image
        crop_dimensions = []
        crop_counts = 0

        f = open(descriptor_path, 'w+')

        for img in os.listdir(pos_images_path):
            path = pos_images_path + img
            rel_path = rel_dir + img

            try:
                original_image = cv2.imread(path)
                image = original_image.copy()
            except Exception as e:
                logger.error(str(e))
                break

            cv2.imshow('image', image)
            cv2.setMouseCallback('image', self.mouse_event)

            while True:
                cv2.imshow('image', image)
                key = cv2.waitKey(100)

                # Draw crop square
                if self.start is not None:
                    # Reset image before drawing another square
                    image = original_image.copy()
                    cv2.rectangle(image, self.start, self.dimension, crop_color)
                    cv2.imshow('image', image)

                # Keyboard input options
                if key == next_key:
                    # If image not cropped, assumes the whole image
                    if crop_counts == 0:
                        crop_counts = 1

                    f.write(rel_path + " " + str(crop_counts))
                    # If no cropped is saved, assume the whole image
                    if len(crop_dimensions) is 0:
                        x, y = 0, 0
                        w_x, h_y = original_image.shape[:2:]
                        img_dimension = "%d %d %d %d" % (x, y, w_x, h_y)
                        f.write(" " + img_dimension)
                    else:
                        for img_dimension in crop_dimensions:
                            f.write(" " + img_dimension)

                    f.write("\n")

                    self.start, self.dimension = None, None
                    crop_dimensions = []
                    crop_counts = 0

                    logger.info("Next image")
                    break

                elif key == save_key:
                    # Check if there is crop selection
                    if self.dimension is not None:
                        top_left_x, top_left_y = self.start
                        bottom_right_x, bottom_right_y = self.dimension
                    else:
                        top_left_x, top_left_y = 0, 0
                        bottom_right_x, bottom_right_y = original_image.shape[:2:]

                    string = "%d %d %d %d" % (top_left_x, top_left_y, bottom_right_x, bottom_right_y)

                    # Don's allow duplicates [most likely whole image saved multiple times
                    if string not in crop_dimensions:
                        logger.info("Saving to file: " + path)
                        crop_dimensions.append(string)
                        crop_counts += 1
                    else:
                        logger.debug("Duplicates not allowed")

                    # Reset Dimensions
                    self.start, self.dimension = None, None

                elif key == exit_key:
                    logger.info("Exiting")
                    f.close()
                    sys.exit(0)

        cv2.destroyAllWindows()
        f.close()
