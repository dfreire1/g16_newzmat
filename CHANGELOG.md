CHANGELOG
=========

Version 1.1.0 - [Date: March 27, 2025]
---------------------------------------

**New Feature:**
- Added connectivity data detection and removal.

**Changes:**
- The script now removes both atomic coordinates **and** connectivity data (bond/angle/dihedral lists) from input files.
- Ensures exactly two blank lines are preserved at the end of the file (required by Gaussian16).
- Improved regex patterns to detect connectivity lines (e.g., `1 2 1.500` or `3 4 1.000 5 1.000`).

**Bug Fixes:**
- Fixed excess empty lines in output files.
- Stopped processing lines after the charge/multiplicity line (`0,1`) to avoid retaining irrelevant data.

**Notes:**
- This update ensures compatibility with Gaussian16’s strict input formatting requirements.
