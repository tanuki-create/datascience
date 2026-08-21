# Statistical Test Video Series

日本語の統計検定を、1検定1本の縦型ショート動画に変換する HyperFrames プロジェクトです。

## 対象

- 1標本の母平均のt検定
- 対応のない2標本の母平均の差のt検定
- 対応のある2標本の母平均の差のt検定
- マン-ホイットニーのU検定
- コルモゴロフ-スミルノフ検定
- 一元配置分散分析

## 使い方

```bash
cd /Users/hm/datascience/statistical_test_video_series
npm run list
npm run build -- one_sample_t_test
npm run check
npm run render:term -- one_sample_t_test
```

今回の出力は、字幕と図解だけで理解できる無音MP4です。ナレーション文は `content/*.json` の `narration` に入っています。

## 全MP4を書き出す

```bash
npm run render:all
```

出力先は `renders/*.mp4` です。生成済みファイルの一覧は `renders/manifest.json` にあります。
