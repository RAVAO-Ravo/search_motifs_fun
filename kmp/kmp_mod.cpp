#include <iostream>
#include <vector>
#include <string>

/**
 * Cette fonction calcule l'automate KMP pour un motif donné.
 * 
 * @param motif : Le motif pour lequel l'automate est calculé.
 * @return : Un vecteur contenant l'automate KMP.
 */
std::vector<int> automate_kmp(const std::string& motif) {
    int len_motif = motif.length();
    std::vector<int> automate(len_motif, -1); // Initialisation de l'automate avec des valeurs par défaut
    int i = 0;
    int j = 1;
    automate[i] = i;

    while (j < len_motif) {
        if (motif[i] == motif[j]) {
            automate[j] = i + 1;
            i++;
            j++;
        } else {
            if (i != 0) {
                i = automate[i - 1];
            } else {
                automate[j] = 0;
                j++;
            }
        }
    }

    return automate;
}

/**
 * Effectue une recherche KMP dans un texte donné à l'aide de l'automate KMP.
 * 
 * @param text : Le texte dans lequel la recherche est effectuée.
 * @param pattern : Le motif recherché.
 * @param kmp_automaton : L'automate KMP précalculé pour le motif.
 * @return Un vecteur d'entiers contenant les positions du motif dans le texte.
 */
std::vector<int> rech_kmp(const std::string& texte, const std::string& motif, const std::vector<int>& automate) {
    int n = texte.length();
    int m = motif.length();
    int i = 0;
    int j = 0;
    std::vector<int> tab_pos;

    while (i < n) {
        if (texte[i] == motif[j]) {
            i++;
            j++;
        } else {
            if (j != 0) {
                j = automate[j - 1];
            } else {
                i++;
            }
        }
        
        if (j == m) {
            tab_pos.push_back(i - j + 1);
            j = automate[j - 1];
        }
    }

    return tab_pos;
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
    std::vector<int> automate = automate_kmp(motif); // Calcul de l'automate KMP
    std::vector<int> positions = rech_kmp(texte, motif, automate); // Recherche KMP

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