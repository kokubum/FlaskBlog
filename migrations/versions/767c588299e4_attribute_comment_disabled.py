"""attribute Comment disabled

Revision ID: 767c588299e4
Revises: 5a8d8e580b23
Create Date: 2020-06-19 11:13:32.797939

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '767c588299e4'
down_revision = '5a8d8e580b23'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('comments', sa.Column('disabled', sa.Boolean(), nullable=True))
    op.create_index(op.f('ix_comments_time_stamp'), 'comments', ['time_stamp'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_comments_time_stamp'), table_name='comments')
    op.drop_column('comments', 'disabled')
    # ### end Alembic commands ###