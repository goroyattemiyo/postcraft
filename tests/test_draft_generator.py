"""draft_generator.py のテスト"""

from synapse.draft_generator import (
    SECTION_TITLES,
    generate_brain_draft,
    generate_note_draft,
    generate_posting_guide,
)

SAMPLE_SECTIONS = [
    {"name": "hero", "content": "<h1>Title</h1><p>Subtitle</p>"},
    {"name": "problem", "content": "<h2>Problem</h2><p>Pain point</p>"},
    {"name": "solution", "content": "<h2>Solution</h2><p>Answer</p>"},
    {"name": "features", "content": "<h2>Features</h2><p>List</p>"},
    {"name": "proof", "content": "<h2>Proof</h2><p>Evidence</p>"},
    {"name": "cta", "content": "<h2>CTA</h2><p>Buy now</p>"},
]

SAMPLE_HTML = (
    chr(60)
    + "section data-section="
    + chr(34)
    + "hero"
    + chr(34)
    + ">"
    + "<h1>Title</h1></section>"
    + chr(60)
    + "section data-section="
    + chr(34)
    + "problem"
    + chr(34)
    + ">"
    + "<h2>Problem</h2></section>"
    + chr(60)
    + "section data-section="
    + chr(34)
    + "solution"
    + chr(34)
    + ">"
    + "<h2>Solution</h2></section>"
    + chr(60)
    + "section data-section="
    + chr(34)
    + "features"
    + chr(34)
    + ">"
    + "<h2>Features</h2></section>"
    + chr(60)
    + "section data-section="
    + chr(34)
    + "proof"
    + chr(34)
    + ">"
    + "<h2>Proof</h2></section>"
    + chr(60)
    + "section data-section="
    + chr(34)
    + "cta"
    + chr(34)
    + ">"
    + "<h2>CTA</h2></section>"
)


class TestBrainDraft:
    def test_contains_paid_boundary(self):
        draft = generate_brain_draft(SAMPLE_HTML, SAMPLE_SECTIONS)
        assert "有料エリア" in draft

    def test_contains_image_placeholders(self):
        draft = generate_brain_draft(SAMPLE_HTML, SAMPLE_SECTIONS)
        assert "01_hero.png" in draft
        assert "06_cta.png" in draft

    def test_contains_section_titles(self):
        draft = generate_brain_draft(SAMPLE_HTML, SAMPLE_SECTIONS)
        assert "ファーストビュー" in draft

    def test_returns_string(self):
        draft = generate_brain_draft(SAMPLE_HTML, SAMPLE_SECTIONS)
        assert isinstance(draft, str)
        assert len(draft) > 0


class TestNoteDraft:
    def test_contains_toc(self):
        draft = generate_note_draft(SAMPLE_HTML, SAMPLE_SECTIONS)
        assert "目次" in draft

    def test_contains_paid_boundary(self):
        draft = generate_note_draft(SAMPLE_HTML, SAMPLE_SECTIONS)
        assert "有料" in draft

    def test_contains_image_placeholders(self):
        draft = generate_note_draft(SAMPLE_HTML, SAMPLE_SECTIONS)
        assert "01_hero.png" in draft

    def test_toc_has_numbered_items(self):
        draft = generate_note_draft(SAMPLE_HTML, SAMPLE_SECTIONS)
        assert "1. " in draft
        assert "6. " in draft

    def test_returns_string(self):
        draft = generate_note_draft(SAMPLE_HTML, SAMPLE_SECTIONS)
        assert isinstance(draft, str)


class TestPostingGuide:
    def test_contains_brain_section(self):
        guide = generate_posting_guide(SAMPLE_SECTIONS, "", "")
        assert "Brain投稿手順" in guide

    def test_contains_note_section(self):
        guide = generate_posting_guide(SAMPLE_SECTIONS, "", "")
        assert "Note投稿手順" in guide

    def test_contains_image_checklist(self):
        guide = generate_posting_guide(SAMPLE_SECTIONS, "", "")
        assert "01_hero.png" in guide
        assert "06_cta.png" in guide

    def test_contains_pre_publish_checklist(self):
        guide = generate_posting_guide(SAMPLE_SECTIONS, "", "")
        assert "公開前チェックリスト" in guide
        assert "誤字脱字" in guide

    def test_contains_pricing_info(self):
        guide = generate_posting_guide(SAMPLE_SECTIONS, "", "")
        assert "12%" in guide

    def test_returns_string(self):
        guide = generate_posting_guide(SAMPLE_SECTIONS, "", "")
        assert isinstance(guide, str)


class TestSectionTitles:
    def test_hero_title(self):
        assert SECTION_TITLES["hero"] == "ファーストビュー"

    def test_cta_title(self):
        assert SECTION_TITLES["cta"] == "今すぐ手に入れる"

    def test_all_values_are_strings(self):
        for k, v in SECTION_TITLES.items():
            assert isinstance(v, str)
            assert len(v) > 0
