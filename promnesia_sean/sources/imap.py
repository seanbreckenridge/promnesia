from my.core.warnings import high

high(
    "The promnesia_sean.sources.imap module is deprecated -- import from promnesia_sean.sources.mail instead"
)

from .mail import *
