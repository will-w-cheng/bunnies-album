"""Initial migration

Revision ID: 0ca9fe379667
Revises: 
Create Date: 2024-08-18 17:14:58.405029

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0ca9fe379667'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('album', schema=None) as batch_op:
        batch_op.add_column(sa.Column('image_path', sa.String(length=255), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('album', schema=None) as batch_op:
        batch_op.drop_column('image_path')

    # ### end Alembic commands ###
