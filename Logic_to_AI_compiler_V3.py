#!/usr/bin/python3
from functools import reduce
#Logic_to_AI_compiler_V2.py
#Evan Nibbe
#January 6, 2022, update January 12th, 2022, update January 13th, 2022
#arg1 is the file of Logic, arg2 is the file where the binary genetic representation is stored.
#the Logic language being used has the following syntax 
#variables consist entirely of characters starting with a capital character and represent the next available hidden neuron
#lines have the format
#{{<variable>|<const output neuron>}={expression}};
#expression expands to
#direct_exp
# |
#variable operator_exp
# |
#<const input neuron> operator_exp
# |
#p<variable> <operator_exp>
# |
#p<const input neuron> <operator_exp>
# |
#-<variable> <operator_exp>
# |
#-<const input neuron> <operator_exp>
# |
#-p<variable> <operator_exp>
# |
#-p<const input neuron> <operator_exp>
#direct_exp expands to
#<variable>*<-4/<=float/<=4>
# |
#<const input neuron>*<-4/<=float/<=4>
# |
#<variable>*<-4/<=float/<=4> + <direct_exp>
# |
#<const input neuron>*<-4/<=float/<=4> + <direct_exp>

#operator_exp expands to
# |
# + <variable> 
# |
# + <const input neuron> 
# |
# * <variable> 
# |
# * <const input neuron>
# |
# - <variable> # interpret as “OR NOT”
# |
# - <const input neuron> # interpret as “OR NOT”
# |
# / <variable> #interpret as “AND NOT”
# |
# / <const input neuron> #interpret as “AND NOT”
# |
# wait <integer>
# |
# + p<variable | const input>
# |
# - p<variable | const input >
# |
# * p<variable | const input>
# |
# / p<variable | const input>


#wait is an operator that means to create a line of hidden neurons integer long where the LHS of the expression is the last neuron and there is a weight of 1 between the first and last neurons.
#p is a unary operator to create a new hidden neuron with its source at that hidden or input neuron and a weight of 1 

def is_num(arg):
	try:
		int(arg)
	except:
		return False
	return True

def is_float(arg):
	try:
		float(arg)
	except:
		return False
	return True
def in_dict(d, k):
	try:
		i=d[k]
	except:
		return False
	return True
def int_to_bin(arg, n): #n is number of binary digits
	arg=int(arg)
	str1=bin(arg)
	str1=str1[2:]
	la=len(str1)
	for i in range(n-la):
		str1="0"+str1
	if n-la<0:
		str1=str1[la-n:]
	return str1

def flat_map(f, xs):
	if type(xs)!=list:
		return f(xs)
	ys=[]
	for x in xs:
		try:
			if list==type(x):
				x=flat_map(f, x)
				ys.extend(x)
			else:
				ys.append(f(x))
		except:
			if list==type(x):
				ys.extend(x)
			else:
				ys.append(f(x))
	return ys

import sys

#A must be the first thing anded, B the second thing anded, interim is the intermediate result, res is the result, 
#sym is the dictionary of symbols, fp is the file pointer that is written to
def neuron_and(A, B, interim, res, sym):
	code=""
	if is_num(A):
		if int(A) > 2**15-1:
			print("value "+str(A)+" is too big.")
			sys.exit()
		code+="000"+int_to_bin(A, 15)
	else:
		code+="111"+int_to_bin(sym[A], 15)
	code+="000"+int_to_bin(sym[interim], 14)+"0"+"00"+"10000010100011110101110001"
	if is_num(B):
		if int(B) > 2**15-1:
			print("value "+str(B)+" is too big.")
			sys.exit()
		code+="000"+int_to_bin(B, 15)
	else:
		code+="111"+int_to_bin(sym[B], 15)
	code+="000"+int_to_bin(sym[interim], 14)+"0"+"00"+"10000010100011110101110001"
	#now the -.3825
	code+="000"+"000000000111111"+"000"+int_to_bin(sym[interim], 14)+"1"+"00"+"01100001111010111000010101"
	#now for going to result
	code+="111"+int_to_bin(sym[interim], 15)
	if is_num(res): #then output neuron
		if int(res)> 2**14-1:
			print("result value "+str(res)+" is too big.")
			sys.exit()
		code+="111"+int_to_bin(res,14)
	else: #res is variable
		code+="000"+int_to_bin(sym[res],14)
	code+="0"+"11"+"11111111111111111111111111"
	return code

def neuron_or(A, B, iA, iB, interim, res, sym):
	code=""
	if is_num(A):
		if int(A) > 2**15-1:
			print("value "+str(A)+" is too big.")
			sys.exit()
		code+="000"+int_to_bin(A, 15)
	else:
		code+="111"+int_to_bin(sym[A], 15)
	code+="000"+int_to_bin(sym[iA], 14)+"0"+"10"+"00000000000000000000000001"
	if is_num(B):
		if int(B) > 2**15-1:
			print("value "+str(B)+" is too big.")
			sys.exit()
		code+="000"+int_to_bin(B, 15)
	else:
		code+="111"+int_to_bin(sym[B], 15)
	code+="000"+int_to_bin(sym[iB], 14)+"0"+"10"+"00000000000000000000000001"
	#now move iA and iB to interim
	code+="111"+int_to_bin(sym[iA], 15)+"000"+int_to_bin(sym[interim], 14)+"0"+"01"+"00000000000000000000000001"
	code+="111"+int_to_bin(sym[iB], 15)+"000"+int_to_bin(sym[interim], 14)+"0"+"01"+"00000000000000000000000001"
	
	#now the +.5
	code+="000"+"000000000111111"+"000"+int_to_bin(sym[interim], 14)+"0"+"00"+"10000000000000000000000001"
	#now for going to result
	code+="111"+int_to_bin(sym[interim], 15)
	if is_num(res): #then output neuron
		if int(res)> 2**14-1:
			print("result value "+str(res)+" is too big.")
			sys.exit()
		code+="111"+int_to_bin(res,14)
	else: #res is variable
		code+="000"+int_to_bin(sym[res],14)
	code+="0"+"11"+"11111111111111111111111111"
	return code
	

