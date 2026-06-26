"""Intelliprint API Python SDK - Send physical mail as easily as sending email."""

from intelliprint_py.client import IntelliprintClient
from intelliprint_py.exceptions import IntelliprintError
from intelliprint_py.models import (
    # Enums
    AddressWindow,
    EnvelopeSize,
    LetterStatus,
    PostageService,
    PostcardSize,
    PrintType,
    SplittingMethod,
    # Address models
    IntelliprintAddress,
    IntelliprintRecipient,
    # Settings models
    BackgroundSettings,
    NudgeSettings,
    PostageSettings,
    PrintingSettings,
    SplittingSettings,
    # User data model
    UserData,
    UserAddress,
)

__version__ = "0.1.0"
__all__ = [
    # Main client
    "IntelliprintClient",
    # Exceptions
    "IntelliprintError",
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
    "UserData",
    "UserAddress",
]
