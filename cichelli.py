### Cichelli's Method Phase 1: Scoring words ###

# getting unique words, put them in unique list
with open("MLKSpeechP1.txt", "r") as file:
    words = (file.read()).strip().split()

word_set = set()
unique = []

for word in words:
    if word not in word_set:
        unique.append(word.lower())
        word_set.add(word.lower())


# count occurences of the first and last letters of each word
first_last = []

# for each unique word, get the first and last letters of each and place them in a collective list 'first_last'
for word in unique:
    first_last.append(word[0]) # first letters
    first_last.append(word[len(word)-1]) # last letters

# count how many times each letter appears in the list
letter_freq = {letter: 0 for letter in first_last} # letter (keys), freq (values)
for letter in first_last:
    letter_freq[letter] += 1


# get all the letters that have the max freq and order them
vals = set(letter_freq.values())
ordered_letter_freq = {}

for i in range(len(vals)): # go max to max, and place letters in order by freq; if same freq, use order of first encounter
    curr_max = max(vals)

    for letter in letter_freq:
        if letter_freq[letter] == curr_max:
            ordered_letter_freq[letter] = letter_freq[letter]
    vals.remove(curr_max)

# assigning a value to each word based on first and last letter freq scores
words_value = {}

for word in unique:
    sum = ordered_letter_freq[word[0]] + ordered_letter_freq[word[len(word)-1]]
    words_value[word] = sum

# order the words_value based on the values
vals = set(words_value.values())
ordered_words = {}

for i in range(len(vals)):
    curr_max = max(vals)

    for word in words_value:
        if words_value[word] == curr_max:
            ordered_words[word] = words_value[word]
    vals.remove(curr_max)

ordered_list = list(ordered_words.keys())

# initialize dicts and variables
g_firsts = {word[0]: 0 for word in ordered_list}
g_lasts = {word[-1]: 0 for word in ordered_list}
prev_slot = {word: set() for word in ordered_list}
hash_table = {i: '' for i in range(len(ordered_list))}

size = len(ordered_list) # amount of key words
max_g = size//2 # max g is %50 of size of hash table (rounded down if hash table size is odd)
using_lasts = False # toggle for using g_lasts instead of gfirsts

# calculate index function
# hash function; h(word) = (length(word) + g*(firstletter(word)) + g*(lastletter(word))) % size
def calc_index(word):
    return (len(word) + g_firsts[word[0]] + g_lasts[word[-1]]) % size



### Cichelli's Method Phase 2: Creating the hash table ###

i = 0
while i < size: # while there are less than 'size' number of filled hash_table slots, mess with the g values of the current word; 'i' is the # of filled slots and also the index for the current word
    word = ordered_list[i] # current word
    slot_found = False
    
    while g_firsts[word[0]] <= max_g:  # try all g values for the current word until max_g
        
        if using_lasts: # if using g_lasts, do this
            while g_lasts[word[-1]] <= max_g: # while g_last less than max_g
                index = calc_index(word)

                if hash_table[index] == '' and index not in prev_slot[word]: # if slot is empty and the word hasn't been placed here before
                    hash_table[index] = word # insert word in slot {index}
                    prev_slot[word].add(index) # add this slot # to the list of previously tried, successful inserts for this word
                    slot_found = True
                    break # stop trying g values
                else: # if slot is taken, increment g_last for the word
                    g_lasts[word[-1]] += 1
            if slot_found: # if successful before g_last reaches max_g
                break # if the word found an empty slot before g_max reached, exit loop, try g_firsts
            g_lasts[word[-1]] = 0 # reset g_lasts if maxed
        
        index = calc_index(word)

        if hash_table[index] == '' and index not in prev_slot[word]: # if slot is empty and the word wasn't there before
            hash_table[index] = word # insert word in slot {index}
            prev_slot[word].add(index) # add this slot # to the list of previously tried, successful inserts for this word
            slot_found = True
            break # stop trying g values
        else:
            g_firsts[word[0]] += 1

    if slot_found:  # if successful within g=0 to max_g, move forward to next word
        i += 1

    else: # if NOT successful and max_g reached, backtrack to prev word and start with g(first/last)+1
        
        i -= 1  # go back to previous word
        g_firsts[word[0]] = 0  # reset g_first value for current word  
        if using_lasts:
            g_lasts[word[-1]] = 0 # reset g_last value for current word  

        for x in hash_table: 
            if hash_table[x] == ordered_list[i]: # pop out prev word
                hash_table[x] = '' 

        if i < 0: # if i has backtracked all the way to the beginning of the list of words
            if using_lasts: # if everything fails and already messed with g_lasts
                break
            else: # if messing with g_firsts failed for all iterations, switch to incrementing g_lasts instead
                using_lasts = True
                i = 0

                # reset all previous g values and clear hash table
                for key in g_firsts:
                    g_firsts[key] = 0
                for key in g_lasts:
                    g_lasts[key] = 0

                for key in prev_slot:
                    prev_slot[key].clear()
                for key in hash_table:
                    hash_table[key] = ''
                continue
                
        g_firsts[ordered_list[i][0]] += 1 # try next g_first for prev word

### Constructed hash table ###
# for key, value in hash_table.items():
#     print(f"{key}: {value}")


### Reading file for keywords ###
total_lines = 0
total_words = 0
word_counter = {x:0 for x in hash_table.values()}
total_key_words = 0

with open("MLKSpeechP2.txt", "r") as file:
    lines = file.readlines()

for line in lines:
    if line.strip() != '': # count only non-empty lines
        total_lines += 1

        for word in line.strip().split():
            total_words += 1 # count all words of each line
            if word.lower() in word_counter.keys(): # if the word encountered is in the key words determined by the hash table
                word_counter[word.lower()] += 1 # add 1 to the individual key word count
                total_key_words +=1 # add 1 to the total keywords count

print(f"""
**********************
***** Statistics *****
**********************
Total Lines Read: {total_lines}
Total Words Read: {total_words}
Break Down by Key Word
""", end='')

for key, val in hash_table.items():
    print(f"    {key} : {val} ({word_counter[val]})")

print(f"""
Total Key Words: {total_key_words}
""")
