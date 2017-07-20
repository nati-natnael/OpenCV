import cv2
import os
import numpy as np
from urllib import urlopen
from urllib import urlretrieve

link = 'http://image-net.org/api/text/imagenet.synset.geturls?wnid=n09618957'

def retriveLink(*args):
    """
    Download all files using the links included
    in path 'links'.

    :param links: Path containing links of files
    :param dir: download destination directory
    :param file_type: file type being downloaded
    :param file_pos: file name start position
    :return:
    """

    # Parse Args
    if len(args) == 4:
        links = args[0]
        dir = args[1]
        file_type = args[2]
        file_pos = args[3]
        how_many = float("inf")

    elif len(args) == 5:
        links = args[0]
        dir = args[1]
        file_type = args[2]
        file_pos = int(args[3])
        how_many = int(args[4])

    else:
        raise Exception("Illegal Argument Count")

    url = urlopen(links).read()

    count = 1
    file_num = file_pos
    for i in url.split('\n'):
        try:
            print i
            urlretrieve(i, dir + str(file_num) + file_type)
            file_num += 1
        except Exception as e:
            print(str(e))

        count += 1
        if count >= how_many:
            break


def removeBadImg(from_dir, bad_imgs_dir):
    """
    Removing Bad images in directory defined 'from_dir' that are the
    equal as images in directory 'bad_imgs_dir'.

    :param from_dir: Directory containing images to be cleaned
    :param bad_imgs_dir: Directory containing sample of bad images
    :return:
    """

    # Images to be tested
    for current in os.listdir(from_dir):
        current_path = from_dir + '\\' + str(current)
        # Known Bad images
        for bad_img in os.listdir(bad_imgs_dir):
            try:
                bad_img_path = bad_imgs_dir + '\\' + str(bad_img)
                cur = cv2.imread(current_path)
                bad = cv2.imread(bad_img_path)

                try:
                    cur_shape = cur.shape
                    bad_shape = bad.shape

                    if bad_shape == cur_shape and not (np.bitwise_xor(cur, bad).any()):
                        print("Removing ..." + current_path)
                        os.remove(current_path)

                except AttributeError:
                    print("Removing ..." + current_path)
                    os.remove(current_path)

            except Exception as e:
                print("Error: " + str(e))


retriveLink(link, "..\\files\\haar_cascades\\images\\", '.jpg', 1, 10)
removeBadImg("..\\files\\haar_cascades\\images\\", "..\\files\\haar_cascades\\bad_imgs\\")
