"""lp_engine.py のテスト（mock API）"""

from unittest.mock import MagicMock, patch

from synapse.lp_engine import run_synapse_lp


def _make_mock_response(text, stop_reason="end_turn"):
    """モックレスポンスを生成"""
    block = MagicMock()
    block.type = "text"
    block.text = text
    response = MagicMock()
    response.stop_reason = stop_reason
    response.content = [block]
    return response


@patch("synapse.lp_engine.anthropic")
@patch("synapse.lp_engine.load_dotenv")
def test_lp_engine_phase_a_approved(mock_dotenv, mock_anthropic_mod):
    """Phase A でHTMLが承認されるフロー"""
    mock_client = MagicMock()
    mock_anthropic_mod.Anthropic.return_value = mock_client

    # Orchestrator → Coder → Reviewer の順で応答
    mock_client.messages.create.side_effect = [
        _make_mock_response("LP設計: ターゲットは初心者..."),
        _make_mock_response("lp.htmlを生成しました"),
        _make_mock_response("構造チェック全パス。APPROVED"),
        _make_mock_response("ドラフトを生成しました"),
        _make_mock_response("ドラフト検証OK。APPROVED"),
    ]

    result = run_synapse_lp("テスト商品 価格1000円")

    assert result["phase_a_approved"] is True
    assert result["phase_b_approved"] is True
    assert result["approved"] is True
    assert result["rounds"] == 1


@patch("synapse.lp_engine.anthropic")
@patch("synapse.lp_engine.load_dotenv")
def test_lp_engine_phase_a_rejected_then_approved(mock_dotenv, mock_anthropic_mod):
    """Phase A で1回リジェクトされてから承認されるフロー"""
    mock_client = MagicMock()
    mock_anthropic_mod.Anthropic.return_value = mock_client

    mock_client.messages.create.side_effect = [
        _make_mock_response("LP設計完了"),
        _make_mock_response("lp.html生成"),
        _make_mock_response("CTAボタンがない。修正してください"),
        _make_mock_response("lp.html修正完了"),
        _make_mock_response("APPROVED"),
        _make_mock_response("ドラフト生成完了"),
        _make_mock_response("APPROVED"),
    ]

    result = run_synapse_lp("テスト商品")

    assert result["phase_a_approved"] is True
    assert result["rounds"] == 2


@patch("synapse.lp_engine.anthropic")
@patch("synapse.lp_engine.load_dotenv")
def test_lp_engine_phase_a_never_approved(mock_dotenv, mock_anthropic_mod):
    """Phase A で承認されずPhase Bに進まないフロー"""
    mock_client = MagicMock()
    mock_anthropic_mod.Anthropic.return_value = mock_client

    mock_client.messages.create.side_effect = [
        _make_mock_response("LP設計完了"),
        _make_mock_response("lp.html生成"),
        _make_mock_response("セクション不足。修正必要"),
        _make_mock_response("lp.html修正"),
        _make_mock_response("まだ不足。修正必要"),
        _make_mock_response("lp.html再修正"),
        _make_mock_response("まだダメ。修正必要"),
    ]

    result = run_synapse_lp("テスト商品")

    assert result["phase_a_approved"] is False
    assert result["phase_b_approved"] is False
    assert result["approved"] is False


@patch("synapse.lp_engine.anthropic")
@patch("synapse.lp_engine.load_dotenv")
def test_lp_engine_error_handling(mock_dotenv, mock_anthropic_mod):
    """API呼び出しでエラーが発生した場合"""
    mock_client = MagicMock()
    mock_anthropic_mod.Anthropic.return_value = mock_client
    mock_client.messages.create.side_effect = Exception("API Error")

    result = run_synapse_lp("テスト商品")

    assert "error" in result
    assert result["approved"] is False


@patch("synapse.lp_engine.anthropic")
@patch("synapse.lp_engine.load_dotenv")
def test_lp_engine_callback_called(mock_dotenv, mock_anthropic_mod):
    """callbackが正しく呼ばれるか"""
    mock_client = MagicMock()
    mock_anthropic_mod.Anthropic.return_value = mock_client
    mock_callback = MagicMock()

    mock_client.messages.create.side_effect = [
        _make_mock_response("LP設計完了"),
        _make_mock_response("HTML生成完了"),
        _make_mock_response("APPROVED"),
        _make_mock_response("ドラフト生成完了"),
        _make_mock_response("APPROVED"),
    ]

    run_synapse_lp("テスト商品", callback=mock_callback)

    assert mock_callback.call_count > 0
    agents_called = [call[0][0] for call in mock_callback.call_args_list]
    assert "System" in agents_called
    assert "Orchestrator" in agents_called
