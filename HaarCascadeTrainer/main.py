import os
import DataRetriever as Trainer

# Links to retrive images from
pos_link = 'http://image-net.org/api/text/imagenet.synset.geturls?wnid=n09618957'
neg_link = 'http://image-net.org/api/text/imagenet.synset.geturls?wnid=n09287968'

# Directories
neg_dir = 'haar_cascades/Training/neg/'
pos_dir = 'haar_cascades/Training/pos/'

rel_path = 'imgs/'

neg_imgs_dir = neg_dir + 'imgs/'
pos_imgs_dir = pos_dir + 'imgs/'
bad_imgs = 'haar_cascades/bad_imgs/'

pos_descriptor_file = pos_dir + 'info.dat'
neg_descriptor_file = neg_dir + 'bg.txt'

file_type = '.jpg'

dr = Trainer.DataRetriever()

# dr.pull_files_link(neg_link, neg_imgs_dir, file_type, 1, (200, 200), 30)
# dr.remove_bad_imgs(neg_imgs_dir, bad_imgs)
# dr.negative(neg_descriptor_file, neg_imgs_dir, rel_path)

dr.pull_files_link(pos_link, pos_imgs_dir, file_type, 1, (100, 100), 2)
dr.remove_bad_imgs(pos_imgs_dir, bad_imgs)
dr.positive(pos_descriptor_file, pos_imgs_dir, rel_path)

# os.system(' > output.txt')