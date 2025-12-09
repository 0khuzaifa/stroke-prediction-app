Security measures:

- Password hashing with Werkzeug
- CSRF protection via Flask-WTF CSRFProtect
- Server-side validation for numeric and categorical input
- SQLAlchemy ORM to avoid SQL injection
- Session cookie flags (HttpOnly, Secure in production)
- Security headers (CSP, X-Content-Type-Options, X-Frame-Options)
- Avoid logging PII
