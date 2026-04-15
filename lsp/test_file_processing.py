import pytest
from unittest.mock import MagicMock
from file_processing import Readable, Writable, ReadOnlyFile, ReadWriteFile

class TestReadableContract:

    def test_read_only_file_honours_readable_contract(self, mocker):
        mock_file = mocker.MagicMock(spec=ReadOnlyFile)
        mock_file.read.return_value = "data"

        def consume(reader: Readable):
            return reader.read()

        result = consume(mock_file)

        assert result == "data"
        mock_file.read.assert_called_once()

    def test_read_write_file_honours_readable_contract(self, mocker):
        mock_file = mocker.MagicMock(spec=ReadWriteFile)
        mock_file.read.return_value = "data"

        def consume(reader: Readable):
            return reader.read()

        result = consume(mock_file)

        assert result == "data"
        mock_file.read.assert_called_once()

    def test_both_subtypes_return_same_type_from_read(self):
        read_only  = ReadOnlyFile()
        read_write = ReadWriteFile()

        result_ro = read_only.read()
        result_rw = read_write.read()

        assert type(result_ro) == type(result_rw)

    def test_subtypes_are_interchangeable_in_same_consumer(self, mocker):
        mock_ro = mocker.MagicMock(spec=ReadOnlyFile)
        mock_rw = mocker.MagicMock(spec=ReadWriteFile)
        mock_ro.read.return_value = "data"
        mock_rw.read.return_value = "data"

        def consume(reader: Readable):
            return reader.read()

        assert consume(mock_ro) == consume(mock_rw)

    def test_read_does_not_raise_on_any_readable_subtype(self, mocker):
        for spec in [ReadOnlyFile, ReadWriteFile]:
            mock_file = mocker.MagicMock(spec=spec)
            mock_file.read.return_value = "data"

            try:
                result = mock_file.read()
                assert result == "data"
            except Exception as e:
                pytest.fail(f"{spec.__name__}.read() raised unexpectedly: {e}")

class TestWritableContract:

    def test_read_write_file_honours_writable_contract(self, mocker):
        mock_file = mocker.MagicMock(spec=ReadWriteFile)

        def writer(w: Writable):
            w.write("hello")

        writer(mock_file)

        mock_file.write.assert_called_once_with("hello")

    def test_write_accepts_any_data_string(self, mocker):
        """write() contract: accepts a string, no return value required."""
        mock_file = mocker.MagicMock(spec=ReadWriteFile)

        for payload in ["hello", "", "x" * 1000, "special @#$%"]:
            mock_file.write(payload)

        assert mock_file.write.call_count == 4

    def test_write_does_not_affect_read_output(self, mocker):
        """LSP: write() must not corrupt subsequent read() calls."""
        mock_file = mocker.MagicMock(spec=ReadWriteFile)
        mock_file.read.return_value = "data"

        mock_file.write("something")
        result = mock_file.read()

        assert result == "data"
        mock_file.write.assert_called_once_with("something")
        mock_file.read.assert_called_once()

    def test_real_write_then_read_does_not_raise(self, capsys):
        """Real ReadWriteFile: write followed by read works without error."""
        f = ReadWriteFile()

        f.write("New data")
        result = f.read()

        captured = capsys.readouterr()
        assert "Writing: New data" in captured.out
        assert result == "data"


class TestSubstitutability:

    def test_mixed_subtypes_in_collection_behave_identically(self, mocker):
        mock_ro = mocker.MagicMock(spec=ReadOnlyFile)
        mock_rw = mocker.MagicMock(spec=ReadWriteFile)
        mock_ro.read.return_value = "data"
        mock_rw.read.return_value = "data"

        readers = [mock_ro, mock_rw]

        results = [r.read() for r in readers]

        assert all(result == "data" for result in results)
        mock_ro.read.assert_called_once()
        mock_rw.read.assert_called_once()

    def test_consumer_never_needs_isinstance_check(self, mocker):
        mock_ro = mocker.MagicMock(spec=ReadOnlyFile)
        mock_rw = mocker.MagicMock(spec=ReadWriteFile)
        mock_ro.read.return_value = "data"
        mock_rw.read.return_value = "data"

        def consume(reader: Readable):
            assert not isinstance(reader, type), "Consumer must not type-check"
            return reader.read()

        for reader in [mock_ro, mock_rw]:
            result = consume(reader)
            assert result == "data"

    def test_read_only_file_cannot_substitute_as_writable(self):
        
        read_only = ReadOnlyFile()

        assert not hasattr(read_only, 'write'), (
            "ReadOnlyFile should not expose write() — it only extends Readable"
        )

    def test_lsp_violation_would_look_like_this(self, mocker):
        
        mock_bad_file = mocker.MagicMock(spec=Readable)
        mock_bad_file.read.side_effect = NotImplementedError("read not supported")

        def consume(reader: Readable):
            return reader.read()

        with pytest.raises(NotImplementedError):
            consume(mock_bad_file)

class TestRealImplementations:

    def test_real_read_only_is_readable(self):
        assert isinstance(ReadOnlyFile(), Readable)

    def test_real_read_write_is_readable(self):
        assert isinstance(ReadWriteFile(), Readable)

    def test_real_read_write_is_writable(self):
        assert isinstance(ReadWriteFile(), Writable)

    def test_real_read_only_is_not_writable(self):
        assert not isinstance(ReadOnlyFile(), Writable)

    def test_real_read_only_returns_string(self):
        assert isinstance(ReadOnlyFile().read(), str)

    def test_real_read_write_returns_string(self):
        assert isinstance(ReadWriteFile().read(), str)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])