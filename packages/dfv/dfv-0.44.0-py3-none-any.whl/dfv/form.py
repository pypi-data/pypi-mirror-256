from typing import Any, cast, Mapping, TypeVar

from django.forms import BaseForm, BoundField, Field, Form
from django.http import HttpRequest, QueryDict

from dfv import is_patch, is_post, is_put


def _convert_querydict_to_initial_values(qd: QueryDict) -> dict[str, str]:
    return {k: v for k, v in qd.items()}


T_FORM = TypeVar("T_FORM", bound=BaseForm)


def create_form(
    request: HttpRequest, form_class: type[T_FORM], *, initial=None, **kwargs
) -> T_FORM:
    """
    Instantiate a form of type `form_class` and returns it.

    If the request method is GET, the form will be created with the `initial` values.

    If the request method is PATCH, the `initial` values will be updated with
    request's body.

    If the request method is POST or PUT, the form will be bound with the POST data.
    """
    if is_post(request) or is_put(request):
        form = form_class(data=request.POST, files=request.FILES, **kwargs)
    elif is_patch(request):
        initial = {} if initial is None else initial
        qd = QueryDict(request.body, encoding=request.encoding)
        initial_from_query = _convert_querydict_to_initial_values(qd)
        initial.update(initial_from_query)
        form = form_class(initial=initial, **kwargs)
    else:
        form = form_class(initial=initial, **kwargs)

    return cast(T_FORM, form)


class _FormStateProxy(Mapping[str, Any]):
    __form: Form

    def __init__(self, form: Form):
        self.__form = form

    def __getitem__(self, name: str) -> Any:
        bf: BoundField = self.__form[name]
        value = bf.value()
        f: Field = bf.field
        return f.to_python(value)

    def __iter__(self):
        raise NotImplementedError()

    def __len__(self):
        raise NotImplementedError()


def get_form_data(form: Form) -> Mapping[str, Any]:
    """
    Returns a state proxy for the form instance. The state proxy can be used to
    read from the form's underlying data structure. If the form is bound,
    the state proxy will reflect the form's `data`. If the form is not bound,
    the state proxy will reflect the form's `initial`.

    In any case, the value will be passed through the field's `to_python` method.
    """
    return _FormStateProxy(form)


def is_valid_submit(request: HttpRequest, form: BaseForm) -> bool:
    return is_post(request) and form.is_valid()
