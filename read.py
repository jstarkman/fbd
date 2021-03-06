def seek(data):
	contents = data
	i = 0
	findings = []
	flag = False
	tag = []
	while i < len(contents):
		if contents[i:i+1] == "[":
			tag.append(i)
			flag = True
		elif contents[i:i+1] == ":" and flag == True:
			tag.append(i)
		elif contents[i:i+1] == "]" and flag == True:
			tag.append(i)
			flag = False
			findings.append(tag)
			tag = []

		else:
			pass
		i+=1

	#print(findings)
	output_str = []
	for i in findings: #each i is a tuple
		head = 0
		parts = []
		j = 0
		while j < len(i)-1:
			temp = contents[i[head]+1:i[head+1]]
			parts.append(temp)
			j+=1
			head+=1
		#print("pieces and", parts)
		output_str.append(parts)
	#print(output_str)
	#everything, in order present, broken from tags to tuples
	
	return output_str

def interpret_opt(places, contents):
	output = {}
	# print(places)
	in_color = 0; out_color = 0; i = 0; types = []; in_PFT = 0; out_PFT = 0; F_types = []
	for term in places:
		if term[0] == "SIZE":
			output["size"] = (int(term[1]), int(term[2]))
		elif term[0] == "COLORS":
			in_color = i
			for type in term: 
				types.append(type)
		elif term[0] == "/COLORS":
			out_color = i
		elif term[0] == "POTENTIAL_FORCE_TYPES":
			output["forces"] = term[1:]
		elif term[0] == "KEYBINDINGS":
			in_PFT = i
		elif term[0] == "/KEYBINDINGS":
			out_PFT = i
		elif term[0] == "TOLERANCE":
			output["tolerance"] = int(term[1])
		elif term[0] == "TIMER":
			output["timer"] = int(term[1])
		else:
			pass
		i+=1
	output["color"] = {}
	for type in types:
		output["color"][type] = {}
		for term in places[in_color+1:out_color]:
		#for type in types:
			if term[0] == type:
				output["color"][type][term[1]] = (int(term[2]), int(term[3]), int(term[4]))
		
	output["PFT"] = {}
	#output["PFT"]["g"] = "gravitational"
	for term in places[in_PFT+1:out_PFT]:
		output["PFT"][term[0]] = term[1]

	
	# print("options output", output)
	return output

def read(filename):
	f = open(filename, "r")
	contents = f.read()
	f.close()
	
	tag_break = seek(contents)
	all_the_raws = []
	#separated for efficiency/speed in file processing
	if filename == "data.txt":
		all_the_raws = tag_break
	elif filename == "options.txt":
		all_the_raws = interpret_opt(tag_break, contents)
	return all_the_raws
	#print(all_the_raws)
	# f = open("output.txt", "w")
	# f.write(str(all_the_raws))
	# f.close()
#read("data.txt")