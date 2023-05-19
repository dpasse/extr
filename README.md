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
from extr.entities.viewers import HtmlViewer

viewer = HtmlViewer()
viewer.append(text, entities)

html = viewer.create_view(custom_styles="""
    .lb-PERSON {
        background-color: orange;
    }

    .lb-POSITION {
        background-color: yellow;
    }
""")
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
annotated_text = EntityAnnotator().annotate(text, entities)
relations = RelationExtractor(relations_to_extract).extract(annotated_text, entities)

## relations == [
##      <Relation e1="Ted" r="is_a" e2="Pitcher">
## ]

```

### 4. Apply Attributes to Entities
> mark entities based on their surroundings

```python
from extr.entities import EntityAttributor, \
                          AttributeToApply, \
                          AttributeApplications, \
                          AttributeSetup


negative_text = 'Ted is not a Pitcher.'
entities = extractor.get_entities(negative_text)

attributor = EntityAttributor(
    attribute_name='ctypes',
    settings = [
        AttributeToApply(
            'NEGATIVE',
            applications=[
                AttributeApplications(
                    entities=['POSITION'],
                    setups=[
                        AttributeSetup(before=r' not a ')
                    ]
                )
            ]
        )
    ]
)

entities = attributor.set_attributes(negative_text, entities)

## entities == [
##      <Entity label="POSITION" text="Pitcher" span=(13, 20) attributes={"ctypes": ["NEGATIVE"]}>,
##      <Entity label="PERSON" text="Ted" span=(0, 3)>
## ]
```
