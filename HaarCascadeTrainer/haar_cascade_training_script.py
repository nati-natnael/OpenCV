import haar_cascade_trainer as trainer
from utils import exec_cmd

# -------------------------------------- Input Params ---------------------------------------------------
NEG_SIZE = (200, 200)
POS_SIZE = (100, 100)

NEG_START = 1
POS_START = 1

NEG_HOW_MANY = 50
POS_HOW_MANY = 50

POS_LINK = 'http://image-net.org/api/text/imagenet.synset.geturls?wnid=n09618957'
POS_RAW = 'haar_cascades/Training/pos/raw_imgs/'
POS_CROPPED = 'haar_cascades/Training/pos/cropped/'
POS_DESCRIPTOR_DIR = 'haar_cascades/Training/training_samples/'

NEG_LINK_1 = 'http://image-net.org/api/text/imagenet.synset.geturls?wnid=n09287968'
NEG_LINK_2 = 'http://image-net.org/api/text/imagenet.synset.geturls?wnid=n03528263'  # home appliances
NEG_RAW = 'haar_cascades/Training/neg/raw_imgs/'
NEG_DESCRIPTOR_FILE = 'haar_cascades/Training/neg/bg.txt'

BAD_IMGS = 'haar_cascades/bad_imgs/'
REL_PATH = 'raw_imgs/'

VEC_PATH = 'haar_cascades/Training/training_samples/positive.vec'
DATA_PATH = '/haar_cascades/haarcascade_xml/'

FILE_TYPE = '.jpg'
# -------------------------------------- End of Params ---------------------------------------------------

neg_samp = trainer.DataRetriever()
pos_samp = trainer.PositiveSamples(NEG_DESCRIPTOR_FILE, POS_DESCRIPTOR_DIR)

# -------------------------------------- Prepare Neg images ----------------------------------------------
neg_samp.pull_files_link(NEG_LINK_1, NEG_RAW, FILE_TYPE, NEG_START, NEG_SIZE, NEG_HOW_MANY)  # link 1
neg_samp.pull_files_link(NEG_LINK_2, NEG_RAW, FILE_TYPE, NEG_START, NEG_SIZE, NEG_HOW_MANY)  # link 2
neg_samp.remove_bad_imgs(NEG_RAW, BAD_IMGS)
neg_num = neg_samp.make_descriptor_file(NEG_DESCRIPTOR_FILE, NEG_RAW, REL_PATH)
# --------------------------------------------- End ------------------------------------------------------

# -------------------------------------- Prepare Pos images ----------------------------------------------
neg_samp.pull_files_link(POS_LINK, POS_RAW, FILE_TYPE, POS_START, POS_SIZE, POS_HOW_MANY)
neg_samp.img_crop_helper(POS_RAW, POS_CROPPED)
# --------------------------------------------- End ------------------------------------------------------

# Creating info list for all images
status = pos_samp.create_pos_images(POS_CROPPED,
                                    "-maxxangle 0.5",
                                    "-maxyangle 0.5",
                                    "-maxzangle 0.5",
                                    "-num %d" % neg_num)

if status:
    img_count, merge_path = pos_samp.merge_samples()
    if img_count > 0:
        status = pos_samp.create_pos_vec(merge_path, VEC_PATH, "-num %d" % img_count)
        if status:
            exec_cmd("opencv_traincascade ",
                     "-data " + DATA_PATH,
                     "-vec " + VEC_PATH,
                     "-bg " + NEG_DESCRIPTOR_FILE,
                     "-numPos %d" % 1,
                     "-numNeg %d" % 2,
                     "-numStages %d " % 3,
                     "-w %d" % 4,
                     "-h %d" % 5)


    # def create_pos_vec(self, info_path, vec_name, *options):
    #     """
    #     options available:
    #         -num <number_of_samples>
    #         -w <sample_width>
    #         -h <sample_height>
    #     :param info_path: descriptor file for all pos images
    #     :param vec_name: name of the vector file. will be saved in top_info_dir
    #     :param options: optional vars
    #     :return:
    #     """
    #     cmd = 'opencv_createsamples ' + \
    #           '-info ' + info_path + ' ' + \
    #           '-vec ' + self.top_info_dir + vec_name
    #
    #     for option in options:
    #         cmd = cmd + ' ' + option
    #
    #     logger.debug("Executing Command: " + cmd)
    #     exit_status = os.system(cmd)
    #     return exit_status is 0