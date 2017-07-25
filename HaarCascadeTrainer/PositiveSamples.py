import os
import sys
from utils.logger import Logger

logger = Logger('log/pos_sample_creater')
logger.set_level(20)


def create_pos_sample(img_dir, bg_path, info_path, *options):
    """
    options Available:
        -num <number_of_samples>
        -bgcolor <background_color>
        -bgthresh <background_color_threshold>
        -inv
        -randinv
        -maxidev <max_intensity_deviation>
        -maxxangle <max_x_rotation_angle>
        -maxyangle <max_y_rotation_angle>
        -maxzangle <max_z_rotation_angle>
        -show
        -w <sample_width>
        -h <sample_height>

    :param img_dir:
    :param bg_path:
    :param info_path:
    :param options:
    :return:
    """
    cmd = 'opencv_createsamples ' + \
          '-img ' + img_dir + ' ' + \
          '-bg ' + bg_path + ' ' + \
          '-info ' + info_path

    for option in options:
        cmd = cmd + ' ' + option

    logger.debug("Command: " + cmd)
    exit_status = os.system(cmd)
    return exit_status is 0


class PositiveSamples(object):
    """

    """

    def __init__(self, imgs_dir, bg_path, info_dir):
        """

        :param imgs_dir:
        :param bg_path:
        :param info_dir:
        """
        self.imgs_dir = imgs_dir
        self.bg_path = bg_path
        self.top_info_dir = info_dir

    def create_pos_samples(self, *options):
        """

        :param options:
        :return:
        """

        logger.info("Creating positive samples ...")
        info_count = 0

        try:
            img_lst = os.listdir(self.imgs_dir)
        except Exception as e:
            logger.error(str(e))
            sys.exit(1)

        for img in img_lst:
            img_path = self.imgs_dir + img
            logger.debug(img_path)

            # make dir for every pos image
            try:
                os.mkdir(self.top_info_dir + '/info_' + str(info_count))
            except OSError:
                logger.debug("Directory already exists")

            info_path = self.top_info_dir + '/info_' + str(info_count) + '/info_' + str(info_count) + '.lst'
            logger.debug("Info Path: " + info_path)

            if not create_pos_sample(img_path, self.bg_path, info_path, *options):
                logger.debug("Command Failed for Image: " + img_path)
                break

            info_count += 1

        logger.info("Done creating positive image samples")

    def merge_samples(self):
        """
        merge info.lst files in to one.
        <p>
        Note: it will only work if create_pos_samples()
        function is used to create the data sets
        and their info file.
        """
        logger.info("Running Merger ...")
        merged_info = 'merged_info.lst'

        # remove old merge file if it exists
        try:
            os.remove(self.top_info_dir + merged_info)
            logger.debug("Old merge file deleted")
        except OSError:
            logger.debug("Old merge file not found. Delete not needed :)")

        try:
            info_dir_list = os.listdir(self.top_info_dir)
        except OSError as os_e:
            logger.error(str(os_e))
            sys.exit(1)

        try:
            f = open(self.top_info_dir + merged_info, 'w+')
        except IOError as e:
            logger.error(str(e))
            sys.exit(1)

        for info_dir in info_dir_list:
            logger.info("Reading: " + info_dir + "...")

            # Only one info file per info directory
            info_path = self.top_info_dir + info_dir + '/' + info_dir + '.lst'
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

            # line_counter = 0
            # lines_len = len(lines)
            for line in lines:
                if line is not '':
                    f.write(info_dir + '/' + line + '\n')

                # line_counter += 1

        logger.info("Done Merging")
