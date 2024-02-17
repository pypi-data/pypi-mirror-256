from django.db import models
from django.utils.translation import gettext_lazy as _

from polymorphic.models import PolymorphicModel

from aleksis.core.mixins import ExtensibleModel, PureDjangoModel


class DisplayGroup(ExtensibleModel):
    SCOPE_PREFIX = "displaygroup"

    name = models.CharField(max_length=255, verbose_name=_("Name"))
    slug = models.SlugField(max_length=255, verbose_name=_("Slug"))

    class Meta:
        verbose_name = _("Display Group")
        verbose_name_plural = _("Display Groups")

    def __str__(self) -> str:
        return self.name

    @property
    def scope(self) -> str:
        """Return OAuth2 scope name to access content via API."""
        return f"{self.SCOPE_PREFIX}_{self.slug}"


class Display(ExtensibleModel):
    PROFILE_CHOICES = [
        ("impressive", _("Impressive based PDF/image/video display")),
        ("surf", _("Website display based on surf browser")),
    ]

    display_group = models.ForeignKey(
        DisplayGroup,
        verbose_name=_("Display group"),
        on_delete=models.CASCADE,
        related_name="displays",
    )
    hostname = models.CharField(max_length=255, verbose_name=_("Hostname"))
    profile = models.CharField(max_length=10, verbose_name=_("Profile"), choices=PROFILE_CHOICES)
    description = models.CharField(max_length=255, verbose_name=_("Description"), blank=True)

    class Meta:
        verbose_name = _("Display")
        verbose_name_plural = _("Displays")

    def __str__(self) -> str:
        return self.hostname


class Slide(PolymorphicModel, PureDjangoModel):
    _supported_profiles = []

    display_group = models.ForeignKey(
        DisplayGroup,
        verbose_name=_("Display group"),
        on_delete=models.CASCADE,
        related_name="slides",
    )
    order = models.PositiveSmallIntegerField(verbose_name=_("Order"))

    class Meta:
        verbose_name = _("Slide")
        verbose_name_plural = _("Slides")
        ordering = ["order"]

    def __str__(self):
        return f"{self.display_group}#{self.order}"

    @classmethod
    def display_supported(cls, display):
        return display.profile in cls._supported_profiles

    def get_public_url(self, display=None, request=None):
        raise NotImplementedError("Slide types need to implement the get_public_url method.")
