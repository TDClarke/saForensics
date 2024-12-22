#“Donated under Volatility Foundation, Inc. Individual Contributor Licensing Agreement”;
import argparse
import os
from PIL import Image
import shutil

parser = argparse.ArgumentParser(description='Process some images')
parser.add_argument("input_directory", help="The input directory to scan")
parser.add_argument("output_directory", help="The output directory to move positive hits")
args = parser.parse_args()

input_directory = args.input_directory
output_directory = args.output_directory

# Load the image
def is_image(filepath):
    try:
        image = Image.open(filepath)
    except (IOError, OSError) as e:
        print(f"Error opening file '{filepath}': {e}")
    
    return "True"
                
def main():
    try:
        for filename in os.listdir(input_directory):
            if filename.endswith(".jpg.dat") or filename.endswith(".png.dat") or filename.endswith(".jpg") or filename.endswith(".png"):
                filepath = os.path.join(input_directory, filename)
                result = is_image(filepath)
                if result == "True":
                    #print(f"This is a image file: {result}")
                    output_filename = os.path.join(output_directory, filename)
                    print(f"File is iamge: Copied to: {output_filename}")
                    shutil.copy(filepath, output_filename)
    except Exception as e:
        print(f"Error processing file '{filepath}': {e}")

if __name__ == "__main__":
    main()

