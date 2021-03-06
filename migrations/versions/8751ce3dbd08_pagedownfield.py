"""PageDownField

Revision ID: 8751ce3dbd08
Revises: b93153e6f10f
Create Date: 2020-06-17 22:41:41.792485

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8751ce3dbd08'
down_revision = 'b93153e6f10f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('posts', sa.Column('body_html', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('posts', 'body_html')
    # ### end Alembic commands ###
