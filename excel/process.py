import argparse

from html.parser import HTMLParser


class XLSTableParser(HTMLParser):

    def __init__(self, *args):
        super().__init__(*args)
        self._output = ''
        self._row_items = []
        self._next_data = False  # Flag that next data should be added to output

    def handle_starttag(self, tag, attrs):
        if tag != 'td':
            return False
        self._next_data = True
        return True

    def handle_data(self, data):
        """
        Grab data into row items if `_next_data` is set.
        """
        if not self._next_data:
            return False
        self._row_items.append(data)
        self._next_data = False
        return True

    def handle_endtag(self, tag):
        """
        If tag is tr, then output the current row's items
        If tag is td, then check if data was found... if non, then pad.
        """
        if tag == 'td':
            if self._next_data:
                self._row_items.append('')
                self._next_data = False
                return True

        elif tag == 'tr':
            self._output += '"{0}"'.format('","'.join(self._row_items))
            self._output += '\n'
            self._row_items = []
            return True

        return False


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('xls')
    args = arg_parser.parse_args()

    parser = XLSTableParser()

    with open(args.xls, encoding='utf-16') as source:
        parser.feed(source.read())

    print(parser._output)
