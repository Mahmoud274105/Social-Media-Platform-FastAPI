"""add unique constrain to phone number in users table

Revision ID: 8ff95f628963
Revises: ec85d0421a63
Create Date: 2025-12-14 17:07:18.414350

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8ff95f628963'
down_revision: Union[str, Sequence[str], None] = 'ec85d0421a63'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_unique_constraint(
        "uq_users_phone_number",   # constraint name
        "users",                   # table name
        ["phone_number"]           # column(s)
    )


def downgrade():
    op.drop_constraint(
        "uq_users_phone_number",
        "users",
        type_="unique"
    )