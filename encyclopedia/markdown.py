from copy import deepcopy
import re

# TODO: Add docstrings and type hinting to this module


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
        self.process_bold()
        self.process_links()
        self.process_paragraphs()
        return "\n".join(self.html_list)

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
        # TODO: Add other * and + as list indicators as well
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

    def process_bold(self):
        regex_pattern = r"\*{2}(.*?)\*{2}"
        for i, line in enumerate(self.markdown_list):
            if not line:
                continue

            matches = re.findall(regex_pattern, line)
            if matches:
                for match in matches:
                    self.html_list[i] = re.sub(re.escape(f"**{match}**"),
                                               f"<strong>{match}</strong>", self.html_list[i])

    def process_links(self):
        regex_pattern = r"\[(.+?)\]\((.+?)\)"
        for i, line in enumerate(self.markdown_list):
            if not line:
                continue

            matches = re.findall(regex_pattern, line)
            if matches:
                for match in matches:
                    self.html_list[i] = re.sub(re.escape(
                        f"[{match[0]}]({match[1]})"), f"<a href='{match[1]}'>{match[0]}</a>", self.html_list[i])

    def process_paragraphs(self):
        # TODO: Organize this mess
        for i, line in enumerate(self.html_list):
            if line:
                if line[0] == "<":
                    continue
                elif (i > 0) and (self.html_list[i-1][0:3] == "<p>"):
                    if i == len(self.html_list)-1:
                        self.html_list[i] = self.html_list[i] + "</p>"
                    elif (not self.html_list[i+1]) or (self.html_list[i+1][0] == "<"):
                        self.html_list[i] = self.html_list[i] + "</p>"
                    else:
                        continue
                else:
                    self.html_list[i] = "<p>" + self.html_list[i]
                if i == len(self.html_list)-1:
                    self.html_list[i] = self.html_list[i] + "</p>"
                    continue
                elif (not self.html_list[i+1]) or (self.html_list[i+1][0] == "<"):
                    self.html_list[i] = self.html_list[i] + "</p>"
