from itertools import product
import sys
import argparse
CLI=argparse.ArgumentParser()
CLI.add_argument(
    "--list",
    nargs="*", 
    type=int
)
CLI.add_argument(
    "--target",
    nargs=1,
    type=int
) 
args = CLI.parse_args()
def sum_nums_with_inverse(a_list, target):
    if len(a_list) == 0:
        return 0
    a_list = [int(x) for x in a_list]
    inverse_list = [-x for x in a_list]
    result = list(product(*zip(a_list, inverse_list)))
    #print(result)  # test print
    lst = [list(x) for x in result]
    #print(lst)  # test print
    hash_table = {}
    num = 0
    for i in lst:
        num = 0
        for j in i:
            num += j
        hash_table[str(i)] = num
    print(hash_table)
    
    found_lists = []
    count = 0 
    for i in hash_table.keys():
        if hash_table[i] == target[0]:
            count += 1
            found_lists.append(i)        
    print("\n")
    #print(found_lists)  # test print
    print("%s LISTS FOUND!" % count)
    #return(count)
    return(found_lists)

def main(argv):
    if(len(sys.argv) < 3):
        print("ERROR: INVALID NUMBER OF ARGS\nUSAGE: python3 --list <[list]> --target <target number>")
        sys.exit(1)
    input_list = args.list
    print(input_list)  # test print
    target = args.target
    print(target)  # test print
    found_lists = sum_nums_with_inverse(input_list, target)
    print("\nFOUND THE FOLLOWING LISTS THAT SUM TO REACH TARGET %s:" % target[0])
    print(found_lists)

if __name__ == "__main__":
    main(sys.argv[1:])
    
