from urllib.parse import urlencode

from django import forms
from django.http import HttpResponse
from django.test import RequestFactory

from dfv import view
from dfv.form import create_form, create_form_and_state, is_valid_submit


class TwoFieldForm(forms.Form):
    p1 = forms.CharField()
    p2 = forms.IntegerField()


def test_form_get(rf: RequestFactory):
    @view()
    def viewfn(request):
        form = create_form(request, TwoFieldForm)
        return HttpResponse(form)

    req = rf.get("/view")
    res = viewfn(req)
    assert res.content == (
        b"""<input type="text" name="p1" required id="id_p1">"""
        b"""<input type="number" name="p2" required id="id_p2">"""
    )


def test_form_patch(rf: RequestFactory):
    form_ref = []

    @view()
    def viewfn(request):
        fi = create_form(request, TwoFieldForm)
        form_ref.append(fi)
        return HttpResponse()

    req = rf.patch(
        "/view",
        urlencode({"p1": "a"}),
        content_type="application/x-www-form-urlencoded",
    )
    viewfn(req)
    form = form_ref[0]
    assert form is not None
    assert form.initial["p1"] == "a"


def test_form_patch_initial(rf: RequestFactory):
    form_ref = []

    @view()
    def viewfn(request):
        fi = create_form(request, TwoFieldForm, initial={"p2": 123})
        form_ref.append(fi)
        return HttpResponse()

    req = rf.patch(
        "/view",
        urlencode({"p1": "a"}),
        content_type="application/x-www-form-urlencoded",
    )
    viewfn(req)
    form = form_ref[0]
    assert form is not None
    assert form.initial["p1"] == "a"
    assert form.initial["p2"] == 123


def test_form_post(rf: RequestFactory):
    cleaned_data = {}

    @view()
    def viewfn(request):
        form = create_form(request, TwoFieldForm)
        assert is_valid_submit(request, form)
        cleaned_data.update(form.cleaned_data)
        return HttpResponse()

    req = rf.post("/view", {"p1": "a", "p2": 123})
    viewfn(req)
    assert cleaned_data["p1"] == "a"
    assert cleaned_data["p2"] == 123


def test_form_initial(rf: RequestFactory):
    @view()
    def viewfn(request):
        form = create_form(request, TwoFieldForm, initial={"p1": "aaa", "p2": 123})
        fs = str(form)
        assert '<input type="text" name="p1" value="aaa" required id="id_p1">' in fs
        assert '<input type="number" name="p2" value="123" required id="id_p2">' in fs

    viewfn(rf.get("/view"))


def test_form_state_get_with_initial(rf: RequestFactory):
    @view()
    def viewfn(request):
        form, state = create_form_and_state(
            request, TwoFieldForm, initial={"p1": "aa", "p2": "12"}
        )
        assert state["p1"] == "aa"

    viewfn(rf.get("/view"))


def test_form_state_get_with_post(rf: RequestFactory):
    @view()
    def viewfn(request):
        form, state = create_form_and_state(request, TwoFieldForm)
        assert state["p1"] == "aa"

    viewfn(rf.post("/view", {"p1": "aa", "p2": "12"}))


def test_form_state_set_with_initial(rf: RequestFactory):
    @view()
    def viewfn(request):
        form, state = create_form_and_state(
            request, TwoFieldForm, initial={"p1": "aa", "p2": "12"}
        )
        state["p1"] = "bb"
        assert state["p1"] == "bb"
        assert state.get("p1") == "bb"
        fs = str(form)
        assert '<input type="text" name="p1" value="bb" required id="id_p1">' in fs

    viewfn(rf.get("/view"))


def test_form_state_set_with_post(rf: RequestFactory):
    @view()
    def viewfn(request):
        form, state = create_form_and_state(request, TwoFieldForm)
        state["p1"] = "bb"
        assert state["p1"] == "bb"
        fs = str(form)
        assert '<input type="text" name="p1" value="bb" required id="id_p1">' in fs

    viewfn(rf.post("/view", {"p1": "aa", "p2": "12"}))


def test_form_state_iter_and_len_with_initial(rf: RequestFactory):
    @view()
    def viewfn(request):
        form, state = create_form_and_state(
            request, TwoFieldForm, initial={"p1": "aa", "p2": "12"}
        )
        assert list(iter(form.initial)) == list(iter(state))
        assert len(form.initial) == len(state)

    viewfn(rf.get("/view"))


def test_form_state_iter_and_len_with_post(rf: RequestFactory):
    @view()
    def viewfn(request):
        form, state = create_form_and_state(request, TwoFieldForm)
        form.is_valid()
        assert list(iter(form.cleaned_data)) == list(iter(state))
        assert len(form.cleaned_data) == len(state)

    viewfn(rf.post("/view", {"p1": "aa", "p2": "12"}))
