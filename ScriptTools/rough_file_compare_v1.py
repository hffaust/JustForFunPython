import filecmp

path = input("type your filepath: ")
folder_1 = input("type folder 1 name: ")
folder_2  = input("type folder 2 name: ")
comparison = filecmp.dircmp(path + folder_1, path + folder_2)
common_files = ', '.join(comparison.common)
left_only_files = ', '.join(comparison.left_only)
right_only_files = ', '.join(comparison.right_only)

with open(path + '_comparison_output.txt', 'w')as folder_report:
  folder_report.write("Common Files: " + common_files + "\n")
  folder_report.write("\nOnly in Folder 1: " + left_only_files + "\n")
  folder_report.write("\nOnly in Folder 1" + right_only_files)