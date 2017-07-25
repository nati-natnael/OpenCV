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

    @staticmethod
    def remove_bad_imgs(from_dir, bad_imgs_dir):
        """
        Removing Bad images in directory defined 'from_dir' that are the
        equal as images in directory 'bad_imgs_dir'.

        :param from_dir: Directory containing images to be cleaned
        :param bad_imgs_dir: Directory containing sample of bad images
        :return:
        """

        logger.debug("Removing bad image from %s" % from_dir)
        # Images to be tested
        test_img_lst = os.listdir(from_dir)
        for current in test_img_lst:
            current_path = from_dir + '/' + str(current)

            # Known Bad images
            bad_img_lst = os.listdir(bad_imgs_dir)
            for bad_img in bad_img_lst:
                try:
                    bad_img_path = bad_imgs_dir + '/' + str(bad_img)
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

    @staticmethod
    def make_descriptor_file(descriptor_path, imgs_path, rel_path):
        """
        Make a descriptor txt file for

        :param descriptor_path: path to descriptor file
        :param imgs_path: path to neg images
        :param rel_path: relative path of images from descriptor path
        :return:
        """

        logger.info("Making Neg descriptor file: %s" % descriptor_path)

        try:
            f = open(descriptor_path, 'w+')
            logger.debug("File opened. Path: %s" % descriptor_path)
        except OSError as e:
            logger.error("Error Opening file: " + str(e))
            sys.exit(1)

        try:
            img_lst = os.listdir(imgs_path)
        except OSError as e:
            logger.error("Error atempting to list files in dir: %s - %s" % (imgs_path, str(e)))
            sys.exit(1)

        for img in img_lst:
            logger.info('Writing file: ' + imgs_path + img)
            f.write(rel_path + img + '\n')

        f.close()

    def mouse_event(self, event, x, y, flags, param):
        """
        Mouse Event
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

    def img_crop_helper(self, images_path, save_to):
        """
        Help crop images

        :param images_path: raw images found here
        :param save_to: save cropped images here
        :return:
        """

        logger.info("Cropping Images")

        WAIT_TIME = 100

        # Valid Keys
        SAVE_KEY = ord('s')
        NEXT_KEY = ord(' ')
        EXIT_KEY = 27

        # Rect colors
        CROP_COLOR = (0, 0, 255)
        CROP_SAVED_COLOR = (0, 255, 0)

        # selected crops per image
        CROP_COUNT = 0

        img_lst = os.listdir(images_path)
        for img in img_lst:
            try:
                original_image = cv2.imread(images_path + img)
                image = original_image.copy()
            except Exception as e:
                logger.error(str(e))
                break

            cv2.imshow('image', image)
            cv2.setMouseCallback('image', self.mouse_event)

            # Event loop
            while True:
                cv2.imshow('image', image)
                key = cv2.waitKey(WAIT_TIME)

                # Draw crop square
                if self.start is not None:
                    # Reset image before drawing another square
                    image = original_image.copy()
                    cv2.rectangle(image, self.start, self.dimension, CROP_COLOR)
                    cv2.imshow('image', image)

                # GO to next image
                if key == NEXT_KEY:
                    self.start, self.dimension = None, None
                    CROP_COUNT = 0

                    logger.info("Next image")
                    break

                # Save the selection
                elif key == SAVE_KEY:
                    if self.start is not None:
                        top_x, top_y = self.start
                        bottom_x, bottom_y = self.dimension

                        save_img = original_image[top_y:bottom_y, top_x:bottom_x]
                        save_path = save_to + img.replace('.', '_' + str(CROP_COUNT) + '.')

                        cv2.imwrite(save_path, save_img)

                        # Changed rect color to green indicating save action
                        cv2.rectangle(image, self.start, self.dimension, CROP_SAVED_COLOR)
                        self.start, self.dimension = None, None

                        CROP_COUNT += 1

                        logger.debug("Image saved: " + save_path)
                    else:
                        logger.warning("Please select an area to save")

                # Abort
                elif key == EXIT_KEY:
                    logger.info("Exiting")
                    sys.exit(0)

        cv2.destroyAllWindows()
        logger.info("Done cropping")
