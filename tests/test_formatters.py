import steamingpile.formatters as formatters
import steamingpile.interfaces as interfaces

# import steamingpile.types as types


class TestJsonFormatter:
    """Test suite that ensures the output of the JSON files/text are valid, or can handle invalid input properly."""

    def test_json_formatter_exists(self):
        """Ensure the JSON formatter exists and that it implements the expected interfaces/abstract classes."""
        val = formatters.JsonOutputter()
        assert val
        # assert isinstance(val, type(formatters.ABCOutput))
        assert isinstance(type(val), type(interfaces.ICommandOutput))


class TestCsvFormatter:
    """Test suite that ensures the output of the CSV files/text are valid, or can handle invalid input properly."""

    def test_csv_formatter_exists(self):
        """Ensure the CSV formatter exists and that it implements the expected interfaces/abstract classes."""
        val = formatters.CsvOutputter()
        assert val
        # # assert isinstance(val, type(formatters.ABCOutputter))
        assert isinstance(type(val), type(interfaces.ICommandOutput))
        pass


class TestTextFormatter:
    """Test suite that ensures the output of the txt files/text are valid, or can handle invalid input properly."""

    def test_txt_formatter_exists(self):
        """Ensure the txt formatter exists and that it implements the expected interfaces/abstract classes."""
        val = formatters.TextOutputter()
        assert val
        # assert isinstance(val, formatters.ABCOutputter)
        assert isinstance(type(val), type(interfaces.ICommandOutput))
