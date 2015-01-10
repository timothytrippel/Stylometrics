import re, os

# Define REGEX's
hamilton_regex = re.compile(r"HAMILTON.*[\n]{1}")
jay_regex = re.compile(r"JAY.*[\n]{1}")
madison_regex = re.compile(r"MADISON.*[\n]{1}")
hamilton_and_madison_regex = re.compile(r"HAMILTON AND MADISON.*[\n]{1}") 
hamilton_or_madison_regex = re.compile(r"HAMILTON OR MADISON.*[\n]{1}")

# Define Directory Setup
os.mkdir("Federalist_Papers")
os.mkdir("Federalist_Papers/Hamilton")
os.mkdir("Federalist_Papers/Jay")
os.mkdir("Federalist_Papers/Madison")
os.mkdir("Federalist_Papers/Hamilton_AND_Madison")
os.mkdir("Federalist_Papers/Hamilton_OR_Madison")
output_file_name = "Paper_"
paper_counter = 1

# Open File
input_file_name = "FederalistPapers.txt"
input_file = open(input_file_name, "rb")
input_file_string = input_file.read()
papers_list = re.split(r"FEDERALIST.*[\d]+", input_file_string)
papers_list.pop(0)

# Close File
input_file.close()

# Process Text
for paper in papers_list:
	if (hamilton_and_madison_regex.search(paper)):
		temp_output_file_name = "Federalist_Papers/Hamilton_AND_Madison/" + output_file_name + str(paper_counter)
		temp_paper = hamilton_and_madison_regex.split(paper)
		temp_paper = temp_paper[-1]
	elif (hamilton_or_madison_regex.search(paper)):
		temp_output_file_name = "Federalist_Papers/Hamilton_OR_Madison/" + output_file_name + str(paper_counter)
		temp_paper = hamilton_or_madison_regex.split(paper)
		temp_paper = temp_paper[-1]
	elif (hamilton_regex.search(paper)):
		temp_output_file_name = "Federalist_Papers/Hamilton/" + output_file_name + str(paper_counter)
		temp_paper = hamilton_regex.split(paper)
		temp_paper = temp_paper[-1]
	elif (jay_regex.search(paper)):
		temp_output_file_name = "Federalist_Papers/Jay/" + output_file_name + str(paper_counter)
		temp_paper = jay_regex.split(paper)
		temp_paper = temp_paper[-1]
	elif (madison_regex.search(paper)):
		temp_output_file_name = "Federalist_Papers/Madison/" + output_file_name + str(paper_counter)
		temp_paper = madison_regex.split(paper)
		temp_paper = temp_paper[-1]
	
	temp_output_file = open(temp_output_file_name, "wb")
	temp_output_file.write(temp_paper)
	temp_output_file.close()
	paper_counter += 1

