"""add content column to posts table

Revision ID: b2bd8f673caf
Revises: b48920b41f62
Create Date: 2023-08-10 11:37:11.171382

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b2bd8f673caf'
down_revision: Union[str, None] = 'b48920b41f62'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("content" , sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column("posts", "content")
    pass
