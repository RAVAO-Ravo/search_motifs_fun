# search_motifs_fun

Ce projet vous permet d'effectuer des recherches de motifs dans un texte à l'aide de différents algorithmes. Vous pouvez également calculer le temps moyen d'exécution de ces algorithmes.

## Installation

1. Assurez-vous d'avoir Python 3 installé sur votre système.

2. Clonez ce dépôt sur votre machine locale :

```shell
git clone https://github.com/RAVAO-Ravo/search_motifs_fun.git
```

3. Accédez au répertoire du projet :

```bash
cd search_motifs_fun
```

4. Installez les dépendances Python requises en utilisant pip :

```shell
pip3 install -r requirements.txt
```

## Utilisation

Le programme principal est `search_motif.py`. Vous pouvez l'exécuter depuis un terminal de commandes avec les options suivantes :

```shell
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

```shell
python3 search_motifs.py --texte texte.txt --motifs motifs.txt --algo kmp bm --n_iter 5 --printALGN
```

## Fichiers de test

Ce dépôt contient deux fichiers de test :

- `texte.txt` : un fichier texte généré aléatoirement pour tester les recherches de motifs.

- `motifs.txt` : un fichier contenant des motifs, formatés sous forme de motifs séparés par des virgules.

## Implémentation

Les algorithmes de recherche utilisés dans ce projet ont été implémentés en C++ pour une exécution rapide et efficace.

## Licence

Ce projet est sous licence Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0). Vous êtes libre de :

- Partager : copier et redistribuer le matériel sous quelque support que ce soit ou sous n'importe quel format.
- Adapter : remixer, transformer et créer à partir du matériel.

Selon les conditions suivantes :

- Attribution : Vous devez donner le crédit approprié, fournir un lien vers la licence et indiquer si des modifications ont été apportées. Vous devez le faire de la manière suggérée par l'auteur, mais pas d'une manière qui suggère qu'il vous soutient ou soutient votre utilisation du matériel.

- Utilisation non commerciale : Vous ne pouvez pas utiliser le matériel à des fins commerciales.

[![Logo CC BY-NC 4.0](https://licensebuttons.net/l/by-nc/4.0/88x31.png)](https://creativecommons.org/licenses/by-nc/4.0/)

[En savoir plus sur la licence CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/)

---

Profitez de la puissance de la recherche de motifs à l'aide de cet outil polyvalent. Si vous avez des questions ou des commentaires, n'hésitez pas à nous contacter.
