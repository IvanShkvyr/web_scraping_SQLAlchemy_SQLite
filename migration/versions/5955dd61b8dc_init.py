"""Init

Revision ID: 5955dd61b8dc
Revises: 
Create Date: 2023-01-07 12:16:18.157153

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5955dd61b8dc'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('authors',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('fullname', sa.String(length=30), nullable=False),
    sa.Column('date_of_birth', sa.Date(), nullable=True),
    sa.Column('lint_to_info', sa.String(length=250), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('fullname')
    )
    op.create_table('tags',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('text', sa.String(length=1200), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('text')
    )
    op.create_table('quotes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('text', sa.String(length=50), nullable=False),
    sa.Column('author_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['author_id'], ['authors.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('text')
    )
    op.create_table('tags_to_quotes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('tag_id', sa.Integer(), nullable=True),
    sa.Column('quotes_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['quotes_id'], ['quotes.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['tag_id'], ['tags.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tags_to_quotes')
    op.drop_table('quotes')
    op.drop_table('tags')
    op.drop_table('authors')
    # ### end Alembic commands ###
