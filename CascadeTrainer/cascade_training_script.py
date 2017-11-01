from trainer import cascade_trainer as trainer
from utils.execs.cmd_executor import Executor

# -------------------------------------- Input Params ---------------------------------------------------
# Sizes of images. Pos images need to fit inside of negative images.
# The bigger the image the longer it takes to train.
NEG_SIZE = (80, 80)
POS_SIZE = (50, 50)
W, H = POS_SIZE  # Width and Height of pos image

STAGES = 20  # Desired cascade stages

# Number of pos and neg images. This can affect the quality of the trained detector
NUM_POS = 40
NUM_NEG = 600

MIN_HIT_RATE = 0.999  # Desired Accuracy

# Type of cascade training
FEATURE_TYPE = 'HAAR'  # 'LBP'

RAM = 1024  # Amount of ram designated for training.

# ----------- POS Dirs ---------------------------------
POS_RAW = 'haar_cascades\\Training\\pos\\raw\\'                     # Original Positive images Dir
POS_CROPPED = 'haar_cascades\\Training\\pos\\cropped\\'             # Cropped Images Dir
POS_READY = 'haar_cascades\\Training\\pos\\ready\\'                 # Ready Positive Images Dir
POS_DESCRIPTOR_DIR = 'haar_cascades\\training\\training_samples\\'  # Descriptor file of positive images
# ------------- End of POS --------------------------------

# -------------- Neg Dirs ---------------------------------
NEG_RAW = 'haar_cascades\\training\\neg\\raw\\'
NEG_READY = 'haar_cascades\\training\\neg\\ready\\'
NEG_DESCRIPTOR_FILE = 'bg.txt'
# ------------ End of Neg Dir ------------------------------

# If bad images need to be filtered. place sample of bad images here.
BAD_IMGS = 'haar_cascades\\bad_imgs\\'

# Path of positive Vector file
VEC_PATH = 'positive.vec'

# Destination of final result [trained cascade]
DATA_PATH = 'haar_cascades\\cascade_xml\\'
# -------------------------------------- End of Params ---------------------------------------------------

sample = trainer.DataRetriever()
pos_samp = trainer.PositiveSamples()

# -------------------------------------- Prepare Neg images ----------------------------------------------
# sample.remove_bad_imgs(NEG_RAW, BAD_IMGS)  # uncomment if there are bad imgs to be cleaned
sample.prep_imgs(NEG_RAW, NEG_READY, NEG_SIZE, NUM_NEG)
sample.make_descriptor_file(NEG_DESCRIPTOR_FILE, NEG_READY)
# --------------------------------------------- End ------------------------------------------------------

# -------------------------------------- Prepare Pos images ----------------------------------------------
sample.img_crop_helper(POS_RAW, POS_CROPPED)        # helps for cropping pos images
sample.prep_imgs(POS_CROPPED, POS_READY, POS_SIZE)
# --------------------------------------------- End ------------------------------------------------------

# Creating info list for all images
status = pos_samp.create_pos_images(POS_READY,
                                    POS_DESCRIPTOR_DIR,
                                    '-bg %s' % NEG_DESCRIPTOR_FILE,
                                    '-w %d' % W,
                                    '-h %d' % H,
                                    '-bgcolor 255',
                                    '-bgthresh 0',
                                    '-maxxangle 1.1 -maxyangle 1.1 -maxzangle 0.5'
                                    '-maxidev 40',
                                    "-num %d" % NUM_NEG)
#
img_count, merge_path = pos_samp.merge_samples(POS_DESCRIPTOR_DIR)

Executor.exec_cmd('opencv_createsamples',
                  '-info ' + merge_path,
                  '-vec ' + VEC_PATH,
                  '-w %d' % W,
                  '-h %d' % H,
                  '-bgcolor 255',
                  '-bgthresh 0',
                  '-maxxangle 1.1',
                  '-maxyangle 1.1',
                  '-maxzangle 0.5',
                  '-maxidev 40',
                  "-num %d" % img_count)

"""
Haar training begins here. using the samples created.
"""
Executor.exec_cmd('opencv_traincascade',
                  '-data %s' % DATA_PATH,
                  '-vec %s' % VEC_PATH,
                  '-bg ' + NEG_DESCRIPTOR_FILE,
                  '-numPos %d' % NUM_POS,
                  '-numNeg %d' % NUM_NEG,
                  '-numStages %d' % STAGES,
                  'inHitRate %.3f' % MIN_HIT_RATE,
                  '-w %d' % W,
                  '-h %d' % H,
                  '-featureType %s' % FEATURE_TYPE,
                  '-precalcValBufSize %d' % RAM,
                  '-precalcIdxBufSize %d' % RAM)
