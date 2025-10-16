# v2 namespaces
from .v2.books import books_ns
from .v2.copies import copies_ns
from .v2.borrows import borrows_ns

# v3 namespaces
from .v3.auth import v3_auth_ns
from .v3.books import v3_books_ns
from .v3.borrows import v3_borrows_ns
from .v3.admin.books import v3_admin_books_ns
from .v3.admin.borrows import v3_admin_borrows_ns
from .v3.admin.copies import v3_admin_copies_ns
from .v4.books import v4_books_ns
from .v5.books import v5_books_ns

# Expose all namespaces in a single list for easy registration
all_namespaces = [
    books_ns,
    copies_ns,
    borrows_ns,
    v3_auth_ns,
    v3_books_ns,
    v3_borrows_ns,
    v3_admin_books_ns,
    v3_admin_borrows_ns,
    v3_admin_copies_ns,
    v4_books_ns,
    v5_books_ns
]