"""add foregin-key to post table

Revision ID: 0ebd61311877
Revises: c069fcc77532
Create Date: 2026-07-09 13:23:22.182030

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0ebd61311877'
down_revision: Union[str, Sequence[str], None] = 'c069fcc77532'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column('owner_id', sa.Integer(), nullable = False))
    op.create_foreign_key('post_user_fk', source_table = "posts", referent_table = "users", local_cols=['owner_id'], remote_cols=['id'], ondelete= "CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint('posts_user-fk', table_name = "posts")
    op.drop_column('posts', 'owner_id')
    pass
