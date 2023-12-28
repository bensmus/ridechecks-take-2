from typing import Dict, List, Tuple, Set, Iterable, Callable, Collection, Any

def without_keys[T](d: Dict[T, Any], keys_to_exclude: Collection[T]) -> Dict[T, Any]:
    return {k: v for k, v in d.items() if k not in keys_to_exclude}

def is_list_of_strings(l: Any): 
    if type(l) != list:
        return False
    return all(map(lambda x: isinstance(x, str), l))
