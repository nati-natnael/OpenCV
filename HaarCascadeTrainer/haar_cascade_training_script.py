import haar_cascade_trainer as trainer
from utils.execs.cmd_executor import Executor

# -------------------------------------- Input Params ---------------------------------------------------
NEG_SIZE = (50, 50)
POS_SIZE = (25, 25)

W, H = POS_SIZE
STAGES = 10
NUM_POS = 2800
NUM_NEG = 1000
MIN_HIT_RATE = 0.995
FEATURE_TYPE = 'HAAR'  # 'LBP'
RAM = 1024

NEG_LINK = 'http://image-net.org/api/text/imagenet.synset.geturls?wnid=n00007846'

POS_RAW = 'haar_cascades/Training/pos/raw_imgs/'
POS_CROPPED = 'haar_cascades/Training/pos/cropped/'
POS_DESCRIPTOR_DIR = 'haar_cascades/Training/training_samples/'

NEG_RAW = 'haar_cascades/Training/neg/raw_imgs/'
NEG_READY = 'haar_cascades/Training/neg/ready/'
NEG_DESCRIPTOR_FILE = 'bg.txt'

BAD_IMGS = 'haar_cascades/bad_imgs/'

VEC_PATH = 'positive.vec'
DATA_PATH = 'haar_cascades/haarcascade_xml/'
# -------------------------------------- End of Params ---------------------------------------------------

sample = trainer.DataRetriever()
pos_samp = trainer.PositiveSamples()

# -------------------------------------- Prepare Neg images ----------------------------------------------
# sample.pull_files_link(NEG_LINK, NEG_RAW, '.jpg', 8827, 1177)
sample.remove_bad_imgs(NEG_RAW, BAD_IMGS)
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
# #
# img_count, merge_path = pos_samp.merge_samples(POS_DESCRIPTOR_DIR)
# #
# Executor.exec_cmd('opencv_createsamples',
#                   '-info ' + merge_path,
#                   '-vec ' + VEC_PATH,
#                   '-w %d' % W,
#                   '-h %d' % H,
#                   "-num %d" % img_count)
#
# Executor.exec_cmd('opencv_traincascade',
#                   '-data %s' % DATA_PATH,
#                   '-vec %s' % VEC_PATH,
#                   '-bg ' + NEG_DESCRIPTOR_FILE,
#                   '-numPos %d' % NUM_POS,
#                   '-numNeg %d' % NUM_NEG,
#                   '-numStages %d' % STAGES,
#                   'inHitRate %.3f' % MIN_HIT_RATE,
#                   '-w %d' % W,
#                   '-h %d' % H,
#                   '-featureType %s' % FEATURE_TYPE,
#                   '-precalcValBufSize %d' % RAM,
#                   '-precalcIdxBufSize %d' % RAM)
