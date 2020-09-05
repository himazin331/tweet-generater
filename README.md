# tweet-generater

Twitter APIを用いてユーザのツイートを取得し、取得したツイートの形態素解析を行い、マルコフ連鎖による文章生成を行うプログラム。

A program that uses Twitter API to retrieve users' tweets, performs morphological analysis of the retrieved tweets, and generates sentences using Markov chains.

## 前提 Prerequisites

**Twitter APIが利用可能**であることが大前提です。

あらかじめconfig.pyにAPIキーとアクセストークンを記述してください。

It is a prerequisite that the **Twitter API is available**.

You must include an API key and an access token in your config.py file.
```
CONSUMER_KEY = "********************************"
CONSUMER_SECRET = "********************************"
ACCESS_TOKEN = "********************************"
ACCESS_TOKEN_SECRET = "********************************"
```

動作には**emoji, janome, markovify**の３つのPythonパッケージが必要です。

下のようにコマンドを実行してインストールしてください。

You need three Python packages: **emoji, janome and markovify** to work.

Run the following commands to install them.
```
pip install emoji
pip install janome
pip install markovify
```

## 詳細 Details

・リツイートは取得するツイートに含めていません。

・メンションやハッシュタグ、URL、絵文字などは除去するようにしてあります。

・全角で書かれた英数字は半角に置き換えるようにしてあります。

・API実行の回数上限の関係で2000ツイートまでの取得にとどめてあります。


・Retweets are not included in the tweets you get.

・Mentions, hashtags, URLs and emojis are removed.

・Full-width alphanumeric characters are replaced with half-width characters.

・Due to the API's limit on the number of times it can be executed, the number of tweets is limited to 2000.
