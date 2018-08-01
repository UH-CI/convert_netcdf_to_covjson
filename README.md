# convert_netcdf_to_covjson
This script converts NetCDF from USGS into covjson files.

To run this easily you can use the following docker contianer that has all the pycovjson and netcdf dependencies.

https://hub.docker.com/r/scleveland/pycovjson/

To run the script you need to start the docker container
```
docker run -t -d -v directory_with_script_and_input:/landuse scleveland/pycovjson:1.0 
docker exec -it container_id /bin/bash
```
Inside the contianer
```
cd /landuse
python convert_nc_to_covjson.py -i inputfilename -o prefix_for_output_files
```
All the files will be written to the volume directory you mounted and will be available on the host.
