# Extr - NLP

> Simple NER / Relation Extraction library using Regular Expressions

### Entity Extraction

```python
from extr import RegEx, RegExLabel, EntityExtactor

entity_extractor = EntityExtactor([
    RegExLabel('PERSON', [
        RegEx([r'ted'], re.IGNORECASE)
    ]),
    RegExLabel('POSITION', [
        RegEx([r'pitcher'], re.IGNORECASE)
    ]),
])

annotation_results = entity_extractor.annotate('Ted is a Pitcher.')

## annotation_results.entities == [
##      <Entity label="POSITION" text="Pitcher" span=(9, 16)>,
##      <Entity label="PERSON" text="Ted" span=(0, 3)>
## ]
```

### Relation Extraction

```python
from extr import RegExRelationLabel, RelationExtractor

relation = RegExRelationLabel('is_a')

## define relationship between PERSON and POSITION
relation.add_e1_to_e2(
    'PERSON', ## e1
    [r'\s+is\s+a\s+'], ## relationship between e1 / e2
    'POSITION' ## e2
)

relations = RelationExtractor([relation]).extract(annotation_results)

## relations == [
##      <Relation e1="Ted" r="is_a" e2="Pitcher">
## ]

```
