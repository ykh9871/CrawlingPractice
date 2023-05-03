import sys
import requests
from bs4 import BeautifulSoup  # 정적 크롤링
from newspaper import Article
from konlpy.tag import Okt
from collections import Counter, OrderedDict
import matplotlib
import matplotlib.pyplot as plt
from wordcloud import WordCloud

URL_BEFORE_KEYWORD = "https://search.naver.com/search.naver?where=news&sm=tab_pge&query="
URL_BEFORE_PAGE_NUM = "&sort=0&photo=0&field=0&pd=0&ds=&de=&cluster_rank=42&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so:r,p:all,a:all&start="

font_name = "Malgun Gothic"

# 주소 추출 함수
def get_link(keyWord, pageRange):
    link = list()

    for page in range(int(pageRange)):
        # 1 -> 11 -> 21 -> 31 ...
        currentPage = 1 + page * 10
        carwlingUrl = URL_BEFORE_KEYWORD + keyWord + URL_BEFORE_PAGE_NUM + str(currentPage)

        response = requests.get(carwlingUrl)
        soup = BeautifulSoup(response.text, "lxml")

        # Class -> "." // ID -> "#"
        urlTag = soup.select(".news_tit")

        for url in urlTag:
            link.append(url["href"])
            # soup.find(), findAll()

    print("뉴스 주소 추출 성공")
    return link


def get_article(url_link, file1):

    with open(file1, "w", encoding="utf8") as f:

        for url2 in url_link:
            article = Article(url2, language="ko")

            try:
                article.download()
                article.parse()
            except:
                continue

            news_title = article.title
            news_content = article.text

            f.write(news_title)
            f.write(news_content)

        f.close()
        print("뉴스 기사 제목, 내용 추출 완료")

def wordcount(file1, file2):

    f = open(file1, "r", encoding="utf8")
    g = open(file2, "w", encoding="utf8")

    engine = Okt()
    data = f.read()
    all_nouns = engine.nouns(data)
    nouns = [n for n in all_nouns if len(n) > 1]

    global count, by_num

    count = Counter(nouns)
    by_num = OrderedDict(sorted(count.items(), key=lambda t: t[1], reverse=True))

    word = [i for i in by_num.keys()]
    number = [i for i in by_num.values()]

    for w, n in zip(word, number):
        final1 = f"{w}   {n}\n"
        # final1 = "{}    {}".format(w, n)
        g.write(final1)

    f.close()
    g.close()
    print("워드 카운팅 완료")

def full_vis_bar(by_num):
    for w, n in list(by_num.items()):
        if n <= 15:
            del by_num[w]

    fig = plt.gcf()  # get current figure 도화지를 먼저 그린다.
    fig.set_size_inches(15, 7)
    matplotlib.rc("font", family=font_name, size=10)
    plt.title("그래프 제목")
    plt.xlabel("단어")
    plt.ylabel("개수")
    plt.bar(by_num.keys(), by_num.values())
    plt.xticks(rotation=45)
    print("그래프 보이나요?")
    plt.savefig("all_words.jpg")
    plt.show()

def top_n_extract_show(file2, topN_number):
    f = open("wordcount_result.txt", "r", encoding="utf-8")
    data = f.readlines()
    new_list = list()
    for i in data[:int(topN_number)]:
        new_list.append(i.replace("\n", ""))

    newDict = dict()
    for i in new_list:
        newDict[i.split()[0]] = int(i.split()[1])

    import matplotlib
    import matplotlib.pyplot as plt

    fig = plt.gcf()  # get current figure 도화지를 먼저 그린다.
    fig.set_size_inches(15, 7)
    matplotlib.rc("font", family="Malgun Gothic", size=10)
    plt.title("그래프 제목")
    plt.xlabel("단어")
    plt.ylabel("개수")
    plt.bar(newDict.keys(), newDict.values(), color="#FF0000")
    plt.xticks(rotation=45)
    print("그래프 보이나요?")
    plt.savefig("top_words.jpg")
    plt.show()


def wordcloud(file1):
    with open(file1, "r", encoding="utf-8") as f:
        data = f.read()
        engine = Okt()
        all_nouns = engine.nouns(data)

        nouns = [n for n in all_nouns if len(n) > 1]
        count = Counter(nouns)

        tags = count.most_common(100)

        wc = WordCloud(font_path="malgun", background_color=(168, 237, 244),
                       width=2500, height=1500)

        cloud = wc.generate_from_frequencies(dict(tags))
        plt.imshow(cloud, interpolation="bilinear")
        plt.axis("off")
        plt.savefig("cloud.jpg")
        plt.show()




def main(argv):
    if len(argv) != 4:
        print("잘못된 사용입니다.")
        print("사용법: python [모듈이름] [키워드] [가져올 페이지 숫자] [TopN개수 입력]")
        return

    file1 = "crawling1.txt"
    file2 = "wordcount_result.txt"
    keyWord = argv[1]
    pageRange = argv[2]
    topN_number = argv[3]
    url_link = get_link(keyWord, pageRange)
    get_article(url_link, file1)
    wordcount(file1, file2)
    full_vis_bar(by_num)
    top_n_extract_show(file2, topN_number)
    wordcloud(file1)

if __name__ == '__main__':
    main(sys.argv)