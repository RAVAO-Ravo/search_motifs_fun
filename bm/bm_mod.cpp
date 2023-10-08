#include <iostream>
#include <string>
#include <vector>
#include <unordered_map>

/**
 * Construit l'automate BM pour un motif donné.
 * 
 * @param pattern: Le motif dont on souhaite construire l'automate BM.
 * @return Un dictionnaire (unordered_map) représentant l'automate BM.
 */
std::unordered_map<char, int> build_bm_automaton(const std::string& pattern) {
    int m = pattern.length();
    std::unordered_map<char, int> bm_automaton;

    for (int i = 0; i < m - 1; ++i) {
        // Distance de décalage pour chaque caractère du motif
        bm_automaton[pattern[i]] = m - i - 1;
    }

    return bm_automaton;
}

/**
 * Effectue une recherche de motif dans un texte à l'aide de l'automate BM.
 * 
 * @param text: Le texte dans lequel effectuer la recherche.
 * @param pattern: Le motif à rechercher dans le texte.
 * @param bm_automaton: L'automate BM préalablement construit pour le motif.
 * @return Un vecteur d'entiers contenant les positions du motif dans le texte.
 */
std::vector<int> search_bm(const std::string& text, const std::string& pattern, const std::unordered_map<char, int>& bm_automaton) {
    int n = text.length();
    int m = pattern.length();
    std::vector<int> positions;

    int pos = 0;
    while (pos <= n - m) {
        int i = m - 1;
        while (i >= 0 && text[pos + i] == pattern[i]) {
            i--;
        }

        if (i == -1) {
            // Correspondance trouvée, ajouter la position à la liste
            positions.push_back(pos + 1);
        }

        // Déplacement en utilisant l'automate BM
        if (bm_automaton.find(text[pos + m - 1]) != bm_automaton.end()) {
            pos += bm_automaton.at(text[pos + m - 1]);
        } else {
            pos += m;
        }
    }

    return positions;
}

int main(int argc, char* argv[]) {

    // Vérifier le bon usage de l'éxécutable
    if (argc != 3) {
        std::cerr << "Usage: " << argv[0] << " <texte> <motif>" << std::endl;
        return 1;
    }

    // Récupération des paramètres
    std::string text(argv[1]);
    std::string pattern(argv[2]);

    // Rechercher les mots
    std::unordered_map<char, int> bm_automaton = build_bm_automaton(pattern); // Calcul de l'automate BM
    std::vector<int> positions = search_bm(text, pattern, bm_automaton); // Recherche BM

    // Afficher les positions
    if (positions.empty()) {
        std::cout << "Aucune position trouvée pour le motif '" << pattern << "' dans le texte." << std::endl;
    } else {
        for (int pos : positions) {
            std::cout << pos << ',';
        }
        std::cout << std::endl;
    }

    return 0;
}