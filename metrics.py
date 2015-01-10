#! usr/bin/env python2.7
import re
import copy

# Function to convert list of words to list of lowercase words
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def CastLowerCase(word_list):
	lower_case_words = []
	for word in word_list:
		lower_case_words.append(word.lower())
	return lower_case_words
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

# Function to convert list of words to list of lowercase words
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def CreateListOfWords(filename):
	inputFile = open(filename, "rb") # open file
	word_list = []
	for line in inputFile:
		temp_word_list = re.findall(r"[\w]+", line) # extract words in line into a list (array) of strings (words)
		lower_case_words = CastLowerCase(temp_word_list) # Cast all words to lowercase
		word_list.extend(copy.deepcopy(lower_case_words)) # Append deep copy of lower case lists
	inputFile.close() # close file
	return word_list
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

# Function to convert list of words to list of lowercase words
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def CreateListOfSentences(filename):
	inputFile = open(filename, "rb") # open file
	sentence_list = []
	input_file_text = inputFile.read()
	temp_sentence_list = re.split(r" *[\.\?\!][\'\"\)\]]* *", input_file_text)
	for sentence in temp_sentence_list:
		sentence_list.append(copy.deepcopy(re.findall(r"[\w]+", sentence)))
	inputFile.close() # close file
	return sentence_list
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

# Function to Extract Word Frequencies from a Text
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def ExtractWordFreqs(word_list, num_words):
	word_dict = {} #declare empty dictionary
	for i in range(num_words):
		word = word_list[i]
		# if word in dictionary --> increment
		if word_dict.has_key(word):
			word_dict[word] += 1
		# otherwise initialize value to 1
		else:
			word_dict[word] = 1

	# sort word dictionary into a list
	# item_list = []
	# for item in word_dict.items():
	# 	item_list.append(item)
	# item_list.sort(key=lambda x: x[1], reverse=True)

	return word_dict
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

# Extract Word Length Frequencies 
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def ExtractWordLengthFrequencies(word_list, num_words):
	length_dict = {} # create empty word lenght frequency dictionary
	for i in range(num_words):
		word = word_list[i]
		# if word length in dictionary --> increment frequency
		if length_dict.has_key(len(word)):
			length_dict[len(word)] += 1
		# otherwise initialize frequency to 1
		else:
			length_dict[len(word)] = 1
	
	# sort word dictionary into a list of tuples
	item_list = []
	for item in length_dict.items():
		item_list.append(item)
	item_list.sort(key=lambda x: x[0], reverse=False)	

	return item_list
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

# Extract Percentage of Words that begin with a Vowel 
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def ExtractVowelPercentage(word_list):
	totalNumWords = len(word_list)
	numVowels = 0
	for word in word_list:
		if word[0] == 'a':
			numVowels += 1
		elif word[0] == 'e':
			numVowels += 1
		elif word[0] == 'i':
			numVowels += 1
		elif word[0] == 'o':
			numVowels += 1
		elif word[0] == 'u':
			numVowels += 1
		# elif word[0] == 'y':
		# 	numVowels += 1
	return (float(numVowels)/float(totalNumWords))*100
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

# Extract Average Number of Words per Sentence
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def CalcAvgWordsPerSentence(word_list, sentence_list):
	return float(len(word_list))/float(len(sentence_list))
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

# Extract Words per Sentence Frequencies
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def ExtractWordsPerSentenceFreqs(sentence_list, num_sentences):
	word_count_dict = {}
	# check if num_sentences is a valid number for number of sentences present in the text
	if num_sentences > len(sentence_list):
		num_sentences = len(sentence_list)
	for i in range(len(sentence_list)):
		sentence = sentence_list[i]
		if word_count_dict.has_key(len(sentence)):
			word_count_dict[len(sentence)] += 1
		else:
			word_count_dict[len(sentence)] = 1

	# sort word dictionary into a list of tuples
	item_list = []
	for item in word_count_dict.items():
		item_list.append(item)
	item_list.sort(key=lambda x: x[0], reverse=False)

	return item_list
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

