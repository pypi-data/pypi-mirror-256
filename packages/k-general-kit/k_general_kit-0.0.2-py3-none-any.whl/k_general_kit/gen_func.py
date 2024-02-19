#!/usr/bin/env python3
# -*-coding:UTF-8 -*

import sys
from pickle import Pickler, Unpickler
from math import*
from string import ascii_uppercase as Upper, ascii_lowercase as Lower

def arr(x, n, b = True):
	"""Renvoie l'arrondi ou la troncature de dégré n d'un nombre x suivant le booléen b"""
	try:
		assert n >= 0
		X2, X = vir(float(x))
		
		if n >= len(X):
			n = len(X)
			X.append(0)
		
		if b == False or X[n] < 5:
			del X[n:]
		else:
			i = 1
			try:
				X[n-1] += 1
				del X[n:]
		
				while X[n-i] == 10:
					del X[n-i]
					X[n-i-1] += 1
					i += 1
					assert X[0] != 10
			except:
				X = [0]
				X2[len(X2)-1] += 1
				
				while X2[len(X2)-i] == 10 and len(X2)-i != 0:
					del X2[len(X2)-i]
					X2[len(X2)-i-1] += 1
					i += 1
			
		return dec(X2 + ["."] + X)
	except:
		return "Les données saisies ne sont pas toutes valides! Veuillez vous réferer à l'aide!"

def bye():
	input("\nGlad to have served you! Press 'Enter' to quit.")
	sys.exit()

def Caesar(msg, key):
	"""It returns the encrypted version of msg following the Cesar process"""
	return msg.translate(str.maketrans(Upper+Lower, Upper[key:]+Upper[:key]+Lower[key:]+Lower[:key]))

def close_str(S1:str, S2:str, precision = 1/3):
	"""It evaluates with a precision given (default=1/3), how closed are two strings S1 and S2"""
	S1 = S1.replace(' ', '').lower()
	S2 = S2.replace(' ', '').lower()
	Diff = sym_diff_list([i for i in S1], [i for i in S2])
	l1 = len(S1)
	l2 = len(S2)
	d = abs(l1-l2)
	m = max(l1, l2)
	#We considerate firstly the differences inside the two strings that we divide by two (because they are counted twice in Diff), and secondly, those due to the difference of length of S1 and S2
	#Then we express how significant are those differences from the longest string between S1 and S2
	if ((len(Diff)-d)/2+d)/m <= precision: 
		return True
	return False

def close_sub_str(S1:str, S2:str, precision = 1/3):
	"""It evaluates with a precision given (default=1/3), how closed is a string S1 to an eventual substring of S2"""
	S1 = S1.replace(' ', '').lower()
	S2 = S2.replace(' ', '').lower()
	l1 = len(S1)
	l2 = len(S2)
	for i in range(l2-l1):
		if close_str(S1, S2[i: i+l1], precision) == True:
			return True
	return False

def dec(v, n = -1):
	"""Renvoie les n premiers chiffres sous forme floattante x d'une variable v"""
	try:
		assert n == -1 or n > 0
		x = ""
		v = str(v)
	
		if n == -1:
			n = len(v)
		
		for i in v:
			try:
				if i == "." and x.count(i) == 0:
					x += "."
				elif i == "-" and x == "":
					x += "-"
				else:                    
					x += str(int(i))
			except:
				pass
			
			l = len(x)

			if x.count("-") == 1:
				l -= 1

			if x.count(".") == 1:
				l -= 1
				
			if l >= n:
				break
		
		if x:
			return float(x)
	except:
		return "Les données saisies ne sont pas toutes valides! Veuillez vous référer à l'aide!"

def decipher_Caesar(S:str, n = 3):
	"""This function cracks the Caesar Cipher """
	MaxOcc = max_occ_str(S, n)
	Inv = [inv_Caesar(S, ord(T[0])-ord('e')) for T in MaxOcc]
	NumWords = [number_words_sentence(S) for S in Inv]
	ind = ind_min_or_max(NumWords, 1)
	return Inv[ind]

def extend(I, J):
	"""It extends an immutable iterable (list, dict or set) I with another one J of same type"""
	if type(I)==type(J):
		if type(I) == list:
			I.extend(J)
		if type(I) == dict:
			I.update(J)
		if type(I) == set:
			I.update(J)

def ent(v, n = -1):
	"""Renvoie les n premiers chiffres sous forme entière e d'une variable v"""
	try:
		assert n == -1 or n > 0
		e = ""
		v = str(v)
	
		if n == -1:
			n = len(v)
	
		for i in v:
			try:
				if i == "-" and e == "":
					e += "-"
				else:
					e += str(int(i))
			except:
				pass

			l = len(e)
			
			if e.count("-") == 1:
				l -= 1
			
			if len(e) >= n:
				break
		if e:
			return int(e)
	except:
		return "Les données saisies ne sont pas toutes valides! Veuillez vous réferer à l'aide!"

def func_rec(f:str, x:float, F0:dict):
	"""It takes a function defined by induction, and its initial values in the form of a dictionary (keys are values and values are their images through f). It returns f(x) if no error and False else"""
	assert type(f) == str, f"f={f} must be a string"
	assert type(x) == float, f"x={x} must be a float"
	assert type(F0) == dict and all([type(key) == float and type(val) == float for key, val in F0.items()]), f"F0 must be a dict where all elts must be floats"
	if x in F0:
		return F0[x]
	if F0 != {}:
		m = min(F0) 
	else:
		m = inf
	g = '' #It will contain the final function to evaluate without induction parts
	try: #We will try to identify parts in the form of f(x-a) in f
		count = 0
		i = 0
		l = len(f)
		l0 = len(F0)
		while i < l:
			if f[i: i+4] != "f(x-":
				g += f[i]
				i += 1
				continue
			i += 4
			j = i
			bool = False
			# We verify if after '-', we have a positive float followed by ')''
			while i<l:
				if f[i].isdigit():
					i+=1
					continue 
				if f[i] == '.' and bool == False:
					i+=1
					bool = True
					continue 
				break				
			if i == l or f[i] != ')':
				assert False
			k = round(x-float(f[j: i]), 6)
			if k < m or isclose(k, x):
				assert False
			count +=1
			if count > l0:
				assert False
			y = func_rec(f, k, F0) #We evaluate the found recurring part in f before putting the result in g
			F0[k] = y
			g += str(y)
			i += 1
		return eval(g.replace('x', str(x))) # We then evaluate the final expression 
	except AssertionError or TypeError:
		print(f"\nf(x)={f} is not a valid expression of a recurrence function or needs more init values than those given.\n")
		raise

