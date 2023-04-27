# Extr
> Named Entity Recognition (NER) and Relation Extraction (RE) library using Regular Expressions

<br />

## Install

```
pip install extr
```

## Example

```python
text = 'Ted is a Pitcher.'
```

### 1. Entity Extraction
> Find Named Entities from text.

```python
from extr import RegEx, RegExLabel
from extr.entities import EntityExtractor

entity_extractor = EntityExtractor([
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

**<i> or add a knowledge base</i>**

```python
from extr import RegEx, RegExLabel
from extr.entities import create_entity_extractor

entity_extractor = create_entity_extractor(
    [
        RegExLabel('POSITION', [
            RegEx([r'pitcher'], re.IGNORECASE)
        ]),
    ],
    kb={
        'PERSON': ['Ted']
    }
)

entities = entity_extractor.get_entities(text)

## entities == [
##      <Entity label="POSITION" text="Pitcher" span=(9, 16)>,
##      <Entity label="PERSON" text="Ted" span=(0, 3)>
## ]
```

### 2. Visualize Entities in HTML
> Annotate text to display in HTML.

```python
from extr.entities import HtmlEntityAnnotator

html = HtmlEntityAnnotator().annotate(text, entities)
```

```html
<!-- customize colors by label -->
<style>
    span.entity {
        border: 1px solid black;
        border-radius: 5px;
        padding: 5px;
        margin: 3px;
        color: gray;
        cursor: pointer;
    }

    span.label {
        font-weight: bold;
        padding: 3px;
        color: black;
    }

    .lb-PERSON {
        background-color: orange;
    }

    .lb-POSITION {
        background-color: yellow;
    }
</style>

<div>
    {{ -- insert html here -- }}
</div>
```

![](https://github.com/dpasse/extr/blob/main/docs/images/annotations.JPG)

### 3. Relation Extraction
> Annotate and Extract Relationships between Entities

```python
from extr.entities import EntityAnnotator
from extr.relations import RelationExtractor, \
                           RegExRelationLabelBuilder

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
