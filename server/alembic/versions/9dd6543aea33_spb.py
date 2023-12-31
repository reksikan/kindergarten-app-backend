"""spb

Revision ID: 9dd6543aea33
Revises: 1020ac804b99
Create Date: 2023-12-26 18:47:22.737067

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9dd6543aea33'
down_revision: Union[str, None] = '1020ac804b99'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('sbp_payments',
    sa.Column('receipt_id', sa.Integer(), nullable=False),
    sa.Column('link', sa.String(), nullable=False),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['receipt_id'], ['receipts.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('receipt_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('sbp_payments')
    # ### end Alembic commands ###
