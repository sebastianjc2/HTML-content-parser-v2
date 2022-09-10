# Filename: CaballeroSebastian_066_P3

### ADD YOUR NAME, STUDENT ID AND SECTION NUMBER BELOW ###
# NAME: Sebastian J. Caballero Diaz
# STUDENT ID: 802-19-2461
# SECTION: 066

"""Parse the contents of an HTML file and output the internal resources used.

We are looking for tags of interest: a, script, link, img, audio, video, and form.
Within each tag of interest we're looking for a particular attribute of
interest (href for a & link, src for script & img, action for form).
Each tag of interest is to be represented by a dictionary, where the attribute names
will be the dictionary keys and the attribute values will be the dictionary values.
A list is created for each type of tag, storing all of the internal 
resources referenced by tags of that type.
Finally, the results are stored in an output file.

Input:  The file index.html will be used as an input file
Output: The results will be stored in a file named index_resources.txt
"""

# CONSTANTS

INPUTFILE = 'index.html'
OUTPUTFILE = 'index_resources.txt'
# We'll use a dictionary where the keys are the tags of interest and the values
# are the corresponding attributes of interest.  That way we can process the HTML
# file using this dictionary without having to look for specific tags or attributes.
DICTOFINTEREST = {'a':'href','link':'href','form':'action',
                  'img':'src','script':'src','audio':'src','video':'src'}


def load_data():
	"""Returns the contents of the input file as a list of lines, or None if an error occurs."""
	try:
		fh = open(INPUTFILE)
	except:
		linesInFile = None
	else: # Only gets executed if no exception was raised
		linesInFile = fh.readlines()
		fh.close()
	return linesInFile


def get_tag_of_interest(line):
	"""Return a tag of interest if one is found in the line, or None otherwise.

	Parameters:
		line - A single line of text from the HTML file being processed.
	Returns:
		A string with the (opening) tag of interest, if one is found, or None otherwise.
	"""
	# The tags of interest are the keys to the dictionary DICTOFINTEREST.
	for tagName in DICTOFINTEREST:
		# Note that, for a tag to have a resource, it must have a space after the tag name
		openingTag = '<' + tagName + ' '
		if openingTag in line: # Found it!
			posTagBegin = line.find(openingTag)
			# Make sure we don't just find any '>', but the next one after the start of the tag.
			posTagEnd = line.find('>', posTagBegin)
			return line[posTagBegin:posTagEnd+1]
	# If we're still in the function, then we didn't find any tags of interest.
	return None


def get_attr_of_interest(tag):
	"""Return value of attribute of interest if one is in the tag, or None otherwise.

	Parameters:
		tag - A tag (as a dict) within which we'll look for the attribute of interest.
		      Attribute names are the dict keys and attribute values are the dict values.
		      The tag name can be found as the value of the 'tagName' key.
	Returns:
		A string representing the value of the attribute of interest for the tag received,
		or None if either the attribute is absent or if the resource is external.
	"""
	# Here we want to retrieve the attribute that we are looking for, so we iterate through the dictionary that we
	# created in the function tag_as_dict to find it. We start of in the for loop with an if statement that basically
	# verifies that there is indeed an attribute in that tag, and if not returns None. If there is, it gathers the value
	# (as long as it doesnt contain 'http' and returns it for use in the next function.
	for key, value in tag.items():
		if DICTOFINTEREST[tag['tagName']] in key:
			val = DICTOFINTEREST[tag['tagName']]
			attribute = tag[val]
			if 'http' in attribute:
				return None
			return attribute
	return None # If no attribute is found


def write_results(dictOfResources):
	"""Write all of the resources to an output file.

	Parameters:
		dictOfResources - Dictionary of resources to be saved in the output file.
		                  The keys are the tags of interest and each value is a
		                  list of all of the resouces for that type of tag.
	"""
	outFile = open(OUTPUTFILE, 'w')
	keys = dictOfResources.keys()
	tagsList = list(keys)
	tagsList.sort()
	for t in tagsList:
		outFile.write(t + '\n')
		for attr in dictOfResources[t]:
			outFile.write('\t' + attr + '\n')
	outFile.close()

	# In this function we create the file that we are going to output and write on it.
	# First we retrieve the keys from the dictionary of Resources, make them into a list and sort them
	# We then iterate through the said list by the tags (or keys), and write each one while having a nested loop, so
	# that for each key, every attribute that represents it is also written. That will basically give one key, and
	# all its attributes below it, and then again another key, and all its attributes below it, and continue until all
	# the keys and attributes are written.


def tag_as_dict(openingTag):
	"""Convert an opening HTML tag into a dictionary.

	The attribute names will be the keys of the dictionary and the attribute values
	will be the values of those keys.  In the case of boolean attributes (the ones
	that don't have a value assigned to them), the value will be set to True. 
	The dictionary will also have the special key 'tagName' to store the tag name
	(e.g. img, audio).
	NOTE: We assume attribute values DO NOT have spaces, and that the only spaces
	in the tag are to separate attributes.

	Parameters:
		openingTag - The opening HTML tag to be converted into a dictionary.
	Returns:
		A dictionary representation of the tag, as detailed above.
	"""
	# In this function we receive a tag that contains the attributes, tagName and other information that we have to
	# store, and we convert it into a dictionary.
	# We start off by finding just the tag, which is enclosed by '<' and '>', so we find those and index the string
	# received according to their positions. Then, we make the tag into a list, by splitting it with its spaces.
	# We save that the first element in the list will be the tag name and then we define a value to help us retrieve
	# this tag name. We iterate through the list  and if there is a value to the key, we store it in the new dictionary
	# If we can't find a value to the key, we store the Boolean variable 'True' to it.
	# After we finish converting everything into the dictionary, we return it.
	startTag = openingTag.find('<')
	endTag = openingTag.find('>')
	openingTag = openingTag[startTag+1:endTag]
	openingTag_list = openingTag.split()
	tagName = openingTag_list[0]
	resourcesDict = {}
	resourcesDict['tagName'] = tagName

	for key_pos in openingTag_list:
		if '=' in key_pos:
			list_kp = key_pos.split('=')
			value = list_kp[1]
			resourcesDict[list_kp[0]] = value
			resourcesDict[list_kp[0]] = resourcesDict[list_kp[0]].replace('"', '')
		elif tagName not in key_pos:
			resourcesDict[key_pos] = True
	return resourcesDict


def main():
	lstOfLines = load_data()	
	if lstOfLines is None:
		print('ERROR: Could not open {}!'.format(INPUTFILE))
		exit()

	# This dictionary will store all the tag names as keys, and the list of tags as values.
	resourcesDict = dict()

	# We make a for loop to iterate through the lines in the file given. In this case, index.html
	# We retrieve the tag of interest from the function, and if we find one, we then turn it int the dictionary
	# and retrieve its attribute. If it has an attribute, then we store it with the values and such into the
	# 'resourcesDict' and sort it. After the loop is finished, we go to the write_results function and enter the
	# dictionary created as the argument.
	for line in lstOfLines:
		tag = get_tag_of_interest(line)
		if tag is not None:
			tag = tag_as_dict(tag)
			attrVal = get_attr_of_interest(tag)
			if attrVal is not None:
				resourcesDict[tag['tagName']] = resourcesDict.get(tag['tagName'], list())
				resourcesDict[tag['tagName']].append(attrVal)
				resourcesDict[tag['tagName']].sort()
	write_results(resourcesDict)


# This line makes python start the program from the main function
# unless our code is being imported
if __name__ == '__main__':
	main()
