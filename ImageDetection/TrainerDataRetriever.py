import cv2
import os
import numpy as np
from urllib import urlopen
from urllib import urlretrieve


class TrainerDataRetriever(object):
    def __init__(self):
        pass

    def retrieveLink(*args):
        """
        Download files using the online image links included
        in img_path 'links'. when downloading images
        are converted to gray scale and sized to [100,100].

        PARAMS IN ORDER
        links: Path containing links of files
        dir: download destination directory
        file_type: file type being downloaded
        file_pos: file name start position
        :return:
        """

        if len(args) < 4:
            raise Exception("Illegal Argument Count")

        links = args[1]
        dir = args[2]
        file_type = args[3]
        file_pos = args[4]
        how_many = float("inf")
        img_size = (100, 100)

        # Parse Args
        if len(args) > 6:
            how_many = int(args[5])

        elif len(args) >= 7:
            how_many = int(args[5])
            img_size = args[6]

            if not isinstance(img_size, tuple):
                raise Exception("Illegal Argument Type: Size")

        else:
            raise Exception("Illegal Argument Count")

        try:
            url = urlopen(links).read()

            count = 1
            file_num = file_pos
            for i in url.split('\n'):
                try:
                    print i
                    img_path = dir + str(file_num) + file_type
                    urlretrieve(i, img_path)
                    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
                    img = cv2.resize(img, img_size)
                    cv2.imwrite(img_path, img)
                    file_num += 1
                except Exception as e:
                    print(str(e))

                count += 1
                if count >= how_many:
                    break

        except IOError as io_e:
            print(str(io_e))

    def removeBadImg(self, from_dir, bad_imgs_dir):
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

    def neg_imgs_descriptor(self, descriptor_path, imgs_path):
        """

        :param descriptor_path: image descriptor txt file path
        :param imgs_path: directory where images live
        :return:
        """

        f = open(descriptor_path, 'w+')
        for img in os.listdir(imgs_path):
            print("Writing file: " + imgs_path + img)
            path = imgs_path + img + '\n'
            path = path.replace("..\\", "")
            f.write(path)

        f.close()


# Test
link = 'http://image-net.org/api/text/imagenet.synset.geturls?wnid=n09618957'
m = TrainerDataRetriever()
# m.retrieveLink(link, "..\\files\\haar_cascades\\images\\", '.jpg', 1, 100, (200, 200))
# m.removeBadImg("..\\files\\haar_cascades\\images\\", "..\\files\\haar_cascades\\bad_imgs\\")
m.neg_imgs_descriptor("..\\files\\haar_cascades\\Training\\neg\\bg.txt", "..\\files\\haar_cascades\\images\\")
