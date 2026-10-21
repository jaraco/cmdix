import io
import types
from unittest import mock

from cmdix.command import wget


class FakeResponse(io.BytesIO):
    """A response object exposing the headers wget reads."""

    def __init__(self, payload):
        super().__init__(payload)
        self.headers = {'content-length': str(len(payload))}


def test_wget_writes_the_document_verbatim(monkeypatch, tmp_path):
    """The downloaded bytes are written as-is, not decoded as text."""
    payload = b'\x00\xff\xfe binary payload'
    opener = mock.Mock()
    opener.open.return_value = FakeResponse(payload)
    monkeypatch.setattr(wget, 'build_opener', lambda: opener)

    target = tmp_path / 'out.bin'
    args = types.SimpleNamespace(
        url=['http://example.invalid/out.bin'],
        outputdocument=str(target),
        useragent=None,
    )
    wget.func(args)

    assert target.read_bytes() == payload
