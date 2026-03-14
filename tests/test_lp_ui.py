"""lp_ui.py のテスト"""

from synapse.lp_ui import _create_zip, render_lp_mode, render_mode_selector


class TestCreateZip:
    def test_creates_valid_zip(self):
        import io
        import zipfile

        files = {"test.html": "<h1>Hello</h1>", "draft.md": "# Draft"}
        data = _create_zip(files)
        assert isinstance(data, bytes)
        assert len(data) > 0
        zf = zipfile.ZipFile(io.BytesIO(data))
        assert set(zf.namelist()) == {"test.html", "draft.md"}

    def test_empty_files(self):
        data = _create_zip({})
        assert isinstance(data, bytes)

    def test_zip_content_matches(self):
        import io
        import zipfile

        files = {"hello.txt": "world"}
        data = _create_zip(files)
        zf = zipfile.ZipFile(io.BytesIO(data))
        assert zf.read("hello.txt").decode("utf-8") == "world"


class TestRenderFunctions:
    def test_render_lp_mode_is_callable(self):
        assert callable(render_lp_mode)

    def test_render_mode_selector_is_callable(self):
        assert callable(render_mode_selector)
