"""Add View user_permissions

Revision ID: 49e6183425c3
Revises: d3ededb8ce83
Create Date: 2024-03-30 23:16:16.571263

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = '49e6183425c3'
down_revision: Union[str, None] = 'd3ededb8ce83'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Criação da view user_permissions
    op.execute("""
        CREATE OR REPLACE VIEW user_permissions AS
        SELECT tasks.tag_name, actions.name AS action_name, users.username, applications.acronym,
               tasks.id AS task_id, roles.id AS role_id, actions.id AS action_id, users.id AS user_id,
               tasks.name AS task_name, roles.name AS role_name, users.name
        FROM actions
        JOIN tasks ON actions.task_id = tasks.id
        JOIN role_action ON actions.id = role_action.action_id
        JOIN roles ON role_action.role_id = roles.id
        JOIN applications ON roles.application_id = applications.id
        JOIN user_role ON roles.id = user_role.role_id
        JOIN users ON user_role.user_id = users.id
    """)

def downgrade():
    # Remoção da view user_permissions
    op.execute("DROP VIEW IF EXISTS user_permissions")