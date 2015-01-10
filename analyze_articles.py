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

# Instantiate HTML Graph Generator Object --> what will generate all plots dynamically
html_graph = HTML_GenerateReport.HTML_Report("graphUI.html", html_output_filename)

#-=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=-
# Get File Paths by calling the function "GetFilePaths" inside the "file_path.py" module
#-=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=-
# Input: home directory (as a string)
# 
# Output: dictionary of file paths, where the key is the AUTHOR and the value is a 
# list of file paths as strings
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
	# Temporary data structures to aggregate data across a SET of DOCUMENTS for a SINGLE AUTHOR
	#-=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=-
	# Word Frequencies - Temp Data
	author_word_freqs = []

	# Word Length Frequencies - Temp Data
	author_word_length_freqs = []
	max_word_length = 0

	# Word Per Sentence Frequencies - Temp Data
	author_words_per_sentence_freqs = []
	max_words_per_sentence_freq = 0

	# Vowel Percentages - Temp Data
	vowel_percentages = [] 

	# Words Per Sentence - Temp Data
	words_per_sentence_counts = []
	#-=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=-

	# Iterate through a set of file paths to read documents, analyzes them, and aggregate all metrics for a single author
	for temp_file_path in temp_file_path_list:
		#-=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=	
		# Extract all stylometrics from the document
		#-=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=	
		# Listed below is the format by which the "ExtractMetrics" function, which is a member of the "metrics.py" module, should
		# be called. This function takes in a file path (as a string), a word count (as an int), and a sentence count (as an int).
		# The function outputs stylometric data for the input document in the form of a dictionary. The format of the dictionary is
		# as described below:
		# 
		# (Each entry in the dictionary is a <key, value> pair, of which all strings in "key"-position below are the actual keys used
		# in each "metrics_dict")
		# 
		# metrics_dict = {
		# 	"freq_dict": <dictionary (of format <word, frequency>) of word frequencies for the first X number of words>, 
		# 	"length_freq_list": <>, 
		# 	"words_per_sentence_freq": <>, 
		# 	"vowel_percentage": <percentage of words that begin with a vowel in a given document as a FLOAT>, 
		# 	"num_sentences": <number of sentences in the given document as an INT>, 
		# 	"avg_words_per_sentence": <average number of words per sentence in the given document as a FLOAT>
		# }
		# 
		# Function Call Format:
		# metrics.ExtractMetrics(<file path of .txt document>, <number of words to analyze>, <number of sentences to analyze>)
		# 
		# Note: if an insufficient number of WORDS or SENTENCES are encounted in a given document, the function will print
		# an error message indicating which is the case, and return "None" (Python equivalent to NULL) instead of a dictionary
		# full of data.

		metrics_dict = metrics.ExtractMetrics(temp_file_path, 400, 10)
		#-=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=	

		# Verify all stylometrics were successfully extracted from the document
		if metrics_dict == None:
			print "Error: could not complete stylometric analysis on document %s." % (temp_file_path)
			print
			sys.exit(1) # exit script with error code 1

		# Word Frequecies --> METRIC #1
		author_word_freqs.append(metrics_dict["freq_dict"])

		# Word Length Frequencies (keep track of max frequency seen so far --> for plotting purposes) --> METRIC #2
		word_length_freqs = metrics_dict["length_freq_list"]
		if word_length_freqs[-1][0] > max_word_length:
			max_word_length = word_length_freqs[-1][0]
		author_word_length_freqs.append(copy.deepcopy(word_length_freqs))

		# Words Per Sentence Frequencies (keep track of max frequency seen so far --> for plotting purposes) --> METRIC #3
		words_per_sentence_freqs = metrics_dict["words_per_sentence_freq"]
		if words_per_sentence_freqs[-1][0] > max_words_per_sentence_freq:
			max_words_per_sentence_freq = words_per_sentence_freqs[-1][0]
		author_words_per_sentence_freqs.append(copy.deepcopy(words_per_sentence_freqs))

		# Percentage of Words that begin with a Vowel --> METRIC #4
		vowel_percentages.append(metrics_dict["vowel_percentage"])

		# Avg Number of Words Per Sentence --> METRIC #5
		words_per_sentence_counts.append(metrics_dict["avg_words_per_sentence"])
		
	#-=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=	
	# Call ADD-FUNCTION in plotting library --> to add all metric data for a single author to html graph generator
	#-=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=	
	# Listed below is the format of the function that needs to be called to add the metric data for ALL of the documents
	# for a given AUTHOR. This adds the data to the library's internal "data base" where it will undergo further processing
	# when it is time to plot the data, after all data for each author has been aggregated.
	# 
	# BASIC FORMAT: def AddAllData(author, metric_1, metric_2, metric_3, metric_4, metric_5) 
	# <data, data format (type)>
	# 
	# DETAILED FORMAT:
	# def AddAllData(<author, string>, <word frequecies, list of dictionaries>, <word length frequencies, list of lists>,
	# 	<maximum word length encounted, int>, <words per sentence frequencies, list of lists>,
	# 	<maximum number of words per sentence encountered, int>, <vowel percentage data, list of floats>, 
	#	<average number of words per sentence per document, list of floats>)
	# 
	# Note: each argument is in the format --> <data, data format (type)>; where the first item listed is the arguement, 
	# and the second value listed is argument format/type.

	html_graph.AddAllData(key, author_word_freqs, author_word_length_freqs, max_word_length, author_words_per_sentence_freqs, max_words_per_sentence_freq, vowel_percentages, words_per_sentence_counts)
	#-=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=	

	#-=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=	
	# Clear out data lists for next author
	#-=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=	
	# REASON: Python uses refereces for ALL variables, so must call a function to mark the references
	# for garbage collection, otherwise they are not cleared until they go out of scope, which in this case (because of the location of
	# their declarations) is not until the script terminates.

	del author_word_freqs
	del author_word_length_freqs
	del author_words_per_sentence_freqs
	del vowel_percentages
	del words_per_sentence_counts
	#-=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=	

# Generate HTML Plot
html_graph.GenerateGraph()




