import json
import random
import re
import pycantonese

reg = re.compile(r'[a-zA-Z]')

# read corpus
hkcancor = pycantonese.hkcancor()
tagged_sents = hkcancor.tokens(by_utterances=True)
examples = []
for tagged_sent in tagged_sents:
    # create lines
    sent = []
    words = []
    ners = []    
    was_eng = False
    for token in tagged_sent:
        this_word = token.word
        if len(this_word) > 1 and reg.match(this_word):
            if was_eng:
                sent += [' ']
                word = [' ']
                ner = ["B"]
                words.extend(word)
                ners.extend(ner) 
            
        if len(this_word) > 1 and (reg.match(this_word[-1:]) or reg.match(this_word[-2:])):
            was_eng = True                       
        else:                        
            was_eng = False           
        sent += [this_word]        
        word = [*this_word]
        ner = ["B"]
        if len(word) > 1:
            ner2 = ["I"] * (len(word)-1)
            ner.extend(ner2)
        words.extend(word)
        ners.extend(ner)       
        
    examples.append({"words":words, "ner": ners})

random.shuffle(examples)
with open('data/finetune_hkcancor.json', 'w') as train_outfile:
    for entry in examples:
        json.dump(entry, train_outfile, ensure_ascii=False)
        train_outfile.write('\n')
