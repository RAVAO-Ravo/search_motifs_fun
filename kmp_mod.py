#!/bin/python3
#-*- coding:utf-8 -*-

# python 3.8.10
# pandas : 1.4.3

import pandas as pd
import time as tm
import typing as tp
from choice_algo import search


def kmp(texte: str, motifs: tp.Union[tp.List[str], str]) -> tp.Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Effectue la recherche de motifs dans un texte en utilisant l'algorithme KMP.

    Parameters:
    -----------
    texte (str): Le texte dans lequel s'effectue la recherche.
    motifs (str/list[str]): Le(s) motif(s) à rechercher dans le texte.

    Returns:
    --------
    Tuple[pd.DataFrame, pd.DataFrame]: Un tuple contenant les positions des motifs dans le texte et le temps de recherche par motif.
    """
    # Si le motifs passé en paramètre est une chaîne de caractères
    if isinstance(motifs, str):
        # Transformer la chaîne en liste
        motifs = [motifs]

    # Récupérer la taille de la liste
    len_motifs = len(motifs)

    # Si la liste contient plus d'un élément
    if len_motifs != 1:
        # Lancer l'algorithme sur la partie gauche de la liste et la partie droite de la liste
        mid = round(len_motifs / 2)
        gauche_res, time_gauche = kmp(texte=texte, motifs=motifs[:mid])
        droite_res, time_droite = kmp(texte=texte, motifs=motifs[mid:])
        
        # Fusionner les dataframes obtenus par récursivité
        return (
            pd.concat(objs=[gauche_res, droite_res], axis=1),
            pd.concat(objs=[time_gauche, time_droite], axis=0)
        )

    # Si la liste contient un seul élément
    else:
        # Effectue la recherche KMP à partir d'un élément unique et calcule le temps mis pour la recherche
        start = tm.perf_counter()
        df_res = search(texte=texte, motif=motifs[0], algo="kmp")
        stop = tm.perf_counter()
        
        return (
            df_res,
            pd.DataFrame(data={"Time (in seconds)": [stop - start]}, index=[motifs[0]])
        )


if __name__ == "__main__" :

	texte = "hello world world world, and universe universe"
	motifs = ["hello", "world", "universe"]
    
	df_res, time_it = kmp(texte=texte, motifs=motifs)

	print(df_res)
	print(time_it)