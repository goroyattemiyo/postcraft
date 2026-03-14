"""
Synapse - プラットフォーム原稿生成
HTMLパースで素材テキストを抽出し、Brain/Note向けドラフトを生成する。
"""

from synapse.image_pipeline import extract_sections, extract_text_from_html

SECTION_TITLES: dict[str, str] = {
    "hero": "ファーストビュー",
    "firstview": "ファーストビュー",
    "problem": "こんな悩みありませんか？",
    "empathy": "その気持ち、わかります",
    "solution": "解決策があります",
    "features": "特徴・メリット",
    "proof": "実績・証拠",
    "testimonials": "お客様の声",
    "comparison": "比較表",
    "details": "商品詳細",
    "offer": "特別オファー",
    "faq": "よくある質問",
    "cta": "今すぐ手に入れる",
    "final_cta": "今すぐ手に入れる",
}


def _section_title(name: str) -> str:
    """セクション名を日本語タイトルに変換する。"""
    return SECTION_TITLES.get(name.lower(), name)


def generate_brain_draft(html_content: str, sections: list[dict[str, str]] | None = None) -> str:
    """Brain投稿用ドラフトを生成する。"""
    if sections is None:
        sections = extract_sections(html_content)

    lines: list[str] = []
    free_boundary = max(len(sections) // 3, 2)

    for i, sec in enumerate(sections):
        name = sec["name"]
        text = extract_text_from_html(sec["content"])
        lines.append(f"## {_section_title(name)}")
        lines.append("")
        lines.append(f"![{name}](<<{i + 1:02d}_{name}.png>>)")
        lines.append("")
        if text:
            lines.append(text)
            lines.append("")
        if i == free_boundary - 1:
            lines.append("---")
            lines.append("")
            lines.append("**>>>  ここから有料エリア  <<<**")
            lines.append("")

    return chr(10).join(lines)


def generate_note_draft(html_content: str, sections: list[dict[str, str]] | None = None) -> str:
    """Note投稿用ドラフトを生成する。"""
    if sections is None:
        sections = extract_sections(html_content)

    lines: list[str] = []
    lines.append("## 目次")
    lines.append("")
    for i, sec in enumerate(sections):
        title = _section_title(sec["name"])
        lines.append(f"{i + 1}. {title}")
    lines.append("")
    lines.append("---")
    lines.append("")

    free_boundary = max(len(sections) // 3, 2)

    for i, sec in enumerate(sections):
        name = sec["name"]
        text = extract_text_from_html(sec["content"])
        lines.append(f"## {_section_title(name)}")
        lines.append("")
        lines.append(f"![{name}](<<{i + 1:02d}_{name}.png>>)")
        lines.append("")
        if text:
            lines.append(text)
            lines.append("")
        if i == free_boundary - 1:
            lines.append("---")
            lines.append("")
            lines.append("**ここから先は有料です**")
            lines.append("")

    return chr(10).join(lines)


def generate_posting_guide(
    sections: list[dict[str, str]],
    brain_draft: str,
    note_draft: str,
) -> str:
    """Brain/Note投稿手順ガイドを生成する。"""
    free_boundary = max(len(sections) // 3, 2)
    lines: list[str] = [
        "# 投稿ガイド",
        "",
        "## 準備物",
        "",
        "- lp.html (ブラウザで確認用)",
        "- sections/ フォルダ内のPNG画像",
        "- brain_draft.md (Brain投稿用テキスト)",
        "- note_draft.md (Note投稿用テキスト)",
        "",
        "---",
        "",
        "## Brain投稿手順",
        "",
        "1. https://brain-market.com/ にログイン",
        "2. 投稿ボタンをクリック",
        "3. サムネイル画像を設定 (推奨: 1280x670px)",
        "4. タイトルを入力",
        "5. brain_draft.md の内容をエディタに貼り付け",
        "6. 画像プレースホルダーの箇所に対応する画像をアップロード",
        f"7. 有料境界を設定 (セクション{free_boundary}の後に設定推奨)",
        "8. 価格を設定 (100円~100,000円)",
        "9. 紹介料を設定 (30~50%推奨)",
        "10. カテゴリを選択",
        "11. 下書き保存 -> プレビュー確認 -> 公開申請",
        "12. 審査通過後、販売開始 (通常24時間以内)",
        "",
        "### Brain注意点",
        "",
        "- 公開申請後は編集ロック",
        "- 公開後の編集は再審査が必要",
        "- 手数料: 売上の12%",
        "",
        "---",
        "",
        "## Note投稿手順",
        "",
        "1. https://note.com/ にログイン",
        "2. 投稿 -> テキストを選択",
        "3. note_draft.md の内容をエディタに貼り付け",
        "4. 画像プレースホルダーの箇所に対応する画像をアップロード",
        f"5. 有料境界を設定 (セクション{free_boundary}の後に設定推奨)",
        "6. 価格を設定 (100円~10,000円)",
        "7. 目次が自動生成されることを確認",
        "8. ハッシュタグを設定",
        "9. プレビュー確認 -> 公開",
        "",
        "### Note注意点",
        "",
        "- 表 (table) は使えない -> 画像で代替済み",
        "- 文字色/サイズ変更不可 -> 画像で代替済み",
        "- 目次はH2/H3見出しから自動生成",
        "",
        "---",
        "",
        "## 画像挿入チェックリスト",
        "",
    ]
    for i, sec in enumerate(sections):
        name = sec["name"]
        lines.append(f"- [ ] {i + 1:02d}_{name}.png -> {_section_title(name)}")
    lines.extend(
        [
            "",
            "---",
            "",
            "## 公開前チェックリスト",
            "",
            "- [ ] 全画像が正しく表示されている",
            "- [ ] 有料境界の位置が適切",
            "- [ ] リンク切れがない",
            "- [ ] 誤字脱字チェック完了",
            "- [ ] 価格設定が正しい",
            "- [ ] サムネイル画像を設定済み",
            "- [ ] SEO用の説明文を記入済み",
        ]
    )
    return chr(10).join(lines)
