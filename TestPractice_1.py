f = open("wordcount_result.txt", "r", encoding="utf-8")
data = f.readlines()
new_list = list()
for i in data[:10]:
    new_list.append(i.replace("\n", ""))

newDict = dict()
for i in new_list:
    newDict[i.split()[0]] = int(i.split()[1])

import matplotlib
import matplotlib.pyplot as plt

fig = plt.gcf()  # get current figure 도화지를 먼저 그린다.
fig.set_size_inches(20, 10)
matplotlib.rc("font", family="Malgun Gothic", size=10)
plt.title("그래프 제목")
plt.xlabel("단어")
plt.ylabel("개수")
plt.bar(newDict.keys(), newDict.values(), color="#FF0000")
plt.xticks(rotation=45)
print("그래프 보이나요?")
plt.savefig("top_words.jpg")
plt.show()