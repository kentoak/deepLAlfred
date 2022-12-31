# DeepLWithNotion

① DeepLで翻訳
② ロングマン英和辞典で単語検索
③ 英辞郎から単語検索
を同時に実行し、Notion Databaseに保存して自分だけの辞書を作ることができるAlfred Workflow。
ランチャーアプリAlfred（Spotlight検索の完全上位互換）の有料版を買うと使うことが出来ます。Alfredの検索窓から`d`+半角スペースのあとに翻訳したい単語（文章）を打つと、DeepLで翻訳&ロングマン英和辞典と英辞郎から単語検索された結果が表示される。英和も和英も対応（OCRは英和のみ）。NotionのDatabaseに保存できる。

![画面収録 2022-12-28 16 31 48 (1)_fps30_width640](https://user-images.githubusercontent.com/43945931/209777244-8d4b5cfd-680d-462f-b395-ee856c0d39c4.gif)



## 機能

* DeepLで翻訳
* Longman英和・和英辞典の単語検索
* 英辞郎英和・和英辞典の単語検索
* スクショ画像をOCRして英和で翻訳
* 翻訳結果をNotionのDatabaseに保存する・クリップボードにコピーする

### DeepLで翻訳
[既存のDeepL用のAlfred Workflow](https://www.packal.org/workflow/deepl-translate)は、ピリオド.を打つ必要があったがそれをなくしている。また、既存のDeepL用のAlfred Workflowは、ただ翻訳文が返ってきていた。これでは勉強にならないし、元の文との対応を見られるようにしている。Titleに翻訳後の文を、Subtitleに翻訳前の文を載せた。さらに、[DeepL.com](https://www.deepl.com/translator)では、日本語訳にカンマピリオドと句読点が混在されることがあるが、句読点に統一している。

![image](https://user-images.githubusercontent.com/43945931/209459707-26a52b81-1e77-4e9d-acca-9960bebc44cc.png)

### Longman英和・和英辞典の単語検索
[Atsu英語氏がLongman英和最強！って言っていた](https://twitter.com/atsueigo/status/1204702821595004928?ref_src=twsrc%5Etfw%7Ctwcamp%5Etweetembed%7Ctwterm%5E1204702821595004928%7Ctwgr%5E3892e63e53556ed517de642ad6e4787c3a44e23c%7Ctwcon%5Es1_&ref_url=https%3A%2F%2Fqiita.com%2Fkentoak%2Fitems%2Ff08c914f1f5c41c09597)ので、ロングマンを使う。
ロングマン英和辞典で辞書検索し、例文も取得できる。

![image](https://user-images.githubusercontent.com/43945931/210131553-e68d9c3c-5187-4f6e-8efb-908d743dafaa.png)



### 英辞郎英和・和英辞典の単語検索
ロングマン英和辞典では、"rack up"などのニッチな英熟語は載っていない。そこで、英熟語が豊富に載っている英辞郎も使えるようにした。例文も取得できる。

![image](https://user-images.githubusercontent.com/43945931/210131555-8818fabd-2dae-4b65-b061-54f8ef290ba9.png)



### スクショ画像をOCRして英和で翻訳
PDFの仕様などでコピーができない場合や、翻訳したい文章が画像の場合のときのため、スクショをOCRでテキストにしてそれをDeepL APIに入れるものも作った。こちらは、検索窓に`dd`と打つと、スクショが保存されるフォルダの最新の画像についてOCRが実行される。pyocrを使っている。スクショ画像が保存されるPathを通す必要がある。


### 翻訳結果をNotionのDatabaseに保存する
`⌘+Enter`でNotionのDatabaseに追加される。
`Enter`でコピーされる。DeepLの場合、リストの一番上で`Enter`すれば全訳がコピーされる。
単語と意味がデータベースに追加され、単語帳のように確認することができる。
   ![68747470733a2f2f71696974612d696d6167652d73746f72652e73332e61702d6e6f727468656173742d312e616d617a6f6e6177732e636f6d2f302f3331363339302f61303863646536312d353132382d376130652d616664342d3732343739623262363933662e706e67](https://user-images.githubusercontent.com/43945931/209459908-3625aec0-a84b-4cfb-97b8-fefa0100381e.png)
  
一連の流れ
1. Alfredの検索窓から`d cocky`
 ![image](https://user-images.githubusercontent.com/43945931/209459972-903abc8a-c8ab-4c04-a516-5c3e94e588f9.png)

2. cockyをデータベースへ追加のところで`⌘+Enter`を押す（Subtitleのリンクを見てロングマンと英辞郎を選択できる。辞書に載っていない場合はDeepL翻訳結果が追加される）
3. 通知が来る
  ![image](https://user-images.githubusercontent.com/43945931/209459663-72679bb9-78ec-4ee6-9eaf-f3b7a3a88aa2.png)
4. Notion Databaseに追加されている
![68747470733a2f2f71696974612d696d6167652d73746f72652e73332e61702d6e6f727468656173742d312e616d617a6f6e6177732e636f6d2f302f3331363339302f37333434653865662d623966632d353835362d333265632d3738346431633939633433312e706e67](https://user-images.githubusercontent.com/43945931/209459922-16fb599b-a3e0-4a52-9060-97b3a940d12d.png)

## ダウンロード
<a href='https://github.com/kentoak/deepLAlfred/releases/download/version1.1/DeepLWithNotion.alfredworkflow'>⤓ Download Workflow</a>

## セットアップ
Workflowの右上
![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/316390/dcd3f12d-feb5-6d6f-a579-2942870bbf3c.png)
の[x]のところ、`Workflow Environment Variables`に各自の`DeepL_AUTH_KEY`, `NOTION_API_KEY`, `NOTION_DATABASE_URL`、`SCREENSHOT_PATH`を入力する。
![IMG_4145.jpg](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/316390/19544028-4424-2de6-6be8-b9aa57e69ad9.jpeg)

### Get DeepLAPI
無料で月50万文字まで利用できる。姓名、メールアドレス、パスワード、住所、クレジットカード番号などの入力が必要（繰り返しになるが、月50万文字まで無料なので請求はされない）。
以下から作成できる ↓↓↓
https://www.deepl.com/pro#developer

![20221225-163130.jpg](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/316390/2e6d25ee-f05c-57ca-d09d-65681d28b75a.jpeg)

`xxxxxxxxxxxxxxxxxxxxx:fx`をコピーし、`DeepL_AUTH_KEY`に入れる。

[参考手順](https://keikenchi.com/how-to-get-a-free-api-key-for-deepl-translator)

### Get NotionAPI
以下からNotionAPIを取得する。
https://www.notion.so/my-integrations

![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/316390/68182318-5cd8-14f5-3083-7b2197d3d1e7.png)
`secret_xxxxxxxxxxxxxxxxx`をコピーして、`NOTION_API_KEY`に入れる。


[参考手順](https://zenn.dev/utah/articles/da8239aca15335)

### Get Notion Database URL
[Notion Database 参考配布](https://sedate-albatross-de7.notion.site/dd45f9f9f9854528825e05ad9a7977cf) から複製をクリックし、Databaseを各自のNotionのWorkSpaceに入れる。
Open as pageからDatabaseのリンクを開く。
![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/316390/11079987-a299-c9e7-6c11-cc6796355c8d.png)

そのときの`https://www.notion.so/XXXXXXXXXXX?v=?????????????????` のようなリンクをコピーして、`NOTION_DATABASE_URL`に入れる。

### OCR用のPath設定

各自のスクショが保存されるPathをコピーして、`SCREENSHOT_PATH`に入れる。（私の場合、`/Users/kt/sccapture/*`。最後の*を忘れないように注意。）

`SCREENSHOT_PATH`の他に、tesseractのPathを通すことも必要。pyocrを使うには、tesseractをインストールして、そのpathを通す必要がある。デフォルトでは`/usr/local/bin/tesseract`にしている。そうでなければ[x]のところに書き直し。必要に応じてPathを通すか、Workflowの中にコマンドをぶち込む。

## Distribution
* [Notion Database 参考配布](
https://sedate-albatross-de7.notion.site/dd45f9f9f9854528825e05ad9a7977cf)
`Word`, `Meaning1~7`, `Date`, `Link`のPropertyがある。使うときはSortでDateの降順にすると最新のものが上に来る。
 
 ![image](https://user-images.githubusercontent.com/43945931/209460636-18168e6f-664c-4040-b897-df2d064e2217.png)


* [Subtitleを見やすくしたAppearance参考配布](https://www.alfredapp.com/extras/theme/hwZohFvH5J/)

   デフォルトはこれ。
   ![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/316390/647d2a42-3d08-57f0-927f-c8aa38c645c1.png)

   このAppearanceは、以下のようにSubtitleの文字をデフォルトより大きくして、よく見えるようにしてある。
   ![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/316390/8529a5ff-f2f9-b7af-d4dc-fbc032c0098e.png)


# こちらも合わせて御覧ください
https://qiita.com/kentoak/items/ed06d331db12d25a4cd2

