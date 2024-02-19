import os
import random
import string
from types import UnionType
from typing import (
    Annotated,
    Any,
    Final,
    TypedDict,
    get_args,
    get_origin,
    get_type_hints,
)
from xml.etree.ElementTree import ParseError, XMLParser

from typeguard import TypeCheckError, check_type

LUDIC_MAX_ELEMENT_DEPTH: Final[int] = int(os.getenv("LUDIC_MAX_ELEMENT_DEPTH", 50))


class _ParsedElement[T](TypedDict):
    tag: str
    children: list[T | str]
    attrs: dict[str, str]


def random_string(n: int) -> str:
    """Generate a random string of length N using uppercase letters and digits.

    :param n: The length of the random string to be generated
    :return: A random string of length N
    """
    return "".join(
        random.SystemRandom().choice(string.ascii_uppercase + string.digits)
        for _ in range(n)
    )


class _LudicElementHandler[T]:
    """Parse HTML elements from a string and collects them as ParsedElement's."""

    def __init__(self, registry: dict[str, type[T]]) -> None:
        self.registry = registry
        self.finished: T | None = None
        self.elements: list[_ParsedElement[T]] = []

    def start(self, tag: str, attrs: dict[str, str]) -> None:
        if len(self.elements) > LUDIC_MAX_ELEMENT_DEPTH:
            raise RuntimeError("Max element depth reached")
        self.elements.append(_ParsedElement(tag=tag, children=[], attrs=attrs))

    def end(self, tag: str) -> None:
        element = self.elements.pop()
        if tag not in self.registry:
            raise TypeError(
                f"Element or component {tag!r} not found in registry, "
                "maybe you forgot to import it?"
            )

        element_type = self.registry[tag]
        attrs = parse_attrs(element_type, element["attrs"])

        new_element: T = self.registry[tag](*element["children"], **attrs)
        if self.elements:
            self.elements[-1]["children"].append(new_element)
        else:
            self.finished = new_element

    def data(self, data: str) -> None:
        self.elements[-1]["children"].append(data)

    def close(self) -> T:
        if self.finished is None:
            raise TypeError("Element is not finished")
        return self.finished


def parse_element[T](tree: str, registry: dict[str, type[T]]) -> T:
    """Parse HTML elements from a string.

    Args:
        tree (str): The string to parse.
        registry (dict[str, Any]): The element registry.

    Returns:
        list[ParsedElement | str]: A list of parsed elements and text.
    """
    parser = XMLParser(target=_LudicElementHandler(registry))  # noqa
    try:
        parser.feed(tree)
    except ParseError as err:
        raise TypeError("The given string is not a valid XHTML.") from err
    return parser.close()


def get_element_generic_args(cls_or_obj: Any) -> tuple[type, ...] | None:
    """Get the generic arguments of the element class.

    Args:
        cls_or_obj (Any): The element to get the generic arguments of.

    Returns:
        dict[str, Any] | None: The generic arguments or :obj:`None`.
    """
    from ludic.base import Element

    for base in getattr(cls_or_obj, "__orig_bases__", []):
        if issubclass(get_origin(base), Element):
            return get_args(base)
    return None


def get_element_attrs_annotations(
    cls_or_obj: Any, include_extras: bool = False
) -> dict[str, Any]:
    """Get the annotations of the element.

    Args:
        cls_or_obj (type[Any]): The element to get the annotations of.
        include_extras (bool): Whether to include extra annotation info.

    Returns:
        dict[str, Any]: The attributes' annotations of the element.
    """
    if (args := get_element_generic_args(cls_or_obj)) is not None:
        return get_type_hints(args[-1], include_extras=include_extras)
    return {}


def validate_attributes(cls_or_obj: Any, values: dict[str, Any]) -> None:
    """Check if the given values are valid for the given class.

    Args:
        cls (type): The expected type of the values.
        values (dict[str, Any]): The values to check.
    """
    if (args := get_element_generic_args(cls_or_obj)) is not None:
        try:
            check_type(values, args[-1])
        except TypeCheckError as err:
            raise TypeError(f"Invalid attributes for {cls_or_obj!r}: {err}.")


