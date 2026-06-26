"""Models package for Intelliprint API."""

from intelliprint_py.models.enums import (
    AddressWindow,
    EnvelopeSize,
    LetterStatus,
    PostageService,
    PostcardSize,
    PrintType,
    SplittingMethod,
)
from intelliprint_py.models.address import (
    IntelliprintAddress,
    IntelliprintRecipient,
)
from intelliprint_py.models.settings import (
    BackgroundSettings,
    NudgeSettings,
    PostageSettings,
    PrintingSettings,
    SplittingSettings,
)
from intelliprint_py.models.user_data import (
    UserAddress,
    UserData,
)

__all__ = [
    # Enums
    "PostageService",
    "EnvelopeSize",
    "PostcardSize",
    "PrintType",
    "LetterStatus",
    "AddressWindow",
    "SplittingMethod",
    # Address models
    "IntelliprintAddress",
    "IntelliprintRecipient",
    # Settings models
    "PrintingSettings",
    "PostageSettings",
    "BackgroundSettings",
    "SplittingSettings",
    "NudgeSettings",
    # User data
    "UserAddress",
    "UserData",
]

