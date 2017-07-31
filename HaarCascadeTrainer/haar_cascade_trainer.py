import os
import sys
import cv2
import numpy as np

from urllib import urlopen, urlretrieve
from utils import Logger
from utils import Executor

# CRITICAL - 50
# ERROR - 40
# WARNING - 30
# INFO - 20
# DEBUG - 10
logger = Logger('log\sample_creator')
logger.set_level(20)

ERROR_TOLERANCE = 20


class DataRetriever(object):
    def __init__(self):
        self.clicked = False
        self.start = None
        self.dimension = None

    @staticmethod
    def prep_imgs(imgs_dir, to_dir, img_size, *options):
        """
        Prepare images for training.
        resize and change to grayscale

        :param imgs_dir:
        :param to_dir:
        :param img_size:
        :param options:
        :return:
        """

        file_num = 0
        count = 0
        error_count = 0
        how_many = float("inf")

        if len(options) == 1:
            how_many = options[0]

        if not isinstance(img_size, tuple):
            raise Exception("Illegal Argument Type: Size")

        images = os.listdir(imgs_dir)
        for img in images:
            try:
                logger.info("Getting: " + img)

                img_from_path = imgs_dir + img
                img_to_path = to_dir + "IMG_" + str(file_num) + '.jpg'

                img = cv2.imread(img_from_path, cv2.IMREAD_GRAYSCALE)

                if img is not None:
                    img = cv2.resize(img, img_size)
                    cv2.imwrite(img_to_path, img)
                    file_num += 1
                else:
                    logger.error("Image Read Failed: " + img_from_path)
                    continue
            except Exception as e:
                logger.error(str(e))
                error_count += 1

                if error_count > ERROR_TOLERANCE:
                    raise Exception(str(e))

            count += 1
            if count >= how_many:
                break

        logger.info("Done Preparing")

    def pull_files_link(*args):
        """
        Download files using the online image links included
        in img_path 'links'.

        PARAMS IN ORDER
        links: Path containing links of files
        dir: download destination directory
        file_type: file type being downloaded
        file_pos: file name start position

        :param args:
        :return: how many pulled
        """

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

        logger.info("Pulling Files from link: %s" % links)
        count = 0

        # Parse Args
        if len(args) == 7:
            how_many = int(args[6])

        try:
            r = urlopen(links).read()

            file_num = file_pos
            links = r.split('\n')
            for link in links:
                try:
                    logger.info("Getting: " + link)

                    img_path = dir_path + "IMG_" + str(file_num) + file_type
                    urlretrieve(link, img_path)
                except Exception as e:
                    logger.error(str(e))

                count += 1
                if count >= how_many:
                    break

        except IOError as io_e:
            logger.error(str(io_e))

        logger.info("Done pulling files")
        return count

    @staticmethod
    def remove_bad_imgs(from_dir, bad_imgs_dir):
        """
        Removing Bad images from directory defined 'from_dir' that are
        equal to bad images included in directory 'bad_imgs_dir'.

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

        logger.info("Done removing bad images")

    @staticmethod
    def make_descriptor_file(descriptor_path, imgs_dir):
        """
        Make a descriptor txt file.

        :param descriptor_path: path to descriptor file
        :param imgs_dir: path to neg images
        :return: number of images
        """

        logger.info("Making descriptor file: %s" % descriptor_path)

        counter = -1

        try:
            f = open(descriptor_path, 'w+')
            logger.debug("File opened. Path: %s" % descriptor_path)
        except OSError as e:
            logger.error("Error Opening file: " + str(e))
            return counter

        try:
            img_lst = os.listdir(imgs_dir)
        except OSError as e:
            logger.error("Error atempting to list files in dir: %s - %s" % (imgs_dir, str(e)))
            return counter

        for img in img_lst:
            logger.info('Writing file: ' + imgs_dir + img)
            f.write(imgs_dir + img + '\n')
            counter += 1

        f.close()
        return counter

    def __mouse_event(self, event, x, y, flags, param):
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

        wait_time = 100

        # Valid Keys
        save_key = ord('s')
        next_key = ord(' ')
        exit_key = 27

        # Rect colors
        crop_color = (0, 0, 255)
        crop_saved_color = (0, 255, 0)

        # selected crops per image
        crop_count = 0

        img_lst = os.listdir(images_path)
        for img in img_lst:
            try:
                original_image = cv2.imread(images_path + img)
                image = original_image.copy()
            except Exception as e:
                logger.error(str(e))
                break

            cv2.imshow('image', image)
            cv2.setMouseCallback('image', self.__mouse_event)

            # Event loop
            while True:
                cv2.imshow('image', image)
                key = cv2.waitKey(wait_time)

                # Draw crop square
                if self.start is not None:
                    # Reset image before drawing another square
                    image = original_image.copy()
                    cv2.rectangle(image, self.start, self.dimension, crop_color)
                    cv2.imshow('image', image)

                # GO to next image
                if key == next_key:
                    self.start, self.dimension = None, None
                    crop_count = 0

                    logger.info("Next image")
                    break

                # Save the selection
                elif key == save_key:
                    if self.start is not None:
                        top_x, top_y = self.start
                        bottom_x, bottom_y = self.dimension

                        save_img = original_image[top_y:bottom_y, top_x:bottom_x]
                        save_path = save_to + img.replace('.', '_' + str(crop_count) + '.')

                        cv2.imwrite(save_path, save_img)

                        # Changed rect color to green indicating save action
                        cv2.rectangle(image, self.start, self.dimension, crop_saved_color)
                        self.start, self.dimension = None, None

                        crop_count += 1

                        logger.debug("Image saved: " + save_path)
                    else:
                        logger.warning("Please select an area to save")

                # Abort
                elif key == exit_key:
                    logger.info("Exiting")
                    sys.exit(0)

        cv2.destroyAllWindows()
        logger.info("Done cropping")


class PositiveSamples(object):
    """

    """

    def __init__(self):
        pass

    @staticmethod
    def create_pos_images(imgs_dir, top_info_dir, *options):
        """

        :param imgs_dir:
        :param top_info_dir:
        :param options:
        :return:
        """

        logger.info("Creating positive samples ...")
        info_count = 0

        try:
            img_lst = os.listdir(imgs_dir)
        except Exception as e:
            logger.error(str(e))
            return False

        for img in img_lst:
            img_path = imgs_dir + img
            logger.debug(img_path)

            # make dir for every pos image
            try:
                os.mkdir(top_info_dir + '/info_' + str(info_count))
            except OSError:
                logger.debug("Directory already exists")

            info_path = top_info_dir + 'info_' + str(info_count) + '/info_' + str(info_count) + '.lst'
            logger.debug("Info Path: " + info_path)

            executable = 'opencv_createsamples ' + \
                         '-img ' + img_path + ' ' + \
                         '-info ' + info_path

            if not Executor.exec_cmd(executable, *options):
                logger.error("Command Failed for Image: " + img_path)
                return False

            info_count += 1

        logger.info("Done creating positive image samples")
        return True

    @staticmethod
    def merge_samples(top_info_dir):
        """
        merge info.lst files in to one.
        <p>
        Note: it will only work if create_pos_samples()
        function is used to create the data sets
        and their own info directory.
        :return merged_info file path
        """
        logger.info("Running Merger ...")
        merged_info = 'merged_info.lst'
        merged_info_path = top_info_dir + merged_info

        line_counter = -1

        # remove old merge file if it exists
        try:
            os.remove(top_info_dir + merged_info)
            logger.debug("Old merge file deleted")
        except OSError:
            logger.debug("Old merge file not found. Delete not needed :)")

        try:
            info_dir_list = os.listdir(top_info_dir)
        except OSError as os_e:
            logger.error(str(os_e))
            return [line_counter, merged_info_path]

        try:
            f = open(merged_info_path, 'w+')
        except IOError as e:
            logger.error(str(e))
            return [line_counter, merged_info_path]

        for info_dir in info_dir_list:
            logger.info("Reading: " + info_dir + "...")

            # Only one info file per info directory
            info_path = top_info_dir + info_dir + '/' + info_dir + '.lst'
            logger.debug("Info Path: " + info_path)

            try:
                info_f = open(info_path, 'r')
                info_r = info_f.read()
            except IOError as e:
                logger.error(str(e))
                logger.debug("Failed to open or read: " + info_path)
                break

            lines = info_r.split('\n')
            logger.debug("Split lines: " + str(lines))

            for line in lines:
                if line is not '':
                    f.write(info_dir + '/' + line + '\n')

                    line_counter += 1

        logger.info("Done Merging")
        return [line_counter, merged_info_path]
