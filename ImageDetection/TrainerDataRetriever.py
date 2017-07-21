import cv2
import os
import numpy as np
import sys
from urllib import urlopen
from urllib import urlretrieve


class TrainerDataRetriever(object):
    def __init__(self):
        self.clicked = False
        self.start = None
        self.dimension = None
        pass

    def pullFiles(*args):
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

        if len(args) < 5:
            raise Exception("Illegal Argument Count")

        links = args[1]
        dir = args[2]
        file_type = args[3]
        file_pos = args[4]
        how_many = float("inf")
        img_size = (100, 100)

        # Parse Args
        if len(args) == 6:
            how_many = int(args[5])

        elif len(args) == 7:
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
                    img_path = dir + "img" + str(file_num) + file_type
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

    def negative(self, descriptor_path, imgs_path):
        """
        Make a descriptor txt file for data sets

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

    def mouse_clicked(self, event, x, y, flags, param):
        """

        :param event:
        :param x:
        :param y:
        :param flags:
        :param param:
        :return:
        """

        if event == cv2.EVENT_LBUTTONDOWN:
            self.clicked = True
            self.start = (x, y)
            print("Left Mouse Button clicked: (x, y) => " + str(x) + ", " + str(y))

        elif event == cv2.EVENT_LBUTTONUP:
            print("Left Mouse Button Relesed")
            self.clicked = False
            self.start = None
            self.dimension = None

        elif event == cv2.EVENT_MOUSEMOVE and self.clicked:
            self.dimension = (x, y)
            print("Mouse Dragged: (x, y) => " + str(self.dimension))

        pass

    def mouse_dragged(self, event, x, y, flags, param):
        if event == cv2.EVENT_MOUSEMOVE and self.clicked:
            print("mouse Moved")
        pass

    def positive(self, desciptor_path, imgs_path):
        """

        :param desciptor_path:
        :param imgs_path:
        :return:
        """

        crop_color = (0, 255, 0)

        for img in os.listdir(imgs_path):
            path = imgs_path + img
            image = cv2.imread(path)

            cv2.imshow('image', image)
            cv2.setMouseCallback('image', self.mouse_clicked)

            while True:
                cv2.imshow('image', image)
                key = cv2.waitKey(100)

                if self.start is not None:
                    cv2.rectangle(image, self.start, self.dimension, crop_color)
                    cv2.imshow('image', image)

                if key == ord(' '):
                    print("Going to next image")
                    self.start = None
                    self.dimension = None
                    break

                elif key == 27:
                    print("Exiting")
                    sys.exit(0)

        cv2.destroyAllWindows()


# Test
link = 'http://image-net.org/api/text/imagenet.synset.geturls?wnid=n09618957'
m = TrainerDataRetriever()
# m.pullFiles(link, "..\\files\\haar_cascades\\images\\", '.jpg', 1, 20, (200, 200))
# m.removeBadImg("..\\files\\haar_cascades\\images\\", "..\\files\\haar_cascades\\bad_imgs\\")
# m.negative("..\\files\\haar_cascades\\Training\\neg\\bg.txt", "..\\files\\haar_cascades\\images\\")
m.positive("..\\files\\haar_cascades\\Training\\neg\\bg.txt", "..\\files\\haar_cascades\\images\\")
