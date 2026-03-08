"""Tests for the http_client built-in skill."""

from __future__ import annotations

import pytest
import httpx

from skills.base import SkillContext, SkillResult
from skills.builtin.http_client import HttpClientSkill
from skills.registry import SkillRegistry


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_ctx() -> SkillContext:
    return SkillContext(agent_id="test", job_id="j1")


def make_response(
    status_code: int = 200,
    content: bytes = b"ok",
    headers: dict | None = None,
) -> httpx.Response:
    return httpx.Response(
        status_code=status_code,
        content=content,
        headers=headers or {"content-type": "text/plain"},
    )


def make_json_response(data: dict, status_code: int = 200) -> httpx.Response:
    import json
    body = json.dumps(data).encode()
    return httpx.Response(
        status_code=status_code,
        content=body,
        headers={"content-type": "application/json"},
    )


# ---------------------------------------------------------------------------
# Metadata
# ---------------------------------------------------------------------------

class TestHttpClientSkillMeta:
    def test_name(self):
        assert HttpClientSkill.name == "http_client"

    def test_description_not_empty(self):
        assert len(HttpClientSkill.description) > 10

    def test_registry_discovers_skill(self):
        reg = SkillRegistry()
        reg.discover()
        assert reg.get("http_client") is not None


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

class TestHttpClientValidation:
    async def test_missing_url_fails(self):
        skill = HttpClientSkill()
        result = await skill.execute(make_ctx(), {"action": "get"})
        assert result.success is False
        assert "url" in result.error.lower()

    async def test_invalid_url_fails(self, monkeypatch):
        skill = HttpClientSkill()
        async def _bad(*_, **__):
            raise httpx.InvalidURL("not a url")

        monkeypatch.setattr(httpx.AsyncClient, "request", _bad)
        result = await skill.execute(make_ctx(), {"action": "get", "url": "not-a-url"})
        assert result.success is False


# ---------------------------------------------------------------------------
# GET requests
# ---------------------------------------------------------------------------

class TestHttpClientGet:
    async def test_get_success(self, monkeypatch):
        skill = HttpClientSkill()
        resp = make_response(200, b"hello world")

        async def _mock_request(self_client, method, url, **kwargs):
            assert method == "GET"
            return resp

        monkeypatch.setattr(httpx.AsyncClient, "request", _mock_request)
        result = await skill.execute(make_ctx(), {"action": "get", "url": "http://example.com"})
        assert result.success is True
        assert result.output["status"] == 200
        assert result.output["ok"] is True
        assert result.output["text"] == "hello world"

    async def test_get_404_still_succeeds(self, monkeypatch):
        """A 404 response is not a skill failure — it's valid HTTP."""
        skill = HttpClientSkill()
        resp = make_response(404, b"not found")

        async def _mock_request(self_client, method, url, **kwargs):
            return resp

        monkeypatch.setattr(httpx.AsyncClient, "request", _mock_request)
        result = await skill.execute(make_ctx(), {"action": "get", "url": "http://example.com/missing"})
        assert result.success is True
        assert result.output["status"] == 404
        assert result.output["ok"] is False

    async def test_json_response_parsed(self, monkeypatch):
        skill = HttpClientSkill()
        resp = make_json_response({"items": [1, 2, 3]})

        async def _mock_request(self_client, method, url, **kwargs):
            return resp

        monkeypatch.setattr(httpx.AsyncClient, "request", _mock_request)
        result = await skill.execute(make_ctx(), {"action": "get", "url": "http://api.example.com/items"})
        assert result.success is True
        assert result.output["json"] == {"items": [1, 2, 3]}

    async def test_latency_ms_present(self, monkeypatch):
        skill = HttpClientSkill()
        resp = make_response(200, b"hi")

        async def _mock_request(self_client, method, url, **kwargs):
            return resp

        monkeypatch.setattr(httpx.AsyncClient, "request", _mock_request)
        result = await skill.execute(make_ctx(), {"action": "get", "url": "http://example.com"})
        assert "latency_ms" in result.output
        assert isinstance(result.output["latency_ms"], (int, float))


# ---------------------------------------------------------------------------
# POST requests
# ---------------------------------------------------------------------------

class TestHttpClientPost:
    async def test_post_sends_json_body(self, monkeypatch):
        skill = HttpClientSkill()
        captured = {}
        resp = make_json_response({"created": True}, status_code=201)

        async def _mock_request(self_client, method, url, **kwargs):
            captured["method"] = method
            captured["json"] = kwargs.get("json")
            return resp

        monkeypatch.setattr(httpx.AsyncClient, "request", _mock_request)
        result = await skill.execute(make_ctx(), {
            "action": "post",
            "url": "http://api.example.com/create",
            "body": {"name": "test"},
        })
        assert result.success is True
        assert captured["method"] == "POST"
        assert captured["json"] == {"name": "test"}
        assert result.output["status"] == 201

    async def test_http_action_with_explicit_method(self, monkeypatch):
        skill = HttpClientSkill()
        captured_method = []
        resp = make_response(200, b"ok")

        async def _mock_request(self_client, method, url, **kwargs):
            captured_method.append(method)
            return resp

        monkeypatch.setattr(httpx.AsyncClient, "request", _mock_request)
        result = await skill.execute(make_ctx(), {
            "action": "http",
            "method": "DELETE",
            "url": "http://api.example.com/resource/1",
        })
        assert result.success is True
        assert captured_method[0] == "DELETE"


# ---------------------------------------------------------------------------
# Ping
# ---------------------------------------------------------------------------

class TestHttpClientPing:
    async def test_ping_reachable(self, monkeypatch):
        skill = HttpClientSkill()
        resp = make_response(200, b"")

        async def _mock_request(self_client, method, url, **kwargs):
            assert method == "HEAD"
            return resp

        monkeypatch.setattr(httpx.AsyncClient, "request", _mock_request)
        result = await skill.execute(make_ctx(), {"action": "ping", "url": "http://example.com"})
        assert result.success is True
        assert result.output["ok"] is True
        assert result.output["status"] == 200
        # Ping should NOT include body text
        assert "text" not in result.output

    async def test_ping_timeout_fails(self, monkeypatch):
        skill = HttpClientSkill()

        async def _mock_request(self_client, method, url, **kwargs):
            raise httpx.TimeoutException("timed out", request=None)

        monkeypatch.setattr(httpx.AsyncClient, "request", _mock_request)
        result = await skill.execute(make_ctx(), {
            "action": "ping",
            "url": "http://unreachable.example.com",
            "timeout": 1.0,
        })
        assert result.success is False
        assert "timed out" in result.error.lower() or "timeout" in result.error.lower()


# ---------------------------------------------------------------------------
# Headers forwarding
# ---------------------------------------------------------------------------

class TestHttpClientHeaders:
    async def test_custom_headers_sent(self, monkeypatch):
        skill = HttpClientSkill()
        captured_headers = {}
        resp = make_response(200, b"ok")

        async def _mock_request(self_client, method, url, **kwargs):
            captured_headers.update(kwargs.get("headers", {}))
            return resp

        monkeypatch.setattr(httpx.AsyncClient, "request", _mock_request)
        await skill.execute(make_ctx(), {
            "action": "get",
            "url": "http://api.example.com",
            "headers": {"Authorization": "Bearer token123"},
        })
        assert captured_headers.get("Authorization") == "Bearer token123"
