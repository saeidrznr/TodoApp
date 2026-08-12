"""Create phone number for user column

Revision ID: e131b0af8f4a
Revises: 
Create Date: 2026-08-11 13:16:29.142374

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e131b0af8f4a'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('phone_number',sa.String(11), nullable=True))


def downgrade() -> None:
    op.drop_column('users', 'phone_number')
