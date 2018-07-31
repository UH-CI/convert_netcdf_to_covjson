#!/usr/bin/python
import json
import subprocess
import sys, getopt
import os.path
import fileinput


def main(argv):
   inputfile = ''
   outputfile = ''
   try:
      opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
   except getopt.GetoptError:
      print('convert_nc_to_covjson.py -i <inputfile> -o <outputfile_prefix>')
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print('convert_nc_to_covjson.py -i <inputfile> -o <outputfile_prefix>')
         sys.exit()
      elif opt in ("-i", "--ifile"):
         inputfile = arg
      elif opt in ("-o", "--ofile"):
         outputfile = arg
      else:
         assert False, "unhandled option"
   print('Input file is "', inputfile)
   if os.path.isfile(inputfile) != True:
     print('Input file does not exist!')
     sys.exit()
   print('Output file prefix is ', outputfile)
   print('Updating input for conversion...')
   #massage metadata for pycov-convert
   os.system('ncatted -a axis,recharge,o,c,"x y" '+inputfile+' '+outputfile+'_input.nc')
   os.system('ncatted -a standard_name,recharge,o,c,"recharge" '+outputfile+'_input.nc '+outputfile+'_input1.nc')
   os.system('rm '+outputfile+'_input.nc')
   os.system('ncatted -a standard_name,scenario,o,c,"scenario" '+outputfile+'_input1.nc '+outputfile+'_input2.nc')
   os.system('rm '+outputfile+'_input1.nc')
   os.system('ncatted -a standard_name,landuse,o,c,"landuse" '+outputfile+'_input2.nc '+outputfile+'_input3.nc')
   os.system('rm '+outputfile+'_input2.nc')
   os.system('ncatted -a long_name,recharge,o,c,"recharge" '+outputfile+'_input3.nc '+outputfile+'_input4.nc')
   os.system('rm '+outputfile+'_input3.nc')
   os.system('ncatted -a long_name,scenario,o,c,"scenario" '+outputfile+'_input4.nc '+outputfile+'_input5.nc')
   os.system('rm '+outputfile+'_input4.nc')
   os.system('ncatted -a long_name,landuse,o,c,"landuse" '+outputfile+'_input5.nc '+outputfile+'_input6.nc')
   os.system('rm '+outputfile+'_input5.nc')
   inputfile = outputfile+'_input6.nc'
   print("Generating subsets and converting...")
   #begin loops for extracting slices 2X30 scenariosxlandusage
   for i in range(0,2):
      i_str = str(i)
      process =  subprocess.call("ncks -d scenario,"+i_str+","+i_str+" -v recharge,x,y,landuse " + inputfile+" "+outputfile+"_sc"+i_str+".nc", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
      for j in range(0,30):
         j_str = str(j)
         print(" . ")
         outfile = outputfile+"_sc"+i_str+"_"+j_str
         subprocess.call("ncks -d landuse,"+j_str+","+j_str+" -v recharge,x,y " + outputfile +"_sc"+i_str+".nc "+outfile+".nc", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
         subprocess.call("pycovjson-convert -i "+ outfile +".nc -o " + outfile +".covjson -v recharge",shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
         #replace some incorrect values to make this valid and renderable
         with open(outfile+'.covjson', 'r') as f:
            with open(outfile+'-fin.covjson', 'w') as new_f:
               for line in f:
                  new_line = line.replace("GeographicCRS", "ProjectedCRS").replace("http://www.opengis.net/def/crs/OGC/1.3/CRS84", "http://www.opengis.net/def/crs/EPSG/0/32604").replace("[1, 1, 732, 920]","[732,920]").replace('["x", " ", "y"]','["y","x"]')
                  new_f.write(new_line)


if __name__ == "__main__":
   main(sys.argv[1:])
