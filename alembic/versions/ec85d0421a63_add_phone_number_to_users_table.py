"""add phone number to users table

Revision ID: ec85d0421a63
Revises: 
Create Date: 2025-12-14 16:29:32.989878

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ec85d0421a63'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users',sa.Column('phone_number', sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column('users','phone_number')
