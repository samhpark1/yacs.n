"""Major Template Table

Revision ID: da82686fce6e
Revises: c959c263997f
Create Date: 2024-10-15 21:13:59.912864

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'da82686fce6e'
down_revision = 'c959c263997f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('major_template',
    sa.Column('major', sa.VARCHAR(length=4), nullable=False),
    sa.Column('year', sa.INTEGER(), nullable=False),
    sa.Column('classes', postgresql.JSON(astext_type=sa.Text()), nullable=False),
    sa.PrimaryKeyConstraint('major', 'year')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('major_template')
    # ### end Alembic commands ###
