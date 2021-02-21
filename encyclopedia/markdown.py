from copy import deepcopy
import re


class Markdown():

    def __init__(self, content):
        self.markdown_list = content.split('\r\n')
        self.html_list = deepcopy(self.markdown_list)

    def markdown(self):
        list_patterns = [
            {
                "type": "unordered list",
                "regex": "^-\s",
                "lineitem_open": "<li>",
                "lineitem_close": "</li>",
                "list_open": "<ul>",
                "list_close": "</ul>"
            },
            {
                "type": "ordered list",
                "regex": "^\d.\s",
                "lineitem_open": "<li>",
                "lineitem_close": "</li>",
                "list_open": "<ol>",
                "list_close": "</ol>"
            }
        ]
        for list_pattern in list_patterns:
            self.process_lists(list_pattern)

        self.process_headers()

    def process_headers(self):
        pattern = re.compile('^(#+)\s')

        for i, line in enumerate(self.markdown_list):
            if line and line[0] == '#':
                matches = re.match(pattern, line)
                if not bool(matches):
                    continue
                h_level = min(len(matches.group(1)), 6)

                self.html_list[i] = f'<h{h_level}>' + \
                    re.sub(pattern, '', line) + f'</h{h_level}>'

    def process_lists(self, patterns):
        for i, line in enumerate(self.markdown_list):
            if not line:
                continue
            is_matched = bool(re.match(patterns["regex"], line))
            if is_matched:
                self.html_list[i] = patterns["lineitem_open"] + \
                    re.sub(patterns["regex"], '', line) + \
                    patterns["lineitem_close"]
                if (i == 0) or not bool(re.match(patterns["regex"], self.markdown_list[i-1])):
                    self.html_list[i] = patterns["list_open"] + \
                        self.html_list[i]
                if (i == len(self.markdown_list)-1) or not bool(re.match(patterns["regex"], self.markdown_list[i+1])):
                    self.html_list[i] = self.html_list[i] + \
                        patterns["list_close"]


converter = Markdown(
    '# This is a test\r\n\r\n## This is a third line\r\n- lineitem - hyphen - in \r\n- lineitem2\r\n1. oli1\r\n2. oli2')
print(converter.markdown_list)
converter.markdown()
print(converter.html_list)
