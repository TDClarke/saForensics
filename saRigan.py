#“Donated under Volatility Foundation, Inc. Individual Contributor Licensing Agreement”;
import argparse
import os
from PIL import Image
import numpy as np
from colorsys import rgb_to_hsv
from scipy.ndimage import label
import shutil

parser = argparse.ArgumentParser(description='Process some images')
parser.add_argument("input_directory", help="The input directory to scan")
parser.add_argument("output_directory", help="The output directory to move positive hits")
args = parser.parse_args()

input_directory = args.input_directory
output_directory = args.output_directory

# Helper functions
def is_skin_pixel(r, g, b):
    # Convert RGB to normalized RGB after converting r, g, b to float
    total = float(r) + float(g) + float(b)
    if total == 0:
        return False
    r_norm, g_norm, b_norm = r / total, g / total, b / total
    
    # Convert RGB to HSV
    h, s, v = rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)
    
    # Skin color detection using HSV values
    return 0 <= h <= 50/360 and 0.23 <= s <= 0.68 and v >= 0.35

        
        
    r_norm, g_norm, b_norm = r / total, g / total, b / total
    
    # Convert RGB to HSV
    h, s, v = rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)
    
    # Skin color detection using HSV values
    return 0 <= h <= 50/360 and 0.23 <= s <= 0.68 and v >= 0.35

def calculate_percentage(part, whole):
    return (part / whole) * 100

def get_bounding_polygon(skin_pixels):
    if len(skin_pixels) == 0:
        return None
    xs, ys = zip(*skin_pixels)
    return (min(xs), min(ys)), (max(xs), max(ys))

def bounding_polygon_area(bounding_polygon):
    if bounding_polygon is None:
        return 0
    (x_min, y_min), (x_max, y_max) = bounding_polygon
    return (x_max - x_min) * (y_max - y_min)

# Load the image
def classify_image(filepath):
    try:
        image = Image.open(filepath)
    except (IOError, OSError) as e:
        print(f"Error opening file '{filepath}': {e}")
            
    pixels = np.array(image)
    height, width, _ = pixels.shape

    # Skin pixel detection and labeling
    skin_mask = np.zeros((height, width), dtype=bool)
    for y in range(height):
        for x in range(width):
            r, g, b = pixels[y, x][:3]
            if is_skin_pixel(r, g, b):
                skin_mask[y, x] = True

    # Label connected skin regions
    labeled_skin, num_regions = label(skin_mask)

    # Analyze the labeled regions to find the largest skin regions
    region_sizes = [(labeled_skin == region).sum() for region in range(1, num_regions + 1)]
    sorted_regions = sorted(enumerate(region_sizes, 1), key=lambda x: x[1], reverse=True)
    
    # Find the three largest regions
    if len(sorted_regions) < 3:
        largest_regions = sorted_regions
    else:
        largest_regions = sorted_regions[:3]

    # Skin region pixel counts
    total_skin_pixels = skin_mask.sum()
    if len(largest_regions) == 0:
        return "No regions"
    largest_skin_region_pixels = largest_regions[0][1] if len(largest_regions) > 0 else 0
    second_largest_skin_region_pixels = largest_regions[1][1] if len(largest_regions) > 1 else 0
    third_largest_skin_region_pixels = largest_regions[2][1] if len(largest_regions) > 2 else 0

    # Find the bounding polygon for the largest region
    skin_pixels = np.argwhere(labeled_skin == largest_regions[0][0])
    bounding_polygon = get_bounding_polygon(skin_pixels)
    polygon_area = bounding_polygon_area(bounding_polygon)

    # Calculate metrics
    skin_percentage = calculate_percentage(total_skin_pixels, height * width)
    largest_skin_region_percentage = calculate_percentage(largest_skin_region_pixels, height * width)
    polygon_skin_pixels = np.sum([is_skin_pixel(*pixels[y, x][:3]) for y, x in skin_pixels])
    polygon_skin_percentage = calculate_percentage(polygon_skin_pixels, polygon_area)
    average_intensity = np.mean([np.mean(pixels[y, x][:3]) for y, x in skin_pixels]) / 255.0

    #Dbug code
    #print("skin percentage               : ", skin_percentage)
    #print("largest skin region percentage: ", largest_skin_region_percentage)
    #print(f"Number of regions: {len(largest_regions)}")
    #print(f"Region sizes: {region_sizes}")



    # Image classification based on the given criteria
    if skin_percentage < 15:
        return "Not Nude"
    if (largest_skin_region_pixels < 0.35 * total_skin_pixels and
        second_largest_skin_region_pixels < 0.3 * total_skin_pixels and
        third_largest_skin_region_pixels < 0.3 * total_skin_pixels):
        return "Not Nude"
    if largest_skin_region_pixels < 0.45 * total_skin_pixels:
        return "Not Nude"
    if (total_skin_pixels < 0.3 * height * width and
        polygon_skin_pixels < 0.55 * polygon_area):
        return "Not Nude"
    if num_regions > 60 and average_intensity < 0.25:
        return "Not Nude"
    
    return "Nude"
                
def main():
    try:
        for filename in os.listdir(input_directory):
            if filename.endswith(".jpg") or filename.endswith(".png"):
                filepath = os.path.join(input_directory, filename)
                result = classify_image(filepath)
                if result == "Nude":
                    #print(f"The image is classified as: {result}")
                    output_filename = os.path.join(output_directory, filename)
                    print(f"Image is Nude: Copied to: {output_filename}")
                    shutil.copy(filepath, output_filename)
    except Exception as e:
        print(f"Error processing file '{filepath}': {e}")

if __name__ == "__main__":
    main()

