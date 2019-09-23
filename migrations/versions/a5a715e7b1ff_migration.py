"""Migration

Revision ID: a5a715e7b1ff
Revises: ea90ab951ba8
Create Date: 2019-09-23 08:55:41.492510

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a5a715e7b1ff'
down_revision = 'ea90ab951ba8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('pitches', 'category',
               existing_type=sa.VARCHAR(length=255),
               nullable=False)
    op.alter_column('pitches', 'post',
               existing_type=sa.TEXT(),
               nullable=False)
    op.alter_column('pitches', 'title',
               existing_type=sa.VARCHAR(length=255),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('pitches', 'title',
               existing_type=sa.VARCHAR(length=255),
               nullable=True)
    op.alter_column('pitches', 'post',
               existing_type=sa.TEXT(),
               nullable=True)
    op.alter_column('pitches', 'category',
               existing_type=sa.VARCHAR(length=255),
               nullable=True)
    # ### end Alembic commands ###