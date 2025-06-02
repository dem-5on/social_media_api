"""create user table with all columns

Revision ID: 1e271973a0d6
Revises: d48cbf0a16d8
Create Date: 2025-06-02 14:17:20.638883

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1e271973a0d6'
down_revision: Union[str, None] = 'd48cbf0a16d8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    if not op.get_bind().dialect.has_table(op.get_bind(), 'users'):
        op.create_table(
            'users',
            sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
            sa.Column('email', sa.String(), nullable=False, unique=True),
            sa.Column('password', sa.String(),nullable=False ),
            sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=(sa.text('now()')))
        )
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('users')
    pass
