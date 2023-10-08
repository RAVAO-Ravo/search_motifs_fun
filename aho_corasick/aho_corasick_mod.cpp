#include <algorithm>
#include <deque>
#include <iostream>
#include <map>
#include <sstream>
#include <string>
#include <vector>

// Valeur du none
const int none = -99;

class ahocorasick {
public:
    // Structure d'un noeud du Trie
    struct TrieNode {
        char value;
        std::vector<int> next_nodes;
        int fail_state;
        std::vector<std::string> outputs;
        TrieNode(char v = '\0', int fail = 0) : value(v), fail_state(fail) {}
    };

    // Constructeur de la machine de recherche
    ahocorasick(std::vector<std::string> words) {
        // Initialiser la racine du Trie
        automaton.emplace_back('\0', 0);

        // Ajouter les mots au Trie
        adds(words);

        // Créer les liens echecs
        set_fail_transitions();
    }

    // Méthode pour ajouter un mot au Trie
    void add(const std::string& word) {
        std::string lowercaseWord = word;
        for (char& c : lowercaseWord) {
            c = std::tolower(c);
        }

        int current_node = 0;
        int pos = 0;
        int len_word = lowercaseWord.length();
        int next_node = nextNode(current_node, lowercaseWord[pos]);

        while (next_node != none) {
            current_node = next_node;
            pos++;

            if (pos < len_word) {
                next_node = nextNode(current_node, lowercaseWord[pos]);
            } else {
                break;
            }
        }

        for (int i = pos; i < len_word; ++i) {
            automaton.emplace_back(lowercaseWord[i], 0);
            automaton[current_node].next_nodes.push_back(automaton.size() - 1);
            current_node = automaton.size() - 1;
        }

        automaton[current_node].outputs.push_back(word);
    }

    // Méthode pour ajouter une liste de mots au Trie
    void adds(const std::vector<std::string>& words) {
        for (const std::string& word : words) {
            add(word);
        }
    }

    // Méthode pour créer les liens echecs
    void set_fail_transitions() {
        std::deque<int> q;
        int r = 0;

        for (int idNode : automaton[0].next_nodes) {
            q.push_back(idNode);
            automaton[idNode].fail_state = 0;
        }

        while (!q.empty()) {
            r = q.front();
            q.pop_front();

            for (int idNode : automaton[r].next_nodes) {
                q.push_back(idNode);
                int current_node = automaton[r].fail_state;

                while (nextNode(current_node, automaton[idNode].value) == none && current_node != 0) {
                    current_node = automaton[current_node].fail_state;
                }

                automaton[idNode].fail_state = nextNode(current_node, automaton[idNode].value);
                if (automaton[idNode].fail_state == none) {
                    automaton[idNode].fail_state = 0;
                }

                automaton[idNode].outputs.insert(
                    automaton[idNode].outputs.end(),
                    automaton[automaton[idNode].fail_state].outputs.begin(),
                    automaton[automaton[idNode].fail_state].outputs.end()
                );
            }
        }
    }

    // Méthode pour effectuer une recherche
    std::vector<std::pair<std::string, int>> search_all(const std::string& text) {
        std::string lowercaseText = text;
        for (char& c : lowercaseText) {
            c = std::tolower(c);
        }

        std::vector<std::pair<std::string, int>> results;
        int current_node = 0;

        for (long unsigned int pos = 0; pos < lowercaseText.length(); ++pos) {
            while (nextNode(current_node, lowercaseText[pos]) == none && current_node != 0) {
                current_node = automaton[current_node].fail_state;
            }

            current_node = nextNode(current_node, lowercaseText[pos]);

            if (current_node == none) {
                current_node = 0;
            } else {
                for (const std::string& word : automaton[current_node].outputs) {
                    results.emplace_back(word, pos - word.length() + 1);
                }
            }
        }

        return results;
    }

private:
    // Méthode pour récupérer l'index du noeud suivant
    int nextNode(int current_node, char value) {
        for (int id_node : automaton[current_node].next_nodes) {
            if (automaton[id_node].value == value) {
                return id_node;
            }
        }
        return none;
    }

    // L'automate de recherche
    std::vector<TrieNode> automaton;
};


int main(int argc, char* argv[]) {
    if (argc != 3) {
        std::cerr << "Usage: " << argv[0] << " <text> \"[mot1, mot2, mot3]\"" << std::endl;
        return 1;
    }

    std::string text = argv[1];
    std::string keywordsArg = argv[2];

    // Supprimer les guillemets extérieurs
    if (keywordsArg.size() >= 2 && keywordsArg.front() == '[' && keywordsArg.back() == ']') {
        keywordsArg = keywordsArg.substr(1, keywordsArg.size() - 2);
    } else {
        std::cerr << "Erreur: Les mots-clés doivent être entre crochets." << std::endl;
        return 1;
    }

    // Utiliser un flux de chaînes de caractères pour extraire les mots individuels
    std::vector<std::string> keywords;
    std::istringstream iss(keywordsArg);
    std::string keyword;

    while (std::getline(iss, keyword, ',')) {
        // Supprimer les espaces des mots-clés
        keyword.erase(std::remove_if(keyword.begin(), keyword.end(), ::isspace), keyword.end());
        keywords.push_back(keyword);
    }

    ahocorasick ac(keywords);

    std::vector<std::pair<std::string, int>> positions = ac.search_all(text);

    // Construire le dictionnaire de sortie
    std::map<std::string, std::vector<int>> resultDictionary;

    for (const std::pair<std::string, int>& entry : positions) {
        resultDictionary[entry.first].push_back(entry.second);
    }

    // Afficher le dictionnaire
    for (const auto& entry : resultDictionary) {
        std::cout << entry.first << " : [";
        for (size_t i = 0; i < entry.second.size(); ++i) {
            std::cout << entry.second[i];
            if (i < entry.second.size() - 1) {
                std::cout << ", ";
            }
        }
        std::cout << "]" << std::endl;
    }

    return 0;
}