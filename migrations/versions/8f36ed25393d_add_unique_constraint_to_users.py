"""Add unique constraint to users

Revision ID: 8f36ed25393d
Revises: 69382a0c5998
Create Date: 2024-04-27 09:26:14.045273

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8f36ed25393d'
down_revision: Union[str, None] = '69382a0c5998'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_unique_constraint('uq_roles_email', 'users', ['email'])
    op.create_unique_constraint('uq_roles_username', 'users', ['username'])

def downgrade():
    op.drop_constraint('uq_roles_email', 'users', type_='unique')
    op.drop_constraint('uq_roles_username', 'users', type_='unique')
