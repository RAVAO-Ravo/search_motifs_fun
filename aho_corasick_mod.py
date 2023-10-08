#!/bin/python3
#-*- coding:utf-8 -*-

# python 3.8.10
# pandas : 1.4.3

import pandas as pd
import time as tm
import typing as tp
from choice_algo import ahocorasick_search


def aho_corasick(texte: str, motifs: tp.Union[tp.List[str], str]) -> tp.Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Effectue la recherche de motifs, à partir de l'algorithme Aho-Corasick, dans un texte, à partir d'un mot ou d'une liste de mots.

    Parameters
    ----------
    texte (str) : Texte dans lequel s'effectue la recherche.
    motifs (str/list[str]) : Motif(s) que l'on recherche dans le texte.

    Return
    ------
    Tuple[DataFrame, DataFrame]
        Retourne un tuple contenant la position des motifs dans le texte et le temps de recherche par motif.
    """

    # Si le motifs passé en paramètre est un string
    if isinstance(motifs, str):
        # Transformer le string en liste
        motifs = [motifs]

    # Effectue la recherche Aho-Corasick à partir de la liste et calcule le temps mis pour la recherche
    start = tm.perf_counter()
    df_res = ahocorasick_search(texte=texte, motifs=motifs)
    stop = tm.perf_counter()

    return (
        df_res,
        pd.DataFrame(data={"Time (in seconds)": [stop - start]}, index=["Total time"])
    )


if __name__ == "__main__":

	texte = "hello world world world, and universe universe"
	motifs = ["hello", "world", "universe"]

	df_res, time_it = aho_corasick(texte, motifs)

	print(df_res)
	print(time_it)