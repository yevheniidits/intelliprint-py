"""Services package for Intelliprint API."""

from intelliprint_py.services.base import BaseService
from intelliprint_py.services.prints import PrintsService
from intelliprint_py.services.backgrounds import BackgroundsService
from intelliprint_py.services.mailing_lists import MailingListsService

__all__ = [
    "BaseService",
    "PrintsService",
    "BackgroundsService",
    "MailingListsService",
]

