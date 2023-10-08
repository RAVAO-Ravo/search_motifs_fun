#!/bin/python3
#-*- coding:utf-8 -*-

import argparse
import pandas as pd
import re
import typing as tp
from aho_corasick_mod import aho_corasick
from bm_mod import bm
from kmp_mod import kmp
from naif_mod import naif
from statistics import mean


def lecture_fichier(name: str, bool_motif: bool=False) -> tp.Union[str, tp.List[str]] :
	"""
	Fonction : ``lecture_fichier``
	--------

		Permet la lecture d'un fichier.

	Paramètres
	----------

	* ``name`` : Str

		Nom du fichier à lire.

	* ``bool_motif`` : Bool

		Valeur booléanne indiquant s'il s'agit d'un fichier texte ou d'un fichier motif.

	Return
	------

	* ``Str/List[Str]`` :

		Retourne soit un string, s'il s'agit d'un fichier texte, soit une liste de string, s'il s'agit d'un fichier motif.

	"""

	# Initialiser la variable de retour
	texte = ""

	# Ouvrir le fichier
	with open(file=name, mode="r") as file:

		# Récupérer les lignes du fichier
		lines = file.readlines()

		# Pour toute les lignes du fichiers
		for line in lines:

			# Ajouter les lignes à la variable de retour
			texte+=line

	# S'il s'agit d'un fichier texte
	if bool_motif == False :

		# retourner simplement le texte
		return texte

	# S'il s'agit d'un fichier motif
	else:

		# Supprimmer les espaces et les tablulations
		texte = re.sub(r"\n+", "", texte)
		texte = re.sub(r"\t+", "", texte)
		texte = re.sub(r"^\s+", "", texte)
		texte = re.sub(r" ", "", texte)

		# Retourner un liste de string dont le séparateur est la virgule
		return texte.split(sep=",")


def rech_motifs(texte: str, motifs: tp.Union[tp.List[str], str], algo: str) -> tp.Tuple[pd.DataFrame, pd.DataFrame] :
	"""
	Fonction : ``rech_motifs``
	--------
		Permet la recherche de motif(s) dans un texte, en fonction d'un algorithme de recherche.

	Paramètres
	----------

	* ``texte`` : Str

		Texte dans lequel s'effectue la recherche.

	* ``motifs`` : List[str]/Str

		Liste des motifs que l'on recherche dans le texte.
	
	* ``algo`` : Str

		Nom de l'algorithme de recherche à utiliser.

	Return
	------

	* ``Tuple[DataFrame, DataFrame]`` :

		Retourne un tuple contenant la position des motifs dans le texte et le temps de recherche par motifs.

	"""

	if algo == "bm" :
		return bm(texte=texte, motifs=motifs)

	elif algo == "naif" :
		return naif(texte=texte, motifs=motifs)

	elif algo == "kmp" :
		return kmp(texte=texte, motifs=motifs)

	elif algo == "aho" :
		return aho_corasick(texte=texte, motifs=motifs)

	else :
		raise ValueError("Only : ['bm', 'naif', 'kmp', 'aho'] are acceptable values.")


def mean_perf(func: callable, n: int=100) -> float:
	"""
	Fonction : ``mean_perf``
	--------

		Calcule le temps moyen d'execution d'une fonction de recherche de motif(s).

	Paramètres
	----------

	* ``func`` : Callable

		Fonction de recherche devant renvoyer un ``Tuple[DataFrame, DataFrame]``.

	* ``n`` : Int, défaut=100

		Nombre d'éxecutions de la fonction, pour calculer le temps moyen.	

	Return
	------

	* ``Float`` :

		Retourne le temps moyen d'exécution d'une fonction.

	"""

	# Initialiser la liste qui contiendra les temps d'exécution
	tab_time = [-1]*n

	# Pour le nombre d'exécutions souhaité
	for i in range(0, n, 1):

		# Exécuter la fonction de recherche de motif(s)
		df_res, time_it = func

		# Récupérer le temps d'exécution, et l'ajouter dans la liste
		tab_time[i] = time_it.iloc[:, 0].sum()

	return mean(tab_time)


def fusion_algn(f_word: str, s_word: str) -> str :
	"""
	Fonction : ``fusion_algn``
	--------

		Permet la fusion de deux alignements de même longueur (= deux motifs alignés sur le même texte).

	Paramètres
	----------

	* ``f_word`` : Str

		Le premier mot.

	* ``s_word`` : Str

		Le second mot.	

	Return
	------

	* ``Str`` :

		Retourne une fusion des deux alignements passés en paramètres.

	"""

	# Si les deux alignements ne sont pas de même longueur
	if len(f_word) != len(s_word):

		# Renvoyer une erreur
		raise ValueError("les deux mots doivent avoir la même longueur.")

	# Sinon
	else:

		# Fusionner les deux alignements
		algn = ""

		for i in range(0, len(f_word), 1):

			if f_word[i] != '-' :
				algn+=f_word[i]

			elif s_word[i] != '-' :
				algn+=s_word[i]

			else:
				algn+='-'

		return algn


