## Export and Filter Data from a PlantCV Database

Utility scripts are available to filter and export data from a PlantCV results database.

### Database exporter

The utility script `db-exporter-pcv2.py` can be used to join tables from the SQLite database, filter data if angles 
are missing, and average signal data (by timestamp) Requires a PlantCV SQLite database.

#### Usage

    Arguments:
    
    -d, --database     <path to sqlite database>, required
    -o, --outfile      <path and name of output files>, required
    -f, --filter       Either 'filter' or 'raw' if filter is selected, there will be a check to make sure that each 
                       timepoint has the correct number of angles (-a flag), default='raw'
    -i, --imgtype      Type of image either 'VIS', 'NIR', or 'BOTH', or 'NONE' if no type is specified in database, 
                       default='BOTH'
    -a, --angles       Total number of angles (TV and SV), default=5
    -s, --signal       If true outputs signal data as well as feature data, default=True
    -n, --signalnorm   If true, normalizes signal data to area of object, default=True
    -v, --signalavg    If true, also output data averaged by timestamp for seperated sv and tv files, default=True
    -D, --debug        Turn on debugging mode, action="store_true"
    -h, --help         Show the help message and exit


```
~/plantcv/utils/db-exporter-pcv2.py -d ~/plantcv.db.sqlite3 -o test-db.csv -f 'filter' -a 3 -i 'BOTH' -s True -n True -v True -D

```
