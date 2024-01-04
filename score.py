from main import info_section1, what_happened_section1, info_section2, what_happened_section2, info_section3, what_happened_section3

import re

stollen_info_regex = [  r'phone number', r'email address', r'address', r'date of birth', r'social security number', 
                        r'name', r'drivers license', r'payment card', r'medical record', r'username', r'password', 
                        r'financial account', r'.*health insurance.*']

attack_vectors_regex = [    r'compromised\s*email', r'compromised\s*machine', r'data\s*found\s*publicly', r'exposed\s*data',
                            r'insider\s*theft', r'lost\s*computer\s*or\s*data', r'phishing\s*email', r'ransomware', 
                            r'social\s*engineering', r'software\s*vulnerability', r'software\s*bug', 
                            r'stolen\s*computer\s*or\s*data', r'stolen\s*credentials', r'unauthorized',
                            r'wrong\s*data\s*sent']

# Class to maintain a 'score' for eaach company (just keeps track of found data in documents)
class Score:
    def __init__(self, name):
        # Name of companys, and 2 sets to hold all found data (used sets for easy lookup/retrieval)
        self.name = name
        self.attackVectors = set()
        self.stolenInfo = set()

    # pdf_section -> string of paragraph text
    # vectors -> list of possible attack vectors to search pdf for
    # stollen_info -> list of possible stollen information options to search pdf for
    def get_attack_vector_score(self, pdf_section, vectors):
        for attack_vector in vectors:
            if re.search(attack_vector, pdf_section, re.IGNORECASE | re.DOTALL):
                self.attackVectors.add(attack_vector)
    
    def get_stolen_info_score(self, pdf_section, stollen_info):
        for info_pattern in stollen_info:
            if re.search(info_pattern, pdf_section, re.IGNORECASE | re.DOTALL):
                self.stolenInfo.add(info_pattern)       

    # Function to output sets of scores for company
    def print_scores(self):
        print('List of Attack Vectors:\n')
        for item in self.attackVectors:
            print(item)
        print('\nList of Stollen Information: \n')
        for item2 in self.stolenInfo:
            print(item2)
        print('========================')
        

# Example Usage
score1 = Score('first_sample')
score1.get_stolen_info_score(info_section1, stollen_info_regex)
score1.get_attack_vector_score(what_happened_section1, attack_vectors_regex)
print('Scores for Sample 1:\n')
score1.print_scores()

score2 = Score('second_sample')
score2.get_stolen_info_score(info_section2, stollen_info_regex)
score2.get_attack_vector_score(what_happened_section2, attack_vectors_regex)
print('\nScores for Sample2:\n')
score2.print_scores()

score3 = Score('third_sample')
score3.get_stolen_info_score(info_section3, stollen_info_regex)
score3.get_attack_vector_score(what_happened_section3, attack_vectors_regex)
print('\nScores for Sample 3:\n')
score3.print_scores()
