from typing import List, Dict, Optional

from .extractor import EntityExtractor
from ..regexes import RegExLabel, transform_knowledge


def create_entity_extractor(regex_labels: List[RegExLabel], kb: Optional[Dict[str, List[str]]] = None):
    all_regex_labels = []

    if len(regex_labels) > 0:
        all_regex_labels.extend(regex_labels)

    if kb:
        all_regex_labels.extend(
            [transform_knowledge(label, expressions) for label, expressions in kb.items()]
        )

    return EntityExtractor(all_regex_labels)
