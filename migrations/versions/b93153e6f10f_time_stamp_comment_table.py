"""Time Stamp Comment Table

Revision ID: b93153e6f10f
Revises: 06ff40a61848
Create Date: 2020-06-17 19:15:51.871081

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b93153e6f10f'
down_revision = '06ff40a61848'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('comments', sa.Column('time_stamp', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('comments', 'time_stamp')
    # ### end Alembic commands ###
