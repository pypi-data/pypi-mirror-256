import argparse
import os
from ocfl_inventory import OcflInventory
from rehydrator import Rehydrator

###
## Main ##
###
if __name__ == '__main__':
  # construct the argument parse and parse the arguments
  ap = argparse.ArgumentParser(description=
                  "Converts the OCFL form of a DRS Object and reconstitutes "\
                  "(rehydrates) a form expected by curators. "\
                  "The input is the OCFL object root directory of object to "\
                  "rehydrate.")

  ap.add_argument('-i', '--input_dir',
                  required=True,
                  help='Local directory containing the OCFL Object root of '\
                       'the object to rehydrate')
  ap.add_argument('-o', '--output_dir',
                  required=True,
                  help='Local directory where rehydrated object will be written')
  args = vars(ap.parse_args())
 
  input_dir  = args['input_dir']
  output_dir = args['output_dir']

  rehydrator = Rehydrator(input_dir, output_dir)
  rehydrator.rehydrate()