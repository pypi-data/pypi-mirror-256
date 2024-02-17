from typing import Any, cast, MutableMapping, Tuple, TypeVar

from django.forms import BaseForm, Form
from django.http import HttpRequest, QueryDict

from dfv import is_patch, is_post, is_put


def _convert_querydict_to_initial_values(qd: QueryDict) -> dict[str, str]:
    return {k: v for k, v in qd.items()}


class _FormStateProxy(MutableMapping[str, Any]):
    _form: Form

    def __init__(self, form: Form):
        self._form = form

    def __getitem__(self, key: str) -> Any:
        if self._form.is_bound:
            self._form.is_valid()
            return self._form.cleaned_data[key]

        return self._form.initial[key]

    def __setitem__(self, key: str, value: Any) -> None:
        if self._form.is_bound:
            qd = QueryDict(mutable=True)
            qd.update(self._form.data)
            qd[key] = value
            self._form.data = qd
            self._form.full_clean()
        self._form.initial[key] = value

    def __delitem__(self, key: str) -> None:
        raise NotImplementedError()

    def __iter__(self):
        return (
            iter(self._form.cleaned_data)
            if self._form.is_bound
            else iter(self._form.initial)
        )

    def __len__(self):
        return (
            len(self._form.cleaned_data)
            if self._form.is_bound
            else len(self._form.initial)
        )


T_FORM = TypeVar("T_FORM", bound=BaseForm)


def create_form_and_state(
    request: HttpRequest, form_class: type[T_FORM], *, initial=None, **kwargs
) -> Tuple[T_FORM, MutableMapping[str, Any]]:
    """
    Instantiate a form of type `form_class` and returns it along with a state object.

    If the request method is GET, the form will be created with the `initial` values
    and the state object will reflect the initial values.

    If the request method is PATCH, the `initial` values will be updated with
    request's body and the state object will reflect the initial values.

    If the request method is POST or PUT, the form will be bound with the POST data
    and the state object will reflect the form's `cleaned_data`. `form.is_valid()` will
    be called on key-lookup on the state object.

    In any case, the state object can be used to write to the underlying data structure.
    If the form is bound, `form.full_clean()` will be called afterward.
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

    return cast(T_FORM, form), _FormStateProxy(form)


def create_form(
    request: HttpRequest, form_class: type[T_FORM], *, initial=None, **kwargs
) -> T_FORM:
    """
    See `create_form_and_state` for details. This function only returns the form.
    """
    form, _ = create_form_and_state(request, form_class, initial=initial, **kwargs)
    return form


def is_valid_submit(request: HttpRequest, form: BaseForm) -> bool:
    return is_post(request) and form.is_valid()