def neuron_not(arg, res, sym):
	code=""
	if is_num(arg):
		code+="000"+int_to_bin(arg, 15)
	else:
		code+="111"+int_to_bin(sym[arg], 15)
	if is_num(res):
		code+="111"+int_to_bin(res,14)+"1"+"01"+"00000000000000000000000001"
	else:
		code+="000"+int_to_bin(sym[res],14)+"1"+"01"+"00000000000000000000000001"
		#return None #int_to_bin(sym["-"+arg], 15)
	return code


filename=sys.argv[1]
foutput=sys.argv[2]
fp=open(filename, "r")
text_data=fp.read()
fp.close()
fp=open(foutput, "w")
repeat=False
sym={}
lineno=1 #line number
see_newline=True #True when newline is seen, becomes false when the first capital letter or number is seen
buffer="" #reset on start of new symbol
p=False #True when p is seen and buffer is empty, false after end of next word
op=0 #set to whatever the operation (besides p) that is found, such as (1) +, (2) -, (3) *, (4) /, (5) w, (6) simple op
LHS="" #reset on newline
RHS="" #reset on newline
eq=False #reset on newline, True when = seen, then everything gets put into RHS instead of LHS
next_h_n=0 #counted upward whenever a hidden neuron is used.
#The following changes are designed to get rid of original occurrances of :, \t, ?, |, and then turn 
#the keywords wait, norepeat, repeat into the individual key letters w, n, r, having removed the occurances 
#of those individual letters otherwise (by turning them into :, ?, |, respectively)
#the program user does not see any of these replacements, as long as wait and repeat do not exist as substrings
#of variable names.
#This string processing step makes it substantially easier to write the compiler as it means the buffers only need to worry about
#variable names and constants, with everything else being established by single characters.
#python encodings table below
#[(0, '\x00'), (1, '\x01'), (2, '\x02'), (3, '\x03'), (4, '\x04'), (5, '\x05'), (6, '\x06'), (7, '\x07'), (8, '\x08'), (9, '\t'), (10, '\n'), 
#(11, '\x0b'), (12, '\x0c'), (13, '\r'), (14, '\x0e'), (15, '\x0f'), (16, '\x10'), (17, '\x11'), (18, '\x12'), (19, '\x13'), (20, '\x14'), (21, '\x15'), (22, '\x16'), (23, '\x17'), (24, '\x18'), (25, '\x19'), (26, '\x1a'), (27, '\x1b'), (28, '\x1c'), (29, '\x1d'), (30, '\x1e'), (31, '\x1f'), 
#(32, ' '), (33, '!'), (34, '"'), (35, '#'), (36, '$'), (37, '%'), (38, '&'), (39, "'"), (40, '('), (41, ')'), 
#(42, '*'), (43, '+'), (44, ','), (45, '-'), (46, '.'), (47, '/'), 
#(48, '0'), (49, '1'), (50, '2'), (51, '3'), (52, '4'), (53, '5'), (54, '6'), (55, '7'), (56, '8'), (57, '9'), (58, ':'), (59, ';'), (60, '<'), (61, '='), (62, '>'), (63, '?'), (64, '@'), 
#(65, 'A'), (66, 'B'), (67, 'C'), (68, 'D'), (69, 'E'), (70, 'F'), (71, 'G'), (72, 'H'), (73, 'I'), (74, 'J'), (75, 'K'), (76, 'L'), (77, 'M'), (78, 'N'), (79, 'O'), (80, 'P'), (81, 'Q'), (82, 'R'), (83, 'S'), (84, 'T'), (85, 'U'), (86, 'V'), (87, 'W'), (88, 'X'), (89, 'Y'), (90, 'Z'), 
#(91, '['), (92, '\\'), (93, ']'), (94, '^'), (95, '_'), (96, '`'), 
#(97, 'a'), (98, 'b'), (99, 'c'), (100, 'd'), (101, 'e'), (102, 'f'), (103, 'g'), (104, 'h'), (105, 'i'), (106, 'j'), (107, 'k'), (108, 'l'), (109, 'm'), (110, 'n'), (111, 'o'), (112, 'p'), (113, 'q'), (114, 'r'), (115, 's'), (116, 't'), (117, 'u'), (118, 'v'), (119, 'w'), (120, 'x'), (121, 'y'), (122, 'z'), 
#(123, '{'), (124, '|'), (125, '}'), (126, '~'), (127, '\x7f'), (128, '\x80'), (129, '\x81'), (130, '\x82'), (131, '\x83'), (132, '\x84'), (133, '\x85'), (134, '\x86'), (135, '\x87'), (136, '\x88'), (137, '\x89'), (138, '\x8a'), (139, '\x8b'), (140, '\x8c'), (141, '\x8d'), (142, '\x8e'), (143, '\x8f'), (144, '\x90'), (145, '\x91'), (146, '\x92'), (147, '\x93'), (148, '\x94'), (149, '\x95'), (150, '\x96'), (151, '\x97'), (152, '\x98'), (153, '\x99'), (154, '\x9a'), (155, '\x9b'), (156, '\x9c'), (157, '\x9d'), (158, '\x9e'), (159, '\x9f'), (160, '\xa0'), 
#(161, '¡'), (162, '¢'), (163, '£'), (164, '¤'), (165, '¥'), (166, '¦'), (167, '§'), (168, '¨'), (169, '©'), (170, 'ª'), (171, '«'), (172, '¬'), (173, '\xad'), (174, '®'), (175, '¯'), (176, '°'), (177, '±'), (178, '²'), (179, '³'), (180, '´'), 
#(181, 'µ'), (182, '¶'), (183, '·'), (184, '¸'), (185, '¹'), (186, 'º'), (187, '»'), (188, '¼'), (189, '½'), (190, '¾'), (191, '¿'), (192, 'À'), (193, 'Á'), (194, 'Â'), (195, 'Ã'), (196, 'Ä'), (197, 'Å'), (198, 'Æ'), (199, 'Ç'), (200, 'È'), (201, 'É'), (202, 'Ê'), (203, 'Ë'), (204, 'Ì'), (205, 'Í'), (206, 'Î'), (207, 'Ï'), (208, 'Ð'), (209, 'Ñ'), (210, 'Ò'), (211, 'Ó'), (212, 'Ô'), (213, 'Õ'), (214, 'Ö'), 
#(215, '×'), (216, 'Ø'), (217, 'Ù'), (218, 'Ú'), (219, 'Û'), (220, 'Ü'), (221, 'Ý'), (222, 'Þ'), (223, 'ß'), (224, 'à'), (225, 'á'), (226, 'â'), (227, 'ã'), (228, 'ä'), (229, 'å'), (230, 'æ'), (231, 'ç'), 
#(232, 'è'), (233, 'é'), (234, 'ê'), (235, 'ë'), (236, 'ì'), (237, 'í'), (238, 'î'), (239, 'ï'), (240, 'ð'), (241, 'ñ'), (242, 'ò'), (243, 'ó'), (244, 'ô'), (245, 'õ'), (246, 'ö'), 
#(247, '÷'), (248, 'ø'), (249, 'ù'), (250, 'ú'), (251, 'û'), (252, 'ü'), (253, 'ý'), (254, 'þ'), (255, 'ÿ')]
text_data=text_data.replace(":", " ").replace("w", ":").replace(" :ait ", " w ")
text_data=text_data.replace("\t", " ").replace("?", " ").replace("|", " ").replace("    ", " ").replace("   ", " ").replace("  ", " ").replace("- ", "-").replace("- ", "-")
simple_text=""
for c in text_data: #this gets rid of all the problematic types of characters
	if ord(c)<10:
		pass
	elif ord(c)>10 and ord(c)<32:
		pass
	elif ord(c)==34:
		pass
	elif ord(c)>35 and ord(c)<42:
		pass
	elif ord(c)>90 and ord(c)<97:
		pass
	elif ord(c)>122 and ord(c)<163:
		pass
	else:
		simple_text+=str(c)


