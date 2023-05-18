from typing import List, Optional

from ...models import Entity
from ..annotator import HtmlEntityAnnotator


__TEMPLATE__ = """
<html>
    <head>
        <style>
{{styles}}
        </style>
    </head>
    <body>
{{body}}
    </body>
</html>
    """


class HtmlViewer:
    __TEMPLATE = __TEMPLATE__

    __DEFAULT_STYLES = """
p { margin: 5px; line-height: 45px; }
span.entity { border: 1px solid black; border-radius: 5px; padding: 5px; margin: 3px; cursor: pointer; }
span.label { font-weight: bold; padding: 3px; color: black; }
"""

    def __init__(self, annotations: Optional[List[str]] = None) -> None:
        self._rows: List[str] = annotations if annotations is not None else []
        self._annotator = HtmlEntityAnnotator()

    def append(self, text: str, entities: List[Entity]) -> None:
        self._rows.append(
            self._annotator.annotate(text, entities).annotated_text
        )

    def create_view(self, custom_styles: Optional[str] = None, spacer='<hr />') -> str:
        styles = self.__DEFAULT_STYLES.strip()
        if custom_styles:
            styles += f'\n{custom_styles.strip()}'

        format_annoations = (f'<p>{annotation}</p>' for annotation in self._rows)
        body = f'{spacer}\n'.join(format_annoations)

        return self.__TEMPLATE \
            .replace('{{styles}}', styles) \
            .replace('{{body}}', body) \
            .strip()
