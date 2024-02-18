from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.utils.translation import gettext as _

from .models import Category, CheckOutProcess, Inventory, Item, ItemType, Location, Manufacturer


class InventoryForm(ModelForm):
    class Meta:
        model = Inventory
        fields = ("name", "check_out_create_group", "check_out_groups")


class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ("inventory", "name", "notes", "colour", "icon")


class ManufacturerForm(ModelForm):
    class Meta:
        model = Manufacturer
        fields = ("inventory", "name", "notes")


class LocationForm(ModelForm):
    class Meta:
        model = Location
        fields = ("name", "notes", "parent", "inventory")


class ItemTypeForm(ModelForm):
    def clean(self):
        cleaned_data = super().clean()
        if (
            cleaned_data.get("manufacturer")
            and cleaned_data["manufacturer"].inventory.id != cleaned_data["category"].inventory.id
        ):
            raise ValidationError(
                _("The manufacturer must be in the same inventory as the category.")
            )
        return cleaned_data

    class Meta:
        model = ItemType
        fields = ("name", "category", "description", "manufacturer", "image", "part_number")


class ItemForm(ModelForm):
    class Meta:
        model = Item
        fields = ("barcode", "name", "category", "item_type", "notes", "location", "serial_number")


class CheckOutProcessForm(ModelForm):
    class Meta:
        model = CheckOutProcess
        fields = ("check_in_until", "condition")
