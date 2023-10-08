#!/bin/python3
#-*- coding:utf-8 -*-

# python 3.8.10
# pandas : 1.4.3

import pandas as pd
import time as tm
import typing as tp
from choice_algo import search


def naif(texte: str, motifs: tp.Union[tp.List[str], str]) -> tp.Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Effectue la recherche naïve de motifs dans un texte, à partir d'un mot ou d'une liste de mots.

    Parameters:
    -----------
    texte (str): Le texte dans lequel s'effectue la recherche.
    motifs (str/list[str]): Le(s) motif(s) à rechercher dans le texte.

    Returns:
    --------
    Tuple[pd.DataFrame, pd.DataFrame]: Un tuple contenant les positions des motifs dans le texte et le temps de recherche par motif.
    """
    # Si le motifs passé en paramètre est une chaîne de caractères, le transforme en liste
    if isinstance(motifs, str):
        motifs = [motifs]

    # Récupère la taille de la liste de motifs
    len_motifs = len(motifs)

    # Si la liste contient plus d'un motif
    if len_motifs != 1:
        # Divise la liste de motifs en deux parties et lance l'algorithme de recherche pour chaque partie
        mid = round(len_motifs / 2)
        gauche_res, time_gauche = naif(texte=texte, motifs=motifs[:mid])
        droite_res, time_droite = naif(texte=texte, motifs=motifs[mid:])
        
        # Fusionne les résultats et les temps de recherche obtenus par récursivité
        return (
            pd.concat(objs=[gauche_res, droite_res], axis=1),
            pd.concat(objs=[time_gauche, time_droite], axis=0)
        )
    else:
        # Si la liste contient un seul motifs, effectue la recherche naïve et mesure le temps de recherche
        start = tm.perf_counter()
        df_res = search(texte=texte, motif=motifs[0], algo="naif")
        stop = tm.perf_counter()

        # Retourne les résultats sous forme d'un tuple de dataframes
        return (
            df_res,
            pd.DataFrame(data={"Time (in seconds)": [stop - start]}, index=[motifs[0]])
        )


if __name__ == "__main__" :

	texte = "hello world world world, and universe universe"
	motifs = ["hello", "world", "universe"]
    
	df_res, time_it = naif(texte=texte, motifs=motifs)

	print(df_res)
	print(time_it)