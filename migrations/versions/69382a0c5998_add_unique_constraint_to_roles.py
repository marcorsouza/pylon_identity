"""Add unique constraint to roles

Revision ID: 69382a0c5998
Revises: 49e6183425c3
Create Date: 2024-04-26 20:21:07.287061

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '69382a0c5998'
down_revision: Union[str, None] = '49e6183425c3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    op.create_unique_constraint('uq_roles_name_application_id', 'roles', ['name', 'application_id'])

def downgrade():
    op.drop_constraint('uq_roles_name_application_id', 'roles', type_='unique')
