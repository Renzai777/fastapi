"""Adding created_at column in posts table

Revision ID: a28b71038269
Revises: 66568e156f65
Create Date: 2023-08-10 12:18:55.789231

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a28b71038269'
down_revision: Union[str, None] = '66568e156f65'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text("now()")))

    pass


def downgrade() -> None:
    op.drop_column("posts", "created_at")

    pass
