# /usr/bin/python
# -*- coding: utf-8 -*-

# before running
# sudo ../public_mm/bin/skrmedpostctl start


# environments for Tagger and Metamap
import geniatagger
from pymetamap import MetaMap

geniatagger_path = '../geniatagger-3.0.2/geniatagger'
mm = MetaMap.get_instance('../public_mm/bin/metamap16')
tagger = geniatagger.GeniaTagger(geniatagger_path)


# Loading sample mri text
import bii_sample_text
test_input = bii_sample_text.sample_mri


# UMLS information loading to memory
import bii_umls_load
umls_cui_sty_dict = bii_umls_load.cui_sty
print 'loading umls sty.....', 'done.\n'

umls_cui_def_dict = bii_umls_load.cui_def
print 'loading umls def.....', 'done.\n'

seen_terms1 = bii_umls_load.seen_terms1
seen_terms2 = bii_umls_load.seen_terms2
print 'loading umls atoms.....', 'done.\n'



def getValue(_key, _dict):
    try:
        return  _dict[_key]
    except KeyError:
        return None
        
def main(paragraph):
	np_list = []
    	np_list_mine = []
    	corresponding_sentence = []
    	corresponding_sentence_mine = []
    	sentence_mgr = []

	# parsing the input text with geniatagger
    	for input_sentence in paragraph.splitlines():
        	sentence_mgr.append(input_sentence)
        	parsed_rlt = tagger.parse(input_sentence)

		# mines
        	for e in seen_terms1 or e in seen_terms2:
            		if e in input_sentence and len(e)>2:
                		np_list_mine.append(e)
               	 		corresponding_sentence_mine.append(input_sentence)
        
        	begin_tag   = 'B-NP'
        	inside_tag  = 'I-NP'
        	np_phrase = ''

		
		for (word, base, POStag, chunktag, NEtag) in parsed_rlt:
            		if chunktag == begin_tag:
               		 	if len(np_phrase)>0:
                    			np_list.append(np_phrase)
                    			corresponding_sentence.append(input_sentence)
                    
                		np_phrase = word
            		elif chunktag == inside_tag:
				np_phrase = np_phrase + ' ' + word

                np_phrase = np_phrase + ' ' + word

	# printing parsed terms to the GUI
    	for row_idx, sen_value in enumerate(sentence_mgr, 1):

		for np_token, target_sen in zip(np_list, corresponding_sentence):
            		if target_sen == sen_value:
                		np_token_start_idx = sen_value.index(np_token)
                		np_token_end_idx = sen_value.index(np_token)+len(np_token)

                		highlight_begin_idx = str(row_idx) + '.' + str(np_token_start_idx)
                		highlight_end_idx = str(row_idx) + '.' + str(np_token_end_idx)

                		print np_token, highlight_begin_idx, highlight_end_idx
		for np_token, target_sen in zip(np_list_mine, corresponding_sentence_mine):
            		if target_sen == sen_value:
                		print np_token
                		try:
                    			np_token_start_idx = sen_value.index(np_token)
                    			np_token_end_idx = sen_value.index(np_token)+len(np_token)
                		except ValueError:
                    			continue
                
                		highlight_begin_idx = str(row_idx) + '.' + str(np_token_start_idx)
                		highlight_end_idx = str(row_idx) + '.' + str(np_token_end_idx)

                		print np_token, highlight_begin_idx, highlight_end_idx

	# Details from MetaMap
	for c, value in enumerate(np_list, 1):
		print '-'*80
		print value
        	concepts,error = mm.extract_concepts([value])
        	for concept_rlt in concepts:
            		print '<Preferred Entity>: ' + concept_rlt.preferred_name

            		if getValue(concept_rlt.cui, umls_cui_sty_dict) != None:
                		print '<ABC Class>: ' + umls_cui_sty_dict[concept_rlt.cui] 

if __name__ == "__main__":

    main(test_input)
