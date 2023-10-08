# search

Ce projet vous permet d'effectuer des recherches de motifs dans un texte à l'aide de différents algorithmes. Vous pouvez également calculer le temps moyen d'exécution de ces algorithmes.

## Installation

1. Assurez-vous d'avoir Python 3 installé sur votre système.

2. Clonez ce dépôt sur votre machine locale :

   ```bash
   git clone https://github.com/RAVAO-Ravo/search_motifs_fun.git
   ```

3. Accédez au répertoire du projet :

   ```bash
   cd search_motifs_fun
   ```

4. Installez les dépendances Python requises en utilisant pip :

   ```bash
   pip install -r requirements.txt
   ```

## Utilisation

Le programme principal est `search_motif.py`. Vous pouvez l'exécuter depuis un terminal de commandes avec les options suivantes :

```bash
python3 search_motifs.py --texte chemin/vers/votre_texte.txt --motifs chemin/vers/vos_motifs.txt --algo [naif, kmp, bm, aho, all] --n_iter N --printALGN
```

### Options

- `--texte` (`-t`) : Nom ou chemin du fichier texte à utiliser (obligatoire).

- `--motifs` (`-m`) : Nom ou chemin du fichier motifs à utiliser, formaté sous forme de motifs séparés par des virgules (obligatoire).

- `--algo` (`-a`) : Algorithme(s) à utiliser. Peut être unique ou multiple. Par défaut, tous les algorithmes sont utilisés. Choix disponibles : `naif`, `kmp`, `bm`, `aho`, `all`.

- `--n_iter` (`-n`) : Nombre d'itérations pour le calcul du temps d'exécution. Par défaut, 1.

- `--printALGN` (`-p`) : Affichage de l'alignement. Par défaut, désactivé.

### Exemple

Voici un exemple d'utilisation :

```bash
python3 search_motifs.py --texte texte.txt --motifs motifs.txt --algo kmp bm --n_iter 5 --printALGN
```

## Fichiers de test

Ce dépôt contient deux fichiers de test :

- `texte.txt` : un fichier texte généré aléatoirement pour tester les recherches de motifs.

- `motifs.txt` : un fichier contenant des motifs, formatés sous forme de motifs séparés par des virgules.

## Implémentation

Les algorithmes de recherche utilisés dans ce projet ont été implémentés en C++ pour une exécution rapide et efficace.

---

Profitez de la puissance de la recherche de motifs à l'aide de cet outil polyvalent. Si vous avez des questions ou des commentaires, n'hésitez pas à nous contacter.
