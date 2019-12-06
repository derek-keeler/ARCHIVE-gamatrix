import io
import json

import steamingpile.formatters as spformatters
import steamingpile.interfaces as spinterfaces
import steamingpile.types as sptypes

# import steamingpile.types as types


class TestJsonFormatter:
    """Test suite that ensures the output of the JSON files/text are valid, or can handle invalid input properly."""

    def test_json_formatter_exists(self):
        """Ensure the JSON formatter exists and that it implements the expected interfaces/abstract classes."""
        val = spformatters.JsonOutputter()
        assert val
        # assert isinstance(val, type(formatters.ABCOutput))
        assert isinstance(type(val), type(spinterfaces.ICommandOutput))


class TestCsvFormatter:
    """Test suite that ensures the output of the CSV files/text are valid, or can handle invalid input properly."""

    def test_csv_formatter_exists(self):
        """Ensure the CSV formatter exists and that it implements the expected interfaces/abstract classes."""
        val = spformatters.CsvOutputter()
        assert val
        # # assert isinstance(val, type(formatters.ABCOutputter))
        assert isinstance(type(val), type(spinterfaces.ICommandOutput))
        pass


class TestTextFormatter:
    """Test suite that ensures the output of the txt files/text are valid, or can handle invalid input properly."""

    def test_txt_formatter_exists(self):
        """Ensure the txt formatter exists and that it implements the expected interfaces/abstract classes."""
        val = spformatters.TextOutputter()
        assert val
        # assert isinstance(val, formatters.ABCOutputter)
        assert isinstance(type(val), type(spinterfaces.ICommandOutput))

    def test_txt_formatter_output(self):
        """Ensure the text formatter outputs some valid information."""
        fmtr = spformatters.TextOutputter()
        assert fmtr
        fmtr.information = [
            sptypes.FriendInformation(name="foo", user_id="100"),
            sptypes.GameInformation(title="bar", appid="200"),
        ]
        stream = io.StringIO()
        fmtr.write(stream=stream)
        stream.seek(0)
        output = "".join(stream.readlines())
        assert len(output)
        assert "FriendInformation" in output
        assert "GameInformation" in output
        assert "foo" in output
        assert "bar" in output
        assert "100" in output
        assert "200" in output

    def test_json_formatter_output(self):
        """Ensure the json formatter outputs some valid information."""
        fmtr = spformatters.JsonOutputter()
        assert fmtr
        fmtr.information = [
            sptypes.FriendInformation(name="foo", user_id="100"),
            sptypes.GameInformation(title="bar", appid="200"),
            sptypes.GameInformation(title="biz", appid="300"),
        ]
        stream = io.StringIO()
        fmtr.write(stream=stream)
        stream.seek(0)
        output = "".join(stream.readlines())

        assert len(output)
        assert "FriendInformation" in output
        assert "GameInformation" in output
        assert "foo" in output
        assert "bar" in output
        assert "100" in output
        assert "200" in output
        assert "200" in output

        jsondata = json.loads(output)
        assert len(jsondata["FriendInformation"]) == 1
        assert len(jsondata["GameInformation"]) == 2
        assert jsondata

    def test_csv_formatter_output(self):
        """Ensure the CSV formatter outputs some valid information."""
        fmtr = spformatters.CsvOutputter()
        assert fmtr
        fmtr.information = [
            sptypes.FriendInformation(name="foo", user_id="100"),
            sptypes.GameInformation(title="bar", appid="200"),
            sptypes.GameInformation(title="biz", appid="300"),
        ]
        stream = io.StringIO()
        fmtr.write(stream=stream)
        stream.seek(0)
        output = "".join(stream.readlines())
        print(output)
        assert len(output)
        assert "foo" in output
        assert "bar" in output
        assert "100" in output
        assert "200" in output
        assert "200" in output
