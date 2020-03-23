import pytest
from ddf import G, N

from fields_history.models import FieldsHistory

from .models import (
    CharFieldModel,
    DateFieldModel,
    DateTimeFieldModel,
    IntegerFieldModel,
    MultipleFieldModel,
    OneOfManyTrackedFieldModel,
)


@pytest.mark.parametrize(
    "model",
    [
        CharFieldModel,
        DateFieldModel,
        DateTimeFieldModel,
        IntegerFieldModel,
        MultipleFieldModel,
        OneOfManyTrackedFieldModel,
    ],
)
def test_no_history_on_create(db, model):
    obj = N(model)
    obj.save()
    assert not FieldsHistory.objects.exists()


@pytest.mark.parametrize(
    "model", [CharFieldModel, DateFieldModel, DateTimeFieldModel, IntegerFieldModel]
)
def test_history_on_field_change_save(db, model):
    obj = G(model)
    new_obj = N(model)

    assert new_obj.field != obj.field
    obj.field = new_obj.field

    assert not FieldsHistory.objects.exists()
    obj.save()
    assert FieldsHistory.objects.count() == 1


def test_no_history_only_on_tracked_fields_change(db):
    obj = G(OneOfManyTrackedFieldModel, tracked="value", not_tracked="value")
    obj.not_tracked = "new_value"
    obj.save()
    assert not FieldsHistory.objects.exists()

    obj.tracked = "new_value"
    obj.save()
    assert FieldsHistory.objects.count() == 1


def test_single_history_on_multiple_changes(db):
    obj = G(MultipleFieldModel, first_field="value", second_field="value")

    obj.first_field = "new_value"
    obj.second_field = "new_value"
    obj.save()
    assert FieldsHistory.objects.count() == 1


@pytest.mark.parametrize(
    "model", [CharFieldModel, DateFieldModel, DateTimeFieldModel, IntegerFieldModel]
)
def test_no_history_if_field_not_changed(db, model):
    obj = G(model)
    obj.field = obj.field
    obj.save()
    assert not FieldsHistory.objects.exists()