lines=simple_text.split("\n")
statements=[] #will be used more when repeat and norepeat rules are considered separately
for line in lines:
	statements.append(line.split("#")[0]) #hashtags are treated as comments in the language
#for i in range(len(lines)):
#	line=lines[i]
#	if line.find("r")>-1:
#		repeat=True
#	elif line.find("n")>=-1:
#		repeat=False
#	elif repeat:
#		statements.append("r "+line)
#	else:
#		statements.append("n "+line)

lines=list(filter(lambda x: x.find('=')>0, statements))
#print("The lines are: \n", lines, "\n^^^^^^^^^^^^^^^^^^")
def find_sym(line):
	line=line.replace("/", "* -")
	res=flat_map(lambda x: x, flat_map(lambda x: x.split("="), line))
	res=flat_map(lambda x: x, flat_map(lambda x: x.split("+"), res))
	res=flat_map(lambda x: x, flat_map(lambda x: x.split("*"), res))
	res=flat_map(lambda x: x, flat_map(lambda x: x.split("w"), res))
	res=flat_map(lambda x: x, flat_map(lambda x: x.replace("- ", "-").replace("-", " -").replace("  ", " ").strip().split(" "), res))
	res=list(filter(lambda x: len(x)>0 and type(x)==str and x.find(".")==-1, res))
	
	#	res=list(filter(lambda x: True if len(x)>0 and type(x)==str and x.find(".")==-1 else True if len(x[0])>0 and type(x[0])==str and x[0].find(".")==-1 else False, 
	#flat_map(lambda x: x.replace("- ", "-").replace("-", " -").replace("  ", " ").strip().split(" "), \
	#flat_map(lambda x: x.split("w"), \
	#flat_map(lambda x: x.split("*"), \
	#flat_map(lambda x: x.split("+"), \
	#flat_map(lambda x: x.split("="), line)))))))
	res=flat_map(lambda x: x.strip(), res)
	#print("find_sym initial res is: \n", res, "\n^^^^^^^^^^^^")
	for s in res:
		if s.find("-")==0 and s.find("p")==1 and len(s)>2:
			res.append(s[1:])
			res.append(s[2:])
		elif s.find("-")==0 and len(s)>1:
			res.append(s[1:])
		elif s.find("p")==0 and len(s)>1:
			res.append(s[1:])
	#print("find_sym final res is: \n", res, "\n^^^^^^^^^^^^")
	return res
symbols=flat_map(lambda x: x, list(flat_map(find_sym, lines)))
#print("initial symbols (before removing duplicates) are: \n", symbols, "\n^^^^^^^^^^^^^^^^^")
symbols=list(set(symbols)) #remove duplicates
#print("The symbols are: \n", symbols, "\n^^^^^^^^^^^^^^^^^^^\n")
for i in symbols:
	if not is_num(i):
		sym[i]=next_h_n
		next_h_n+=1
