"""empty message

Revision ID: d9ac923e0c6e
Revises: 6abf81176a38
Create Date: 2023-09-20 17:10:46.740094

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd9ac923e0c6e'
down_revision: Union[str, None] = '6abf81176a38'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
