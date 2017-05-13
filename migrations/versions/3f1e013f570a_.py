"""empty message

Revision ID: 3f1e013f570a
Revises: b7f1d120e922
Create Date: 2017-05-13 11:39:39.186086

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3f1e013f570a'
down_revision = 'b7f1d120e922'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('post', sa.Column('body_html', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('post', 'body_html')
    # ### end Alembic commands ###