"""empty message

Revision ID: 6abf81176a38
Revises: 43130cd7eeaf
Create Date: 2023-09-07 16:02:00.730073

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6abf81176a38'
down_revision: Union[str, None] = '43130cd7eeaf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
