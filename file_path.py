import os, copy

# Get Full Paths to All TXT files to be analyzed
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def GetFilePaths(home_dir):
	author_ind = 0
	all_docs_dict = {}
	for root, dirs, files in os.walk(home_dir):
		if root == home_dir:
			author_list = dirs
			num_authors = len(author_list)
		else:
			temp_path_list = []
			for file_name in files:
				if file_name != ".DS_Store": # Mac OSX Specific Directory file 
					temp_path_list.append(copy.deepcopy(root + "/" + file_name))
			all_docs_dict[author_list[author_ind]] = copy.deepcopy(temp_path_list)
			del temp_path_list
			author_ind += 1
	return all_docs_dict
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

# Function to print all retrieved file paths
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def PrintAllFilePaths(all_docs_dict):
	num_docs = 0
	# Print out All File Paths
	for key in all_docs_dict:
		print key + ":"
		num_docs += len(all_docs_dict[key])
		for file_path in all_docs_dict[key]:
			print file_path
		print
	print "Number of Text Files Found: " + str(num_docs)
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=