def get_real(label='x', type=float):
	"""
	Prompt the user for input and convert it to a specified type.

	Args:
		label (str): The label to display when prompting for input.
		type (type): The type to convert the input to.

	Returns:
		The user input converted to the specified type.
	"""
	while True:
		x = input("\n" + label + " = ")
		if x.strip() == '':
			bye()
		try:
			x = type(x)
		except ValueError:
			print(f"\n!You didn't enter a/an {type}!")
			continue
		break
	return x

def har1(p1, p2):
	"""Renvoie la somme harmonique s de puissance p1 des p2 premiers nombres entiers positifs non nuls"""
	try:
		s = 0
	
		for i in range (1, p2+1):
			s += 1/(i**p1)
		
		return s
	except:
		return "Les données saisies ne sont pas toutes valides!"

def har2(p1, p2):
	"""Renvoie le produit harmonique p3 de puissance p1 des p2 premiers nombres entiers strictemrnt positifs"""
	with open("datas/prime/prime_numbers", "rb") as f:
		p = Unpickler(f)
		P = p.load()

	p3 = 1
	
	for i in range(0, p2):
		p3 *= 1/(1-1/(P[i]**p1))
		
	return p3

def ind_min_or_max(L:list, type=0):
	"""It returns the position of the min of a list L if type = 0 or of the max if type = 1"""
	imin = 0
	for i in range(len(L)):
		if (L[i] < L[imin])+type == 1:
			imin = i
	return imin

def is_int(S:str):
	"""It evaluates whether S is an int or not"""
	if S.isdigit() or (S[0] == '-' and S[1:].isdigit()):
		return True
	else:
		return False

def is_Lichrel(numb:int, n:int = 100):
	"""It tests if numb is a pseudo-number of Lychrel of order n"""
	if is_palindrome(str(numb)) == True:
			return False
	for i in range(n):
		numb = numb+int(str(numb)[-1::-1])
		if is_palindrome(str(numb)) == True:
			return False
	return True

def is_palindrome(S:str):
	"""It tests if S is a palindrome or not"""
	for i in range(int(len(S)/2)):
		if S[i] != S[-i-1]:
			return False
	return True    
	
def is_float(S:str):
	"""It evaluates whether S is an unsigned float or not"""
	try:
		float(S)
		return True
	except ValueError:
		return False 

def is_u_float(S:str):
	"""It evaluates whether S is an unsigned float or not"""
	try:
		x = float(S)
		assert x >= 0
		return True
	except ValueError or AssertionError:
		return False

def inv_Caesar(msg, key):
	"""It returns the decrypted version of msg following the Cesar process"""
	return msg.translate(str.maketrans(Upper[key:]+Upper[:key]+Lower[key:]+Lower[:key], Upper+Lower))

def lis(v, c = "", b = True):
	"""Renvoie une variable v listée en L suivant c"""
	try:
		L = []
		v = str(v)
		
		if c == "":
			for i in v:
				L.append(i)
		else:
			L = v.split(c)

		if b:
			for i, i2 in enumerate(L):
				try:
					L[i] = int(i2)
				except:
					pass

		return L
	except:
		return "Les données saisies ne sont pas toutes valides! Veuillez vous référer à l'aide!"

def max_occ_str(S:str, n:int=3)-> list[str, int]:
	"""It returns the letters that appears the most in a string S, with their occurrences"""
	LettersOcc = {}
	for c in S:
		if c.isalnum():
			if c not in LettersOcc:
				LettersOcc[c] = 1
			else:
				LettersOcc[c] += 1
	LettersOcc = [(i, LettersOcc[i]) for i in LettersOcc]
	return mins_or_maxs2(LettersOcc, n, 1)

def mins_or_maxs2(I:list[str, float], n:int = 2, type:int = 0)-> list:
	""""This function returns if type = 0, the n minima couples of a list I = [['x', n],...] in terms of the second  elt of each elt of I. If type = 1, we do th contrary"""
	l = len(I)
	assert 1 <= n <= l
	I1 = I[:n]
	# We first sort the n first element of I
	for i in range(n):
		mem = I1[i]
		j = i-1
		while j >= 0 and (I1[j][1] > mem[1])+type == 1:
			I1[j+1] = I1[j]
			j -= 1
		I1[j+1] = mem
	# We try to insert if possible by replacing, the other element of I in I1, using the insertion principle in sorts.
	for i in range(n, l):
		if (I[i][1] < I1[n-1][1])+type == 1:
			j = n-2
			while j >= 0 and (I1[j][1] > I[i][1])+type == 1:
				I1[j+1] = I1[j]
				j -= 1
			I1[j+1] = I[i]
	return I1

