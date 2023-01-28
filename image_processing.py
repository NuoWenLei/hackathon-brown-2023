from PIL import Image
import io, numpy as np


def image_to_byte_array(image: Image) -> bytes:

	im_resized_and_padded = image_resize_and_pad(image)

	# BytesIO is a fake file stored in memory
	imgByteArr = io.BytesIO()

	# image.save expects a file as a argument, passing a bytes io ins
	im_resized_and_padded.save(imgByteArr, format="jpeg")

	# seek start of file to allow read() from AWS
	imgByteArr.seek(0)

	# Turn the BytesIO object back into a bytes object
	return imgByteArr


def image_resize_and_pad(image: Image) -> Image:

	# stream to byte array to numpy array as uint8
	image_array = np.asarray(image, dtype=np.uint8)

	# pad image to form perfect square
	h, w, _ = image_array.shape

	if h > w:
		diff = h - w
		padded_image_array = np.uint8(np.pad(image_array,
		((0, 0),
		(diff // 2,
		(diff // 2) + (diff % 2)),
		(0, 0)),
		mode = "constant",
		constant_values = 0))

	if h == w:
		padded_image_array = image_array
	
	if h < w:
		diff = w - h
		padded_image_array = np.uint8(np.pad(image_array,
		((diff // 2,
		(diff // 2) + (diff % 2)),
		(0, 0),
		(0, 0)),
		mode = "constant",
		constant_values = 0))

	im = Image.fromarray(padded_image_array)

	# resize image to uniform size
	return im.resize((512, 512))