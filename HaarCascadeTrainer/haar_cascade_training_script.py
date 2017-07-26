import haar_cascade_trainer as trainer

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

NEG_LINK = 'http://image-net.org/api/text/imagenet.synset.geturls?wnid=n09287968'
NEG_RAW = 'haar_cascades/Training/neg/raw_imgs/'
NEG_DESCRIPTOR_FILE = 'haar_cascades/Training/neg/bg.txt'

BAD_IMGS = 'haar_cascades/bad_imgs/'
REL_PATH = 'raw_imgs/'

VEC_PATH = 'haar_cascades/Training/training_samples/positive.vec'
DATA_PATH = '/haar_cascades/haarcascade_xml/'

FILE_TYPE = '.jpg'
# -------------------------------------- End of Params ---------------------------------------------------

dr = trainer.DataRetriever()
ex = trainer.PositiveSamples(NEG_DESCRIPTOR_FILE, POS_DESCRIPTOR_DIR)
tr = trainer.TrainCascade(DATA_PATH, VEC_PATH)

# -------------------------------------- Prepare Neg images ----------------------------------------------
dr.pull_files_link(NEG_LINK, NEG_RAW, FILE_TYPE, NEG_START, NEG_SIZE, NEG_HOW_MANY)
dr.remove_bad_imgs(NEG_RAW, BAD_IMGS)
neg_num = dr.make_descriptor_file(NEG_DESCRIPTOR_FILE, NEG_RAW, REL_PATH)
# --------------------------------------------- End ------------------------------------------------------

# -------------------------------------- Prepare Pos images ----------------------------------------------
dr.pull_files_link(POS_LINK, POS_RAW, FILE_TYPE, POS_START, POS_SIZE, POS_HOW_MANY)
dr.img_crop_helper(POS_RAW, POS_CROPPED)
# --------------------------------------------- End ------------------------------------------------------

# Creating info list for all images
status = ex.create_pos_images(POS_CROPPED,
                              "-maxxangle 0.5",
                              "-maxyangle 0.5",
                              "-maxzangle 0.5",
                              "-num %d" % neg_num)

if status:
    img_count, merge_path = ex.merge_samples()
    if img_count > 0:
        status = ex.create_pos_vec(merge_path, 'positive.vec', "-num %d" % img_count)
        if status:
            print("Train Cascade")