def align_motifs(texte: str, pos: pd.DataFrame) -> str :
	"""
	Fonction : ``align_motifs``
	--------

		Permet d'obtenir l'alignement de motifs sur un texte, à partir d'un dataframe de positions des motifs dans le texte.

	Paramètres
	----------

	* ``texte`` : Str

		Le texte sur lequel doit être aligner les motifs.

	* ``pos`` : DataFrame

		Dataframe dont les colonnes sont les motifs, et les lignes les positions (des motifs) dans le texte.	

	Return
	------

	* ``Str`` :

		Retourne l'alignement de motifs, sur un texte.

	"""

	# Récupérer le nombre de colonnes du dataframe
	n_col = pos.shape[1]

	# S'il y a plus d'une colonne
	if n_col != 1:

		# Effectuer l'algorithme récusivement jusqu'obtenir une colonne
		mid = round(n_col/2)
		gauche = align_motifs(texte, pos.iloc[:, :mid])
		droite = align_motifs(texte, pos.iloc[:, mid:])

		# Fusionner tout les alignements obtenus
		return fusion_algn(gauche, droite)
	
	# Sinon
	else : 

		# Récupérer le motifs (le nom de la colonne)
		motifs = str(pos.columns[0])

		# Initialiser l'alignemnt résultat
		algn = ""

		# Initiliser l'itérateur de parcours i, et la longueur du motifs
		i = 0
		len_motifs = len(motifs)

		# Transformer le dataframe en une liste
		tab_pos = pos.iloc[:, 0].values.tolist()

		# Tant que l'on n'a pas parcouru tout le texte
		while len(algn) != len(texte):

			# Vérifier si la position actuelle correspond à une occurence du motifs
			if i+1 in tab_pos :

				# Ajouter le mot à l'alignement, et incrémenter l'itérateur de parcours
				algn+=motifs
				i+=len_motifs

			# Sinon
			else:

				# Continuer le parcours du texte
				algn+='-'
				i+=1
	
		return algn


def affiche_alignement(texte: str, pos: pd.DataFrame) -> str :
	"""
	Fonction : ``affiche_alignement``
	--------

		Permet l'alignement de motifs sur un texte, à partir d'un dataframe de positions des motifs dans le texte.

	Paramètres
	----------

	* ``texte`` : Str

		Le texte sur lequel doit être aligner les motifs.

	* ``pos`` : DataFrame

		Dataframe dont les colonnes sont les motifs, et les lignes les positions (des motifs) dans le texte.	

	Return
	------

	* ``Str`` :

		Retourne un alignement de motifs, sur un texte.

	"""

	# Récupérer l'alignement fusionné, des alignements des différents motifs
	algn = align_motifs(texte=texte, pos=pos)

	# Retourner l'alignement par rapport au texte
	return texte+'\n'+algn


if __name__ == "__main__" :

	# Créer un objet ArgumentParser
	parser = argparse.ArgumentParser(description='Effectue de la recherche de motifs dans un texte, à l\'aide de différents algorithmes.')

	# Ajouter les arguments
	parser.add_argument('--texte', '-t', required=True, help='Nom ou chemin du fichier à utiliser (argument obligatoire).', type=str)
	parser.add_argument('--motifs', '-m', required=True, help='Nom ou chemin du fichier à utiliser, formaté sous forme de motifs séparés par des virgules (argument obligatoire).', type=str)
	parser.add_argument('--algo', '-a', nargs='+', default=['all'], choices=['naif', 'kmp', 'bm', 'aho', 'all'], help='Algorithme(s) à utiliser. Peut être unique ou multiple. Par défaut, tous les algorithmes sont utilisés.', type=str)
	parser.add_argument('--n_iter', '-n', default=1, help='Nombre d\'itérations pour le calcul du temps d\'exécution. Par défaut, 1.', type=int)
	parser.add_argument('--printALGN', '-p', action='store_true', help='Affichage de l\'alignement. Par défaut, désactivé.')

	# Analyser les arguments de la ligne de commande
	args = parser.parse_args()

	# Accéder aux valeurs des arguments
	texte : str = args.texte
	motifs : str = args.motifs
	algo: str = args.algo
	n_iter : int = args.n_iter
	printALGN : bool = args.printALGN

	# Afficher les valeurs des arguments (pour vérification)
	print(f"Texte : {texte}")
	print(f"Motifs : {motifs}")
	print(f"Algorithmes : {algo}")
	print(f"Nombre d'itérations : {n_iter}")
	print(f"Affichage de l'alignement : {printALGN}")

	# Lecture des fichier
	texte = lecture_fichier(name=texte, bool_motif=False)
	motifs = lecture_fichier(name=motifs, bool_motif=True)

	# Utilisation des algorithmes
	for a in algo:
		print(f"Time {a} : {mean_perf(func=rech_motifs(texte=texte, motifs=motifs, algo=a), n=n_iter):.5f} s")

	# Affichage de l'alignement
	pos, time_naif = rech_motifs(texte=texte, motifs=motifs, algo="aho")
	pos = pos.fillna(value=-1)
	pos = pos.astype(dtype=int)
	pos.index = [i+1 for i in pos.index]
	print(f"\nDataframe des positions :\n\n{pos}\n")
	if printALGN == True:
		print(affiche_alignement(texte=texte, pos=pos))