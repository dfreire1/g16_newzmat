GAUSSIAN16 INPUT FILE GENERATOR SCRIPT
======================================

A Python script to automate Gaussian16 input file (.gjf) creation from checkpoint files (.chk) using the newzmat utility.

------------------------------------------------------------------------------

TABLE OF CONTENTS
-----------------
1. Introduction
2. Features
3. Requirements
4. Installation
5. Usage
6. Examples
7. Technical Notes
8. Troubleshooting
9. License

------------------------------------------------------------------------------

1. INTRODUCTION
---------------
This script converts Gaussian16 checkpoint files (.chk) into formatted input files (.gjf). Key functionalities include:
- Automated filename numbering (e.g., file_01.gjf, file_02.gjf).
- Addition of required headers (%nprocshared, %mem).
- Keyword management (e.g., opt=calcfc, freq=raman).
- Enforcement of geom=checkpoint and guess=read for checkpoint-based jobs.

------------------------------------------------------------------------------

2. FEATURES
-----------
- Batch processing of .chk files in a directory or single file.
- Filename numbering modes:
  * Default: filename_of001.chk → filename_of002.gjf
  * -xx flag: filename_01.chk → filename_02.gjf
- Keyword replacement and addition (e.g., replaces opt with opt=calcfc).
- Automatic removal of atomic coordinates to avoid conflicts.
- Error handling for invalid files.

------------------------------------------------------------------------------

3. REQUIREMENTS
---------------
- Gaussian16 (ensure newzmat is accessible at /home/apps/g16/newzmat).
- Python 3.6+ (download: https://www.python.org/downloads/).

------------------------------------------------------------------------------

4. INSTALLATION
---------------
1. Download the script:
   git clone https://github.com/yourusername/g16_newzmat.git

2. Configure paths:
   Open g16_newzmat.py and update the newzmat path (Line 7) if needed:
   command = "/home/apps/g16/newzmat -ichk -step 999 {file_name} {new_file_name}"

------------------------------------------------------------------------------

5. USAGE
--------
Basic Commands:
- Process all .chk files in current directory:
  python3 g16_newzmat.py

- Process a specific directory:
  python3 g16_newzmat.py /path/to/chk_files

- Use -xx numbering mode:
  python3 g16_newzmat.py -xx

Keyword Replacement:
- Add/replace keywords (e.g., opt=calcfc):
  python3 g16_newzmat.py opt=calcfc freq=raman

------------------------------------------------------------------------------

6. EXAMPLES
-----------
Example 1: Default Mode
- Command: python3 g16_newzmat.py
- Input: molecule_of001.chk
- Output: molecule_of002.gjf
- Route line: # geom=checkpoint guess=read

Example 2: Custom Keywords with -xx
- Command: python3 g16_newzmat.py -xx opt=calcfc
- Input: molecule_01.chk
- Output: molecule_02.gjf
- Route line: # opt=calcfc geom=checkpoint guess=read

------------------------------------------------------------------------------

7. TECHNICAL NOTES
------------------
- Atomic coordinates are removed to enforce geom=checkpoint.
- Filename patterns:
  * Default mode: *_ofXXX.chk → increments XXX.
  * -xx mode: *_XX.chk → increments XX.
- Headers added automatically: %oldchk, %nprocshared=128, %mem=50GB, %chk.

------------------------------------------------------------------------------

8. TROUBLESHOOTING
------------------
- Error: "keyword is not a valid file":
  → Place keywords after directory/file arguments.
- Error: "newzmat: command not found":
  → Update the newzmat path in the script (Line 7).
- Empty output file:
  → Ensure the .chk file is valid (e.g., from a completed job).

------------------------------------------------------------------------------

9. LICENSE
----------
MIT License. See LICENSE for details.

==============================================================================