# Function to Print Word Frequencies
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def PrintWordFreqs(freqDict):
	print "Word Frequencies"
	for key in freqDict:
		print key + ": " + str(freqDict[key])
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

# Function to Print Word Length Frequencies
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def PrintWordLengthFreqs(lengthFreqList):
	print "Word Length Frequencies"
	for entry in lengthFreqList:
		print str(entry[0]) + ": " + str(entry[1])
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

# Function to Print Vowel Percentage Frequencies
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def PrintVowelPercentage(vowelPercentage):
	print "Percentage of Words that begin with a Vowel:"
	print format(vowelPercentage, '.2f') + "%"
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

# Function to Print Number of Sentences in a Text
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def PrintNumTotalSentences(total_num_sentences):
	print "Number of Sentences in Text: " + str(total_num_sentences)
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

# Function to Print Average Number of Words Per Sentence in a Text
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def PrintAvgWordsPerSentence(avgWordsPerSentence):
	print "Average Number of Words Per Sentence: " + str(avgWordsPerSentence)
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

# Function to Print Words Per Sentence Frequencies
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def PrintWordsPerSentenceFreqs(word_counts):
	print " Words Per Sentence Frequencies: "
	for entry in word_counts:
		print str(entry[0]) + ": " + str(entry[1])
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

# Function to evaluate metrics on a text
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def ExtractMetrics(filename, num_words, num_sentences):
	word_list = CreateListOfWords(filename) # Extract word list from a .txt file
	sentence_list = CreateListOfSentences(filename) # Extract sentence list from a .txt file

	# Verify document contains at least "num_words" number of words --> return None (python equivalent to NULL) if condition not met
	if num_words > len(word_list):
		print "Error: document %s does not contain enough words to complete stylometric analysis." % (filename)
		print # Print new line char
		return None

	# Verify documnet contains at least "num_sentences" number of sentences --> return None (python equivalent to NULL) if condition not met
	if num_sentences > len (sentence_list):
		print "Error: document %d does not contain enough sentences to complete stylometric analysis." % (filename)
		print # Print new line char
		return None

	# Extract all metrics for the given document
	freqDict = ExtractWordFreqs(word_list, num_words) # Extract word frequencies from word list
	lengthFreqList = ExtractWordLengthFrequencies(word_list, num_words) # Extract word length frequencies from word list
	vowelPercentage = ExtractVowelPercentage(word_list) # Extract percentage of words that begin with a vowel
	avgWordsPerSentence = CalcAvgWordsPerSentence(word_list, sentence_list) # Calculate average number of words per sentence
	wordsPerSentenceFreqs = ExtractWordsPerSentenceFreqs(sentence_list, num_sentences) # Extract words per sentence frequencies

	# Return all gathered metrics in a dictionary
	return {"freq_dict": freqDict, "length_freq_list": lengthFreqList, "words_per_sentence_freq": wordsPerSentenceFreqs, "vowel_percentage": vowelPercentage, "num_sentences": len(sentence_list), "avg_words_per_sentence": avgWordsPerSentence}

# Function to print out all metrics on a text
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def PrintMetrics(metrics_dict):
	PrintWordFreqs(metrics_dict["freq_dict"]) # print out word frequencies
	print # print new line char
	PrintWordLengthFreqs(metrics_dict["length_freq_list"]) # print out word frequencies
	print # print new line char
	PrintVowelPercentage(metrics_dict["vowel_percentage"]) # print out vowel percentage
	print # print new line char
	PrintNumTotalSentences(metrics_dict["num_sentences"]) # print out total number of sentences in a text
	print # print new line char
	PrintAvgWordsPerSentence(metrics_dict["avg_words_per_sentence"]) # print out average number of words per sentence
	print # print new line char
	PrintWordsPerSentenceFreqs(metrics_dict["words_per_sentence_freq"]) # print out words per sentence frequencies
	print # print new line char

