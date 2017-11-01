# OpenCV
This framework is designed to make it easier and efficient to train for specific image.

# Requirements
    *path to executable and lib must be added to environment path
        Python 2
        numpy
        OpenCV

# Functionality Descriptions
## DataRetriever
	 prep_imgs
		Resize and grayscale images which required for training.

	 pull_files_link
		Pull images from online file that contain links of images.

	 remove_bad_imgs
		This function requires a sample of bad images to remove bad images from larger set of images.

	 make_descriptor_file
		Creates a descriptor file with path provided. Descriptor file is relative or absolute path of images. It is
		used by OpenCV create samples and train.

	 img_crop_helper
		Crop helper opens images from provided directory one by one in a window and marker to for drawing crop area.
		After desired crop area is selected, hit key 's' on the keyboard to save image and hit space bar to continue
		to next image. Multiple crops can be done on one image.

## PositiveSamples
	 create_pos_images
		For each positive image in provided directory, creates samples of positive image superimposed on all negative
		images using opencv_createsamples. Each positive samples will have their own directory with dedicated
		descriptor files.

	 merge_samples
		When working with more than one positive image and use them as training sample, It is necessary to have
		one descriptor file for all samples. This util merges all descriptor files for each positive image into
		one descriptor file.


# Recommendations
    - Number of negative images need be greater than number of positive images
    - If creating virtual samples, using create_samples, dimensions of positive images need to be smaller than negative images.
      positive images are being superimposed on negative images with virtual translations.
    -

# Recommended File Structure
    OpenCV [Top Dir]
        CascadeTrainer [This is where main event and scripts of trainer exist]
            cascadeTest [Test script Dir]
                pic_recognition_test.py [Test script to try trained data on a sample picture]
                vid_recognition_test.py [Test script to try trained data on a video (live)]

            haar_cascades [Data Dir]
                cascade_xml [Destination of trained xml data]
                training    [Raw data needed for training]
                    neg [Negative image dir]
                        raw   [Unprocessed neg image dir]
                        ready [Neg images ready for training]
                    pos [Positive image dir]
                        cropped [Cropped pos images dir]
                        raw     [Unprocessed pos images dir]
                        ready   [Pos images ready for training]

                    training_samples [Final images of pos imposed on neg dir. Descriptor files are created for each pos image. those descriptors are merged into one descriptor file]

            log [Created log files during runs are located here]

            utils [Utilities needed in the framework]
                execs  [Static executor class. executes commands on the command line]
                libs   [Needed library files that may not be found in the OpenCV packege]
                logger [Logger class]
            
        files [Optional - collection of positive images]


