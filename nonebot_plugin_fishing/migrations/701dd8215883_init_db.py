"""init db

迁移 ID: 701dd8215883
父迁移: 
创建时间: 2024-03-24 11:32:01.614944

"""
from __future__ import annotations

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa


revision: str = '701dd8215883'
down_revision: str | Sequence[str] | None = None
branch_labels: str | Sequence[str] | None = ('nonebot_plugin_fishing',)
depends_on: str | Sequence[str] | None = None


def upgrade(name: str = "") -> None:
    if name:
        return
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('nonebot_plugin_fishing_fishingrecord',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.String(), nullable=False),
    sa.Column('time', sa.Integer(), nullable=False),
    sa.Column('frequency', sa.Integer(), nullable=False),
    sa.Column('fishes', sa.String(), nullable=False),
    sa.Column('coin', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_nonebot_plugin_fishing_fishingrecord')),
    info={'bind_key': 'nonebot_plugin_fishing'}
    )
    # ### end Alembic commands ###


def downgrade(name: str = "") -> None:
    if name:
        return
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('nonebot_plugin_fishing_fishingrecord')
    # ### end Alembic commands ###
