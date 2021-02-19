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

    def process_lists(self):
        pattern = re.compile('^-\s')

        for i, line in enumerate(self.markdown_list):

            if line and line[0:2] == '- ':
                self.html_list[i] = f'<li>' + \
                    re.sub(pattern, '', line) + f'</li>'

                if i == 0:
                    self.html_list[i] = '<ul>' + self.html_list[i]
                elif self.markdown_list[i-1][0:2] != '- ':
                    self.html_list[i] = '<ul>' + self.html_list[i]

                if i == len(self.markdown_list)-1:
                    self.html_list[i] = self.html_list[i] + '</ul>'
                elif self.markdown_list[i+1][0:2] != '- ':
                    self.html_list[i] = self.html_list[i] + '</ul>'


converter = Markdown(
    '# This is a test\r\n\r\nThis is a third line\r\n- lineitem\r\n- lineitem2')
print(converter.markdown_list)
converter.process_headers()
converter.process_lists()
print(converter.html_list)
