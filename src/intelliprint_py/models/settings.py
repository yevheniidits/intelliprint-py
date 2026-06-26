"""Settings models for Intelliprint API print jobs."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

from intelliprint_py.models.enums import (
    EnvelopeSize,
    PostageService,
    PostcardSize,
    SplittingMethod,
)


class PrintingSettings(BaseModel):
    """Printing settings for a print job.

    Controls quality, color, and finishing options.

    Attributes:
        double_sided: Double-sided printing option ('no', 'yes', or 'mixed').
        double_sided_specific_pages: Page indexes to print double-sided when mixed.
        premium_quality: Whether to use premium quality printing.
        black_and_white: Whether to print in black and white (letters only).
        matt_finish: Whether to use matt finish (postcards only).
    """

    double_sided: Literal["no", "yes", "mixed"] = Field(
        default="no",
        description="Double-sided printing option"
    )
    double_sided_specific_pages: list[int] | None = Field(
        default=None,
        description="Page indexes to print double-sided when mixed (0-indexed)"
    )
    premium_quality: bool = Field(
        default=False,
        description="Whether to use premium quality printing"
    )
    black_and_white: bool = Field(
        default=False,
        description="Whether to print in black and white"
    )
    matt_finish: bool = Field(
        default=False,
        description="Whether to use matt finish (postcards only)"
    )


class PostageSettings(BaseModel):
    """Postage settings for a print job.

    Controls postage service, envelope size, and scheduling.

    Attributes:
        service: The postage service to use.
        ideal_envelope: The ideal envelope size for letters or postcard size.
        mail_date: UNIX timestamp for scheduled mailing date.
    """

    service: PostageService = Field(
        default=PostageService.UK_SECOND_CLASS,
        description="The postage service to use"
    )
    ideal_envelope: EnvelopeSize | PostcardSize = Field(
        default=EnvelopeSize.C5,
        description="The ideal envelope/postcard size"
    )
    mail_date: int | None = Field(
        default=None,
        description="UNIX timestamp for scheduled mailing date"
    )


class BackgroundSettings(BaseModel):
    """Background settings for a print job.

    Specifies letterhead backgrounds for different pages (letters only).

    Attributes:
        first_page: Background ID for the first page (typically a letterhead).
        other_pages: Background ID for subsequent pages.
    """

    first_page: str | None = Field(
        default=None,
        description="Background ID for the first page"
    )
    other_pages: str | None = Field(
        default=None,
        description="Background ID for other pages"
    )


class SplittingSettings(BaseModel):
    """Splitting settings for a print job.

    Used when a single file contains multiple letters (letters only).

    Attributes:
        method: The splitting method to use.
        phrase: Phrase to split on (for split_on_phrase method).
        pages: Pages per letter (for split_on_pages method).
    """

    method: SplittingMethod = Field(
        default=SplittingMethod.NONE,
        description="The splitting method"
    )
    phrase: str | None = Field(
        default=None,
        description="Phrase to split on (for split_on_phrase method)"
    )
    pages: int | None = Field(
        default=None,
        description="Pages per letter (for split_on_pages method)"
    )


class NudgeSettings(BaseModel):
    """Nudge settings for address positioning.

    Helps position pre-inserted addresses within the envelope window (letters only).

    Attributes:
        x: Horizontal nudge in millimeters (positive = right).
        y: Vertical nudge in millimeters (positive = down).
    """

    x: float | None = Field(
        default=None,
        description="Horizontal nudge in millimeters"
    )
    y: float | None = Field(
        default=None,
        description="Vertical nudge in millimeters"
    )

