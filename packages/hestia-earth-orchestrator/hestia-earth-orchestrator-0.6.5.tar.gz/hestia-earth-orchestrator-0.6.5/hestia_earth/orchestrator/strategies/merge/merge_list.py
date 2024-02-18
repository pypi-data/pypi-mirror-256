import pydash
from hestia_earth.schema import UNIQUENESS_FIELDS

from hestia_earth.orchestrator.utils import _non_empty_list, update_node_version
from .merge_node import merge as merge_node


def _matching_properties(model: dict, node_type: str):
    return UNIQUENESS_FIELDS.get(node_type, {}).get(model.get('key'), [])


def _match_list_el(source: list, dest: list, key: str):
    src_values = _non_empty_list([x.get(key) for x in source])
    dest_values = _non_empty_list([x.get(key) for x in dest])
    return sorted(src_values) == sorted(dest_values)


def _match_el_count(source: dict, dest: dict, keys: list):
    # assign different points to matched keys
    # 1 if both keys are defined and match
    # -1 if src and dest differ
    # 0 otherwise
    def match(key: str):
        keys = key.split('.')
        src_value = pydash.objects.get(source, key)
        dest_value = pydash.objects.get(dest, key)
        is_list = len(keys) == 2 and (
            isinstance(pydash.objects.get(source, keys[0]), list) or
            isinstance(pydash.objects.get(dest, keys[0]), list)
        )
        value = (
            1 if _match_list_el(
                pydash.objects.get(source, keys[0], []),
                pydash.objects.get(dest, keys[0], []),
                keys[1]
            ) else -1
        ) if is_list else (
            1 if all([
                src_value is not None,
                dest_value is not None,
                src_value == dest_value
            ]) else -1 if src_value != dest_value else 0
        )
        return value

    return sum(map(match, keys))


def _find_match_el_index(values: list, el: str, same_methodModel: bool, model: dict, node_type: str):
    properties = list(set(_matching_properties(model, node_type) + (['methodModel.@id'] if same_methodModel else [])))

    # order other elements by number of matching properties, then take the highest one
    # this is to handle cases where we add a unique property to the element
    elements = [(i, _match_el_count(values[i], el, properties)) for i in range(0, len(values))]
    # make sure there is at least one matching property
    elements = [(i, match_count) for i, match_count in elements if match_count > 0]
    elements = sorted(elements, key=lambda x: x[1])
    return elements[-1][0] if elements else None


def merge(source: list, merge_with: list, version: str, model: dict = {}, merge_args: dict = {}, node_type: str = ''):
    source = source if source is not None else []

    # only merge node if it has the same `methodModel`
    same_methodModel = merge_args.get('sameMethodModel', False)
    # only merge if the
    skip_same_term = merge_args.get('skipSameTerm', False)

    for el in _non_empty_list(merge_with):
        source_index = _find_match_el_index(source, el, same_methodModel, model, node_type)
        if source_index is None:
            source.append(update_node_version(version, el))
        elif not skip_same_term:
            source[source_index] = merge_node(source[source_index], el, version, model, merge_args)
    return source
