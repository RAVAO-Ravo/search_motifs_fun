CXX = g++   # Le compilateur C++
CXXFLAGS = -std=c++11 -Wall -Werror -Wextra -O3  # Les options du compilateur

# Les fichiers sources et les exécutables
SOURCES = ./aho_corasick/aho_corasick_mod.cpp ./bm/bm_mod.cpp ./kmp/kmp_mod.cpp ./naif/naif_mod.cpp
EXECUTABLES = ./aho_corasick/aho_corasick_search ./bm/bm_search ./kmp/kmp_search ./naif/naif_search

all: $(EXECUTABLES)

# Compile les fichiers source en exécutables
$(EXECUTABLES): $(SOURCES)
	$(CXX) $(CXXFLAGS) -o $@ $(@:_search=)_mod.cpp

clean:
	rm -f $(EXECUTABLES)

.PHONY: all clean