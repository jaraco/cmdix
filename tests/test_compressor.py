import io
import types

import pytest

from cmdix import compressor
from cmdix.exception import StdErrException, StdOutException


def fake_compresstype(path, mode, compresslevel=None):
    return io.BytesIO(b'payload')


def test_decompress_derives_output_name_from_the_file_name(tmp_path):
    """The output name comes from the file name, not from the open file."""
    source = tmp_path / 'data.txt.gz'
    source.write_bytes(b'payload')
    args = types.SimpleNamespace(
        FILE=['data.txt.gz'], stdout=False, compresslevel=9, prog='gunzip'
    )

    infile, outfile = compressor.decompress(args, fake_compresstype, str(source), '.gz')

    assert outfile.name == str(tmp_path / 'data.txt')
    outfile.close()
    infile.close()


def test_decompress_refuses_to_overwrite(tmp_path, monkeypatch):
    """Declining the overwrite prompt is an error, not a silent no-op."""
    source = tmp_path / 'data.txt.gz'
    source.write_bytes(b'payload')
    (tmp_path / 'data.txt').write_bytes(b'existing')
    args = types.SimpleNamespace(
        FILE=['data.txt.gz'], stdout=False, compresslevel=9, prog='gunzip'
    )
    monkeypatch.setattr('builtins.input', lambda prompt='': 'n')

    with pytest.raises(StdOutException):
        compressor.decompress(args, fake_compresstype, str(source), '.gz')


def test_compress_refuses_to_overwrite(tmp_path, monkeypatch):
    """Declining the overwrite prompt is an error, not a silent no-op."""
    source = tmp_path / 'data.txt'
    source.write_bytes(b'payload')
    (tmp_path / 'data.txt.gz').write_bytes(b'existing')
    args = types.SimpleNamespace(
        FILE=['data.txt'], stdout=False, compresslevel=9, prog='gzip'
    )
    monkeypatch.setattr('builtins.input', lambda prompt='': 'n')

    with pytest.raises(StdErrException):
        compressor.compress(args, fake_compresstype, str(source), None, '.gz')
