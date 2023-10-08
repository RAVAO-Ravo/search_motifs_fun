#include <iostream>
#include <vector>
#include <string>

/**
 * Recherche naïve d'un motif dans un texte.
 * 
 * @param texte: Le texte dans lequel effectuer la recherche.
 * @param motif: Le motif à rechercher dans le texte.
 * @return Un vecteur d'entiers contenant les positions du motif dans le texte.
 */
std::vector<int> naive_search(const std::string& texte, const std::string& motif) {
	std::vector<int> tab_pos;  // Initialise le vecteur pour stocker les positions.
	int len_texte = texte.length();  // Taille du texte.
	int len_motif = motif.length();  // Taille du motif.

	for (int i = 0; i < len_texte; ++i) {
		int match = 0;  // Compteur de correspondance.

		for (int j = 0; j < len_motif; ++j) {
			if (i + match < len_texte && texte[i + match] == motif[j]) {
				match++;  // Incrémente le compteur de correspondance.
			} else {
				break;  // Sort de la boucle si la correspondance est rompue.
			}
		}

		if (match == len_motif) {
			tab_pos.push_back(i + 1);  // Ajoute la position au vecteur.
		}
	}

	return tab_pos;  // Retourne le vecteur contenant les positions du motif.
}

int main(int argc, char* argv[]) {

	// Vérifier le bon usage de l'éxécutable
	if (argc != 3) {
		std::cerr << "Usage: " << argv[0] << " <texte> <motif>" << std::endl;
		return 1;
	}

	// Récupération des paramètres
	std::string texte(argv[1]);
	std::string motif(argv[2]);

	// Rechercher les mots
	std::vector<int> positions = naive_search(texte, motif);

	// Afficher les positions
    if (positions.empty()) {
        std::cout << "Aucune position trouvée pour le motif '" << motif << "' dans le texte." << std::endl;
    } else {
        for (int pos : positions) {
            std::cout << pos << ',';
        }
        std::cout << std::endl;
    }

	return 0;
}