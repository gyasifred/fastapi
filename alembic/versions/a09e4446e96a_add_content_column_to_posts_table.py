"""add content column to posts table

Revision ID: a09e4446e96a
Revises: 8c33afa61904
Create Date: 2022-07-02 21:07:44.403294

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a09e4446e96a'
down_revision = '8c33afa61904'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column("posts", 'content')
    pass
