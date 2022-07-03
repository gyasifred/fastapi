"""add users table

Revision ID: 686088c81c81
Revises: a09e4446e96a
Create Date: 2022-07-02 21:29:53.777872

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '686088c81c81'
down_revision = 'a09e4446e96a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                    )
    pass


def downgrade() -> None:
    op.drop_table("users")
    pass
