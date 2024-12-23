"""empty message

Revision ID: 0408ec7df0da
Revises: d48baf4558e2
Create Date: 2024-09-11 12:24:45.666539

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '0408ec7df0da'
down_revision: Union[str, None] = 'd48baf4558e2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


from sqlalchemy.engine.reflection import Inspector
conn = op.get_bind()
inspector = Inspector.from_engine(conn)
tables = inspector.get_table_names()


def upgrade() -> None:

    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('questions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('text', sa.String(length=50), nullable=True),
    sa.Column('active', sa.Integer(), nullable=False),
    sa.Column('updated_dt', sa.DateTime(timezone=True), 
              server_default=sa.text("TIMEZONE('utc', now())"), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=255), nullable=False),
    sa.Column('password', sa.String(length=255), nullable=False),
    sa.Column('active', sa.Integer(), nullable=False, server_default="1"),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )

    op.create_table('answers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('text', sa.String(length=255), nullable=True),
    sa.Column('correct', sa.Boolean(), nullable=True),
    sa.Column('question_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['question_id'], ['questions.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )

    op.create_table('players',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('tg_id', sa.Integer(), nullable=False),
    sa.Column('score', sa.Integer(), nullable=False, server_default="0"),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('tg_id')
    )

    op.create_table('rounds',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('asked', sa.Boolean(), nullable=True, server_default="False"),
    sa.Column('question_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['question_id'], ['questions.id'], ondelete='CASCADE'),
    sa.Column('player_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['player_id'], ['players.tg_id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )

    if 'tg_update' not in tables:
        op.create_table('tg_update',
        sa.Column('id', sa.Integer(), nullable=False, server_default="0"),
        sa.PrimaryKeyConstraint('id')
        )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('rounds')
    op.drop_table('players')
    op.drop_table('answers')
    op.drop_table('users')
    op.drop_table('questions')

    # op.drop_table('tg_update')
    # ### end Alembic commands ###