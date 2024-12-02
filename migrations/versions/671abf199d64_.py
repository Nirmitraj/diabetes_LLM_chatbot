"""empty message

Revision ID: 671abf199d64
Revises: b893ca6e995b
Create Date: 2024-12-01 21:16:18.882028

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '671abf199d64'
down_revision = 'b893ca6e995b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('chat_history',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=255), nullable=False),
    sa.Column('last_message', sa.Text(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('role', sa.String(length=10), nullable=True),
    sa.Column('content', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.create_unique_constraint('uq_user_email', ['email'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')
        batch_op.drop_constraint('uq_user_email', type_='unique')

    op.drop_table('chat_history')
    # ### end Alembic commands ###
