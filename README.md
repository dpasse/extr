# Extr - NLP

> Named Entity Recognition (NER) and Relation Extraction (RE) library using Regular Expressions

<br />

## Install

```
pip install extr-nlp
```

## Example

```python
text = 'Ted is a Pitcher.'
```

### 1. Entity Extraction
> Find Named Entities from text.

```python
from extr_nlp import RegEx, RegExLabel, EntityExtactor

entity_extractor = EntityExtactor([
    RegExLabel('PERSON', [
        RegEx([r'ted'], re.IGNORECASE)
    ]),
    RegExLabel('POSITION', [
        RegEx([r'pitcher'], re.IGNORECASE)
    ]),
])

entities = entity_extractor.get_entities(text)

## entities == [
##      <Entity label="POSITION" text="Pitcher" span=(9, 16)>,
##      <Entity label="PERSON" text="Ted" span=(0, 3)>
## ]
```

### 2. Relation Extraction
> Annotate and Extract Relationships between Entities

```python
from extr_nlp import EntityAnnotator
from extr_nlp import RegExRelationLabelBuilder, RelationExtractor

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

## `entities` see 'Entity Extraction' above
annotation_results = EntityAnnotator().annotate(text, entities)
relations = RelationExtractor(relations_to_extract).extract(annotation_results)

## relations == [
##      <Relation e1="Ted" r="is_a" e2="Pitcher">
## ]

```
