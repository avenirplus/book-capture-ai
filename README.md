# Book Capture AI

Windows向けのローカル電子書籍キャプチャ支援アプリです。

通常表示できる電子書籍画面を、

**自動ページ送り → キャプチャ → Kindle UIトリミング → 見開き自動分割 → PDF/OCR化**

します。

> DRM解除、暗号化解除、キャプチャ防止機能の回避は行いません。  
> 権利・利用規約で認められる範囲で使用してください。

## v0.6.0 完成版

- Windows上の対象ウィンドウ選択
- マウスドラッグによるキャプチャ範囲指定
- ← / → / Space / PageDown による自動ページ送り
- Windowsネイティブのキー送信
- **撮影終了方法を2種類から選択**
  - Smart Guardで本の終わりを自動判定
  - 固定枚数まで必ず撮影
- 一時停止 / 再開 / 手動終了
- `F8` 一時停止/再開
- `F9` を2回で終了してPDF作成
- `キャンセル（PDFを作らず停止）` で撮影済み画像だけ残す
- 元スクリーンショットを `images/` に保持
- **KindleクリーンPDF**
  - 上部ヘッダー / 下部フッターを割合でトリミング
  - 初期値 上8% / 下6%
  - きっちり範囲選択できる場合は0%運用も可能
- **見開き自動分割**
  - 右→左（日本語書籍）
  - 左→右（洋書等）
- 画像PDF
- 内蔵Tesseract OCRによる検索可能PDF / OCR TXT
- **キャプチャ後処理をQThreadへ分離**
  - 分割中 / PDF生成中 / OCR n/Nページ / 完了を表示
  - OCR中もGUIが固まりにくい構成
  - OCRだけ失敗しても画像PDFと元画像を保持
- 小さいノートPC画面対応：設定部だけスクロール、主要操作ボタンは固定表示
- **`？ 使い方` ボタンから `manual.html` を1タップで開く**

## まず使う

1. WindowsでKindle for Web等を開き、本文を表示する。
2. Book Capture AIで `ウィンドウ更新` → 対象ウィンドウを選択。
3. `画面範囲を選択` で本文・見開き範囲を囲う。
4. 必要なら見開き分割・上下トリミング・OCRをON。
5. `キャプチャ開始` を押し、待ち時間の間に本へ戻る。
6. 撮影終了後、PDF/OCRはバックグラウンドで自動処理。

詳しい説明：[`manual.html`](manual.html)

公開マニュアル：https://branzfamily01.github.io/book-capture-ai/manual.html

## 出力例

```text
本の名前-日時/
├── 本の名前.pdf
├── 本の名前-searchable.pdf
├── 本の名前.txt
├── images/              # 元スクリーンショット
└── images-split/        # 見開き分割 + トリミング後
```

見開き分割OFFで上下トリミングのみ使用する場合は `images-clean/` を作ります。

## OCR

Windows配布版には Tesseract OCR と言語データを同梱しています。別途インストール不要です。

- `jpn+eng`：日本語横書き＋英語
- `jpn_vert+eng`：日本語縦書き＋英語

OCRはローカルPC内で処理します。

## 開発環境から起動

```powershell
py -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python app_v7.py
```

## EXEを作る

GitHub Actions `.github/workflows/build-windows.yml` が Windows runner 上でテスト・ビルド・OCR同梱・完成EXE自己診断を行います。

Artifact:

```text
Book-Capture-AI-v0.6.0-Windows
```

## 自動テスト

- Pythonコンパイル
- 主要ロジックテスト
- 固定枚数キャプチャ
- PostProcessThread
- 見開き分割
- 上下トリミング
- 画像PDF
- 内蔵Tesseract OCR
- 検索可能PDF
- 小型画面で開始ボタンが表示されること
- manual.htmlの実UI表記一致
- `？ 使い方` ボタン
- 完成EXE自己診断

## 公開

- GitHub: https://github.com/branzfamily01/book-capture-ai
- 公開案内: https://branzfamily01.github.io/book-capture-ai/
- マニュアル: https://branzfamily01.github.io/book-capture-ai/manual.html

## 既知の制約

- Windowsデスクトップアプリです。iPhone/iPad単体ではキャプチャできません。
- 見開き分割は基本的に選択範囲中央です。
- 表紙・章扉など片側だけの画面では不要な半ページができる場合があります。
- OCR精度は表示解像度・文字サイズ・レイアウトに依存します。
- キャプチャ禁止・保護機能は回避しません。
