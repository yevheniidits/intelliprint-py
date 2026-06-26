"""Enumerations for Intelliprint API."""

from enum import Enum


class PostageService(str, Enum):
    """Available postage services for Intelliprint.

    Note: Postcards can only use UK_SECOND_CLASS or UK_FIRST_CLASS services.
    """

    UK_SECOND_CLASS = "uk_second_class"
    UK_SECOND_CLASS_SIGNED_FOR = "uk_second_class_signed_for"
    UK_FIRST_CLASS = "uk_first_class"
    UK_FIRST_CLASS_SIGNED_FOR = "uk_first_class_signed_for"
    UK_SPECIAL_DELIVERY_9AM = "uk_special_delivery_9am"
    UK_SPECIAL_DELIVERY = "uk_special_delivery"
    INTERNATIONAL = "international"
    TRACKED_24 = "tracked_24"
    TRACKED_48 = "tracked_48"


class EnvelopeSize(str, Enum):
    """Available envelope sizes for letters.

    The API may upgrade a letter to a larger envelope if the content
    is too large for the chosen envelope size.
    """

    C4 = "c4"
    C5 = "c5"
    C4_PLUS = "c4_plus"
    A4_BOX = "a4_box"


class PostcardSize(str, Enum):
    """Available sizes for postcards."""

    A6 = "postcard_a6"
    A5 = "postcard_a5"
    A5_ENVELOPED = "postcard_a5_enveloped"


class PrintType(str, Enum):
    """Type of print job."""

    LETTER = "letter"
    POSTCARD = "postcard"


class LetterStatus(str, Enum):
    """Status of a letter/mail item representing its lifecycle from creation to dispatch."""

    DRAFT = "draft"
    WAITING_TO_PRINT = "waiting_to_print"
    PRINTING = "printing"
    ENCLOSING = "enclosing"
    SHIPPING = "shipping"
    SENT = "sent"
    CANCELLED = "cancelled"
    RETURNED = "returned"
    FAILED_WRONG_ADDRESS = "failed_wrong_address"


class AddressWindow(str, Enum):
    """Position of the address window on the envelope.

    Only available for letters.
    """

    LEFT = "left"
    RIGHT = "right"


class SplittingMethod(str, Enum):
    """Method to split a print job into multiple letters.

    Used when a single file contains multiple letters with pre-inserted addresses.
    Splitting is only available for letters.
    """

    NONE = "none"
    SPLIT_ON_PHRASE = "split_on_phrase"
    SPLIT_ON_PAGES = "split_on_pages"
    MAILING_LIST = "mailing_list"

