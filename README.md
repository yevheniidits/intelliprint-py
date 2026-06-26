# intelliprint-py

Unofficial Python SDK for the [Intelliprint API](https://docs.intelliprint.net) - Send physical mail as easily as sending email.

[![PyPI version](https://badge.fury.io/py/intelliprint-py.svg)](https://badge.fury.io/py/intelliprint-py)
[![Python versions](https://img.shields.io/pypi/pyversions/intelliprint-py.svg)](https://pypi.org/project/intelliprint-py/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Installation

```bash
pip install intelliprint-py
```

## Quick Start

```python
from intelliprint_py import (
    IntelliprintClient,
    IntelliprintAddress,
    IntelliprintRecipient,
)

# Initialize the client
client = IntelliprintClient(api_key="your-api-key")
# Or use environment variable: INTELLIPRINT_API_KEY

# Create a simple print job
print_job = client.prints.create(
    content="<h1>Hello World!</h1><p>This is my first letter.</p>",
    testmode=True,  # Required: explicitly set test mode
    recipients=[
        IntelliprintRecipient(
            address=IntelliprintAddress(
                name="John Doe",
                line="123 Main Street, London",
                postcode="SW1A 1AA",
            )
        )
    ],
)

print(f"Created print job: {print_job['id']}")
```

## Using UserData

For more structured recipient management, use the `UserData` model:

```python
from intelliprint_py import (
    IntelliprintClient,
    UserData,
    UserAddress,
)

client = IntelliprintClient(api_key="your-api-key")

# Create user data with extra fields for template variables
user = UserData(
    first_name="John",
    last_name="Doe",
    email="john@example.com",
    user_id="customer_12345",
    address=[
        UserAddress(
            building_number="123",
            thoroughfare="Main Street",
            post_town="London",
            postcode="SW1A 1AA",
        )
    ],
    extra={
        "membership_level": "gold",
        "account_balance": "£150.00",
    },
)

# Create a print job using user data
print_job = client.prints.create(
    content="""
    <h1>Welcome, {first_name}!</h1>
    <p>Your membership level: {membership_level}</p>
    <p>Current balance: {account_balance}</p>
    """,
    testmode=True,
    user_data=user,
)
```

## Services

### Prints

Create and manage print jobs (letters and postcards):

```python
# Create a print job
print_job = client.prints.create(
    content="Hello World!",
    testmode=True,
    recipients=[...],
)

# Get a print job
print_job = client.prints.get("print_xxx")

# List print jobs
jobs = client.prints.list(limit=10, testmode=True)

# Update a print job
client.prints.update("print_xxx", reference="Updated reference")

# Confirm a print job for printing
client.prints.confirm("print_xxx")

# Delete/cancel a print job
client.prints.delete("print_xxx")
```

### Backgrounds

Manage letterhead backgrounds (no user data required):

```python
# Create a background
with open("letterhead.pdf", "rb") as f:
    background = client.backgrounds.create(
        file_content=f.read(),
        file_name="letterhead.pdf",
        name="Company Letterhead",
    )

# List backgrounds
backgrounds = client.backgrounds.list()

# Use a background in a print job
print_job = client.prints.create(
    content="Hello!",
    testmode=True,
    recipients=[...],
    background=BackgroundSettings(
        first_page="bg_xxx",
        other_pages="bg_yyy",
    ),
)
```

### Mailing Lists

Manage mailing lists and recipients:

```python
# Create a mailing list
mailing_list = client.mailing_lists.create(name="Newsletter Subscribers")

# Add a user to the mailing list
client.mailing_lists.add_user(
    mailing_list_id="mal_xxx",
    user_data=user,
    additional_variables={"signup_date": "2024-01-15"},
)

# List recipients
recipients = client.mailing_lists.list_recipients("mal_xxx")

# Send to a mailing list
print_job = client.prints.create(
    template="tmpl_xxx",
    testmode=True,
    mailing_list="mal_xxx",
)
```

## Configuration Options

### Print Settings

```python
from intelliprint_py import (
    PrintingSettings,
    PostageSettings,
    PostageService,
    EnvelopeSize,
)

print_job = client.prints.create(
    content="Important document",
    testmode=True,
    recipients=[...],
    printing=PrintingSettings(
        double_sided="yes",
        premium_quality=True,
        black_and_white=False,
    ),
    postage=PostageSettings(
        service=PostageService.UK_FIRST_CLASS,
        ideal_envelope=EnvelopeSize.C4,
    ),
)
```

## Error Handling

```python
from intelliprint_py import IntelliprintClient, IntelliprintError

client = IntelliprintClient(api_key="your-api-key")

try:
    print_job = client.prints.get("invalid_id")
except IntelliprintError as e:
    print(f"Error: {e.message}")
    print(f"Type: {e.error_type}")
    print(f"Code: {e.error_code}")
```

## Development

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run linting
ruff check src/

# Run type checking
mypy src/
```

## License

MIT License - see [LICENSE](LICENSE) for details.

## Links

- [Intelliprint API Documentation](https://docs.intelliprint.net)
- [Intelliprint Dashboard](https://account.intelliprint.net)
- [PyPI Package](https://pypi.org/project/intelliprint-py/)

