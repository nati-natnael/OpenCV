import haar_cascade_trainer as trainer
from utils import Executor as cmd

# -------------------------------------- Input Params ---------------------------------------------------
NEG_SIZE = (400, 400)
POS_SIZE = (24, 24)

W, H = POS_SIZE
STAGES = 10
NUM_POS = 1000
NUM_NEG = 1000
MIN_HIT_RATE = 0.995
FEATURE_TYPE = 'LBP'
RAM = 2048

POS_RAW = 'haar_cascades/Training/pos/raw_imgs/'
POS_CROPPED = 'haar_cascades/Training/pos/cropped/'
POS_DESCRIPTOR_DIR = 'haar_cascades/Training/training_samples/'

NEG_RAW = 'haar_cascades/Training/neg/raw_imgs/'
NEG_READY = 'haar_cascades/Training/neg/ready/'
NEG_DESCRIPTOR_FILE = 'bg.txt'

BAD_IMGS = 'haar_cascades/bad_imgs/'

VEC_PATH = 'positive.vec'
DATA_PATH = 'haar_cascades/haarcascades_xml/'
# -------------------------------------- End of Params ---------------------------------------------------

sample = trainer.DataRetriever()
pos_samp = trainer.PositiveSamples()

# -------------------------------------- Prepare Neg images ----------------------------------------------
# sample.prep_imgs(NEG_RAW, NEG_READY, NEG_SIZE)
# neg_num = sample.make_descriptor_file(NEG_DESCRIPTOR_FILE, NEG_READY)
# --------------------------------------------- End ------------------------------------------------------

# -------------------------------------- Prepare Pos images ----------------------------------------------
# sample.prep_imgs(POS_RAW, POS_CROPPED, POS_SIZE)
# sample.img_crop_helper(POS_RAW, POS_CROPPED)
# --------------------------------------------- End ------------------------------------------------------

# Creating info list for all images
# status = pos_samp.create_pos_images(POS_CROPPED,
#                                     POS_DESCRIPTOR_DIR,
#                                     '-bg %s' % NEG_DESCRIPTOR_FILE,
#                                     "-maxxangle 0.5",
#                                     "-maxyangle 0.5",
#                                     "-maxzangle 0.5",
#                                     "-num %d" % neg_num)
#
# img_count, merge_path = pos_samp.merge_samples(POS_DESCRIPTOR_DIR)

# cmd.exec_cmd('opencv_createsamples',
#              '-info ' + merge_path,
#              '-vec ' + VEC_PATH,
#              "-num %d" % img_count)

cmd.exec_cmd('opencv_traincascade',
             '-data ' + DATA_PATH,
             '-vec ' + VEC_PATH,
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
