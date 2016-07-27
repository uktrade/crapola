from pytest import fixture

from process import XLSTableParser


@fixture()
def parser():
    return XLSTableParser()


def test_fixture_parser(parser):
    assert parser._row_items == []
    assert parser._next_data is False


class TestStartTag:

    def test_happy(self, parser):
        """
        Start 'td' tag sets next data
        """
        result = parser.handle_starttag('td', {'stuff': 1234})

        assert parser._next_data is True
        assert result is True

    def test_happy_not_td(self, parser):
        """
        starttag: Non-td tag does not trigger next data
        """
        result = parser.handle_starttag('a', {'stuff', 1234})

        assert parser._next_data is False
        assert result is False


class TestDataTag:

    def test_happy_set(self, parser):
        """
        Data tag in active mode saves data to the row
        """
        parser._next_data = True
        parser._row_items = ['__STUFF__']

        result = parser.handle_data('__DATA__')

        assert result is True
        assert parser._row_items == ['__STUFF__', '__DATA__']
        assert parser._next_data is False

    def test_happy_unset(self, parser):
        """
        Data tag ignores data if it's not set
        """
        parser._next_data = False
        parser._row_items = ['__STUFF__']

        result = parser.handle_data('__DATA__')

        assert result is False
        assert parser._row_items == ['__STUFF__']
        assert parser._next_data is False


class TestEndTag:

    def test_happy_tr(self, parser):
        """
        endtag: Finds tr, joins row items with comma and adds them to output
        """
        parser._row_items = ['__A__', '__B__', '__C__']
        parser._output = '__STUFF__\n'

        result = parser.handle_endtag('tr')

        assert result is True
        assert parser._output == '__STUFF__\n"__A__","__B__","__C__"\n'
        assert parser._row_items == []

    def test_happy_td_found(self, parser):
        """
        endtag: if data has been found and td closes, then does nothing
        """
        parser._row_items = []
        parser._next_data = False

        result = parser.handle_endtag('td')

        assert result is False
        assert parser._next_data is False
        assert parser._row_items == []

    def test_happy_td_not_found(self, parser):
        """
        endtag: if data has not been found and td closes, creates empty item
        """
        parser._row_items = []
        parser._next_data = True

        result = parser.handle_endtag('td')

        assert result is True
        assert parser._next_data is False
        assert parser._row_items == ['']

    def test_happy_other(self, parser):
        """
        endtag: does nothing for a
        """
        parser._row_items = ['__A__', '__B__', '__C__']
        parser._output = '__STUFF__\n'

        result = parser.handle_endtag('a')

        assert result is False
        assert parser._row_items == ['__A__', '__B__', '__C__']
        assert parser._output == '__STUFF__\n'


class TestParser:

    def test_happy(self, parser):
        data = (
            '<html><tr><td>First</td><td>Second</td><td>Third<td></tr>'
            '<tr><td>1</td><td>2</td><td>3</td></tr>'
        )

        parser.feed(data)

        expected_output = '"First","Second","Third"\n"1","2","3"\n'
        assert parser._output == expected_output

    def test_infield_comma(self, parser):
        data = (
            '<html><tr><td>First, thirst</td><td>Second, reckoned</td><td>Third<td></tr>'
            '<tr><td>1</td><td>2</td><td>3</td></tr>'
        )

        parser.feed(data)

        expected_output = '"First, thirst","Second, reckoned","Third"\n"1","2","3"\n'
        assert parser._output == expected_output
