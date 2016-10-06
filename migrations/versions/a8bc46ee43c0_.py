"""empty message

Revision ID: a8bc46ee43c0
Revises: 850d9df3e6e6
Create Date: 2016-10-06 19:15:38.229000

"""

# revision identifiers, used by Alembic.
revision = 'a8bc46ee43c0'
down_revision = '850d9df3e6e6'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('book', sa.Column('description', sa.String(length=512), nullable=True))
    op.add_column('book', sa.Column('imagepath', sa.String(length=140), nullable=True))
    op.add_column('user', sa.Column('provider', sa.String(length=128), nullable=True))
    op.create_index(op.f('ix_user_provider'), 'user', ['provider'], unique=False)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_provider'), table_name='user')
    op.drop_column('user', 'provider')
    op.drop_column('book', 'imagepath')
    op.drop_column('book', 'description')
    ### end Alembic commands ###
