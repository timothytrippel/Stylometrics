#! usr/bin/env python2.7
import re, copy
#-----------------------------------------------------------------------------------------------------------------------
class HTML_Report():
	def __init__(self, template_filename, newFileName, num_words_to_plot_frequencies):
		self.HTML_Report_template = template_filename
		self.HTML_Report_Output = newFileName
		self.num_words_to_plot_frequencies = num_words_to_plot_frequencies
		self.chart_colors = ['#e2431e', '#6f9654', '#1c91c0', '#e7711b', '#f1ca3a', '#43459d']

		#-=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=-
		# Temp Graphing Data
		#-=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=-
		# Temp Data for Word Frequency Graph
		self.word_freq_data_string = "var word_freq_data = google.visualization.arrayToDataTable([\n['Word'"
		self.word_freq_master_dict = {}
		self.word_freq_author_list = []
		self.wf_data = ""

		# Temp Data for Word Length Frequency Graph
		self.word_length_data_string_1 = "var word_length_data_1 = google.visualization.arrayToDataTable([\n ['Word Length'"
		self.word_length_data_string_2 = "var word_length_data_2 = google.visualization.arrayToDataTable([\n ['Word Length'"
		self.word_length_data = []
		self.word_length_data_max_freq = 0
		self.wlf_data_1 = ""
		self.wlf_data_2 = ""

		# Temp Data for Word Length Frequency Graph
		self.words_per_sentence_freq_data_string_1 = "var words_per_sentence_freq_data_1 = google.visualization.arrayToDataTable([\n ['Words Per Sentence'"
		self.words_per_sentence_freq_data_string_2 = "var words_per_sentence_freq_data_2 = google.visualization.arrayToDataTable([\n ['Words Per Sentence'"
		self.words_per_sentence_freq_data = []
		self.words_per_sentence_freq_data_max_freq = 0
		self.wpsf_data_1 = ""
		self.wpsf_data_2 = ""

		# Temp Data for Vowel Percentages
		self.vowel_percentage_data = []
		self.vp_max_num_docs = 0
		self.vowel_percentage_data_string_1 = "var vowel_percentage_data_1 = google.visualization.arrayToDataTable([\n [\"Author\", \"Percent\", {role: \"style\"}],"
		self.vowel_percentage_data_string_2 = "var vowel_percentage_data_2 = google.visualization.arrayToDataTable([\n [\"Author\""
		self.vp_data_1 = ""
		self.vp_data_2 = ""

		# Temp Data for Words Per Sentence Counts
		self.words_per_sentence_data = []
		self.wps_max_num_docs = 0
		self.words_per_sentence_data_string_1 = "var words_per_sentence_data_1 = google.visualization.arrayToDataTable([\n [\"Author\", \"Percent\", {role: \"style\"}],"
		self.words_per_sentence_data_string_2 = "var words_per_sentence_data_2 = google.visualization.arrayToDataTable([\n [\"Author\""
		self.wps_data_1 = ""
		self.wps_data_2 = ""
		#-=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=-

	#-=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=-
	def AddAllData(self, key, metrics):	
		# Word Frequencies - Temp Data
		author_word_freqs = []
		doc_word_lengths = []

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

		# Metric Dictionary List (will hold all metric dictionary for a SINGLE AUTHOR)
		list_of_metric_dictionaries = []

		for metrics_dict in metrics:
			# Word Frequecies --> METRIC #1
			author_word_freqs.append(metrics_dict["freq_dict"])
			doc_word_lengths.append(metrics_dict["num_words"])

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

		# Add word frequency (for a single author) data to html graph generator
		self.AddWordFreqData(key, author_word_freqs, doc_word_lengths)
		# Add all word length frequency (for a single author) data to html graph generator
		self.AddWordLengthFreqData(key, author_word_length_freqs, max_word_length)
		# Add all words per sentence frequency (for a single author) data to html graph generator
		self.AddWordsPerSentenceFreqData(key, author_words_per_sentence_freqs, max_words_per_sentence_freq)
		# Add all vowel percentage (for a single author) data to html graph generator
		self.AddVowelPercentageData(key, vowel_percentages)
		# Add all words per sentence counts (for a single author) data to html graph generator
		self.AddWordsPerSentenceData(key, words_per_sentence_counts)

	#-=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=-
	def AddWordFreqData(self, author, data, doc_lengths):
		self.word_freq_author_list.append([author, data, doc_lengths])

		# Add author to header string
		self.word_freq_data_string += (", '%s', {role: \"style\"}" % (author))

		# Add frequencies to master list
		for doc_word_dict in data:
			for key in doc_word_dict:
				if self.word_freq_master_dict.has_key(key):
					self.word_freq_master_dict[key] += doc_word_dict[key]
				else:
					self.word_freq_master_dict[key] = doc_word_dict[key]

	def AddWordLengthFreqData(self, author, data, max_freq):
		# Created matrix of 0's of proper size
		formatted_data = [[0]*max_freq]
		for i in range(len(data)-1):
			formatted_data.append([0]*max_freq)

		# Fill in zero matrix with values
		for i in range(len(data)):
			for entry in data[i]:
				formatted_data[i][entry[0]-1] = entry[1]

		# Store Formatted Data
		self.word_length_data_string_1 += (", \'" + author + "\', {role: \"style\"}")
		self.word_length_data_string_2 += (", \'" + author + "\', {role: \"style\"}")*len(data)
		self.word_length_data.append(formatted_data) # store data
		if self.word_length_data_max_freq < max_freq: # store/update max freq value
			self.word_length_data_max_freq = max_freq

	def AddWordsPerSentenceFreqData(self, author, data, max_freq):
		# Created matrix of 0's of proper size
		formatted_data = [[0]*max_freq]
		for i in range(len(data)-1):
			formatted_data.append([0]*max_freq)

		# Fill in zero matrix with values
		for i in range(len(data)):
			for entry in data[i]:
				formatted_data[i][entry[0]-1] = entry[1]

		# Store Formatted Data
		self.words_per_sentence_freq_data_string_1 += (", \'" + author + "\', {role: \"style\"}")
		self.words_per_sentence_freq_data_string_2 += (", \'" + author + "\', {role: \"style\"}")*len(data)
		self.words_per_sentence_freq_data.append(formatted_data) # store data
		if self.words_per_sentence_freq_data_max_freq < max_freq: # store/update max freq value
			self.words_per_sentence_freq_data_max_freq = max_freq

	def AddVowelPercentageData(self, author, data):
		self.vowel_percentage_data.append([author, data]) # temporarily store data
		# keep track of max number of docs used by any one author
		if len(data) > self.vp_max_num_docs:
			self.vp_max_num_docs = len(data)

	def AddWordsPerSentenceData(self, author, data):
		self.words_per_sentence_data.append([author, data]) # temporarily store data
		# keep track of max number of docs used by any one author
		if len(data) > self.wps_max_num_docs:
			self.wps_max_num_docs = len(data)

	#-=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=-
	def ProcessWordFreqData(self):
		# define number of words
		num_words_to_plot = self.num_words_to_plot_frequencies

		# sort master word frequency dictionary into a list of decreasing frequecies
		sorted_master_list = []
		for item in self.word_freq_master_dict.items():
			sorted_master_list.append(item)
		sorted_master_list.sort(key=lambda x: x[1], reverse=True)

		# calculate average word frequencies for each author
		averaged_author_word_freqs = []
		for author_data in self.word_freq_author_list:
			author = author_data[0]
			num_docs = len(author_data[1])
			num_total_words = sum(author_data[2])
			all_docs_data = author_data[1]
			author_temp_freq_dict = {}
			for doc_word_dict in all_docs_data:
				for word_entry in sorted_master_list[0:num_words_to_plot]:
					if author_temp_freq_dict.has_key(word_entry[0]):
						if doc_word_dict.has_key(word_entry[0]):
							author_temp_freq_dict[word_entry[0]] += doc_word_dict[word_entry[0]]
					else:
						if doc_word_dict.has_key(word_entry[0]):
							author_temp_freq_dict[word_entry[0]] = doc_word_dict[word_entry[0]]

			for key in author_temp_freq_dict:
				author_temp_freq_dict[key] = (float(author_temp_freq_dict[key])/float(num_total_words))*100.000
			averaged_author_word_freqs.append([author, copy.deepcopy(author_temp_freq_dict)])

		# create data strings
		for i in range(len(sorted_master_list[0:num_words_to_plot])):
			word = sorted_master_list[i][0]
			self.wf_data += ("],\n[\'%s\'" % (word))
			for j in range(len(averaged_author_word_freqs)):
				author_color = self.chart_colors[j]
				author_word_dict = averaged_author_word_freqs[j][1]
				self.wf_data += (", %f, \"%s\"" % (author_word_dict[word], author_color))
		self.wf_data = self.word_freq_data_string + self.wf_data + "]\n]);"

	def ProcessWordLengthFreqData1(self):
		# Calculate averages for each author
		average_data_list = []
		for author_data in self.word_length_data:
			num_docs_for_author = len(author_data)
			temp_avgs = [0.0]*self.word_length_data_max_freq
			for doc_data in author_data:
				for j in range(len(doc_data)):
					temp_avgs[j] += doc_data[j]
			for i in range(len(temp_avgs)):
				temp_avgs[i] = float(temp_avgs[i])/float(num_docs_for_author)
			average_data_list.append(copy.deepcopy(temp_avgs))
			del temp_avgs

		# Comlete data string
		data_strings = []
		for i in range(self.word_length_data_max_freq):
			data_strings.append("],\n[" + str(i+1)) # complete header string and start new data table row entry
			for j in range(len(average_data_list)):
				author_data = average_data_list[j]
				data_strings[i] += (", " + str(author_data[i]) + (", \"%s\"" % (self.chart_colors[j])))
		data_strings[-1] += "]\n]);"
		self.wlf_data_1 = self.word_length_data_string_1 + ''.join(data_strings)

	def ProcessWordLengthFreqData2(self):
		# Setup data string
		data_strings = []
		for i in range(self.word_length_data_max_freq):
			data_strings.append("],\n[" + str(i+1)) # complete header string and start new data table line
			for j in range(len(self.word_length_data)):
				author_data = self.word_length_data[j] 
				for doc_data in author_data:
					if i < len(doc_data):
						data_strings[i] += (", " + str(doc_data[i]) + (", \"%s\"" % (self.chart_colors[j])))
					else:
						data_strings[i] += (", null, null")
		data_strings[-1] += "]\n]);"

		# Build Data String
		self.wlf_data_2 = self.word_length_data_string_2 + ''.join(data_strings) 

	def ProcessWordsPerSentenceFreqData1(self):
		# Calculate averages for each author
		average_data_list = []
		for author_data in self.words_per_sentence_freq_data:
			num_docs_for_author = len(author_data)
			temp_avgs = [0.0]*self.words_per_sentence_freq_data_max_freq
			for doc_data in author_data:
				for j in range(len(doc_data)):
					temp_avgs[j] += doc_data[j]
			for i in range(len(temp_avgs)):
				temp_avgs[i] = float(temp_avgs[i])/float(num_docs_for_author)
			average_data_list.append(copy.deepcopy(temp_avgs))
			del temp_avgs

		# Comlete data string
		data_strings = []
		for i in range(self.words_per_sentence_freq_data_max_freq):
			data_strings.append("],\n[" + str(i+1)) # complete header string and start new data table row entry
			for j in range(len(average_data_list)):
				author_data = average_data_list[j]
				data_strings[i] += (", " + str(author_data[i]) + (", \"%s\"" % (self.chart_colors[j])))
		data_strings[-1] += "]\n]);"
		self.wpsf_data_1 = self.words_per_sentence_freq_data_string_1 + ''.join(data_strings)

	def ProcessWordsPerSentenceFreqData2(self):
		# Setup data string
		data_strings = []
		for i in range(self.words_per_sentence_freq_data_max_freq):
			data_strings.append("],\n[" + str(i+1)) # complete header string and start new data table line
			for j in range(len(self.words_per_sentence_freq_data)):
				author_data = self.words_per_sentence_freq_data[j] 
				for doc_data in author_data:
					if i < len(doc_data):
						data_strings[i] += (", " + str(doc_data[i]) + (", \"%s\"" % (self.chart_colors[j])))
					else:
						data_strings[i] += (", null, null")
		data_strings[-1] += "]\n]);"

		# Build Data String
		self.wpsf_data_2 = self.words_per_sentence_freq_data_string_2 + ''.join(data_strings) 

	def ProcessVowelPercentageData1(self):
		# Format Data data as percentages for each author only
		formatted_data = []
		for i in range(len(self.vowel_percentage_data)):
			author_data = self.vowel_percentage_data[i]
			author = author_data[0]
			data = author_data[1]
			avg_of_data = sum(data)/len(data)
			formatted_data.append("\n[\"%s\", %f, \"%s\"]" % (author, avg_of_data, self.chart_colors[i]))
		self.vp_data_1 = self.vowel_percentage_data_string_1 + ', '.join(formatted_data)
		self.vp_data_1 += "\n]);"

	def ProcessVowelPercentageData2(self):
		# Complete header data string
		header_strings_list = []
		for i in range(self.vp_max_num_docs):
			header_strings_list.append("\"Document_%d\", {role: \"style\"}" % (i+1))
		header_string = ', '.join(header_strings_list)
		self.vowel_percentage_data_string_2 += (", " + header_string)

		# Setup list of data strings
		for i in range(len(self.vowel_percentage_data)):
			formatted_vowel_data = []
			author_data = self.vowel_percentage_data[i]
			formatted_vowel_data.append("\"%s\"" % (author_data[0]))
			for j in range(self.vp_max_num_docs):
				# make data table symmetric even if an unequal number fo documents per author were provided
				if j < len(author_data[1]):
					doc_data_val = author_data[1][j]
					formatted_vowel_data.append("%s, \"%s\"" % (format(doc_data_val, '2.0f'), self.chart_colors[i]))
				else:
					doc_data_val = "null"
					formatted_vowel_data.append("%s, \"%s\"" % (doc_data_val, self.chart_colors[i]))
			self.vp_data_2 += ("], \n[" + ', '.join(formatted_vowel_data))
		self.vp_data_2 = self.vp_data_2 + "] \n]);"
		self.vp_data_2 = self.vowel_percentage_data_string_2 + self.vp_data_2

	def ProcessWordsPerSentenceData1(self):
		# Format Data data as percentages for each author only
		formatted_data = []
		for i in range(len(self.words_per_sentence_data)):
			author_data = self.words_per_sentence_data[i]
			author = author_data[0]
			data = author_data[1]
			avg_of_data = sum(data)/len(data)
			formatted_data.append("\n[\"%s\", %f, \"%s\"]" % (author, avg_of_data, self.chart_colors[i]))
		self.wps_data_1 = self.words_per_sentence_data_string_1 + ', '.join(formatted_data)
		self.wps_data_1 += "\n]);"

	def ProcessWordsPerSentenceData2(self):
		# Complete header data string
		header_strings_list = []
		for i in range(self.wps_max_num_docs):
			header_strings_list.append("\"Document_%d\", {role: \"style\"}" % (i+1))
		header_string = ', '.join(header_strings_list)
		self.words_per_sentence_data_string_2 += (", " + header_string)

		# Setup list of data strings
		for i in range(len(self.words_per_sentence_data)):
			formatted_wps_data = []
			author_data = self.words_per_sentence_data[i]
			formatted_wps_data.append("\"%s\"" % (author_data[0]))
			for j in range(self.wps_max_num_docs):
				# make data table symmetric even if an unequal number fo documents per author were provided
				if j < len(author_data[1]):
					doc_data_val = author_data[1][j]
					formatted_wps_data.append("%s, \"%s\"" % (format(doc_data_val, '2.0f'), self.chart_colors[i]))
				else:
					doc_data_val = "null"
					formatted_wps_data.append("%s, \"%s\"" % (doc_data_val, self.chart_colors[i]))
			self.wps_data_2 += ("], \n[" + ', '.join(formatted_wps_data))
		self.wps_data_2 = self.wps_data_2 + "] \n]);"
		self.wps_data_2 = self.words_per_sentence_data_string_2 + self.wps_data_2
	
	#-=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=-
	def GenerateGraph(self):
		self.ProcessAllData()
		self.WriteGraphData()

	def ProcessAllData(self):
		self.ProcessWordFreqData() 
		self.ProcessWordLengthFreqData1()
		self.ProcessWordLengthFreqData2()
		self.ProcessWordsPerSentenceFreqData1()
		self.ProcessWordsPerSentenceFreqData2()
		self.ProcessVowelPercentageData1()
		self.ProcessVowelPercentageData2()
		self.ProcessWordsPerSentenceData1()
		self.ProcessWordsPerSentenceData2()

	def WriteGraphData(self):
		template = open(self.HTML_Report_template, "r") #open template file
		outputReport = open(self.HTML_Report_Output, "wb") #open output file
		
		# define/compile line regex
		word_length_freq_graph1_regex = re.compile(r"/\*-----<INSERT0>-----\*/")
		word_length_freq_graph2_regex = re.compile(r"/\*-----<INSERT1>-----\*/")
		vowel_percentage_graph1_regex = re.compile(r"/\*-----<INSERT2>-----\*/")
		vowel_percentage_graph2_regex = re.compile(r"/\*-----<INSERT3>-----\*/")
		words_per_sentence_graph1_regex = re.compile(r"/\*-----<INSERT4>-----\*/")
		words_per_sentence_graph2_regex = re.compile(r"/\*-----<INSERT5>-----\*/")
		words_per_sentence_freq_graph1_regex = re.compile(r"/\*-----<INSERT6>-----\*/")
		words_per_sentence_freq_graph2_regex = re.compile(r"/\*-----<INSERT7>-----\*/")
		word_freq_graph_regex = re.compile(r"/\*-----<INSERT8>-----\*/")
		
		# scan file line by line
		for line in template:
			if word_length_freq_graph1_regex.search(line):
				line = re.sub(r"/\*-----<INSERT0>-----\*/", self.wlf_data_1, line, count=0)
			elif word_length_freq_graph2_regex.search(line):
				line = re.sub(r"/\*-----<INSERT1>-----\*/", self.wlf_data_2, line, count=0)
			elif vowel_percentage_graph1_regex.search(line):
				line = re.sub(r"/\*-----<INSERT2>-----\*/", self.vp_data_1, line, count=0)
			elif vowel_percentage_graph2_regex.search(line):
				line = re.sub(r"/\*-----<INSERT3>-----\*/", self.vp_data_2, line, count=0)
			elif words_per_sentence_graph1_regex.search(line):
				line = re.sub(r"/\*-----<INSERT4>-----\*/", self.wps_data_1, line, count=0)
			elif words_per_sentence_graph2_regex.search(line):
				line = re.sub(r"/\*-----<INSERT5>-----\*/", self.wps_data_2, line, count=0)
			elif words_per_sentence_freq_graph1_regex.search(line):
				line = re.sub(r"/\*-----<INSERT6>-----\*/", self.wpsf_data_1, line, count=0)
			elif words_per_sentence_freq_graph2_regex.search(line):
				line = re.sub(r"/\*-----<INSERT7>-----\*/", self.wpsf_data_2, line, count=0)
			elif word_freq_graph_regex.search(line):
				line = re.sub(r"/\*-----<INSERT8>-----\*/", self.wf_data, line, count=0)
			outputReport.write(line) #write line of code to output file		
		
		#Close Files
		template.close() #close template file
		outputReport.close() #close output report