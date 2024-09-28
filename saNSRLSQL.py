# “Donated under Volatility Foundation, Inc. Individual Contributor Licensing Agreement”;
import hashlib
import shutil
import os
import argparse
import mysql.connector
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class NSRLFileScanner:
    @classmethod
    def connect_to_mysql(cls, host, user, password, database):
        try:
            return mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database
            )
        except mysql.connector.Error as err:
            logging.error(f"Error connecting to MySQL: {err}")
            raise

    @classmethod
    def check_hash_in_db(cls, connection, sha256_hash):
        """Query the database to check if the file's SHA-256 hash exists."""
        try:
            cursor = connection.cursor()
            query = "SELECT COUNT(*) FROM nsrl_hashes WHERE sha256_hash = %s"
            cursor.execute(query, (sha256_hash,))
            result = cursor.fetchone()
            return result[0] > 0  # Return True if the hash is found
        except mysql.connector.Error as err:
            logging.error(f"Error querying the database for hash {sha256_hash}: {err}")
            raise

    @classmethod
    def check_file_positive_hit(cls, file_path, connection):
        """Calculate the file's SHA-256 hash and check if it's in the NSRL database."""
        try:
            with open(file_path, 'rb') as file_data:
                data = file_data.read()
                sha256_hash = hashlib.sha256(data).hexdigest()

            # Query the database for this specific hash
            is_known = cls.check_hash_in_db(connection, sha256_hash)
            if not is_known:
                logging.info(f"KFF Unknown : {file_path}")
                return True
            else:
                logging.info(f"KFF Known : {file_path}")
                return False
        except Exception as err:
            logging.error(f"Error processing file {file_path}: {err}")
            return False

    @classmethod
    def export_positive_hits(cls, input_directory, connection, output_directory):
        """Scan the directory, check each file against the NSRL database, and move positive hits."""
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

        for root, _, files in os.walk(input_directory):
            for file in files:
                full_path = os.path.join(root, file)
                try:
                    if cls.check_file_positive_hit(full_path, connection):
                        new_file_path = os.path.join(output_directory, file)
                        shutil.move(full_path, new_file_path)
                        logging.info(f"Moved {file} to {output_directory}")
                except Exception as err:
                    logging.error(f"Error moving file {full_path}: {err}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_directory", help="The input directory to scan")
    parser.add_argument("output_directory", help="The output directory to move positive hits")

    args = parser.parse_args()

    connection = None
    try:
        # Connect to the MySQL database
        connection = NSRLFileScanner.connect_to_mysql(
            host="your_mysql_host",
            user="your_mysql_user",
            password="your_mysql_password",
            database="your_mysql_database"
        )

        # Export positive hits to the output directory, querying hash one by one
        NSRLFileScanner.export_positive_hits(args.input_directory, connection, args.output_directory)
    finally:
        if connection:
            connection.close()
            logging.info("MySQL connection closed")

if __name__ == "__main__":
    main()

