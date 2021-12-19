""" Image manipulation 

Edge cases:
JPG:
	01. jpg to jpeg  - works
	02. jpg to png  - works
	03. jpg to webp - works
	04. jpg to svg  - ValueError: Unknown file extension: .svg

PNG:
	05. png to png  - works
	06. png to jpeg  - OSError: cannot write mode RGBA as JPEG
		#Error is because png and webp has image format as RGBA while jpg has only RGB
	07. png to webp - works
	08. png to svg  - ValueError: Unknown file extension: .svg
	
WEBP: 
	09. webp to webp - works
	10. webp to jpeg  - OSError: cannot write mode RGBA as JPEG
	11. webp to png  - works
	12. webp to svg  - ValueError: Unknown file extension: .svg

SVG:
	13. svg to svg  - PIL.UnidentifiedImageError: cannot identify image file
	14. svg to jpeg  - 
	15. svg to png  - 
	16. svg to webp - 
"""

import io

import boto3
from PIL import Image
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
from botocore.exceptions import ClientError

WIDTH  = 250
HEIGHT = 250

images = [
	"spacex.jpeg", "private/up/up-balloon-home.jpg", "private/cdn.png", 
	"aws-partner-card.webp", "bigfish.svg"
]

session   = boto3.Session(profile_name='karthick-learner')
s3_client = session.client('s3')


def get_object(bucket, key):
	try:
		res = s3_client.get_object(Bucket=bucket, Key=key)
	except ClientError as client_err:
		print(f"ClientError has occured - {client_err}")
	else:
		return res


def convert_image_format(image_object: Image.Image, output_format: str) -> Image.Image:
	new_img_obj = image_object
	if output_format and output_format.upper() == "SVG":
		print(f"Unable to convert to svg")
		return new_img_obj
	
	if output_format and not (image_object.format == output_format.upper()):
		print("Inside convert image format if condition")
		bytes_io = io.BytesIO()
		image_object.convert("RGB").save(bytes_io, output_format, lossless=True)
		new_img_obj = Image.open(bytes_io)

	return new_img_obj


def main():
	image = images[2]
	res = get_object("karthick-leaner-ccp-2021-demo", image)
	body = res.get("Body")
	if not image.endswith(".svg"):
		with Image.open(body) as f:
			converted_image = convert_image_format(f, "jpeg")
			resized_image = converted_image.resize((WIDTH, HEIGHT))
			print(resized_image)
			# resized_image_in_bytes = resized_image.tobytes()

	# if image.endswith(".svg"):
	# 	drawing = svg2rlg(body)
	# 	renderPM.drawToFile(drawing, "my.png", fmt="PNG")


if __name__ == '__main__':
	main()
