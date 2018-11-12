#Path: /Users/nayana/Desktop/College/3rdSem/DSC/SelfStudy

#Import modules

import dict
import time
import os
import sys

try:
    # Python 2
    from future_builtins import filter
except ImportError:
    # Python 3
    pass
    
try:
    #Python 2
    from itertools import imap,izip
except ImportError:
    # Python 3
    imap=map
    izip=zip
    
#Program     

class BKTree:
    def __init__(self, distancefunction,words,definitions):
        
        '''
        Creates a BK-tree using Levenshtein distance and the given word and definition lists.
        Parameters:
        distancefunction: Returns the Levenshtein distance between two words
        words: An iterable which produces words that can be passed to the distance function
        '''
        
        self.distancefunction = distancefunction
        
        #Declare iterators it over the given list of words and definitions
        it_word = iter(words)
        it_def = iter(definitions)
        root_word = next(it_word)
        root_def = next(it_def)
        
        #Initialize the tree to root and empty dictionary representing children
        self.tree = (root_word, root_def, {})
        
        #Call add_word for each word in the list to create the tree
        for i,j in izip(it_word,it_def):
            #node = Node()
            self.add_word(self.tree,i,j)
         
        print("The BK-tree has been created.\n")

    def add_word(self, parent, word, definition):
        parent_word,_,children = parent #Parent associated with a word, definition and a list of children
        
        #Calculate the distance of the given word from the parent word
        d = self.distancefunction(word, parent_word)
        
        #If there is a child node of the calculated distance, then recursively call add_word for that subtree. Otherwise add a new child node to the parent node.
        if d in children:
            self.add_word(children[d], word, definition)
        else:
            children[d] = (word, definition, {})

    def query_util(self,parent,word,n):
        
        parent_word,definition,children = parent
        
        #Calculate the distance of the given word from the parent word
        d = self.distancefunction(word, parent_word)
        
        results = []
        
        #If distance is less than n, add the word to the results
        if d <= n:
            results.append((d, parent_word,definition))
        
        #Recursively iterate over subtrees    
        for i in range(d-n, d+n+1): #from d-n to d+n

            child = children.get(i)
            
            #If the child exists, extend the list 'results' with the words found in the child subtrees
            if child is not None:
               results.extend(self.query_util(child,word,n))
                
        return results
    
    def query(self, word, n):
        
        '''
        This function returns the words in the tree which are at a distance <=n from the given word.  
        Parameters:
        word: The word to be queried for
        n: A non-negative integer that specifies the allowed distance from the query word.  
        It return a list of tuples (distance, word, definition) sorted in ascending order of distance.
        '''

        # sort by distance
        return sorted(self.query_util(self.tree,word,n))
       
        
def brute_query(word, words, distancefunction, n):
    
    '''
    This function is a brute force distance query, for the purpose of evaluating performance.
    Parameters:
    word: the word to be queried for
    words: An iterable which produces words
    distancefunction: Returns the Levenshtein distance between 'word' and another word in 'words'
    n: A non-negative integer that specifies the allowed distance from the query word
    '''
    
    return [i for i in words
            if distancefunction(i, word) <= n]

def levenshtein(string1, string2):
    
    #Iterative with full matrix implementation
    #Based on Wagner-Fischer Algorithm
    
    m, n = len(string1), len(string2)
    d = [range(n+1)]
    d += [[i] for i in range(1,m+1)]
    for i in range(0,m):
        for j in range(0,n):
            cost = 1
            if string1[i] == string2[j]: cost = 0

            d[i+1].append( min(d[i][j+1]+1, #deletion
                               d[i+1][j]+1, #insertion
                               d[i][j]+cost) #substitution
                           )
            #if i>0 and j>0 and string1[i]==string2[j-1] and string1[i-1]==string2[j]:
               #d[i+1].append( min((d[i+1][j+1], d[i-1][j-1] + cost)) ) #transposition
    return d[m][n]

def timeof(fn, *args):
   
    start = time.time()
    res = fn(*args)
    end = time.time()
    print ("Time in seconds:", (end - start))
    return res
    
def maxdepth(tree, count=0):
    _,_, children = tree
    if len(children):
        return max(maxdepth(i, count+1) for i in children.values())
    else:
        return count

if __name__ == "__main__":
   
    wordlist = []
    defintionlist = []
    
    wordlist, definitionlist = dict.load_dict()
    
    print("Creating BK-tree...\n")
    dict_tree = timeof(BKTree,levenshtein,filter(len,wordlist),filter(len,definitionlist))
    print("Size of dictionary: "+str(len(wordlist))+"\n")
    
    while(1):
       
       print("DICTIONARY USING BK-TREES\n")
       print("1: Insert a new word into the dictionary")
       print("2: Look up a word in the dictionary")
       print("3: Check whether the spelling of a given word is correct")
       print("4: Compare searches by brute query and Levenshtein distance-based query")
       print("5: Depth")
       print("6: Exit\n")
       
       try:
          x = int(input())
          
       except:       
          print("Enter a valid choice")
          continue
          
       if x==1:
          
          print("Enter the word to be added:")
          wd = str(input())
          
          print("Enter the definition of the word:")
          defn = str(input())
          
          search_res = dict_tree.query(wd, 0)
          if not search_res:
             dict_tree.add_word(dict_tree.tree,wd,defn)
             dict.add_dict(wd,defn)
          else:
             print("This word aleady exists in the dictionary.")
          
       elif x==2:
          
          print("Enter the word to look up")
          wd = str(input())
          
          search_res = dict_tree.query(wd, 0)
          
          if not search_res:
             print("No match found!")
             
          else:
             print(search_res[0][1]+" : "+search_res[0][2])
             
       elif x==3:
          
          print("Enter the word")
          wd = str(input())
          
          distance = 0
          
          search_res = dict_tree.query(wd, distance)
          
          if not search_res:

             distance = 2
             search_res = dict_tree.query(wd, distance)
             
             if not search_res:
                print("Suitable suggestions were not found")
                   
             else:
                print("No matches found. Did you mean:")
                count = 0
                for res in search_res:
                   if count==10:
                      break
                   #print(res[0])
                   print(res[1])
                   count = count + 1
                
          else:
             
             print("The spelling is correct! The word entered was:")
             print(search_res[0][1]+" : "+search_res[0][2])
       
       elif x==4:
          
          print("Enter the word to look up")
          wd = str(input())
          
          search_res = dict_tree.query(wd, 0)
          
          if not search_res:
             print("No match found!")
             
          else:
             print(search_res[0][1]+" : "+search_res[0][2])
             print("Levenshtein Distance-based query:")
             timeof(dict_tree.query,wd,0)
             print("Brute query:")
             timeof(brute_query,wd,filter(len,wordlist),levenshtein,0)
       
       
       elif x==5:
          print(maxdepth(dict_tree.tree))
       
       elif x==6:
          sys.exit(0)
       
       else:
          print("Enter a valid choice")
          continue
       
       print("\nContinue? (Y/N)")
       c = input()
       
       if ((c=='Y') or (c=='y')):
          os.system('clear||cls')
          continue
          
       else:
          print("Are you sure you want to exit? (Y/N)")
          c = input()
          if ((c=='Y') or (c=='y')):
             break
          else:
             os.system('clear||cls')
             continue
             
