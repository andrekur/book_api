"""edit discount_price

Revision ID: b76c17ea9bb5
Revises: fc7c0699febe
Create Date: 2022-05-30 10:04:21.964301

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b76c17ea9bb5'
down_revision = 'fc7c0699febe'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('books_prices', sa.Column('discount', sa.Integer(), nullable=True))
    op.drop_column('books_prices', 'discount_price')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('books_prices', sa.Column('discount_price', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_column('books_prices', 'discount')
    # ### end Alembic commands ###