def nal(n1 , n2):
	"""Renvoie un nombre entier aléatoire n3 strictement positif  compris dans [n1, n2["""
	if type(n1) != int or n1 < 0:
		return "'{}' n'est pas un nombre entier strictement positif!".format(n1)
	elif type(n2) != int or n2 <= 0:
		return "'{}' n'est pas un nombre entier strictement positif!".format(n2)
	elif n1 >= n2:
		return "{} >= {}".format(n1, n2)
	else:
		with open("datas/random_seeds/nal_seed", "rb") as f:
			p = Unpickler(f)
			x = p.load()

		n3 = n1 - 1

		def dec(x1, x2):
			"""Renvoie dans une chaine c contenant les 1er chiffres de la partie décimale d'un nombre x1 telque le nombre formé soit <= x2"""
			if type(x1) != float:
				return "'{}' n'est pas un flottant!".format(x1)
			elif type(x2) != int or x2 <= 0:
				return "'{}' n'est pas un nombre entier strictement positif!".format(x2)
			else:
				c = x2 + 1
				i1 = 1

				for i2 in str(x1): 
					if i2 == ".":
						i1 = 0
						c = ""
						continue
					elif i1 == 0:
						c = i2
				
					if x2 >= int(c):
						break
			
				return c
		
		while n3 < n1 or n3 >= n2:
			x = sqrt(x)
			n3 = ""
			
			try:
				if int(x) == x:
					x = sqrt(x**2 + 1)
			except ValueError:
				s = s

			n3 = dec(x, n2-n1)
			
			if n3 != "0":
				n3 = trunc((n2-n1)/int(n3))*(-1)**int(n3) + trunc((n1 + n2)/2)
			else:
				n3 = trunc((n2-n1)/2)*(-1)**int(n3) + trunc((n1 + n2)/2)
			
			x = x**2 + 1

		with open("datas/random_seeds/nal_seed", "wb") as f:
			p = Pickler(f)
			p.dump(x)
			
		return n3

