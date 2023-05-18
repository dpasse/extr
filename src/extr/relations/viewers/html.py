from typing import List, Optional

from ...models import Relation
from ...entities.viewers.html import __TEMPLATE__
from ..annotator import HtmlRelationAnnotator

class HtmlViewer:
    __TEMPLATE = __TEMPLATE__ \
        .replace(
            '{{body}}',
            """        <table>
{{body}}
        </table>"""
        )

    __DEFAULT_STYLES = """
table { width: 100%; }
span.entity { border: 1px solid black; border-radius: 5px; padding: 5px; margin: 3px; cursor: pointer; }
span.label { font-weight: bold; padding: 3px; color: black; }
span.e1 { background-color: aqua; }
span.e2 { background-color: coral; }
tr.delete { background-color: black !important; }
tr.delete span { background-color: black !important; }
td { line-height: 30px; border: 1px solid black; padding: 5px; }
td.header { font-weight: bold; }
td.label { font-weight: bold; text-align: center; }
"""

    def __init__(self) -> None:
        self._relation_index = 0
        self._rows: List[str] = []
        self._annotator = HtmlRelationAnnotator()

    def append_header(self, header: str) -> None:
        self._rows.append(
            '<tr>' + \
                f'<td class="header" colspan=3>{header}</td>' + \
            '</tr>'
        )

    def append_relation(self, text: str, relation: Relation) -> None:
        index = self._relation_index
        annotation = self._annotator.annotate(text, relation)
        self._rows.append(
            f'<tr id="{index}">' + \
                f'<td>{index}</td>' + \
                f'<td class="label">{relation.label}</td>' + \
                f'<td>{annotation}</td>' + \
            '</tr>'
        )

        self._relation_index += 1

    def create_view(self, custom_styles: Optional[str] = None) -> str:
        styles = self.__DEFAULT_STYLES.strip()
        if custom_styles:
            styles += f'\n{custom_styles.strip()}'

        body = '\n'.join(self._rows)

        return self.__TEMPLATE \
            .replace('{{styles}}', styles) \
            .replace('{{body}}', body) \
            .strip()
