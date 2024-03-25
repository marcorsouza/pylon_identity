from datetime import datetime

from pylon.api.models.base import Base
from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

# Tabela intermediária para representar o relacionamento N x N entre User e Role
user_role = Table(
    'user_role',
    Base.metadata,
    Column('user_id', ForeignKey('users.id')),
    Column('role_id', ForeignKey('roles.id')),
)


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    username: Mapped[str]
    password: Mapped[str]
    email: Mapped[str]
    is_locked_out: Mapped[bool] = mapped_column(default=False)
    failed_pass_att_count: Mapped[int] = mapped_column(default=0)
    creation_date: Mapped[datetime] = mapped_column(
        nullable=False, default=datetime.utcnow
    )
    last_login_date: Mapped[datetime] = mapped_column(nullable=True)
    last_change: Mapped[datetime] = mapped_column(nullable=True)
    temporary_password: Mapped[str] = mapped_column(nullable=True)
    temporary_password_expiration: Mapped[datetime] = mapped_column(
        nullable=True
    )

    # Definindo relacionamento com Role
    roles = relationship('Role', secondary=user_role, back_populates='users')

    def is_locked(self):
        """
        Verifica se o usuário está bloqueado.

        Returns:
            bool: True se o usuário está bloqueado, False caso contrário.
        """
        return self.is_locked_out


class Application(Base):
    __tablename__ = 'applications'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    acronym: Mapped[str] = mapped_column(nullable=False)
    creation_date: Mapped[datetime] = mapped_column(
        nullable=False, default=datetime.utcnow
    )

    roles: Mapped[list['Role']] = relationship(
        back_populates='application', cascade='all, delete-orphan'
    )


class Role(Base):
    __tablename__ = 'roles'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    application_id: Mapped[int] = mapped_column(ForeignKey('applications.id'))

    application: Mapped[Application] = relationship(back_populates='roles')

    # Definindo relacionamento com User
    users = relationship('User', secondary=user_role, back_populates='roles')
