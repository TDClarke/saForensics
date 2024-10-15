# saForensics
Post extraction scripts used after carving files from a drive or drive image or dumping files using volitility framework:
This can be done with volatility 3, by using the command:
```vol.py -f “/path/to/file” -o “/path/to/dir” windows.dumpfiles```

```saNSFW.py Standalone script:
Uses the https://github.com/yahoo/open_nsfw CAFFE classifier to sort NSFW images.
C:\volatility3>python saNSFW.py -h
usage: saNSFW.py [-h] input_directory output_directory

positional arguments:
  input_directory   The input directory to scan
  output_directory  The output directory to move positive hits

options:
  -h, --help        show this help message and exit

Example C:\volatility3>python saNSFW.py TEST OUTPUT

saNSRL.py Standalone script:
Uses a md5 idx file from https://sourceforge.net/projects/autopsy/files/NSRL/ to sort known images.
C:\volatility3>python saNRSL.py -h
usage: saNSRL.py [-h] nsrl_file input_directory output_directory

positional arguments:
  nsrl_file         The NSRL index file Downloadable from https://sourceforge.net/projects/autopsy/files/NSRL/
  input_directory   The input directory to scan
  output_directory  The output directory to move positive hits

options:
  -h, --help        show this help message and exit

Example:
C:\volatility3>python saNSRL.py NSRLFile-md5.idx DUMPI DUMPO
Opening NSRL file
KFF Unknown :  DUMP\file.0xbf0f66995ef0.0xbf0f6af7c8d0.DataSectionObject.EtwRTEventlog-Security.etl.dat

#### SQL ###
saNSRLSQL.py Standalone script:
Uses a database connection, editable within the script to sort NSRL known images.
https://www.nist.gov/itl/ssd/software-quality-group/national-software-reference-library-nsrl/nsrl-download/current-rds
C:\volatility3>python saNSRLSQL.py -h
usage: saNSRLSQL.py [-h] input_directory output_directory

positional arguments:
  input_directory   The input directory to scan
  output_directory  The output directory to move positive hits

options:
  -h, --help        show this help message and exit```

saPT.py Standalone script:
Uses https://talhassner.github.io/home/publication/2015_CVPR to sort images of pre teen childen.
C:\volatility3>python saPT.py -h
usage: saPT.py [-h] input_directory output_directory

positional arguments:
  input_directory   The input directory to scan
  output_directory  The output directory to move positive hits

options:
  -h, --help        show this help message and exit

Example C:\volatility3>python saPT.py TEST OUTPUT


saRigan.py Standalone script:
Uses the rigan ap-apaid algorithum for nudity detection to sort images.
C:\volatility3>python saRigan.py -h
usage: saRigan.py [-h] input_directory output_directory

positional arguments:
  input_directory   The input directory to scan
  output_directory  The output directory to move positive hits

options:
  -h, --help        show this help message and exit

Example C:\volatility3>python saRigan.py TEST OUTPUT
