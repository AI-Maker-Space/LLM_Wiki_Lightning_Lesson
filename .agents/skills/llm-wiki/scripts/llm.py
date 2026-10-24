"""Provider-agnostic LLM client for the wiki pipeline.

The wiki is stateless: the LLM writes each Markdown page directly (see prompts.py), and the pages
under wiki/ are the only source of truth. This client just returns the model's text (or parses a
small JSON payload for the query-selection and relationship-planning prompts).

Configuration (all via environment):
  LLM_PROVIDER   "anthropic" (default) or "openai"
  LLM_MODEL      model id. Defaults to claude-opus-5-5 for anthropic; REQUIRED for openai.
  ANTHROPIC_API_KEY / OPENAI_API_KEY   credentials for the chosen provider.
"""

from __future__ import annotations

import json
import os
import re

DEFAULT_ANTHROPIC_MODEL = "claude-opus-5-5"


class LLMError(RuntimeError):
    """Raised when the model call or its JSON response cannot be used."""


def model_id() -> str:
    """The model id this run will use, honouring LLM_MODEL / LLM_PROVIDER."""
    provider = os.environ.get("LLM_PROVIDER", "anthropic").lower()
    model = os.environ.get("LLM_MODEL")
    if model:
        return model
    if provider == "openai":
        raise LLMError("LLM_MODEL is required when LLM_PROVIDER=openai.")
    return DEFAULT_ANTHROPIC_MODEL


def _extract_json(text: str):
    """Parse a JSON object/array from model text, tolerating ```json fences and prose."""
    text = text.strip()
    fence = re.search(r"```(?:json)?\s*(.*?)```", text, re.DOTALL)
    if fence:
        text = fence.group(1).strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    # Fall back to the first balanced {...} or [...] span.
    for opener, closer in (("{", "}"), ("[", "]")):
        start = text.find(opener)
        if start == -1:
            continue
        depth = 0
        for i in range(start, len(text)):
            if text[i] == opener:
                depth += 1
            elif text[i] == closer:
                depth -= 1
                if depth == 0:
                    try:
                        return json.loads(text[start : i + 1])
                    except json.JSONDecodeError:
                        break
    raise LLMError(f"Model did not return parseable JSON:\n{text[:500]}")


def complete_json(system: str, user: str, max_tokens: int = 16000):
    """Send one request and return the parsed JSON the prompt asked for."""
    return _extract_json(complete_text(system, user, max_tokens, _json=True))


def complete_text(system: str, user: str, max_tokens: int = 16000, _json: bool = False) -> str:
    """Send one request and return the raw text response (used for prose answers like query)."""
    provider = os.environ.get("LLM_PROVIDER", "anthropic").lower()
    if provider == "anthropic":
        return _anthropic(system, user, max_tokens)
    if provider == "openai":
        return _openai(system, user, max_tokens, _json=_json)
    raise LLMError(f"Unknown LLM_PROVIDER: {provider!r} (use 'anthropic' or 'openai').")


def _anthropic(system: str, user: str, max_tokens: int):
    try:
        import anthropic
    except ImportError as exc:  # pragma: no cover - environment dependent
        raise LLMError("The 'anthropic' package is not installed (pip install anthropic).") from exc
    try:
        client = anthropic.Anthropic()
        resp = client.messages.create(
            model=model_id(),
            max_tokens=max_tokens,
            system=system,
            messages=[{"role": "user", "content": user}],
        )
    except anthropic.AuthenticationError as exc:
        raise LLMError("Anthropic auth failed. Set ANTHROPIC_API_KEY or run `ant auth login`.") from exc
    except anthropic.APIError as exc:  # pragma: no cover - network dependent
        raise LLMError(f"Anthropic API error: {exc}") from exc
    if resp.stop_reason == "refusal":
        raise LLMError("Model refused the request.")
    return "".join(b.text for b in resp.content if b.type == "text")


def _openai(system: str, user: str, max_tokens: int, _json: bool = False) -> str:
    try:
        import openai
    except ImportError as exc:  # pragma: no cover - environment dependent
        raise LLMError("The 'openai' package is not installed (pip install openai).") from exc
    kwargs = {"response_format": {"type": "json_object"}} if _json else {}
    try:
        client = openai.OpenAI()
        resp = client.chat.completions.create(
            model=model_id(),
            max_tokens=max_tokens,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            **kwargs,
        )
    except openai.AuthenticationError as exc:
        raise LLMError("OpenAI auth failed. Set OPENAI_API_KEY.") from exc
    except openai.OpenAIError as exc:  # pragma: no cover - network dependent
        raise LLMError(f"OpenAI API error: {exc}") from exc
    return resp.choices[0].message.content or ""
