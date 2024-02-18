from material import Layout, Row

from aleksis.core.mixins import ExtensibleForm

from .models.base import Display, DisplayGroup


class EditDisplayGroupForm(ExtensibleForm):
    layout = Layout("name", "slug")

    class Meta:
        model = DisplayGroup
        fields = ["name", "slug"]


class EditDisplayForm(ExtensibleForm):
    layout = Layout(
        "display_group",
        Row("hostname", "profile"),
    )

    class Meta:
        model = Display
        fields = ["display_group", "hostname", "profile"]
