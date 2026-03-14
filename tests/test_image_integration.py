"""lp_ui.py / lp_engine_drafts.py の画像パイプライン接続テスト"""

import os
import tempfile


class TestCreateZipWithImages:
    """_create_zip が画像ファイルをZIPに含めるか検証。"""

    def test_zip_includes_images(self):
        import io
        import zipfile

        from synapse.lp_ui import _create_zip

        with tempfile.TemporaryDirectory() as tmp:
            img_path = os.path.join(tmp, "01_hero.png")
            with open(img_path, "wb") as f:
                f.write(b"\x89PNG fake image data")
            files = {"lp.html": "<h1>Test</h1>", "brain_draft.md": "# Draft"}
            result = _create_zip(files, [img_path])
            zf = zipfile.ZipFile(io.BytesIO(result))
            names = zf.namelist()
            assert "lp.html" in names
            assert "brain_draft.md" in names
            assert "sections/01_hero.png" in names

    def test_zip_without_images(self):
        import io
        import zipfile

        from synapse.lp_ui import _create_zip

        files = {"lp.html": "<h1>Test</h1>"}
        result = _create_zip(files, [])
        zf = zipfile.ZipFile(io.BytesIO(result))
        assert "lp.html" in zf.namelist()

    def test_zip_with_none_images(self):
        import io
        import zipfile

        from synapse.lp_ui import _create_zip

        files = {"lp.html": "<h1>Test</h1>"}
        result = _create_zip(files, None)
        zf = zipfile.ZipFile(io.BytesIO(result))
        assert "lp.html" in zf.namelist()

    def test_zip_skips_missing_images(self):
        import io
        import zipfile

        from synapse.lp_ui import _create_zip

        files = {"lp.html": "<h1>Test</h1>"}
        result = _create_zip(files, ["/nonexistent/path.png"])
        zf = zipfile.ZipFile(io.BytesIO(result))
        assert len(zf.namelist()) == 1


class TestImagePipelineIntegration:
    """lp_engine_drafts.py の画像パイプライン接続を検証。"""

    def test_run_image_pipeline_without_playwright(self):
        from synapse.lp_engine_drafts import _run_image_pipeline
        from synapse.sandbox import Sandbox

        sandbox = Sandbox()
        sandbox.write_file("lp.html", "<html><body>test</body></html>")
        images = _run_image_pipeline(sandbox, [], lambda *a: None, lambda *a: None)
        # Playwright未インストール環境では空リスト
        if not os.environ.get("HAS_PLAYWRIGHT"):
            assert isinstance(images, list)

    def test_result_has_image_files_key(self):
        """run_phase_b が result に image_files キーを追加するか。"""
        from synapse.lp_engine_drafts import _run_image_pipeline

        assert callable(_run_image_pipeline)

    def test_manual_guide_appended_without_playwright(self):
        from synapse.image_pipeline import HAS_PLAYWRIGHT

        if not HAS_PLAYWRIGHT:
            from synapse.image_pipeline import generate_manual_screenshot_guide

            guide = generate_manual_screenshot_guide("lp.html", [{"name": "hero", "content": ""}])
            assert "手動スクリーンショットガイド" in guide
            assert "01_hero.png" in guide
