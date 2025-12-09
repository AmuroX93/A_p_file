mammoth="""We have seen thee, queen of cheese, 
Lying quietly at your ease, 
Gently fanned by evening breeze, 
Thy fair form no flies dare seize. 
All gaily dressed soon you'll go 
To the great Provincial show, 
To be admired by many a beau 
In the city of Toronto. 
Cows numerous as a swarm of bees, 
Or as the leaves upon the trees,
It did require to make thee please, 
And stand unrivalled, queen of cheese. 
May you not receive a scar as 
We have heard that Mr. Harris 
Intends to send you off as far as 
The great world's show at Paris. 
Of the youth beware of these, 
For some of them might rudely squeeze 
And bite your cheek, then songs or glees 
We could not sing, oh! queen of cheese. 
We'rt thou suspended from balloon, 
You'd cast a shade even at noon, 
Folks would think it was the moon 
About to fall and crush them soon. """

import re
c_word=re.findall(r'\bc\w*\b', mammoth, re.IGNORECASE)
c_word_4=re.findall(r'\bc\w{3}\b',mammoth)
r_word=re.findall(r'\b\w*r\b',mammoth)
moto_word=re.findall(r'\b\w*[aeiou]\w*\b',mammoth)
#print(moto_word)

# 首先提取所有单词
all_words = re.findall(r'\b\w+\b', mammoth)

# 定义元音字母（包括大小写）
vowels = 'aeiouAEIOU'

# 找出包含且仅包含3个元音的单词
words_with_3_vowels = []
for word in all_words:
    vowel_count = sum(1 for char in word if char in vowels)
    if vowel_count == 3:
        words_with_3_vowels.append(word)

# 打印结果
print("所有包含且仅包含3个元音的单词:")
for i, word in enumerate(words_with_3_vowels, 1):
    print(f"{i}. {word} (元音: {[char for char in word if char in vowels]})")