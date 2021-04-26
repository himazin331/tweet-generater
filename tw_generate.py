import config
import tweepy
import re
import emoji

from janome.tokenizer import Tokenizer
from janome.analyzer import Analyzer
from janome.charfilter import UnicodeNormalizeCharFilter
import markovify


class GetTweet():
    def __init__(self, user_id):
        # APIキー & アクセストークン
        CK = config.CONSUMER_KEY
        CS = config.CONSUMER_SECRET
        AT = config.ACCESS_TOKEN
        ATS = config.ACCESS_TOKEN_SECRET

        # Twitter API認証
        auth = tweepy.OAuthHandler(CK, CS)
        auth.set_access_token(AT, ATS)
        self.api = tweepy.API(auth)

        self.tweet_list = []  # ツイート内容
        self.user_id = user_id  # ユーザID
        self.max_id = None

    # ツイート取得
    def get_tweet(self, cnt, flg=1):
        # ツイート取得(RT含まない)
        for status in self.api.user_timeline(id=self.user_id, count=cnt, include_rts=False,
                                                max_id=self.max_id, tweet_mode="extended"):
            # 過剰取得分をスルー
            if flg == 1:
                flg = 0
                continue
            tweet = self.removal(status.full_text)  # テキスト除去
            self.tweet_list.append(tweet)
        self.max_id = status.id  # max_id更新(max_id以降のツイートを取得する)

        return self.tweet_list

    # テキスト除去
    def removal(self, tweet):
        tweet = tweet.replace("#", "")  # ハッシュタグ除去

        # メンション除去
        tweet = tweet.replace('\n', " ")
        tweet = re.sub(r"[^\w]@\w+\s", " ", tweet)
        tweet = re.sub(r"^@\w+\s+", " ", tweet)
        tweet = re.sub(r"\s+@\w+\s+", " ", tweet)
        tweet = re.sub(r"\s@\w+$", " ", tweet)
        tweet = re.sub(r"\s@\w+\s+", " ", tweet)

        # URL除去
        tweet = re.sub(r"https://t.co/[a-zA-Z0-9]+\s*", " ", tweet)

        # 絵文字、文字コードの除去
        tweet = ''.join(c for c in tweet if c not in emoji.UNICODE_EMOJI)
        tweet = tweet.replace('\u200d️️️', '')
        tweet = re.sub(r"\\U[a-zA-Z0-9]+\s*", " ", tweet)

        # 特殊記号の置換
        tweet = tweet.replace('&lt;', '<')
        tweet = tweet.replace('&gt;', '>')
        tweet = tweet.replace('&amp;', "&")

        return tweet


class GenerateTweet():
    def __init__(self):
        char_filters = [UnicodeNormalizeCharFilter('NFKC')]  # Unicode正規化&全角->半角
        self.a = Analyzer(char_filters, Tokenizer())  # Analyzer作成

    # 文章生成
    def generate_tweet(self, tweet_list):
        text_list = []

        # 分かち書き
        for i in range(len(tweet_list)):
            text = [token.surface for token in self.a.analyze(tweet_list[i])]
            text = ' '.join(text)
            text_list.append(text)
        
        model = markovify.Text(text_list, state_size=1)  # マルコフモデル作成

        while True:
            sentence = model.make_short_sentence(280)  # 280文字の文章生成
            sentence = sentence.replace(" ", "")  # 空白除去
            print(sentence)

            yn = input("Continue? y/n: ")
            if yn == "n":
                break
            print("")


# 入力処理
def input_def():
    print("")
    # ユーザID
    user_id = ""
    while True:
        user_id = input("User ID : ")
        if user_id != "":
            break

    # ツイート取得数(上限 2000ツイート)
    while True:
        get_tweet_num = int(input("Number of tweets to get(Max=2000) : "))
        if get_tweet_num > 0 and get_tweet_num <= 2000:
            break
    print("")

    return user_id, get_tweet_num


def main():
    try:
        user_id, get_tweet_num = input_def()

        # Twitter API認証(インスタンス生成)
        getTW = GetTweet(user_id)

        # API実行回数
        exec_num = int(get_tweet_num / 200)
        exec_num_d = get_tweet_num % 200

        # ツイート取得
        flg = 0
        while exec_num > 0:
            tweet_list = getTW.get_tweet(200, flg)
            exec_num -= 1
            flg = 1

        # 端数分の取得
        if exec_num_d != 0:
            tweet_list = getTW.get_tweet(exec_num_d + flg, flg)

        # 不足分の取得
        exec_num_add = get_tweet_num - len(tweet_list)
        while exec_num_add > 0:
            tweet_list = getTW.get_tweet(exec_num_add + 1)
            exec_num_add = get_tweet_num - len(tweet_list)

        generateTW = GenerateTweet()
        generateTW.generate_tweet(tweet_list)  # 文章生成

    except tweepy.TweepError as e:  # Twitter API例外
        try:
            print("\nError Code: {}".format(e.args[0][0]['code']))
            print(e.args[0][0]['message'])
        except TypeError:  # 鍵垢に対して実行した->例外
            print("")
            print(e)
            print("The user has set their tweets to private.")

    except ValueError:  # 不適切な入力->例外
        print("\nPlease enter an integer value.")


if __name__ == "__main__":
    main()
