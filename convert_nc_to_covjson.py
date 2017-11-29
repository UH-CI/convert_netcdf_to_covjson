#!/usr/bin/python
import json
import subprocess
import sys, getopt
import os.path

def main(argv):
   inputfile = ''
   outputfile = ''
   try:
      opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
   except getopt.GetoptError:
      print 'convert_nc_to_covjson.py -i <inputfile> -o <outputfile_prefix>'
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print 'convert_nc_to_covjson.py -i <inputfile> -o <outputfile_prefix>'
         sys.exit()
      elif opt in ("-i", "--ifile"):
         inputfile = arg
      elif opt in ("-o", "--ofile"):
         outputfile = arg
      else:
         assert False, "unhandled option"
   print 'Input file is "', inputfile
   if os.path.isfile(inputfile) != True:
     print 'Input file does not exist!'
   print 'Output file prefix is "', outputfile
  
   #massage metadata for pycov-convert
   subprocess.call('ncatted -a axis,recharge,o,c,"x y" '+inputfile+' '+outputfile+'_input.nc', shell=True)
   subprocess.call('ncatted -a standard_name,recharge,o,c,"recharge" '+outputfile+'_input.nc '+outputfile+'_input1.nc', shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
   subprocess.call('ncatted -a standard_name,scenario,o,c,"scenario" '+outputfile+'+_input.nc '+outputfile+'_input2.nc', shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
   subprocess.call('ncatted -a standard_name,landuse,o,c,"landuse" '+outputfile+'+input.nc '+outputfile+'_input3.nc', shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
   subprocess.call('ncatted -a long_name,recharge,o,c,"recharge" '+outputfile+'_input.nc '+outputfile+'_input4.nc', shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
   subprocess.call('ncatted -a long_name,scenario,o,c,"scenario" '+outputfile+'_input.nc '+outputfile+'_input5.nc', shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
   subprocess.call('ncatted -a long_name,landuse,o,c,"landuse" '+outputfile+'_input.nc '+outputfile+'_input6.nc', shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)

   for i in range(0,2):
      print 'i is: ',i
      i_str = str(i)
      process =  subprocess.call("ncks -d scenario,"+i_str+","+i_str+" -v recharge,x,y,landuse " + outfile +"_input.nc "+outputfile+"_sc"+i_str+".nc", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
      for j in range(0,30):
         print 'j is: ',j
         j_str = str(j)
         outfile = outputfile+"_sc"+i_str+"_"+j_str
         print subprocess.call("ncks -d landuse,"+j_str+","+j_str+" -v recharge,x,y " + outputfile +"_sc"+i_str+".nc "+outfile+".nc", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
         print subprocess.call("pycovjson-convert -i "+ outfile +".nc -o " + outfile +".covjson -v recharge",shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
      #   print subprocess.check_output(['ncks','-d '])
      #   ncks -d time,0,1 -v potential_recharge,lat,lon,x,y in.nc out.nc
#with open('data.json', 'r+') as f:
#    data = json.load(f)
#    data['id'] = 134 # <--- add `id` value.
#    f.seek(0)        # <--- should reset file position to the beginning.
#    json.dump(data, f, indent=4)
#    f.truncate()     # remove remaining part

if __name__ == "__main__":
   main(sys.argv[1:])

