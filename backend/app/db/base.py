from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


from app.models import category, document, expense, supplier, user  # noqa: E402,F401