print("The symbol table is:\n", sym, "\n^^^^^^^^^^^^^^^^^^^\n")
#now every possible symbol has an assignment, note that I have established repeats as the standard, norepeat is not an available function yet
def encode(line):
	global sym, next_h_n
	#check for direct_exp
	line=line.replace("/", "* -")
	#consider for direct expression removing the filter x.find(".")==-1
	#terms=list(filter(lambda x: len(x)>0 and x.find(".")==-1, flat_map(lambda x: x.replace("- ", "-").replace("-", " -").replace("  ", " ").strip().split(" "), flat_map(lambda x: x.split("w"), flat_map(lambda x: x.split("*"), flat_map(lambda x: x.split("+"), flat_map(lambda x: x.split("="), line)))))))
	res=flat_map(lambda x: x, flat_map(lambda x: x.split("="), line))
	res=flat_map(lambda x: x, flat_map(lambda x: x.split("+"), res))
	res=flat_map(lambda x: x, flat_map(lambda x: x.split("*"), res))
	res=flat_map(lambda x: x, flat_map(lambda x: x.split("w"), res))
	res=flat_map(lambda x: x, flat_map(lambda x: x.replace("- ", "-").replace("-", " -").replace("  ", " ").strip().split(" "), res))
	res=list(filter(lambda x: len(x)>0 and type(x)==str and x.find(".")==-1, res))
	terms=res
	code="" #this is the genetic code to export
	res=terms[0]
	#print("result is ", res)
	#first we establish the p-results, then we establish the negative results
	for s in terms:
		if s.find("-")==0 and s.find("p")==1 and len(s)>2:
			if is_num(s[2:]):
				code+="000"+int_to_bin(s[2:], 15)+"000"+int_to_bin(sym[s[1:]], 14)+"0"+"01"+"00000000000000000000000001"
				code+="111"+int_to_bin(s[1:], 15)+"000"+int_to_bin(sym[s], 14)+"1"+"01"+"00000000000000000000000001"
			else:
				code+="111"+int_to_bin(sym[s[2:]], 15)+"000"+int_to_bin(sym[s[1:]], 14)+"0"+"01"+"00000000000000000000000001"
				code+="111"+int_to_bin(sym[s[1:]], 15)+"000"+int_to_bin(sym[s], 14)+"1"+"01"+"00000000000000000000000001"
		elif s.find("-")==0 and len(s)>1:
			if is_num(s[1:]):
				code+="000"+int_to_bin(s[1:], 15)+"000"+int_to_bin(sym[s], 14)+"1"+"01"+"00000000000000000000000001"
			else:
				code+="111"+int_to_bin(sym[s[1:]], 15)+"000"+int_to_bin(sym[s], 14)+"1"+"01"+"00000000000000000000000001"
			#res.append(s[1:])
		elif s.find("p")==0 and len(s)>1:
			if is_num(s[1:]):
				code+="000"+int_to_bin(s[1:], 15)+"000"+int_to_bin(sym[s], 14)+"0"+"01"+"00000000000000000000000001"
			else:
				code+="111"+int_to_bin(sym[s[1:]], 15)+"000"+int_to_bin(sym[s], 14)+"0"+"01"+"00000000000000000000000001"
			#res.append(s[1:])
	if line.find(".")>0: #direct expression
		#terms=list(filter(lambda x: len(x)>0, flat_map(lambda x: x.replace("- ", "-").replace("-", " -").replace("  ", " ").strip().split(" "), flat_map(lambda x: x.split("w"), flat_map(lambda x: x.split("*"), flat_map(lambda x: x.split("+"), flat_map(lambda x: x.split("="), line)))))))
		res=flat_map(lambda x: x, flat_map(lambda x: x.split("="), line))
		res=flat_map(lambda x: x, flat_map(lambda x: x.split("+"), res))
		res=flat_map(lambda x: x, flat_map(lambda x: x.split("*"), res))
		res=flat_map(lambda x: x, flat_map(lambda x: x.split("w"), res))
		res=flat_map(lambda x: x, flat_map(lambda x: x.replace("- ", "-").replace("-", " -").replace("  ", " ").strip().split(" "), res))
		res=list(filter(lambda x: len(x)>0, res))
		terms=res
		res=terms[0]
		#now we have the floating point terms included in the expression
		for i in range(1, len(terms)-1, 2): #increment by 2 because the variable is paired with a float
			if is_float(terms[i+1]):
				if is_num(terms[i]):
					code+="000"+int_to_bin(terms[i], 15)
				else: #terms[i] is a variable in sym
					code+="111"+int_to_bin(sym[terms[i]], 15)
				if is_num(res):
					code+="111"+int_to_bin(res, 14)
				else: #res is a variable in sym
					code+="000"+int_to_bin(sym[res], 14)
				num=float(terms[i+1])
				neg="0"
				if num<0:
					neg="1"
					num=-num
				code+=neg+int_to_bin(int(num*67108864/2), 27)+"1"
			else:
				print("Error on line "+line+" item "+terms[i+1]+" is not a float")
	else:
		eq=0
		#logic code
		if len(terms)==3:
			if line.find("*")>0: #AND
				A=terms[1]
				B=terms[2]
				interim=""
				if A<B:
					interim=A+"*"+B
				else:
					interim=B+"*"+A
				if not in_dict(sym, interim):
					sym[interim]=next_h_n
					next_h_n+=1
				code+=neuron_and(A, B, interim, res, sym)
			elif line.find("+")>0 or terms[2][0]=='-': #OR
				A=terms[1]
				B=terms[2]
				iA=A+"i"
				iB=B+"i"
				interim=""
				if A<B:
					interim=A+"+"+B
				else:
					interim=B+"+"+A
				if not in_dict(sym, interim):
					sym[interim]=next_h_n
					next_h_n+=1
				if not in_dict(sym, iA):
					sym[iA]=next_h_n
					next_h_n+=1
				if not in_dict(sym, iB):
					sym[iB]=next_h_n
					next_h_n+=1
				code+=neuron_or(A, B, iA, iB, interim, res, sym)
			elif line.find("w")>0 and is_num(terms[2]): #wait
				for i in range(int(terms[2])-1):
					if not in_dict(sym, "p"+terms[1]):
						sym["p"+terms[1]]=next_h_n
						next_h_n+=1
						code+="111"+int_to_bin(sym[terms[1]], 15)+"000"+int_to_bin(sym["p"+terms[1]], 14)+"0"+"01"+"00000000000000000000000001"
					terms[1]="p"+terms[1]
				if is_num(res):
					code+="111"+int_to_bin(sym[terms[1]], 15)+"111"+int_to_bin(res, 14)+"0"+"01"+"00000000000000000000000001"
				else:
					code+="111"+int_to_bin(sym[terms[1]], 15)+"000"+int_to_bin(sym[res], 14)+"0"+"01"+"00000000000000000000000001"
			else:
				print("Line "+line+" does not have a supported operation")
		else: #just set res equal to term1
			if is_num(terms[1]):
				code+="000"+int_to_bin(terms[1], 15)
			else: #terms[1] is variable
				code+="111"+int_to_bin(sym[terms[1]], 15)
			if is_num(res):
				code+="111"+int_to_bin(res, 14)
			else: #res is variable
				code+="000"+int_to_bin(sym[res], 14)
			code+="0"+"01"+"00000000000000000000000001"
	return code

