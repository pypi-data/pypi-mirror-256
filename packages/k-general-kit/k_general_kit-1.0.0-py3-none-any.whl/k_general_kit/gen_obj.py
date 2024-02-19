#!/usr/bin/env python3
# -*-coding:UTF-8 -*
from math import factorial

real = int|float
Real = {int, float}

def aid():
    """Affiche l'aide integral du module Obj"""
    import gen_obj
    print("Obj est un module comportant une multitude d'outils et objets pouvant s'avérer utiles très souvent.\nEn voici une aide plus précise :\n") 
    help(gen_obj)

def exm(p = 18):
    """Renvoie la valeur de la constante mathematique e avec une precision p"""
    i = 2
    e = 2     

    while i < p:
        e += 1/factorial(i)
        i += 1

    return e

def orm(p = 39):
    """Renvoie la valeur du nombre d'or avec une precision p1 avec p2 chiffres décimaux"""
    F = [1, 1]
    
    for i in range(0, p):
        F.append(F[0] + F[1])
        del F[0]
          
    return F[1] / F[0]

def pim(p = 11):
    """Renvoie la valeur de la constante mathematique pi avec une precision p"""
    i = 0
    pi = 0

    while i < p:
        j = 2*i+1
        pi += (((-1)**i)/j)*(4/(5**j)-1/(239**j))
        i += 1

    return 4*pi

exposant_unicode = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")
FrCharFreq = {'e':0.12, 'a':0.0711, 'i':0.0659, 's':0.0651, 'n':0.0639, 'r':0.0607, 't':0.0592, '0':0.0502, 'l':0.0496, 'u':0.0449, 'd':0.0367, 'c':0.0318, 'm':0.0262, 'p':0.0249, 'é':0.0194, 'g':0.0123, 'b':0.0114, 'v':0.0111, 'h':0.0111, 'q':0.0065, 'y':00.046, 'x':0.0038, 'j':0.0034, 'è':0.0031, 'à':0.0031, 'k':0.0029, 'w':0.0017, 'z':0.0015, 'ê':0.0008, 'ç':0.0006, 'ô':0.0004, 'â':0.0003, 'î':0.0003, 'û':0.0002, 'ù':0.0002, 'ï':0.0001, 'ü':0.0001, 'ë':0.0001, 'ö':0.0001} #In %
Acc = ["é", "à", "è", "ù", "@", "ê", "î", "â", "û", "ô", "&", "ç", "ä", "ë", "ï", "ö", "ü"]
Chi = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"] 
Maj = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
Min = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
Ponc = [".", ";", ",", "?", "!", "...", ":", "-", "\"", "'", "(", ")", "[", "]", "{", "}"]
Sym = [".", "!", "?", ":", ";", "/", "-", "+", "=", "%", "#", "{", "}", "(", ")", "[", "]", "\\", "|", "<", ">"]
ex = exm()
no = orm()
pi = pim()

if __name__ == "__main__":
    aid()
    input("Glad to have served you! Press 'Enter' to quit.")
