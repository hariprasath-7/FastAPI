"""add last few columns to posts table

Revision ID: 884bfb6d49ba
Revises: 0ebd61311877
Create Date: 2026-07-09 14:11:49.932726

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '884bfb6d49ba'
down_revision: Union[str, Sequence[str], None] = '0ebd61311877'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column(
        'published', sa.Boolean(), nullable = False, server_default= 'True'),)
    op.add_column('posts', sa.Column(
            'created_at', sa.TIMESTAMP(timezone=True), nullable = False, server_default = sa.text('NOW()')),
        )
    pass


def downgrade() -> None:
    op.dronp_column('posts', 'published')
    op.dronp_column('posts', 'created_at')
    pass
