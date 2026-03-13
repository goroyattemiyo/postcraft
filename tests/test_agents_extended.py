"""agents.py の拡張テスト（max_tokens引数）"""

from unittest.mock import MagicMock

from synapse.agents import run_agent
from synapse.config import MAX_TOKENS


def test_run_agent_default_max_tokens():
    """max_tokens未指定時はMAX_TOKENSが使われる"""
    mock_client = MagicMock()
    block = MagicMock()
    block.type = "text"
    block.text = "response"
    response = MagicMock()
    response.stop_reason = "end_turn"
    response.content = [block]
    mock_client.messages.create.return_value = response

    sandbox = MagicMock()
    log_fn = MagicMock()

    run_agent(
        mock_client, "model", "system", [{"role": "user", "content": "hi"}], None, sandbox, log_fn
    )

    call_kwargs = mock_client.messages.create.call_args
    assert call_kwargs[1]["max_tokens"] == MAX_TOKENS


def test_run_agent_custom_max_tokens():
    """max_tokens指定時はその値が使われる"""
    mock_client = MagicMock()
    block = MagicMock()
    block.type = "text"
    block.text = "response"
    response = MagicMock()
    response.stop_reason = "end_turn"
    response.content = [block]
    mock_client.messages.create.return_value = response

    sandbox = MagicMock()
    log_fn = MagicMock()

    run_agent(
        mock_client,
        "model",
        "system",
        [{"role": "user", "content": "hi"}],
        None,
        sandbox,
        log_fn,
        max_tokens=16384,
    )

    call_kwargs = mock_client.messages.create.call_args
    assert call_kwargs[1]["max_tokens"] == 16384