def validate_elements(cls_or_obj: Any, elements: tuple[Any, ...]) -> None:
    """Check if the given elements are valid for the given class.

    Args:
        cls (type): The expected type of the elements.
        elements (tuple[Any, ...]): The elements to check.
    """
    if (args := get_element_generic_args(cls_or_obj)) is not None:
        types = args[:-1]
        if len(types) == 0:
            if len(elements) != 0:
                raise TypeError(
                    f"The element {cls_or_obj!r} doesn't expect any elements. "
                    f"Got {len(elements)} elements."
                )
        elif len(types) > 1 or get_origin(types[0]) is UnionType:
            if len(types) != len(elements):
                raise TypeError(
                    f"The element {cls_or_obj!r} got an invalid number of elements. "
                    f"Expected {len(types)} but got {len(elements)}."
                )
            for element, type_ in zip(elements, types, strict=True):
                check_type(element, type_)
        else:
            try:
                check_type(elements, types)
            except TypeCheckError as err:
                raise TypeError(f"Invalid elements for {cls_or_obj!r}: {err}.")


def _format_attr_value(key: str, value: Any, html: bool = False) -> str:
    """Format an HTML attribute with the given key and value.

    Args:
        key (str): The key of the attribute.
        value (Any): The value of the attribute, can be a string or a dictionary.
    Returns:
        str: The formatted HTML attribute.
    """
    if isinstance(value, dict):
        value = ";".join(f"{dkey}:{dvalue}" for dkey, dvalue in value.items())  # type: ignore
    if isinstance(value, bool):
        if html:
            if value:
                value = key
            else:
                return ""
        else:
            value = "true" if value else "false"
    return value


def _parse_attr_value(value_type: type[Any], value: str, html: bool = False) -> Any:
    """Parse an HTML attribute with the given key and value.

    Args:
        key (str): The key of the attribute.
        value (Any): The value of the attribute, can be a string or a dictionary.
    Returns:
        Any: The parsed value.
    """
    if value_type is bool:
        return True if html else value not in ("false", "off", "0")
    elif value_type is int:
        return int(value)
    elif value_type is float:
        return float(value)
    elif value_type is dict:
        return dict(tuple(part.split(":", 1)) for part in value.split(";"))
    else:
        return value


def format_attrs(
    element_type: Any, attrs: dict[str, Any], html: bool = False
) -> dict[str, Any]:
    """Format the given attributes according to the element's attributes.

    Here is an example of TypedDict definition:

        class PersonAttrs(TypedDict):
            name: str
            class_: Annotated[str, "class"]
            is_adult: bool

    And here is the attrs that will be formatted:

        attrs = {"name": "John", "class_": "person", "is_adult": True}

    The result will be:

        >>> format_attrs(PersonAttrs, attrs)
        >>> {"name": "John", "class": "person"}

    Args:
        element_type (Any): The element.
        attrs (dict[str, Any]): The attributes to format.

    Returns:
        dict[str, Any]: The formatted attributes.
    """
    hints = get_element_attrs_annotations(element_type, include_extras=True)

    def _get_key(key: str) -> str:
        if get_origin(hints[key]) is Annotated:
            args = get_args(hints[key])
            if len(args) > 1 and isinstance(args[1], str):
                return args[1]
        return key

    return {
        _get_key(key): _format_attr_value(key, value, html=html)
        for key, value in attrs.items()
    }


def parse_attrs(
    element_type: Any, attrs: dict[str, Any], html: bool = False
) -> dict[str, Any]:
    """Parse the given attributes according to the element's attributes.

    Here is an example of TypedDict definition:

        class PersonAttrs(TypedDict):
            name: str
            class_: Annotated[str, "class"]
            is_adult: bool

    And here is the attrs that will be parsed:

        attrs = {"name": "John", "class": "person", "is_adult": "is_adult"}

    The result will be:

        >>> parse_attrs(PersonAttrs, attrs)
        >>> {"name": "John", "class_": "person", "is_adult": True}

    Args:
        element_type (type): The element class.
        attrs (dict[str, Any]): The attributes to parse.

    Returns:
        dict[str, Any]: The parsed attributes.
    """

    def _get_info(annotation: Any, default: str) -> tuple[type[Any], str]:
        if get_origin(annotation) is Annotated:
            args = get_args(annotation)
            if len(args) > 1 and isinstance(args[1], str):
                return args
        return annotation, default

    result: dict[str, Any] = {}
    for key, ann in get_element_attrs_annotations(
        element_type, include_extras=True
    ).items():
        annotation, key_alias = _get_info(ann, key)
        if (value := attrs.get(key_alias)) is not None:
            result[key] = _parse_attr_value(annotation, value, html=html)
    return result