#previous writing for encode
#	eq=line.find("=")
#	if line.find(" ")<eq and line.find(" ")>0:
#		eq=line.find(" ")
#	res=line[0:eq]
#	#try:
#	if line.find(".")>=0:
#		i=eq+1
#		non=False
#		term=""
#		num=0
#		while i<len(line):
#			if not non and ((line[i]<='9' and line[i]>='0') or (line[i]>='A' and line[i]<='Z') or (line[i]>='a' and line[i]<='z') or line[i]==':' or line[i]=='?' or line[i]=='|'):
#				term+=line[i]
#			elif line[i]=='+':
#				
#				non=False
#			elif line[i]=='*':
#				non=True
#			elif ((line[i]<='9' and line[i]>='0') or (line[i]>='A' and line[i]<='Z') or (line[i]>='a' and line[i]<='z') or line[i]==':' or line[i]=='?' or line[i]=='|'):
#				if line[i]<='9' and line[i]>='0':
#					if line[i-1]=='.' or (line[i-1]<='9' and line[i-1]>='0'):
#						pass
#					else: #first digit
#						neg="0"
#						if line[i-1]=='-' or line[i-2]=='-':
#							neg="1"
#						num=0
#						k=i+1
#						while k<len(line) and (line[k]=='.' or (line[k]>='0' and line[k]<='9')):
#							k+=1
#						num=float(line[i:k])
#						if is_num(term) and is_num(res):
#							code+="000"+int_to_bin(int(term), 15)+"111"+int_to_bin(int(res), 14)+neg+int_to_bin(int(67108864/2 *num), 27)+"1" #"0001100001111010111000010101"
#						elif is_num(term):
#							code+="000"+int_to_bin(int(term), 15)+"000"+int_to_bin(sym[res], 14)+neg+int_to_bin(int(67108864/2 *num), 27)+"1" #"0001100001111010111000010101"
#						elif is_num(res):
#							code+="111"+int_to_bin(sym[term], 15)+"111"+int_to_bin(int(res), 14)+neg+int_to_bin(int(67108864/2 *num), 27)+"1" #"0001100001111010111000010101"
#						else:
#							code+="111"+int_to_bin(sym[term], 15)+"000"+int_to_bin(sym[res], 14)+neg+int_to_bin(int(67108864/2 *num), 27)+"1" #"0001100001111010111000010101"
#			i+=1
#		return code
#	else: #not a direct_exp
#		#first we evaluate the "p"s, then the "-"s, then "/" -> " * -" with the minus evaluated first
#		#the sym[parg] = sym["p "+arg]
#		#the sym[-arg] = sym["not "+arg] evaluated using neuron not before establishing that negative
#		#then evaluate the different operations like + (or), * (and), w (wait)
#		
#		s_l=line[eq+1:].replace("/", "* -")+" "
#		term1=""
#		term2=""
#		p1=s_l.find("p")
#		if p1==0 or p1>0: 
#			ss_l=s_l[p1:]
#			if ((s_l[p1-1]>'Z' or s_l[p1-1]<'A') and (s_l[p1-1]>'z' or s_l[p1-1]<'a') and s_l[p1-1]!=':' and s_l[p1-1]!='|' and s_l[p1-1]!='?'):
#				pterm=ss_l[:reduce(lambda x, y: x if x>0 and x<y else y, [ss_l.find(" "), ss_l.find("+"), ss_l.find("*"), ss_l.find("-"), ss_l.find("w")])]
#				if (s_l[p1-1]!='-' and s_l[p1-2]!='-' and in_dict(sym, "p"+pterm)) or ((s_l[p1-1]=='-' or s_l[p1-2]=='-') and in_dict(sym, "-p"+pterm)):
#					pass
#				else:
#					if s_l[p1-1]!='-' and s_l[p1-2]!='-':
#						if max(ss_l.find("+"), ss_l.find("*"), ss_l.find("-"), ss_l.find("w"))<=1:
#							term2="p"+pterm
#						else:
#							term1="p"+pterm
#						print("line 405, pterm=", pterm)
#						sym["p"+pterm]=sym["p "+pterm]
#						if is_num(pterm):
#							code+="000"+int_to_bin(int(pterm), 15)+"000"+int_to_bin(sym["p"+pterm], 14)+"0"+"01"+"00000000000000000000000001" #+int_to_bin(int(67108864 *num), 28) #"0001100001111010111000010101"
#						else:
#							code+="111"+int_to_bin(sym[pterm], 15)+"000"+int_to_bin(sym["p"+pterm], 14)+"0"+"01"+"00000000000000000000000001" #"0001100001111010111000010101"
#					else:
#						if max(ss_l.find("+"), ss_l.find("*"), ss_l.find("-"), ss_l.find("w"))<=1:
#							term2="-p"+pterm
#						else:
#							term1="-p"+pterm
#						sym["-p"+pterm]=sym["not p "+pterm]
#						if is_num(pterm):
#							code+="000"+int_to_bin(int(pterm), 15)+"000"+int_to_bin(sym["-p"+pterm], 14)+"1"+"01"+"00000000000000000000000001" #+int_to_bin(int(67108864 *num), 28) #"0001100001111010111000010101"
#						else:
#							code+="111"+int_to_bin(sym[pterm], 15)+"000"+int_to_bin(sym["-p"+pterm], 14)+"1"+"01"+"00000000000000000000000001" #"0001100001111010111000010101"
#			p2=ss_l[1:].find("p")+1
#			if p2>2 and s_l.find("w")==-1: #the wait operation does not support two pterms
#				sss_l=ss_l[p2:]
#				if (ss_l.find("*") > 1 or ss_l.find("+")>1 or ss_l.find("-")>1) and sss_l.find("*")==-1 and sss_l.find("+")==-1 and sss_l.find("-")==-1:
#					pterm=sss_l[:sss_l.find(" ")]
#					if (ss_l[p2-1]!='-' and ss_l[p2-2]!='-' and in_dict(sym, "p"+pterm)) or ((ss_l[p2-1]=='-' or ss_l[p2-2]=='-') and in_dict(sym, "-p"+pterm)):
#						pass
#					else:
#						if ss_l[p2-1]!='-' and ss_l[p2-2]!='-':
#							term2="p"+pterm
#							sym["p"+pterm]=sym["p "+pterm]
#							if is_num(pterm):
#								code+="000"+int_to_bin(int(pterm), 15)+"000"+int_to_bin(sym["p"+pterm], 14)+"0"+"01"+"00000000000000000000000001" #+int_to_bin(int(67108864 *num), 28) #"0001100001111010111000010101"
#							else:
#								code+="111"+int_to_bin(sym[pterm], 15)+"000"+int_to_bin(sym["p"+pterm], 14)+"0"+"01"+"00000000000000000000000001" #"0001100001111010111000010101"
#						else:
#							term2="-p"+pterm
#							sym["-p"+pterm]=sym["not p "+pterm]
#							if is_num(pterm):
#								code+="000"+int_to_bin(int(pterm), 15)+"000"+int_to_bin(sym["-p"+pterm], 14)+"1"+"01"+"00000000000000000000000001" #+int_to_bin(int(67108864 *num), 28) #"0001100001111010111000010101"
#							else:
#								code+="111"+int_to_bin(sym[pterm], 15)+"000"+int_to_bin(sym["-p"+pterm], 14)+"1"+"01"+"00000000000000000000000001" #"0001100001111010111000010101"
#		if len(term1)==0 and len(term2)==0: #p was not used
#			#check for wait operation
#			#check for only one term
#			i=0
#			while (s_l[i]>'Z' or s_l[i]<'A') and (s_l[i]>'9' or s_l[i]<'0'):
#				i+=1
#			k=i+1
#			while (s_l[k]<='Z' and s_l[k]>='A') or (s_l[k]<='9' and s_l[k]>='0') or (s_l[k]<='z' and s_l[k]>='a') or s_l[k]==':' or s_l[k]=='?' or s_l[k]=='|':
#				k+=1
#			term1=s_l[i:k]
#			if (i>0 and s_l[i-1]=='-') or (i>1 and s_l[i-2]=='-'):
#				code+=neuron_not(term1, "not "+term1)
#				term1="-"+term1
#			i=max(s_l.find("+"), s_l.find("*"), s_l.find("w"))
#			if i==-1: #this means either only one term or term1 - term2
#				if s_l[s_l.find(term1[1:]):].find("-")>0: #then term1 - term2
#					op="neg"
#					i=s_l[s_l.find(term1[1:]):].find("-")
#				else:
#					#only one term
#					if is_num(res):
#						code+="111"+int_to_bin(sym[term1], 15)+"111"+int_to_bin(res, 14)+"0"+"01"+"00000000000000000000000001"
#					else:
#						code+="111"+int_to_bin(sym[term1], 15)+"000"+int_to_bin(sym[res], 14)+"0"+"01"+"00000000000000000000000001"
#			if i>0:
#				while (s_l[i]>'Z' or s_l[i]<'A') and (s_l[i]>'9' or s_l[i]<'0'):
#					i+=1
#				k=i+1
#				while (s_l[k]<='Z' and s_l[k]>='A') or (s_l[k]<='9' and s_l[k]>='0') or (s_l[k]<='z' and s_l[k]>='a') or s_l[k]==':' or s_l[k]=='?' or s_l[k]=='|':
#					k+=1
#				term2=s_l[i:k]
#				if (i>0 and s_l[i-1]=='-') or (i>1 and s_l[i-2]=='-'):
#					code+=neuron_not(term2, "not "+term2)
#					term2="-"+term2
#				if s_l.find("*")>0:
#					A=term1
#					B=term2
#					interim=""
#					if A<B:
#						interim=A+"*"+B
#					else:
#						interim=B+"*"+A
#					if not in_dict(sym, interim):
#						sym[interim]=next_h_n
#						next_h_n+=1
#					code+=neuron_and(A, B, interim, res, sym) 
#				elif s_l.find("+")>0 or op=="neg":
#					A=term1
#					B=term2
#					iA=A+"i"
#					iB=B+"i"
#					interim=""
#					if A<B:
#						interim=A+"+"+B
#					else:
#						interim=B+"+"+A
#					if not in_dict(sym, interim):
#						sym[interim]=next_h_n
#						next_h_n+=1
#					if not in_dict(sym, iA):
#						sym[iA]=next_h_n
#						next_h_n+=1
#					if not in_dict(sym, iB):
#						sym[iB]=next_h_n
#						next_h_n+=1
#					code+=neuron_or(A, B, iA, iB, interim, res, sym)
#				elif s_l.find("w")>0: #wait operation
#					if is_num(term2):
#						i=0
#						for i in range(int(term2)-1):
#							if not in_dict(sym, "p"+term1):
#								sym["p"+term1]=next_h_n
#								next_h_n+=1
#								code+="111"+int_to_bin(sym[term1], 15)+"000"+int_to_bin(sym["p"+term1], 14)+"0"+"01"+"00000000000000000000000001"
#							term1="p"+term1
#						if is_num(res):
#							code+="111"+int_to_bin(sym[term1], 15)+"111"+int_to_bin(res, 14)+"0"+"01"+"00000000000000000000000001"
#						else:
#							code+="111"+int_to_bin(sym[term1], 15)+"000"+int_to_bin(sym[res], 14)+"0"+"01"+"00000000000000000000000001"
#					else:
#						print("Number not given for wait on line "+line+" !")
#						sys.exit()
#				else: 
#					print("Error line "+line+" operation invalid")
#					sys.exit()
#		elif len(term1)==0: #term2 starts with p
#			#wait op is impossible
#			i=0
#			while (s_l[i]>'Z' or s_l[i]<'A') and (s_l[i]>'9' or s_l[i]<'0'):
#				i+=1
#			k=i+1
#			while (s_l[k]<='Z' and s_l[k]>='A') or (s_l[k]<='9' and s_l[k]>='0') or (s_l[k]<='z' and s_l[k]>='a') or s_l[k]==':' or s_l[k]=='?' or s_l[k]=='|':
#				k+=1
#			term1=s_l[i:k]
#			if (i>0 and s_l[i-1]=='-') or (i>1 and s_l[i-2]=='-'):
##				code+=neuron_not(term1, "not "+term1)
#				term1="-"+term1
#			if s_l.find("*")>0:
#				A=term1
#				B=term2
#				interim=""
#				if A<B:
#					interim=A+"*"+B
#				else:
#					interim=B+"*"+A
#				if not in_dict(sym, interim):
#					sym[interim]=next_h_n
#					next_h_n+=1
#				code+=neuron_and(A, B, interim, res, sym) 
#			elif s_l.find("+")>0:
#				A=term1
#				B=term2
#				iA=A+"i"
#				iB=B+"i"
#				interim=""
#				if A<B:
#					interim=A+"+"+B
#				else:
#					interim=B+"+"+A
#				if not in_dict(sym, interim):
#					sym[interim]=next_h_n
#					next_h_n+=1
#				if not in_dict(sym, iA):
#					sym[iA]=next_h_n
#					next_h_n+=1
#				if not in_dict(sym, iB):
#					sym[iB]=next_h_n
#					next_h_n+=1
#				code+=neuron_or(A, B, iA, iB, interim, res, sym)
#			else: 
#				print("Error line "+line+" operation invalid")
#				sys.exit()
#		elif len(term2)==0: #term1 starts with p
#			#check for wait operation
#			#check for only one term
#			i=max(s_l.find("+"), s_l.find("*"), s_l.find("w"))
#			if i==-1: #this means either only one term or term1 - term2
#				if s_l[s_l.find(term1[1:]):].find("-")>0: #then term1 - term2
#					op="neg"
#					i=s_l[s_l.find(term1[1:]):].find("-")
#				else:
#					#only one term
#					if is_num(res):
#						code+="111"+int_to_bin(sym[term1], 15)+"111"+int_to_bin(res, 14)+"0"+"01"+"00000000000000000000000001"
#					else:
#						code+="111"+int_to_bin(sym[term1], 15)+"000"+int_to_bin(sym[res], 14)+"0"+"01"+"00000000000000000000000001"
#			if i>0:
#				while (s_l[i]>'Z' or s_l[i]<'A') and (s_l[i]>'9' or s_l[i]<'0'):
#					i+=1
#				k=i+1
#				while (s_l[k]<='Z' and s_l[k]>='A') or (s_l[k]<='9' and s_l[k]>='0') or (s_l[k]<='z' and s_l[k]>='a') or s_l[k]==':' or s_l[k]=='?' or s_l[k]=='|':
#					k+=1
#				term2=s_l[i:k]
#				if (i>0 and s_l[i-1]=='-') or (i>1 and s_l[i-2]=='-'):
#					code+=neuron_not(term2, "not "+term2)
#					term2="-"+term2
#				if s_l.find("*")>0:
#					A=term1
#					B=term2
#					interim=""
#					if A<B:
#						interim=A+"*"+B
#					else:
#						interim=B+"*"+A
#					if not in_dict(sym, interim):
#						sym[interim]=next_h_n
#						next_h_n+=1
#					code+=neuron_and(A, B, interim, res, sym) 
#				elif s_l.find("+")>0 or op=="neg":
#					A=term1
#					B=term2
#					iA=A+"i"
#					iB=B+"i"
#					interim=""
#					if A<B:
#						interim=A+"+"+B
#					else:
#						interim=B+"+"+A
#					if not in_dict(sym, interim):
#						sym[interim]=next_h_n
#						next_h_n+=1
#					if not in_dict(sym, iA):
#						sym[iA]=next_h_n
#						next_h_n+=1
#					if not in_dict(sym, iB):
#						sym[iB]=next_h_n
#						next_h_n+=1
#					code+=neuron_or(A, B, iA, iB, interim, res, sym)
#				elif s_l.find("w")>0: #wait operation
#					if is_num(term2):
#						i=0
#						for i in range(int(term2)-1):
#							if not in_dict(sym, "p"+term1):
#								sym["p"+term1]=next_h_n
#								next_h_n+=1
#								code+="111"+int_to_bin(sym[term1], 15)+"000"+int_to_bin(sym["p"+term1], 14)+"0"+"01"+"00000000000000000000000001"
#							term1="p"+term1
#						if is_num(res):
#							code+="111"+int_to_bin(sym[term1], 15)+"111"+int_to_bin(res, 14)+"0"+"01"+"00000000000000000000000001"
#						else:
#							code+="111"+int_to_bin(sym[term1], 15)+"000"+int_to_bin(sym[res], 14)+"0"+"01"+"00000000000000000000000001"
#					else:
#						print("Number not given for wait on line "+line+" !")
#						sys.exit()
#				else: 
#					print("Error line "+line+" operation invalid")
#					sys.exit()
#		else: #both terms start with p, and have been checked for '-'
#			if s_l.find("*")>0:
#				A=term1
#				B=term2
#				interim=""
#				if A<B:
#					interim=A+"*"+B
#				else:
#					interim=B+"*"+A
#				if not in_dict(sym, interim):
#					sym[interim]=next_h_n
#					next_h_n+=1
#				code+=neuron_and(A, B, interim, res, sym)
#			else: #use OR between the terms.
#				A=term1
#				B=term2
#				iA=A+"i"
#				iB=B+"i"
#				interim=""
#				if A<B:
#					interim=A+"+"+B
#				else:
#					interim=B+"+"+A
#				if not in_dict(sym, interim):
#					sym[interim]=next_h_n
#					next_h_n+=1
#				if not in_dict(sym, iA):
#					sym[iA]=next_h_n
#					next_h_n+=1
#				if not in_dict(sym, iB):
#					sym[iB]=next_h_n
#					next_h_n+=1
#				code+=neuron_or(A, B, iA, iB, interim, res, sym)
#		return code
#	#except KeyError:
#	#	print("Undefined reference on line: "+line)
#
prev_code=[]
for i in range(len(lines)):
	line=lines[i]
	#try:
	code=encode(line)
	k=0
	for i in range(64, len(code), 64):
		if code[k:i] in prev_code:
			pass
		else:
			prev_code.append(code[k:i])
		k=i
	#except:
	#	print("Error on line "+str(i)+" stating: "+line)
	#finally:
	#	print("The error on line "+str(i)+" would have quit the program, continuing with errors")
