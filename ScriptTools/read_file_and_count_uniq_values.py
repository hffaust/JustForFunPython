import sys

# Initially made to count and tally IP addresses in a network flows log. 
# Could potetnailly be restructured for another purpose
# Author: HARRY FAUST  4.8.19
def main(argv):
  file_name = sys.argv[1]
  f = open(str(file_name), "r")
  #if(f.mode == "r"):
  #  contents = f.read()
  #  print(contents)
  file_lines = f.readlines()
  uniq_vals = []
  uniq_vals_hash = {}
  for line in file_lines:
    line_trimmed = line.rstrip().split(':') #trim off port 
    line_eval = line_trimmed[0]
    if(line_eval in uniq_vals_hash.keys()):
      temp = {line_eval: uniq_vals_hash.get(line_eval) + 1}
      uniq_vals_hash.update(temp)
    else:
      temp2 = {line_eval: 1}
      uniq_vals_hash.update(temp2)
  #print(uniq_vals_hash)
  count = 1
  for addr in uniq_vals_hash.keys():
    print(str(count) + "   " + str(addr) + "     frequency: " + str(uniq_vals_hash.get(addr)))
    count += 1
if __name__=="__main__":
  main(sys.argv[1:])
