#!/bin/python3
#-*- coding:utf-8 -*-

# python 3.8.10
# pandas : 1.4.3

import numpy as np
import pandas as pd
import subprocess
import re


def search(texte: str, motif: str, algo: str="naif") -> pd.DataFrame:
    """
    Effectue une recherche d'un motif dans un texte, en spécifiant un algorithme.

    Parameters:
    -----------
    texte (str): Le texte dans lequel s'effectue la recherche.
    motif (str): Le motif à rechercher dans le texte.
    algo (str): Algorithme à utiliser.

    Returns:
    --------
    pd.DataFrame: Un DataFrame contenant les positions du motif dans le texte.
    """
    # Choix de l'algorithme à utiliser
    if algo == "naif":
        executable = "./naif/naif_search"
    elif algo == "kmp":
        executable = "./kmp/kmp_search"
    elif algo == "bm":
        executable = "./bm/bm_search"

    # Exécute le programme C++ de recherche en tant que processus
    result = subprocess.run([executable, texte, str(motif)], capture_output=True, text=True)
    
    # Récupère la sortie du processus, qui est une chaîne de positions séparées par des virgules
    positions_str = result.stdout.strip()
    
    # Si des positions ont été trouvées, les convertit en une liste d'entiers
    if positions_str:
        positions = [int(pos) for pos in positions_str.split(',') if pos != '']
    else:
        positions = []
    
    # Crée un DataFrame à partir de la liste de positions
    return pd.DataFrame(data={motif: positions})


def ahocorasick_search(texte: str, motifs: list) -> pd.DataFrame:
    """
    Effectue la recherche de motifs dans un texte en utilisant l'algorithme Aho-Corasick.

    Parameters:
    -----------
    texte (str): Le texte dans lequel s'effectue la recherche.
    motifs (list): La liste des motifs à rechercher dans le texte.

    Returns:
    --------
    pd.DataFrame: Un DataFrame contenant les positions des motifs dans le texte.
    """
    # Formater la liste de motifs pour la ligne de commande C++
    motifs_str = "[" + ", ".join(motifs) + "]"

    # Appeler le programme C++
    command = ["./aho_corasick/aho_corasick_search", texte, motifs_str]
    output = subprocess.check_output(args=command, text=True, stderr=subprocess.PIPE)

    # Analyser la sortie du programme C++ pour extraire le dictionnaire
    result_dict = {}
    matches = re.findall(r'(\w+) : \[([\d, ]*)\]', output)
    for match in matches:
        motif, positions = match
        positions = [int(pos) + 1 for pos in positions.split(", ") if pos]
        result_dict[motif] = positions

    # Trouver la longueur maximale parmi toutes les listes
    max_length = max(len(lst) for lst in result_dict.values())

    # Remplir les listes avec des NaN pour qu'elles aient la même longueur
    for key in result_dict:
        result_dict[key] += [np.nan] * (max_length - len(result_dict[key]))

    # Convertir le dictionnaire en DataFrame
    return pd.DataFrame(data=result_dict)