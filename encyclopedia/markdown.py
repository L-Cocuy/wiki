from copy import deepcopy
import re


class Markdown():

    def __init__(self, content):
        self.markdown_list = content.split('\r\n')
        self.html_list = deepcopy(self.markdown_list)

    def process_headers(self):
        pattern = re.compile('^(#+)\s')
        for i, line in enumerate(self.markdown_list):
            if line and line[0] == '#':
                matches = re.match(pattern, line)
                h_level = min(len(matches.group(1)), 6)

                self.html_list[i] = f'<h{h_level}>' + \
                    re.sub(pattern, '', line) + f'</h{h_level}>'


converter = Markdown('# This is a test\r\n\r\n### This is a third line')
print(converter.markdown_list)
converter.process_headers()
print(converter.html_list)
