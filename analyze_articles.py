import os
import sys
import copy
import metrics # This module should be developed by Christopher (a.k.a. Mom)

# Libraries imported below were developed by Timothy D. Trippel
import file_path
import HTML_GenerateReport

# User Defined Inputs (can edit script everytime or can integrate command line args)
html_output_filename = "fed_paper_metrics.html" 
home_dir = "Federalist_Papers"
num_words_to_plot_frequencies_for = 20

#-=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=-
# Instantiate HTML Graph Generator Object --> what will generate all plots dynamically
#-=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=-
# Input: 3 parameters --> (<name of template HTML file>, <name of desired output html file>, <top number of words to plot frequencies for>)
# 
# Output: is an instantiated "HTML_Report" class (an object)

html_graph = HTML_GenerateReport.HTML_Report("graphUI.html", html_output_filename, num_words_to_plot_frequencies_for)
#-=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=-

#-=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=-
# Get File Paths by calling the function "GetFilePaths" inside the "file_path.py" module
#-=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=-
# Input: home directory (as a string)
# 
# Output: dictionary of file paths, where the key is the AUTHOR and the value is a 
# list of file paths as strings
# 
# all_docs_dict = {
# 	author1: [<full_path_1>, <full_path_2>, <full_path_3>, ..., <full_path_3>],
# 	author2: [<full_path_1>, <full_path_2>, <full_path_3>, ..., <full_path_3>],
# 	author3: [<full_path_1>, <full_path_2>, <full_path_3>, ..., <full_path_3>],
# 	author4: [<full_path_1>, <full_path_2>, <full_path_3>, ..., <full_path_3>],
# 	.
# 	.
# 	.
# }
# 
# Directory structure of the "home directory" given as input to the function should be:
# Home_Directory:
# 	Author_Directory_1:
# 		Document_1.txt
# 		Document_2.txt
# 		.
# 		.
# 		.
# 	Author_Directory_2:
# 		Document_1.txt
# 		Document_2.txt
# 		.
# 		.
# 		.
# 	Author_Directory_3:
# 		Document_1.txt
# 		Document_2.txt
# 		.
# 		.
# 		.
# 	Author_Directory_4:
# 		Document_1.txt
# 		Document_2.txt
# 		.
# 		.
# 		.

all_docs_dict = file_path.GetFilePaths(home_dir) # Retrieve full file paths
# file_path.PrintAllFilePaths(all_docs_dict) # Print all file paths (for debugging/verification)
#-=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=-

# Gather Metrics
for key in all_docs_dict:
	temp_file_path_list = all_docs_dict[key]

	#-=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=-
	# Temporary data structure to aggregate data across a SET of DOCUMENTS for a SINGLE AUTHOR
	#-=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=-

	# Metric Dictionary List (will hold all metric dictionary for a SINGLE AUTHOR)
	list_of_metric_dictionaries = []
	#-=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=-

	# Iterate through a set of file paths to read documents, analyzes them, and aggregate all metrics for a single author
	for temp_file_path in temp_file_path_list:
		#-=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=	
		# Extract all stylometrics from the document
		#-=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=	
		# Listed below is the format by which the "ExtractMetrics" function, which is a member of the "metrics.py" module, should
		# be called. This function takes in a file path (as a string). The function outputs stylometric data for the input 
		# document in the form of a dictionary. The format of the dictionary is as described below:
		# 
		# (Each entry in the dictionary is a <key, value> pair, of which all strings in "key"-position below are the actual keys used
		# in each "metrics_dict")
		# 
		# metrics_dict = {
		# 	"freq_dict": <dictionary (of format <word, frequency>) of word frequencies for the first X number of words>, 
		# 	"length_freq_list": <list (of tuples of format (word length, frequency)) of word length frequencies>, 
		# 	"words_per_sentence_freq": <list (of tuples of format (sentend length, frequency)) of sentence length frequecies>,
		# 	"vowel_percentage": <percentage of words that begin with a vowel in a given document as a FLOAT>, 
		# 	"num_sentences": <number of sentences in the given document as an INT>, 
		# 	"avg_words_per_sentence": <average number of words per sentence in the given document as a FLOAT>
		# }
		# 
		# Function Call Format:
		# metrics.ExtractMetrics(<file path of .txt document>)

		metrics_dict = metrics.ExtractMetrics(temp_file_path)
		#-=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=	

		# Append all metric information for a single document to a list
		list_of_metric_dictionaries.append(metrics_dict)
		
	#-=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=	
	# Call ADD-FUNCTION in plotting library --> to add all metric data for a single author to html graph generator
	#-=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=	
	# Listed below is the format of the function that needs to be called to add the metric data for ALL of the documents
	# for a given AUTHOR. This adds the data to the library's internal "data base" where it will undergo further processing
	# when it is time to plot the data, after all data for each author has been aggregated.
	# 
	# BASIC FORMAT: def AddAllData(author, list of metric dictionaries) 
	# 
	# DETAILED FORMAT:
	# def AddAllData(<author, string>, <list of metrics, list of dictionaries>)
	# 
	# <data, data format (type)>
	# 
	# Note: each argument is in the format --> <data, data format (type)>; where the first item listed is the arguement, 
	# and the second value listed is argument format/type.

	html_graph.AddAllData(key, list_of_metric_dictionaries)
	#-=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=	

	#-=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=	
	# Clear out data list for next author
	#-=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=	
	# REASON: Python uses refereces for ALL variables, so you must call a function to mark the references
	# for garbage collection, otherwise they are not cleared until they go out of scope, which in this case (because of the location of
	# their declarations) is not until the script terminates, or possibly when the outer loop terminates.

	del list_of_metric_dictionaries
	#-=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=	

# Generate HTML Plot
html_graph.GenerateGraph()




