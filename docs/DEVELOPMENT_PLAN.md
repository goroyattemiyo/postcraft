# PostCraft - 開発ドキュメント

最終更新: 2026-03-14

## 概要

HTMLからBrain/Note投稿素材を一括生成する変換ツール。
セクション画像・投稿原稿・投稿ガイドをZIPで出力する。

## リポジトリ構成

    synapse/
        config.py          定数定義
        prompts.py         通常モード用プロンプト
        lp_prompts.py      LP生成用プロンプト
        agents.py          エージェント実行
        tools.py           ツール定義・実行
        sandbox.py         サンドボックス環境
        engine.py          通常モードエンジン
        lp_engine.py       LP生成エンジン (Phase A)
        lp_engine_drafts.py LP生成エンジン (Phase B + 画像)
        image_pipeline.py  Playwright画像キャプチャ
        draft_generator.py Brain/Note原稿生成
        lp_manual_utils.py 手動モードユーティリティ
        ui.py              Streamlitエントリポイント
        lp_ui.py           LP自動生成UI
        lp_ui_manual.py    手動LP変換UI
    tests/                 テストスイート (116件)
    docs/
        RULES.md           開発ルール
        DEVELOPMENT_PLAN.md 本ファイル
        archive/           旧ドキュメント

## 主要フロー

手動モード (APIキー不要):
  Step 1: 商品情報入力 + 配色テーマ選択
  Step 2: AIチャット用プロンプト自動生成
  Step 3: 完成版HTML貼付
  Step 4: セクション画像 + Brain/Note原稿 + ガイド生成 → ZIP

APIモード (Anthropic APIキー必要):
  商品情報入力 → Orchestrator → Coder → Reviewer → 全自動生成

## セクション検出の優先順位

1. data-section属性
2. sectionタグ
3. h1-h3見出し分割
4. ページ全体を1枚撮影

## 出力ファイル

- lp.html (単一HTML、インラインCSS)
- sections/*.png (セクション画像、800px幅、1MB以下)
- brain_draft.md (有料境界マーカー + 画像プレースホルダー)
- note_draft.md (目次 + 有料境界 + 画像プレースホルダー)
- posting_guide.md (投稿手順 + チェックリスト)

## テスト・CI

116テスト合格、1スキップ。
静的解析: ruff, mypy, bandit 全てゼロエラー。
GitHub Actions: push/PRごとに自動実行。

## 依存関係

本番: anthropic>=0.40.0, python-dotenv>=1.0.0, streamlit>=1.30.0
画像(任意): playwright>=1.40.0, Pillow>=10.0.0
開発: pytest>=8.0.0, mypy>=1.8.0, ruff>=0.4.0, bandit>=1.7.0

## 今後の課題

- 受託運用での品質検証（実案件ベース）
- プロンプトチューニング（実生成結果ベース）
- Brain/Noteへの実投稿テスト
- synapseフォルダ名のpostcraftへのリネーム（低優先）

旧開発計画書は docs/archive/DEVELOPMENT_PLAN_v1.md を参照。
開発ルールの詳細は docs/RULES.md を参照。