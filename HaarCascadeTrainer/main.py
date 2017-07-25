import DataRetriever as Trainer
import PositiveSamples as pos

# Links to retrive images from
pos_link = 'http://image-net.org/api/text/imagenet.synset.geturls?wnid=n09618957'
neg_link = 'http://image-net.org/api/text/imagenet.synset.geturls?wnid=n09287968'

# Directories
neg_dir = 'haar_cascades/Training/neg/'
pos_dir = 'haar_cascades/Training/pos/'

# Path relative to descriptor files
rel_path = 'raw_imgs/'

# Raw images Dir
neg_imgs_dir = neg_dir + 'raw_imgs/'
pos_imgs_dir = pos_dir + 'raw_imgs/'

# Bad images Dir
bad_imgs = 'haar_cascades/bad_imgs/'

# Positive and negative samples ready for training
pos_descriptor_dir = 'haar_cascades/Training/training_samples/'
neg_descriptor_file = neg_dir + 'bg.txt'

# File Types being pulled from online
file_type = '.jpg'

# Retrieve Neg Data
dr = Trainer.DataRetriever()
# dr.pull_files_link(neg_link, neg_imgs_dir, file_type, 1, (200, 200), 100)
# dr.remove_bad_imgs(neg_imgs_dir, bad_imgs)
# dr.negative(neg_descriptor_file, neg_imgs_dir, rel_path)
#
# # Retrieve Pos Data
# dr.pull_files_link(pos_link, pos_imgs_dir, file_type, 1, (100, 100), 10)
# dr.remove_bad_imgs(pos_imgs_dir, bad_imgs)
dr.img_crop_helper(pos_imgs_dir, pos_dir + 'cropped/')

# Creating samples
# ex = pos.PositiveSamples(pos_dir + 'cropped/', neg_descriptor_file, pos_descriptor_dir)
#
# ex.create_pos_samples("-maxxangle 0.5",
#                       "-maxyangle 0.5",
#                       "-maxzangle 0.5",
#                       "-num 90")
# ex.merge_samples()
