#“Donated under Volatility Foundation, Inc. Individual Contributor Licensing Agreement”;
import hashlib
import shutil
import os
import argparse

class NSRLFileScanner:

    @classmethod
    def load_nsrl_hashes(self, nsrl_file):
        #nsrl_file = "NSRLFile-2023.06.01m-computer.txt-md5.idx"
        nsrl_hashes = {}
        nsrl_file_path = os.path.join(nsrl_file)

        # Read the NSRL KFF hash database
        print("Opening NSRL file")
        with open(nsrl_file_path, 'r', encoding='utf-8', errors='ignore') as nsrl_file:
            for line in nsrl_file:
                parts = line.strip().split(',')
                md5_hash = parts[0].lower()
                nsrl_hashes[md5_hash] = True
        return nsrl_hashes

    @classmethod
    def check_file_positive_hit(self, file_path, nsrl_hashes):
        # Calculate the MD5 hash of the file
        with open(file_path, 'rb') as file_data:
            data = file_data.read()
            md5_hash = hashlib.md5(data).hexdigest()

        # Check if the MD5 hash is in the NSRL hash database
        if not md5_hash in nsrl_hashes:
            print("KFF Unknown : ", file_path)
            return True
        else:
            print("KFF Known : ", file_path)
            return False

    @classmethod
    def export_positive_hits(self, input_directory, nsrl_hashes, output_directory):
        # Create the output directory
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

        # Scan the specified directory and move positive hits to the output directory
        for root, _, files in os.walk(input_directory):
            for file in files:
                full_path = os.path.join(root, file)
                if NSRLFileScanner.check_file_positive_hit(full_path, nsrl_hashes):
                    new_file_path = os.path.join(output_directory, file)
                    shutil.move(full_path, new_file_path)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("nsrl_file", help="The NSRL index file Downloadable from https://sourceforge.net/projects/autopsy/files/NSRL/", required=True)
    parser.add_argument("input_directory", help="The input directory to scan", required=True)
    parser.add_argument("output_directory", help="The output directory to move positive hits", required=True)

    args = parser.parse_args()

    # Load the NSRL hash database
    nsrl_hashes = NSRLFileScanner.load_nsrl_hashes(args.nsrl_file)

    # Export positive hits to the output directory
    NSRLFileScanner.export_positive_hits(args.input_directory, nsrl_hashes, args.output_directory)

if __name__ == "__main__":
    main()
