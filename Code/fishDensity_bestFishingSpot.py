//This Code has been generated by OpenAI ChatGPT
//Prompts used are listed in-line at the end

from PIL import Image
import os
import numpy as np

# Replace 'path_to_images' with the actual path to your image directory
image_folder = 'D:\\fishmaps'
output_folder = 'D:\\fishmaps'

# Get a list of all PNG files in the directory
image_files = [f for f in os.listdir(image_folder) if f.endswith('.png')]

# Load the first image to get dimensions
first_image = Image.open(os.path.join(image_folder, image_files[0])).convert('L')

# Initialize an accumulator array with zeros
accumulator = np.zeros_like(np.array(first_image), dtype=np.uint64)

# Sum pixel values across all images
for image_file in image_files:
    image_path = os.path.join(image_folder, image_file)
    img = np.array(Image.open(image_path).convert('L'))
    accumulator += img.astype(np.uint64)

# Normalize the accumulated values to the range [0, 255]
stacked_image = (accumulator * 255 / (len(image_files) * 255)).astype(np.uint8)

# Find the coordinates of the top N pixel values
top_n_coords = np.unravel_index(np.argpartition(stacked_image.flatten(), -500)[-500:], stacked_image.shape)

# Create an image highlighting the top N areas with the most fish
highlighted_image = np.zeros_like(stacked_image)
highlighted_image[top_n_coords] = 255

# Save or display the highlighted image
Image.fromarray(highlighted_image).save(os.path.join(output_folder, 'highlighted_image_top_500.png'))

//ChatGPT Prompts Used:
// Would it be possible to modify the code to have it highlight the area where there are most fish when the images are stacked (i.e the area with the most white)
//	That's great but instead of highlighting a single pixel, maybe we can have it highlight the top 100 or so?
