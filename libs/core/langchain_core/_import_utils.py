import re
from importlib import import_module

# Allowlist pattern: only valid Python dotted identifiers are permitted.
# This prevents arbitrary or malicious strings from reaching import_module().
_VALID_PYTHON_NAME_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*(\.[A-Za-z_][A-Za-z0-9_]*)*$")


def _validate_python_name(name: str, label: str) -> None:
    """Raise ValueError if *name* is not a valid dotted Python identifier."""
    if not _VALID_PYTHON_NAME_RE.match(name):
        msg = (
            f"Invalid {label} {name!r}: only dotted Python identifiers are allowed."
        )
        raise ValueError(msg)


def import_attr(
    attr_name: str,
    module_name: str | None,
    package: str | None,
) -> object:
    """Import an attribute from a module located in a package.

    This utility function is used in custom `__getattr__` methods within `__init__.py`
    files to dynamically import attributes.

    Args:
        attr_name: The name of the attribute to import.
        module_name: The name of the module to import from.

            If `None`, the attribute is imported from the package itself.
        package: The name of the package where the module is located.

    Raises:
        ValueError: If *attr_name*, *module_name*, or *package* are not valid
            Python identifiers.
        ImportError: If the module cannot be found.
        AttributeError: If the attribute does not exist in the module or package.

    Returns:
        The imported attribute.
    """
    # Allowlist check: reject any value that is not a valid dotted Python identifier
    # before it reaches importlib.import_module(), preventing arbitrary module loading.
    _validate_python_name(attr_name, "attr_name")
    if module_name is not None and module_name != "__module__":
        _validate_python_name(module_name, "module_name")
    if package is not None:
        _validate_python_name(package, "package")

    if module_name == "__module__" or module_name is None:
        try:
            result = import_module(f".{attr_name}", package=package)
        except ModuleNotFoundError:
            msg = f"module '{package!r}' has no attribute {attr_name!r}"
            raise AttributeError(msg) from None
    else:
        try:
            module = import_module(f".{module_name}", package=package)
        except ModuleNotFoundError as err:
            msg = f"module '{package!r}.{module_name!r}' not found ({err})"
            raise ImportError(msg) from None
        result = getattr(module, attr_name)
    return result
