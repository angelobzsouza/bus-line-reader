# coding: utf-8
import utils
import sys
import attempts

# Create images
image = utils.openImage(sys.argv[1])
binaryOrangeImage = utils.binaryByOrange(image)
binaryOrangeDilatedImage = utils.dilateBinary(binaryOrangeImage, 5)
binaryWhiteImage = utils.binaryByWhite(image)
binaryWhiteDilatedImage = utils.dilateBinary(binaryWhiteImage, 3)

attempts.localAttempt(binaryOrangeImage, 'Binarização com laranja')
attempts.localAttempt(binaryOrangeDilatedImage, 'Dilatação e binarização por laranja')
attempts.cloudAttempt(binaryOrangeImage, 'BinaryOrangeImage', 'Binarização com laranja na cloud')
attempts.cloudAttempt(binaryOrangeDilatedImage, 'BinaryOrangeDilatedImage', 'Dilatação e binarização com laranja na cloud')
attempts.cloudAttempt(binaryWhiteImage, 'BinaryWhiteImage', 'Binarização com branco na cloud')
attempts.cloudAttempt(binaryWhiteDilatedImage, 'BinaryWhiteDiletedImage', 'Dilatação e binarização com branco na cloud')
attempts.cloudAttempt(image, 'NormalImage', 'Imagem normal na cloud')