def nel(x1):
	"""Renvoie l'écriture c1 d'un nombre x1 en lettres"""
	if type(x1) != int and type(x1) != float:
		return "'{}' n'est pas un nombre!".format(x1)   
	else:
		c1 = ""
		i1 = 0
		L1 = []
		L2 = ['', 'un', 'deux', 'trois', 'quatre', 'cinq', 'six', 'sept', 'huit', 'neuf']
		L3 = ['dix', 'onze', 'douze', 'treize', 'quatorze', 'quinze', 'seize', 'dix-sept', 'dix-huit', 'dix-neuf']
		L4 = ['', '', 'vingt', 'trente', 'quarante', 'cinquante', 'soixante', 'soixante', 'quatre-vingt', 'quatre-vingt']   
		L5 = ['mille ', 'mille ', 'un million ', 'millions ', 'un milliard ', 'milliards ']

		def net(c1):
			"""Renvoie une chaine de caractère c1 après l'avoir débarassée de ses espaces inutiles"""
			i1 = 0
			
			while i1 < len(c1):
				try:
					while c1[0] == " ":
						c1 = c1[1:]
					while c1[len(c1)-1] == " ":
						c1 = c1[:len(c1)-1]
					while c1[i1] == " " and c1[i1 + 1] == " ":
						c1 = c1[:i1] + c1[i1+1:]
				except:
					pass
				
				i1 += 1
				
			return c1
		
		if int(x1) != x1:
			r = True
			if str(x1).count("e") == 1:
				if x1 > 0:
					x1 += 1
				else:
					x1 -= 1

				x2 = 0
				r = False
				
			x1 = str(x1)
			i1 = 0
			i2 = 0
		
			while i1 < len(x1):
				if x1[i1] == ".":
					break
				i1 += 1
			
			if r:
				x2 = x1[:i1]
				  
			x3 = x1[i1+1:]
			c2 = nel(int(x2))
			c3 = nel(int(x3))

			if int(x2) == 0 and float(x1) < 0:
				c2 = "moins zéro"

			while i2 < len(x3):
				if x3[i2] != '0':
					break
				i2 += 1

			if i2 == 0:
				c4 = ""
			elif i2 == 1:
				c4 = "(zéro) "
			else:
				c4 = "({} zéro) ".format(i2)
				
			return net(c2 + " virgule " + c4 + c3)

		x1 = int(x1)
		
		if x1 < 0:
			c1 = "moins "
			x1 = -x1

		for i1 in str(x1):
			L1.append(int(i1))
		
		l = len(L1)
		i1 = 13
		i2 = 12

		while i1 < l+1:
			L5 += (L5 + L5)
			i2 += 12
			i1 += 12
		
		for i3 in range(0, i2-l):
			L1.insert(0, 0)
			
		for i3 in range(0, i2//2):
			L1[i3], L1[i2-1-i3] = L1[i2-1-i3], L1[i3] 
		
		if x1 == 0:
			c1 = "zéro"
		else:
			while i2 > 2:
				if L1[i2-3] == 1 and L1[i2-2] == 0 and L1[i2-1] == 0:
					if L1[0] == 1 and i2 == 3:
						c1 += ' un'  
					else:
						c1 += L5[int((i2/3-2)*2)]
				elif L1[i2-1] != 0 or L1[i2-2] != 0 or L1[i2-3] != 0:
					if L1[i2-2] == 1:
						c2 = L3[L1[i2-3]]
					elif L1[i2-2] == 7 or L1[i2-2] == 9:
						if L1[0] == 1 and i2 == 3:
							c2 = L4[L1[1]]  + '-et-onze'
						else:
							c2 = L4[L1[i2-2]] + '-' + L3[L1[i2-3]]
					else:
						if L1[1] == 8 and L1[0] == 0 and i2 == 3:
							c2 = 'quatre-vingts'
						elif L1[1] != 8 and L1[0] == 1 and i2 == 3:
							c2 = L4[L1[1]]  + '-et-un' 
						else:
							c2 = L4[L1[i2-2]]  + ' ' + L2[L1[i2-3]]
					
					if L1[i2-1] != 0:
						L = list(L2)
						del L[1]
						
						if L1[2] != 1 and L1[1] == 0 and L1[0] == 0 and i2 == 3:
							c2 = L[L1[i2-1]-1] + ' cents'
						else:
							c2 = L[L1[i2-1]-1] + ' cent ' + c2 
					
					if i2 != 3:
						c1 += c2 + ' ' + L5[int((i2/3-2)*2+1)]
					else:
						c1 += c2
						
				if i2 != 3 and (i2-3) % 12 == 0 and L1[i2-4] == 0 and L1[i2-5] == 0 and L1[i2-6] == 0:
					c1 += 'milliards '
				
				i2 -= 3
				
			c1 = net(c1)
			
	return c1

def net(c):
	"""Renvoie une chaine de caractère c après l'avoir débarassée de ses espaces inutiles"""
	i = 0
	try:
		assert type(c) == str
		
		while i < len(c):
			try:
				while c[0] == " ":
					c = c[1:]
				while c[len(c)-1] == " ":
					c = c[:len(c)-1]
				while c[i] == " " and c[i + 1] == " ":
					c = c[:i] + c[i+1:]
			except:
				pass
				
			i += 1
				
		return c
	except:
		return "Les données saisies ne sont pas toutes valides! Veuillez vous réferer à l'aide!"

def number_pseudo_words_sentence(Phrase):
	"""Cette fonction prend en entrée une chaine de caractères et renvoie le nbre de pseudo-mots qu'elle contient
	NB: -Un pseudo-mot est une suite accolée de caractères exceptionnellement alphabétiques
	"""
	Nbre=0   
	l=len(Phrase)
	for i in range(l):
		if Phrase[i].isalpha()==True and (i==0 or Phrase[i-1].isalnum()==False):
			"""En parcourant Phrase, on dénombre un nouveau pseudo-mot chaque fois qu'on arrive sur un caractère qui est dans l'alphabet et telque le précédent
			soit un caractère non alphanumérique
			"""
			Nbre+=1
			while i<l-1 and (Phrase[i+1].isalpha()==True): 
				#On essaye de savoir jusqu'ou va le pseudo-mot détecté ; on arrive à sa fin lorsqu'on tombe sur un blanc
				i+=1
	return Nbre

def number_words_sentence(Phrase:str, lang = 'fr')-> int:
	"""Cette fonction prend en entrée une phrase (chaine de caractères) et renvoie le nbre de mots qu'elle contient
	NB: -Un mot est une suite accolée de caractères exceptionnellement alphabétiques ayant un sens (pouvant être retrouvé dans un dictionnaire)
	ou un nom propre (débutant par une lettre majuscule) ; les mots sont séparés par des blancs les uns des autres.\
	-Le programme s'appuie sur un dictionnaire qui permet de vérifier l'existence des éventuels mots de la phrase.\
	Par défaut le dictionnaire esr fr. Il n'y a plus que la version anglaise qui répond au paramètre lang = 'en'\
	-Pour un bon fonctionnement de la fonction, bien vouloir écrire uniquement les noms propres avec la première lettre en majuscule pour qu'ils puissent etre identifiés\
	-Bien vouloir n'inclure des majuscules dans un mot que ssi c'est un nom propre\
	-Bien vouloir aussi ne commencer vos phrases par une lettre majuscule que si le premier mot est un mom propre ; car en cas d'erreur sur le premier mot, il sera vu comme un nom propre et donc comme un nom\
	-Bien vouloir prendre la peine d'écrire des phrases grammaticalement correctes car des nots erronés ne seront pas compter comme des mots\
	Tout ceci dans la phrase 'Phrase', passée en paramètre.
	"""
	Nbre=0
	if lang == 'fr':
		file = "datas/dicts/fr_dict.txt"
	else:
		file = "datas/dicts/en_dict.txt"

	with open(file, "r") as Dict_F:
		#On va rechercher tout ce qui semble être un mot dans un dictionnaire contenu dans le fichier ouvert
		Dict_L=Dict_F.readlines() # On mets les mots de ce dictionnaire dans une liste
		
	l=len(Phrase)
	for i in range(l):
		if Phrase[i].isalpha()==True and (i==0 or Phrase[i-1].isalnum()==False) and Phrase[i-1]!='-' :
			"""En parcourant Phrase, on dénombre un nouveau pseudo-mot chaque fois qu'on arrive sur un caractère qui est dans l'alphabet et tel que le précédent
			soit un caractère non alphanumérique différent de '-' car '-' est le seul caractère qui peut servir à former des mots (dits composés)
			"""
			m=i
			while i<l-1 and (Phrase[i+1].isalpha()==True or Phrase[i+1]=='-'): 
				#On essaye de savoir jusqu'ou va le pseudo-mot détecté ; on arrive à sa fin lorsqu'on tombe sur un blanc
				i+=1
			if (Phrase[m : i+1]+'\n' in Dict_L) or Phrase[m].isupper()==True or ((i<l-1 and Phrase[i+1]=="'") and ((Phrase[m : i+1]+'i\n' in Dict_L) or (Phrase[m : i+1]+'e\n' in Dict_L))):
				"""Ici on compte ce pseudo mot comme véritable mot ssi soit il est dans le dictionnaire, soit s'il est un nom propre
				(dans ce cas il commence par une lettre majuscule) ou alors il est un mot se terminant par l'apostrophe dont on a oté
				le 'e' ou 'i'. Ex: j' pour je; s' pour si
				"""
				Nbre+=1
					
	if Phrase.lower().find("aujourd'hui")!=-1 and lang == 'fr':
		"""Vu que la logique précédente va voir 'aujourd'hui' comme 'aujourd' et 'hui' qui ne sont pas dans le dictionnaire,
		alors 'aujourd'hui' ne sera pas compté comme mot d'ou la nécessité de le compter maintenant"""
		Nbre+=1
	return Nbre

def occ_str(S:str, S2:str):
	"""It returns a list containing all the eventual indices (in the ascending order) of the str S2 in the str S"""
	assert type(S) == str and type(S2) == str, f"S={S} and S2={S2} must be str"
	Occ = []
	i=0
	l = len(S2)
	while i < len(S)-l+1:
		if S[i: i+l] == S2:
			Occ.append(i)
			i += l
		else:
			i += 1
	return Occ

def open_binary_file(Datas, path, mode='rb'):
	"""It takes as input the path of a binary file, the mode of access to this file ('rb' or 'wb') and a data structure 'Datas'
	-If mode='rb' it puts the contents of this file in 'Datas'
	-If mode='wb', it copies the contents of 'Datas' in this file
	"""
	with open(path, mode) as f:
		if mode == 'rb':
			p = Unpickler(f)
			extend(Datas, p.load())  
		if mode == 'wb':
			p = Pickler(f)
			p.dump(Datas)
		
def ord(r, *N):
	"""Renvoie une liste R contenant les nombres d'une liste N, rangés dans un ordre suivant le booléen r"""
	if type(r) != bool:
		return "'{}' n'est pas un booléen".format(r)
	for i in N:
		if type(i) != float and type(i) != int:
			return "'{}' n'est pas un nombre".format(i)
	
	R = []
	L = list(N)

	if r == True:
		while len(L) > 0:
			m = min(*L)
			R.append(m)
			L.remove(m)
	else:
		while len(L) > 0:
			m = max(*L)
			R.append(m)
			L.remove(m)
			
	return R

def Pascal(height:int):
	"It prints a pascal triangle of size height"
	assert type(height) == int and height >= 1, "the height of the Pascal triangle to print is not a strict positive integer"
	Pascal = [1]
	comb = lambda n,p: 0 if (p > n or p < 0) else 1 if p == 0 else n/p*comb(n-1,p-1)
	max = len(str(int(comb(height-1, round((height-1)/2)))))
	if max%2 == 1:
		max1 = round((max+1)/2)
		max2 = max
	else:
		max1 = round((max+2)/2)
		max2 = max+1
	for i in range(height):
		print(" "*(height-i-1)*max1, " ".join([str(elt).center(max2) for elt in Pascal]))
		Pascal = [1]+[Pascal[j]+Pascal[j+1] for j in range(len(Pascal)-1)]+[1]

def paw(m, e = 5):
	"""Accorde l'accès à un système via un mot de passe m avec e essai(s)"""
	if type(e) != int or e <= 0:
		return "'{}' n'est pas un nombre entier strictement positif".format(e)
	else:
		i = 0
		while True:
			if i == e:
				print("Vous avez épuisez toutes vos possibilités! Veuillez sortir!")
				return False
			p = input("Mot de passe : ")
			if p == m:
				break
			i += 1
		print("Bienvenue!")
		return True

def per(*L):
	"""Renvoie une liste L2 contenant les caractères permutés d'une liste L"""
	try:
		with open("datas/random_seeds/per_seed", "rb") as f:
			p = Unpickler(f)
			x = p.load()

		x = sqrt(x)
		l = len(L)
		
		while int(x) == x:
			x = sqrt(x**2 + 1)
	
		L1 = vir(arr(x, l, False), False)
	
		j = 0
		D = {}
	
		for i in L:
			if L1[:j].count(L1[j]) == 0:
				D[L1[j]] = i
			else:
				while L1[:j].count(L1[j]) != 0:
					x = sqrt(x**2 + 1)

					while int(x) == x:
						x = sqrt(x**2 + 1)

					L1[j] = int(str(L1[j]) + str(vir(arr(x, l, False), False)[0]))
				D[L1[j]] = i
			j += 1
		
		L1 = ord(False, *L1)
		L2 = []
	
		for i in L1:
			L2.append(D[i])
		
		x = x**2 + 1

		with open("datas/random_seeds/per_seed", "wb") as f:
				p = Pickler(f)
				p.dump(x)
				
		return L2
	except:
		return "Les données saisies ne sont pas toutes valides! Veuillez vous référer à l'aide!"

def pfp(n1):
	"""Renvoie la décomposition en produit de facteurs premiers c d'un entier strictement positif n1"""
	if type(n1) != int or n1 <= 0:
		return "'{}' n'est pas un entier strictement positif!" 
	else:
		if n1 == 1 or n1 == 0:
			return "n"
		else:
			with open("datas/prime/prime_numbers", "rb") as f:
				p = Unpickler(f)
				L1 = p.load()
			
			with open("datas/prime/prime_decompositions", "rb") as f:
				p = Unpickler(f)
				D = p.load()
			
			L = ["1"]
			
			for i1, i2 in D.items():
				if i1 == n1:
					L = i2
					return " × ".join(L)

			i1 = 2
			i2 = 1
			i3 = 0
			n2 = n1        
			for i1 in L1:

				while n2 - (n2 // i1)*i1 == 0:
					i3 += 1
					i2 *= i1
					n2 = n2 // i1
					   
				if i3 != 0:
					if i3 == 1:
						L.append(str(i1))
					else:
						L.append(str(i1) + "˄" + str(i3))
					i3 = 0
				
				if i2 == n1:
					break

			i1 += 1
			
			while i2 != n1:
				i4 = i1
				i5 = 2
				
				while i5 <= i1/i5:
					if i1 % i5 == 0:
						i1 += 1
						break
					i5 += 1

				if  i4 == i1:
					i3 = 0
					
					while n2 - (n2 // i1)*i1 == 0:
						i3 += 1
						i2 *= i1
						n2 = n2 // i1

					if i3 != 0:
						if i3 == 1:
							L.append(str(i1))
						else:
							L.append(str(i1) + "˄" + str(i3))
						i3 = 0
					
					L1.append(i1)
					i1 += 1
					
					if i2 == n1:
						break
		D[n1] = L
					
		with open("datas/prime/prime_numbers", "wb") as f:
			p = Pickler(f)
			p.dump(L1)

		with open("datas/prime/prime_decompositions", "wb") as f:
			p = Pickler(f)
			p.dump(D)
			
		return " × ".join(L)

def gcd(n1, n2):
	"""Renvoie le gcd de 2 entiers relatifs n1, n2 non tous nuls"""
	try:
		assert n1 != 0 or n2 != 0
		
		c = max(abs(n1), abs(n2))
		d = min(abs(n1), abs(n2))
		
		if d == 0:
			p = c
		elif d == 1:
			p = 1
		else:
			p = gcd(d, c-d*(c//d))
		return p
	except:
		return "Les données saisies ne sont pas toutes valides! Veuillez vous réferer à l'aide!"

def lcm(n1, n2):
	"""Renvoie le lcm de 2 entiers relatifs n1, n2 non tous nuls"""
	try:
		assert n1 != 0 or n2 != 0
		return abs(trunc((n1*n2)/gcd(n1, n2)))
	except:
		return "Les données saisies ne sont pas toutes valides! Veuillez vous réferer à l'aide!"

def pow_in_fac(n:int, p:int):
	"""It returns the power of the prime number p in the decomposition into prime factors of the factorial of the strict positive integer n"""
	assert type(n) == int and n > 0, f"n={n} must be a strict positive integer"
	assert pri1(p), f"p={p} must be a prime number"
	return sum([floor(n/p**i) for i in range(1, floor(log(n)/log(p))+1)])

def pri1(n):
	"""Renvoie un booléen r correspondant à la primalité d'un nombre entier positif n"""
	if type(n) != int or n < 0:
		raise f"n='{n}' n'est pas un nombre entier positif"
	else:
		i = 2
		r = True

		if n == 0 or n == 1:
			r = False
		else:
			while i <= n/i:
				if n % i == 0:
					r = False
					break
				i += 1

		return r

def pri2(n1, n2):
	"""Renvoie une liste contenant les nombres premiers de l'intervalle [n1, n2["""
	if type(n1) != int or n1 < 0:
		raise TypeError("'n1={}' n'est pas un nombre entier strictement positif!".format(n1))
	elif type(n2) != int or n2 < 0:
		raise TypeError("'n2={}' n'est pas un nombre entier strictement positif!".format(n2))
	elif n1 >= n2:
		raise TypeError("Erreur! {} >= {}, while it shoudn't be like this!".format(n1, n2))
	else:
		L = []
	
		for i in range(n1, n2):
			if pri1(i):
				L.append(i)
		return L

def pri3(n: int, start: int = 0) -> list:
    """
    Returns a list of the first 'n' prime numbers, starting at 'start'.

    Parameters:
        n (int): The number of prime numbers to return.
        start (int): The starting point to search for prime numbers. Default is 0.

    Returns:
        list: A list of the first 'n' prime numbers.

    Raises:
        AssertionError: If 'n' is not a positive integer or 'start' is not a non-negative integer.

    """

    # Check if 'n' is a positive integer
    assert type(n) == int and n > 0, f"n={n} must be a strict positive integer."

    # Check if 'start' is a non-negative integer
    assert type(start) == int and start >= 0, f"start={start} must be a strict positive integer."

    # Initialize an empty list to store the prime numbers
    Pri = []

    # Initialize a counter and starting value for prime number search
    i = 0
    pri = start

    # Iterate until 'n' prime numbers are found
    while i < n:
        # Check if 'pri' is a prime number using a helper function 'pri1()'
        if pri1(pri):
            # If 'pri' is prime, append it to the list and increment the counter
            Pri.append(pri)
            i += 1
        
        # Move to the next number
        pri += 1
    
    # Return the list of prime numbers
    return Pri
	
def print_func(h:str, before:str = "")-> bool:
	"""It evaluates and prints an expression h, managing errors. It returns True if operations were held normally and False else. It puts a message 'before', before printing the result if no error occurred. It returns True if no error occurred and False else."""
	assert type(h) == str, f"h={h} must be a str"
	assert type(before) == str, f"before={before} must be a str"
	try:
		print(before+str(eval(h)))
		return True
	except ValueError:
		print(f"\nThe entered function is not defined for an entered value")
	except ZeroDivisionError:
		print(f"\nThe entered function is not defined for an entered value, due to a division by 0 which occured while evaluating it")
	except SyntaxError:
		print(f"\nThe entered function is syntaxically incorrect.")
	except NameError:
		print(f"\nThe entered function has unknown python math functions.")
	except ArithmeticError:
		print(f"\nThe evaluation of the given function reaches the arithmetic limits of Python")

def print_func_rec(g:str, before:str = "")-> bool:
	"""It evaluates and prints an expression g defined by induction, managing errors. It returns True if operations were held normally and False else. It puts a message 'before', before printing the result if no error occurred. It returns True if no error occurred and False else."""
	assert type(g) == str, f"g={g} must be a str"
	assert type(before) == str, f"before={before} must be a str"
	try:
		print(before+str(eval(g)))
		return True
	except ValueError:
		print(f"\nThe entered function is not defined for an entered value")
	except ZeroDivisionError:
		print(f"\nThe entered function is not defined for an entered value, due to a division by 0 which occured while evaluating it")
	except SyntaxError:
		print(f"\nThe entered function is syntaxically incorrect.")
	except NameError:
		print(f"\nThe entered function has unknown python math functions.")
	except ArithmeticError:
		print(f"\nThe evaluation of the given function reaches the arithmetic limits of Python")
	except AssertionError or TypeError:
		pass

def print_table(Datas, Label:str = '',End = '', place="cmd"):
	"""This functions displays datas in 'Datas' on 'place' with the label 'label'and an end expression 'End'
	Args:
		Label (str): title of the datas that are going to be displayed
		Datas (list(list)): it contains the datas to display. It's a table
		End (str): it is a final eventual expression. Defaults to ""
		place (str): it indicates the place where to display the datas. Defaults to "cmd". it can also take as value the path of a file where to diplay the table
	"""
	try:
		if all([len(i)==len(Datas[0]) for i in Datas]) == False:
			print("Le structure fournie n'est pas un tableau n*m valide")
		else:
			TransposeDatas = [[Datas[j][i] for j in range(len(Datas))] for i in range(len(Datas[0]))]
			Space = [max([len(str(data)) for data in Data]) for Data in TransposeDatas]
			Str = ''
			if Label != '':
				Str = Label.center(sum([i+3 for i in Space])+1)+"\n"
			for i in range(len(Datas)):
				Str+="+"
				for j in range(len(Datas[i])):
					Str += "-"*(Space[j]+2)+"+"
				Str+="\n| "
				for j in range(len(Datas[i])):
					Str += f"{Datas[i][j]}".center(Space[j])+" | "
				Str+="\n"
				if i == len(Datas)-1:
					Str+="+"
					for j in range(len(Datas[i])):
						Str += "-"*(Space[j]+2)+"+"
					Str+="\n"
					
			if End != "":
				Str+=End.center(sum([i+3 for i in Space])+1)+"\n"
			
			if place == "cmd":
				print(Str)
			else:
				with open(place, "w") as f:
					f.writelines(Str)
	except:
		pass

def prod_func(func:str, start:float, end:str, step:float)-> float:
	"""It returns the products of func(x) for x going from 'start' to 'end' by step of 'step'"""
	return prod(eval(func.replace('x', str(x))) for x in range_float(start, end, step))

def prod_func_rec(func:str, start:float, end:str, step:float, F:dict)-> float:
	"""It returns the products of func(x) (defined by recurrence) for x going from 'start' to 'end' by step of 'step. The init values of func are in F"""
	return prod([func_rec(func, x, F) for x in range_float(start, end, step)])

def pseudo_words_sentence(Phrase):
	"""Cette fonction prend en entrée une chaine de caractères et renvoie les pseudo-mot(s) qu'elle contient dans une liste
	NB: -Un pseudo-mot est une suite accolée de caractères exceptionnellement alphabétiques
	"""
	PseudoWords = []
	l=len(Phrase)
	for i in range(l):
		if Phrase[i].isalpha()==True and (i==0 or Phrase[i-1].isalnum()==False):
			"""En parcourant Phrase, on dénombre un nouveau pseudo-mot chaque fois qu'on arrive sur un caractère qui est dans l'alphabet et telque le précédent
			soit un caractère non alphanumérique
			"""
			pseudoWord = ''
			while i<l-1 and (Phrase[i+1].isalpha()==True): 
				#On essaye de savoir jusqu'ou va le pseudo-mot détecté ; on arrive à sa fin lorsqu'on tombe sur un blanc
				pseudoWord += Phrase[i]
				i+=1
			pseudoWord += Phrase[i]   
			if pseudoWord != '':
				PseudoWords.append(pseudoWord)
				
	return PseudoWords

def range_float(start:float, end:float, step:float = 1)-> list:
	"""It returns the floats between 'start' and 'end', starting at 'start', with a step of 'step'"""
	if step == 0:
		return [start]
	return [start+step*n for n in range(0, floor((end-start)/step)+1)]

def replace_iter(S:str, I1, I2, count:int = -1):
	"""It replaces in S respectively the elts of I1 by those of I2
	NB: - I1, I2 are iterables and must to have same length
		- count indicates the maximum of occurences to replace. By default count = -1, meaning that all the occurences'll be replaced
	"""
	for i in range(min(len(I1), len(I2))):
		S = S.replace(I1[i], I2[i], count)
	return S

def root2(L):
	"""This function returns all the roots of a second degre polynomial which coefficients are in a list L"""
	try: #We verify if we have 3 coefs which are all floats with the first one != 0
		assert len(L)==3
		assert L[0]!=0
		for i in range(3):
			L[i]=float(L[i])
	except:
		return ()

	d= L[1]**2-4*L[0]*L[2]
	if d>0:
		return (-L[1]-sqrt(d))/(2*L[0]), (-L[1]+sqrt(d))/(2*L[0])
	elif d==0:
		return (-L[1]/(2*L[0]),)
	else:
		return ()

def split_alpha(S:str):
	"""It splits S following the non-alphabetic symbols that it contains"""
	Split = []
	for i in S:
		if i.isalpha() == False:
			Split.append(i)
	return split_iter(S, Split)

def split_alphanum(S:str):
	"""It splits S following the non-alphanumeric symbols that it contains"""
	Split = []
	for i in S:
		if i.isalnum() == False:
			Split.append(i)
	return split_iter(S, Split)

def split_iter(S:str, I = [''], bool = True):
	"""It splits S following the elements of I.
	NB: - I is an iterable
		- bool indicates wheter the list to be returned won't contain '' or not
	"""
	if I == [''] or I == '':
		return [i for i in S]
	for i in I[1:]:
		S = S.replace(i, I[0])
	Split = S.split(I[0])
	if bool == False:
		return Split
	i = 0
	while True:
		if i == len(Split):
			break
		if Split[i] == '':
			Split.pop(i)
		else:
			i += 1
	return Split

def stairs(n:int, m:int):
	"""It returns S(n) where S(n+m)=S(n+m-1)+...+S(n)"""
	try:
		n = int(n)
		m = int(m)
		assert n > 0 and m > 0 and n >= m
	except:
		print("Les données entrées ne sont pas toutes valides!")
		return False
	
	if m == 1:
		return 1
	
	S = [1]
	for i in range(n):
		S.append(sum(S))
		if len(S) == m+1:
			S.pop(0)
			
	return S[-1]

def stars_triangle(m):
	"""Cette fonction prend en entrée un entier m et affiche un triangle d'étoiles(*) avec m ligne(s) d'étoiles"""
	for i in range(1, m+1):
		print(' '*(m+1-i), '* '*i) #On a m ligne(s) et chaque ligne i, a i étoile(s) et commence après m+1-i espace(s)

def sum_func(func:str, start:float, end:str, step:float)-> float:
	"""It returns the sum of func(x) for x going from 'start' to 'end' by step of 'step'"""
	return fsum(eval(func.replace('x', str(x))) for x in range_float(start, end, step))

def sum_func_rec(func:str, start:float, end:str, step:float, F:dict)-> float:
	"""It returns the sum of func(x) (defined by recurrence) for x going from 'start' to 'end' by step of 'step. The init values of func are in F'"""
	return fsum([func_rec(func, x, F) for x in range_float(start, end, step)])

def sym_diff_list(L1:list, L2:list):
	"""It returns a list which elts indicate a chronological difference between the two lists given as parameters """
	Diff = []
	while True:
		l1 = len(L1)
		l2 = len(L2)
		if l2 < l1:
			L1, L2 = L2, L1
		if L1 == []:
			Diff.extend(L2)
			break
		i = 0
		while i < l2:
			#We try to find if the concerned elt is in L2 too and so, can't be count as a difference
			if L1[0] == L2[i] and i <= abs(l2-l1):
				#To ensure the chronological similarity between L1 and L2, we remove all elts before L2[i] because they indicate a chronological difference between the two lists
				L1.pop(0)
				for j in range(i):
					Diff.append(L2[0])
					L2.pop(0)
				L2.pop(0)
				break
			i += 1
		if i == l2:
			#In this case, no elts of L2 corresponds to L1[0], so we count it as a difference between the two lists
			Diff.append(L1[0])
			L1.pop(0)
	return Diff

def titlecase(S:str, sep:str = ' '):
	"""A better version of str.title() where for exmple "'s'" won't become "'S'", but will stay the same"""
	return sep.join([i.capitalize() for i in S.split(sep)])

def tranpose(Table):
	"""It returns the transpose of a table Table"""
	return [[Table[j][i] for j in range(len(Table))] for i in range(len(Table[0]))]

def vir(x, e = True, d = True):
	"""Renvoie la partie entière dans une liste E (e = True et d = False),
	   la partie décimale  dans une liste D (e = False et d = True),
	   ou la partie entière dans une liste E et celle décimale dans une liste D (e = True et d = True)  
	d'un nombre x"""
	try:
		x = float(x)
		x = str(x)
		E = []
		D = []
		
		def ent():
			"""Renvoie la partie entière dans une liste E d'un nombre chainé x"""
			for i in x:
				if i == ".":
					break

				try:
					i = int(i)
				except:
					pass

				E.append(i)
				
			return E
		
		def dec():
			"""Renvoie la partie décimale dans une liste D d'un nombre chainé x"""
			r = True
			
			for i in x:
				if i != "." and r:
					continue

				if i == ".":
					r = False
					continue

				D.append(int(i))
				
			return D

		if e == True and d == False:
			return ent()
		elif e == False and d == True:
			return dec()
		else:
			return ent(), dec()
	except:
		return "Les données saisies ne sont pas toutes valides! Veuillez vous réferer à l'aide!"

def words_sentence(Phrase, lang = 'fr'):
	"""Cette fonction prend en entrée une phrase (chaine de caractères) et renvoie la liste des mots qu'elle contient
	NB: -Un mot est une suite accolée de caractères exceptionnellement alphabétiques ayant un sens (pouvant être retrouvé dans un dictionnaire)
	ou un nom propre (débutant par une lettre majuscule) ; les mots sont séparés par des blancs les uns des autres.\
	-Le programme s'appuie sur un dictionnaire qui permet de vérifier l'existence des éventuels mots de la phrase.\
	Par défaut le dictionnaire esr fr. Il n'y a plus que la version anglaise qui répond au paramètre lang = 'en'\
	-Pour un bon fonctionnement de la fonction, bien vouloir écrire uniquement les noms propres avec la première lettre en majuscule pour qu'ils puissent etre identifiés\
	-Bien vouloir n'inclure des majuscules dans un mot que ssi c'est un nom propre\
	-Bien vouloir aussi ne commencer vos phrases par une lettre majuscule que si le premier mot est un mom propre ; car en cas d'erreur sur le premier mot, il sera vu comme un nom propre et donc comme un nom\
	-Bien vouloir prendre la peine d'écrire des phrases grammaticalement correctes car des nots erronés ne seront pas compter comme des mots\
	Tout ceci dans la phrase 'Phrase', passée en paramètre.
	"""
	Mots = []
	if lang == 'fr':
		file = "datas/dicts/fr_dict.txt"
	else:
		file = "datas/dicts/en_dict.txt"

	with open(file, "r") as Dict_F:
		#On va rechercher tout ce qui semble être un mot dans un dictionnaire contenu dans le fichier ouvert
		Dict_L=Dict_F.readlines() # On mets les mots de ce dictionnaire dans une liste
		
	l=len(Phrase)
	for i in range(l):
		if Phrase[i].isalpha()==True and (i==0 or Phrase[i-1].isalnum()==False) and Phrase[i-1]!='-' :
			"""En parcourant Phrase, on dénombre un nouveau pseudo-mot chaque fois qu'on arrive sur un caractère qui est dans l'alphabet et telque le précédent
			soit un caractère non alphanumérique différent de '-' car '-' est le seul caractère qui peut servir à former des mots (dits composés)
			"""
			m=i
			while i<l-1 and (Phrase[i+1].isalpha()==True or Phrase[i+1]=='-'): 
				#On essaye de savoir jusqu'ou va le pseudo-mot détecté ; on arrive à sa fin lorsqu'on tombe sur un blanc
				i+=1
			if (Phrase[m : i+1]+'\n' in Dict_L) or Phrase[m].isupper()==True:
				"""Ici on compte ce pseudo mot comme véritable mot ssi soit il est dans le dictionnaire, soit s'il est un nom propre
				(dans ce cas il commence par une lettre majuscule)
				"""
				Mots.append(Phrase[m : i+1])
			if (i<l-1 and Phrase[i+1]=="'") and ((Phrase[m : i+1]+'i\n' in Dict_L) or (Phrase[m : i+1]+'e\n' in Dict_L)):
				"""Ici on compte ce pseudo mot comme véritable mot ssi il est un mot se terminant par l'apostrophe dont on a oté
				le 'e' ou 'i'. Ex: j' pour je; s' pour si"""
				Mots.append(Phrase[m : i+1] + "'")
	
	f = Phrase.lower().find("aujourd'hui")
	if lang == 'fr' and f != -1 and Phrase[f+11].isalpha() == False and (f == 0 or Phrase[f-1].isalpha() == False):
		"""Vu que la logique précédente va voir 'aujourd'hui' comme 'aujourd' et 'hui' qui ne sont pas dans le dictionnaire,
		alors 'aujourd'hui' ne sera pas compté comme mot d'ou la nécessité de le compter maintenant en se rassurant qu'il soit séparé du reste de la phrase par des blancs"""
		Mots.append("aujourd'hui")
 
	return Mots


if __name__ == "__main__":
	import gen_func
	print("'GenFunc' is a module full of general functions and objects, varied and very practical. Here are some detailed help:")      
	help(gen_func)
	input("Glad to have served you! Press 'Enter' to quit.")
