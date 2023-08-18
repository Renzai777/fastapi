"""add last few columns to post table

Revision ID: 66568e156f65
Revises: de9387ceffab
Create Date: 2023-08-10 11:59:25.850975

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '66568e156f65'
down_revision: Union[str, None] = 'de9387ceffab'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("published", sa.Boolean(), nullable=False, server_default="TRUE"))
    pass


def downgrade() -> None:
    op.drop_column("posts", "published")

    pass
