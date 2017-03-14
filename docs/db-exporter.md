## Export and Filter Data from Database

This utility script can be used to join tables from the sqlite database, filter data if angles are missing, and average signal data (by timestamp)
Requires a plantcv sqlite database.

### Running the Utility Script
    - First call the db-exporter-pcv2.py script
    - -d, --database, < path to sqlite database>, required
    - -o, --outfile,  < path and name of output files>, required
    - -f, --filter,  either 'filter' or 'raw' if filter is selected, there will be a check to make sure that each timepoint has the correct number of angles (-a flag), default='raw'
    - -i, --imgtype, Type of image either 'VIS', 'NIR', or 'BOTH', or 'NONE' if no type is specified in database, default='BOTH'
    - -a, --angles, Total number of angles (TV and SV), default=5
    - -s, --signal, if true outputs signal data as well as feature data, default=True
    - -n, --signalnorm, if true, normalizes signal data to area of object, default=True
    - -v, --signalavg, if true, also output data averaged by timestamp for seperated sv and tv files, default=True
    - -D, --debug, Turn on debugging mode, action="store_true"

```
/home/mgehan/plantcv/utils/db-exporter-pcv2.py -d /home/mgehan/testdata/ricesalt082016.sqlite3 -o test-db.csv -f 'filter' -a 3 -i 'BOTH' -s True -n True -v True -D

```
