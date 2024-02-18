from lexInterface import WeightedLexicon, loadWeightedLexiconFromSparse, loadLexiconFromSparse

#weighted - MySQL
lexicon = loadWeightedLexiconFromSparse("unweighted.csv")
print(lexicon.keys())
lexicon = WeightedLexicon(weightedLexicon=lexicon)
lexicon.createLexiconTable("unweighted")

"""
#weighted - SQLite
lexicon = loadWeightedLexiconFromSparse("weighted.csv")
lexicon = WeightedLexicon(weightedLexicon=lexicon, lexicon_db="dlatk_lexica", lex_db_type="sqlite")
lexicon.createLexiconTable("weighted")

#unweighted - MySQL
lexicon = loadLexiconFromSparse("unweighted.csv")
print(lexicon.keys())
lexicon = WeightedLexicon(lex=lexicon)
lexicon.createLexiconTable("unweighted")

#unweighted - SQLite
lexicon = loadLexiconFromSparse("unweighted.csv")
lexicon = WeightedLexicon(lex=lexicon, lexicon_db="dlatk_lexica", lex_db_type="sqlite")
lexicon.createLexiconTable("unweighted")
"""
