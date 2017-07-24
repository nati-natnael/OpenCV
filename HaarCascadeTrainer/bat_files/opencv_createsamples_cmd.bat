SET IMG_PATH="../haar_cascades/Training/pos/imgs/img2.jpg"
SET BG_PATH="../haar_cascades/Training/neg/bg.txt"
SET INFO_PATH="../haar_cascades/Training/training_samples/info.lst"

SET MAX_ANGLE=0.5

SET NUM=20

opencv_createsamples^
	-img %IMG_PATH%^
	-bg %BG_PATH%^
	-info %INFO_PATH%^
	-maxxangle %MAX_ANGLE%^
	-maxyangle %MAX_ANGLE%^
	-maxzangle %MAX_ANGLE%^
	-num %NUM%