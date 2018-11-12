def load_dict():
    
    count = 0
    words=[]
    definitions = []
    
    print('Loading dictionary from file...\n')

    with open('dictionary1.txt', 'r') as document:
        for line in document:
            if (count%2==0):
                words.append(line.strip())
            else:
                definitions.append(line.strip('\n'))
            count += 1

    print('Dictionary loaded.\n') 
    
    return words,definitions 
    
def add_dict(word, definition): 
   f=open('dictionary1.txt', 'a')
   
   if word:
      f.write(word)
      f.write("\n")
      if definition:
         f.write(definition)
         f.write("\n")
      else:
         f.write("---")
         f.write("\n")