for code in prev_code:
	fp.write(code+"\n")






fp.close()
sys.exit()


#for j in range(len(text_data)):
#	i=text_data[j]
#	#this inner loop is meant to find '.', which indicates a simple op instead of the other kinds of operations.
#	if i=='\n':
#		k=j+1
#		op=0
#		LHS=""
#		RHS=""
#		
#		while text_data[k]!='\n':
#			k+=1
#			if text_data[k]=='.':
#				op=6
#				break
#		if op==6: #this is a literal statement
#
#		else:
#			
#	if i=='p':
#		p=True
#	elif i=='n':
#		repeat=False #norepeat
#	elif i=='r':
#		repeat=True
#	elif i=='-':
#		if len(RHS)>1: #this is the operation
#			#must assign space for the OR operations
#		else: #this is the first operand
#			k=j+1
#			buffer=""
#			while text_data[k]=='?' or text_data[k]=='|' or text_data[k]==':' or (text_data[k]<='Z' and text_data[k]>='A') or (text_data[k]<='z' and text_data[k]>='a' and text_data[k]!='w') or (text_data[k]<='9' and text_data[k]>='0'):
#				buffer+=text_data[k]
#				k+=1
#			if len(buffer)>0:
#				#if is_num(buffer): #is an input neuron
#				#	
#				#else: #must assign space 
#				sym["not "+buffer]=next_h_n
#				next_h_n+=1
#				neuron_not(buffer, "not "+buffer, sym, fp )
#				#sym["not "+buffer]
#				#neuron_not
#	elif i==' ':
#		if len(buffer)>=1:
#			if eq: #check buffer for RHS symbol
#				if is_num(buffer): #this is the number representing the input neuron being used
#					
#				elif is_float(buffer): #this means that the direct_exp is being used
#					
#				else: #this means buffer is a variable
#					if in_dict(sym, buffer):
#						
#					else:
#						print("At line "+str(lineno)+", symbol "+buffer+" was undefined.")
#						sys.exit()
#			else: #create new LHS symbol
#				
#		p=False
#		buffer=""
#	elif i=='\n':
#		see_newline=True
#		buffer=""
#		p=False
#		LHS=""
#		RHS=""
#		eq=False
#		lineno+=1
#	elif i<='Z' and i>='A':
#		buffer+=i
#		if eq:
#			RHS+=i
#		else:
#			LHS+=i
#
#
#
#fp.close()
