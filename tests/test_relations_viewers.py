import os
import sys

sys.path.insert(0, os.path.join('../src'))

from extr import Location, Entity
from extr.relations import RelationExtractor, RegExRelationLabelBuilder
from extr.relations.viewers import HtmlViewer


def test_html_viewer():
    text = 'Ted is a Pitcher.'
    annotated_text = '##ENTITY_PERSON_2## is a ##ENTITY_POSITION_1##.'
    entities = [
        Entity(1, 'POSITION', 'Pitcher', Location(9, 16)),
        Entity(2, 'PERSON', 'Ted', Location(0, 3))
    ]

    ## define relationship between PERSON and POSITION    
    relationship = RegExRelationLabelBuilder('is_a') \
        .add_e1_to_e2(
            'PERSON', ## e1
            [
                ## define how the relationship exists in nature
                r'\s+is\s+a\s+',
            ],
            'POSITION' ## e2
        ) \
        .build()
        
    relations_to_extract = [relationship]

    relations = RelationExtractor(relations_to_extract).extract(annotated_text, entities)

    viewer = HtmlViewer()
    viewer.append_header('r("PERSON", "POSITION")')
    viewer.append_relation(text, relation=relations[0])

    html = viewer.create_view()

    assert html == """<html>
    <head>
        <style>
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
        </style>
    </head>
    <body>
        <table>
<tr><td class="header" colspan="3">r("PERSON", "POSITION")</td></tr>
<tr id="0"><td>0</td><td class="label">is_a</td><td><span class="entity lb-PERSON e1"><span class="label">PERSON</span>Ted</span> is a <span class="entity lb-POSITION e2"><span class="label">POSITION</span>Pitcher</span>.</td></tr>
        </table>
    </body>
</html>"""
    