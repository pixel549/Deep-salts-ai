"""
Thin wrapper around the Gemini API for structured-output calls. Swapped in from
the original Anthropic version -- the public function, call_structured(role,
system_prompt, user_content, schema_name) -> dict, is unchanged, so nothing in
turn_loop.py or session_end.py needed to change.

Each role reads its API key from its own env var (config/models.json's
"api_key_env" field), defaulting all roles to the same GEMINI_API_KEY. That
means one free key works out of the box -- but if you ever want separate quota
pools per role, point specific roles at their own env var and add that as a
second GitHub secret. Note: a second *key* only gets you a second quota pool if
it comes from a different Google Cloud project (or account) than the first --
generating more keys under the same project does not multiply your quota.

Docs: https://ai.google.dev/gemini-api/docs/structured-output
Gemini's API has been changing fast lately (model deprecations, free-tier
rules) -- if a model name in config/models.json 404s, check the current model
list before assuming the code is wrong.
"""

import json
import os
import time
from pathlib import Path

from google import genai
from google.genai import types
from google.genai import errors as genai_errors

ROOT = Path(__file__).resolve().parent.parent
SCHEMAS_DIR = ROOT / "schemas"
CONFIG_PATH = ROOT / "config" / "models.json"

_clients_by_key: dict[str, genai.Client] = {}

MAX_RETRIES = 3
RETRY_BACKOFF_SECONDS = [5, 20, 60]  # this is a set-and-forget system; nobody's
# there to hit retry on a transient free-tier rate limit, so we do it for them.


def load_model_config() -> dict:
    with open(CONFIG_PATH) as f:
        return json.load(f)


def load_schema(name: str) -> dict:
    path = SCHEMAS_DIR / f"{name}.schema.json"
    with open(path) as f:
        return json.load(f)


def get_client(api_key_env: str) -> genai.Client:
    api_key = os.environ.get(api_key_env)
    if not api_key:
        raise RuntimeError(
            f"Environment variable {api_key_env} is not set. "
            f"Set it locally or add it as a GitHub Actions secret."
        )
    if api_key not in _clients_by_key:
        _clients_by_key[api_key] = genai.Client(api_key=api_key)
    return _clients_by_key[api_key]


def _is_retryable(exc: Exception) -> bool:
    # Free-tier rate limits and transient server errors -- both worth a retry
    # in an unattended run. Everything else (bad schema, bad key) should fail
    # loudly instead of silently retrying a request that will never succeed.
    status = getattr(exc, "code", None) or getattr(exc, "status_code", None)
    text = str(exc)
    return status in (429, 500, 503) or "RESOURCE_EXHAUSTED" in text or "429" in text


def call_structured(role: str, system_prompt: str, user_content: str, schema_name: str) -> dict:
    """
    Make one structured-output call for a given agent role.

    role: key into config/models.json ('gm', 'player_a', 'player_b', 'god', 'dm_adjudication')
    system_prompt: the role's system prompt text (already filled with any templates)
    user_content: the actual turn context (state, memory, narration so far, etc.)
    schema_name: which schema in schemas/ to enforce on the response

    Returns a parsed dict matching the schema.
    """
    models = load_model_config()
    role_cfg = models[role]
    schema = load_schema(schema_name)

    client = get_client(role_cfg.get("api_key_env", "GEMINI_API_KEY"))

    config = types.GenerateContentConfig(
        system_instruction=system_prompt,
        max_output_tokens=role_cfg["max_tokens"],
        response_mime_type="application/json",
        response_json_schema=schema,
        # Gemini 3.x models think by default, and thinking tokens count
        # against the SAME max_output_tokens budget as the visible answer --
        # combined, not separate, despite what older docs implied. Without
        # this, a chunk of the budget silently goes to invisible reasoning
        # and the actual JSON can get cut off mid-string (JSONDecodeError:
        # Unterminated string). MINIMAL is appropriate here -- structured
        # JSON generation from a fully-specified schema isn't a task that
        # benefits from extended reasoning.
        thinking_config=types.ThinkingConfig(
            thinking_level=types.ThinkingLevel.MINIMAL
        ),
    )

    last_exc = None
    for attempt in range(MAX_RETRIES):
        try:
            response = client.models.generate_content(
                model=role_cfg["model"],
                contents=user_content,
                config=config,
            )
            return json.loads(response.text)
        except genai_errors.APIError as exc:
            last_exc = exc
            if not _is_retryable(exc) or attempt == MAX_RETRIES - 1:
                raise
            wait = RETRY_BACKOFF_SECONDS[min(attempt, len(RETRY_BACKOFF_SECONDS) - 1)]
            print(f"[{role}] retryable error ({exc}), waiting {wait}s (attempt {attempt + 1}/{MAX_RETRIES})")
            time.sleep(wait)

    raise last_exc
