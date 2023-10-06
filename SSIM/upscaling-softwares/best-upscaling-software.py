# imports
import cv2
import numpy as np
from skimage import io
from skimage.metrics import structural_similarity as ssim
import os

# access files
directory_path = "upscaling-softwares"

# Load the reference image
reference_image = io.imread(os.path.join(directory_path, "reference_picture.jpg"))
reference_image_gray = cv2.cvtColor(reference_image, cv2.COLOR_BGR2GRAY)

# Iterate through files in the directory
results = dict()
for filename in os.listdir(directory_path):
    if filename.endswith(".jpg") and filename != "reference_picture.jpg":
        # Load the current image
        current_image = io.imread(os.path.join(directory_path, filename))

        # Ensure the current image has the same dimensions as the reference image (resize if necessary)
        if current_image.shape != reference_image.shape:
            current_image = cv2.resize(current_image, (reference_image.shape[1], reference_image.shape[0]))

        # Convert the current image to grayscale
        current_image_gray = cv2.cvtColor(current_image, cv2.COLOR_BGR2GRAY)

        # calculate SSIM index
        ssim_score = ssim(reference_image_gray, current_image_gray)

        # edit the dictionary
        results[filename[:-4]] = round(ssim_score, 3)

# sort the dictionary by value and print the result
sorted_results = dict(sorted(results.items(), key=lambda item: item[1]))

for image in sorted_results:
    print(f"quality when upscaled with {image} = {sorted_results[image]}")
# %%
import matplotlib.pyplot as plt

softwares = []
ssim_scores = []

plt.figure(figsize=(12, 8))
plt.bar(sorted_results.keys(), sorted_results.values())
plt.title("Comparing upscaling softwares")
plt.xlabel("software")
plt.ylabel("SSIM score")
plt.grid(False)
plt.ylim(0, 1)
plt.show()
