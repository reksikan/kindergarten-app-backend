from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, func, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

if TYPE_CHECKING:
    class Base(DeclarativeBase, _mapped_columnExpressionArgument):  # type: ignore # noqa
        pass
else:
    class Base(DeclarativeBase):
        pass


class IDMixin:
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, nullable=False)


class CreatedAtMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, server_default=func.now(), nullable=False
    )


class UpdatedAtMixin:
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow,
        server_default=func.now(), server_onupdate=func.now(), nullable=False
    )


class TimestampMixin(CreatedAtMixin, UpdatedAtMixin):
    pass

