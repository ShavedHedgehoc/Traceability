"""empty message

Revision ID: da7b277b020a
Revises: e5fc690e9aee
Create Date: 2021-03-19 13:22:32.969657

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'da7b277b020a'
down_revision = 'e5fc690e9aee'
branch_labels = None
depends_on = None


def upgrade(engine_name):
    globals()["upgrade_%s" % engine_name]()


def downgrade(engine_name):
    globals()["downgrade_%s" % engine_name]()





def upgrade_():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade_():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def upgrade_data():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('XMLData', sa.Column('catched', sa.Boolean(), server_default=sa.text('0'), nullable=True))
    op.add_column('XMLData', sa.Column('task_id', sa.String(length=64), nullable=True))
    op.create_index(op.f('ix_XMLData_task_id'), 'XMLData', ['task_id'], unique=False)
    # ### end Alembic commands ###


def downgrade_data():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_XMLData_task_id'), table_name='XMLData')
    op.drop_column('XMLData', 'task_id')
    op.drop_column('XMLData', 'catched')
    # ### end Alembic commands ###
