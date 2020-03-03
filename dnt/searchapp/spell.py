import re, collections,os

def tolower(text):   
    #will match any lowercase 
    pattern =  '[a-z]+'  

    # searching pattern 
    return re.findall(pattern,text.lower())


def prior(cwords):  
    #creat any terms that we can try to access
    model = collections.defaultdict(lambda:1)
    for f in cwords:
        model[f]+=1
    return model

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
ipath = os.path.join(__location__, 'dict.txt')  #name of the medicine name

htxt = open(ipath,'r')  # read the file 

cwords = tolower(htxt.read())


nwords = prior(cwords)  # nowrds


alpha = 'abcdefghijklmnopqrstuvwxyz'  # 26 letters used when try to add or delete one or two letter from the word


def version1(word):  

    n = len(word) #get the length of the name
    # if we can a one letter in the word from a-z at any position
    add_a_char = [word[0:i] + c + word[i:] for i in range(n+1) for c in alpha]
    # if we delete one any chat at any position
    delete_a_char = [word[0:i] + word[i+1:] for i in range(n)]
    #If we revise one char
    revise_a_char = [word[0:i] + c + word[i+1:] for i in range(n) for c in alpha]
    #if we swap any two chars 
    swap_adjacent_two_chars = [word[0:i] + word[i+1]+ word[i]+ word[i+2:] for i in range(n-1)] 
    # Return all different possible solution
    return set( add_a_char + delete_a_char +
               revise_a_char +  swap_adjacent_two_chars)


def version2(word):  
    # we do exactly same thing we did in version1 but with edit distance 2 instead
    return set(e2 for e1 in version1(word) for e2 in version1(e1))



def identify(words):  
    #if we finf the word
    return set(w for w in words if w in nwords)



def bayesClassifier(word):

    #We need to run different methids: 
    # 1. When the word is match the word in the database
    # 2. When the edit distance is 1
    # 3. When the edit distance is 2
    # 4. When nothing can be found from the database

    candidates=identify([word])or identify(version1(word)) or identify(version2(word)) or [word]
    #return the most closest possible solution
    return max(candidates,key=lambda w:nwords[w])



