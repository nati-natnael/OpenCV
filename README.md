# OpenCV
This framework is designed to make it easier and efficient to train for specific image.

# Requirements
    Python 2 - path to executable and lib must be added to environment path
    OpenCV   - path to executable must be added to environment path

# File Structure
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


