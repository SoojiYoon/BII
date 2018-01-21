umls_semantictype_file 	= './umls_data/umls_cui_semantictype'
umls_definition_file	= './umls_data/umls_cui_def'
seen_terms_file1	= './umls_data/bii_seen_terms_highconf'
seen_terms_file2	= './umls_data/bii_seen_terms'


cui_sty = {}
for row in open(umls_semantictype_file):
	cui, sty = row.strip().split('\t')
	cui_sty[cui] = sty


cui_def = {}
for row in open(umls_definition_file):
	cui, sty = row.strip().split('\t')
	cui_def[cui] = sty

	
seen_terms1 = set([])
for row in open(seen_terms_file1):
	if row.strip():
		seen_terms1.add(row.strip())



seen_terms2 = set([])
for row in open(seen_terms_file2):
	if row.strip():
		seen_terms2.add(row.strip())



