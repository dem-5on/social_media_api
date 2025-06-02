"""create table called post

Revision ID: 121708b41b6a
Revises: 
Create Date: 2025-06-02 11:56:36.549177

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '121708b41b6a'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Check if table exists before creating
    if not op.get_bind().dialect.has_table(op.get_bind(), 'posts'):
        op.create_table(
            'posts',
            sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
            sa.Column('title', sa.String(), nullable=False)
        )



def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('posts')
    pass
