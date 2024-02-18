from urllib.parse import urlencode

from django import forms
from django.http import HttpResponse
from django.test import RequestFactory

from dfv import view
from dfv.form import create_form, get_form_data, is_valid_submit


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


def test_form_data_unbounded_initial(rf: RequestFactory):
    @view()
    def viewfn(request):
        form = create_form(request, TwoFieldForm, initial={"p1": "aa", "p2": "123"})
        data = get_form_data(form)
        assert data["p1"] == "aa"
        assert data["p2"] == 123

    viewfn(rf.get("/view"))


def test_form_data_bounded_data(rf: RequestFactory):
    @view()
    def viewfn(request):
        form = create_form(request, TwoFieldForm, initial={"p1": "aa", "p2": "123"})
        data = get_form_data(form)
        assert data["p1"] == "bb"
        assert data["p2"] == 456

    viewfn(rf.post("/view", {"p1": "bb", "p2": "456"}))
