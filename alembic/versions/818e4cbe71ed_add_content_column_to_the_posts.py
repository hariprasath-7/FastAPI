"""add content column to the posts

Revision ID: 818e4cbe71ed
Revises: f0f954770c9c
Create Date: 2026-07-08 17:59:29.770191

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '818e4cbe71ed'
down_revision: Union[str, Sequence[str], None] = 'f0f954770c9c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('posts', sa.Column('contents', sa.String(), nullable = False))
    pass


def downgrade():
    op.drop_column('posts', 'contents')
    pass
