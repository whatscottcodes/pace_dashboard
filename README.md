# PACE Dashboard

Flask web app built using dash that displays important indicators for PACE programs. Uses a SQLite database that contains information from PaceLogic report and other sources. (Could be created without other sources and be used as a dashboard for PaceLogic EHR data.)

Still a work in progress - some indicators do not currently have the required data source. Clean up for a dashboard that *only* uses PaceLogic data ongoing.

## Requirements

All required packages are in the requirements.txt file. There is also an included environment.yml file for setting up a conda environment. Requires paceutils package to be installed in environment - use pip install e <local_path/to/pace_utils>.

### PaceUtils

Requires that the paceutils package to be installed. Can be found at http://github.com/whatscottcodes/paceutils.

Requires a SQLite database set up to the specifications in https://github.com/whatscottcodes/database_mgmt

## Use

See Dashboard Technical Guide in the docs folder.

