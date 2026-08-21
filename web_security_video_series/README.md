# Web Security Glossary Video Series

日本語のWebセキュリティ用語を、1用語1本の縦型ショート動画に変換する HyperFrames プロジェクトです。

## 使い方

```bash
cd /Users/hm/datascience/web_security_video_series
npm run list
npm run build -- ch01_origin
npm run check
npm run render:term -- ch01_origin
```

`content/*.json` にある用語データを読み込み、指定した `id` の動画を `index.html` として生成します。
今回の出力は字幕と図解だけで理解できる無音MP4です。ナレーション文は各JSONの `narration` に入っています。

## 全HTMLを書き出す

```bash
npm run build:all-html
```

出力先は `generated_html/<term-id>/index.html` です。MP4を量産する場合は、まず代表用語で `npm run check` と `npm run render:term -- <id>` を通してから進めてください。

## 全MP4を書き出す

```bash
npm run render:all
```

出力先は `renders/*.mp4` です。生成済みファイルの一覧は `renders/manifest.json` にあります。
