"""empty message

Revision ID: 256a3c9ab318
Revises: 
Create Date: 2019-04-06 14:37:27.078146

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '256a3c9ab318'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('addr',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('zip', sa.String(length=6), nullable=False),
    sa.Column('city', sa.String(length=64), nullable=False),
    sa.Column('street', sa.String(length=64), nullable=False),
    sa.Column('street_number', sa.Integer(), nullable=False),
    sa.Column('state', sa.String(length=64), nullable=False),
    sa.Column('country', sa.String(length=64), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('phone',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('phone_1', sa.String(length=9), nullable=False),
    sa.Column('phone_2', sa.String(length=9), nullable=True),
    sa.Column('phone_3', sa.String(length=9), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('chain',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=False),
    sa.Column('hotels_owned', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=128), nullable=False),
    sa.Column('rating', sa.Integer(), nullable=False),
    sa.Column('address', sa.Integer(), nullable=True),
    sa.Column('phone', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['address'], ['addr.id'], ),
    sa.ForeignKeyConstraint(['phone'], ['phone.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('pwd_hash', sa.String(length=128), nullable=True),
    sa.Column('sin', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=32), nullable=False),
    sa.Column('middle_name', sa.String(length=32), nullable=True),
    sa.Column('last_name', sa.String(length=32), nullable=False),
    sa.Column('email', sa.String(length=128), nullable=False),
    sa.Column('priv', sa.Integer(), nullable=False),
    sa.Column('address', sa.Integer(), nullable=True),
    sa.Column('phone', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['address'], ['addr.id'], ),
    sa.ForeignKeyConstraint(['phone'], ['phone.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)
    op.create_table('hotel',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('rooms_amt', sa.Integer(), nullable=False),
    sa.Column('rating', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=128), nullable=False),
    sa.Column('address', sa.Integer(), nullable=True),
    sa.Column('phone', sa.Integer(), nullable=True),
    sa.Column('manager', sa.Integer(), nullable=True),
    sa.Column('owned_by', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['address'], ['addr.id'], ),
    sa.ForeignKeyConstraint(['manager'], ['user.id'], ),
    sa.ForeignKeyConstraint(['owned_by'], ['chain.id'], ),
    sa.ForeignKeyConstraint(['phone'], ['phone.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('room',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('capacity', sa.Integer(), nullable=False),
    sa.Column('price', sa.Numeric(precision=2), nullable=False),
    sa.Column('condition', sa.String(length=256), nullable=False),
    sa.Column('view', sa.String(length=256), nullable=False),
    sa.Column('amenities', sa.String(length=256), nullable=False),
    sa.Column('extendable', sa.Boolean(), nullable=False),
    sa.Column('hotel_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['hotel_id'], ['hotel.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('archive',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('checked_in', sa.Boolean(), nullable=False),
    sa.Column('from_date', sa.Date(), nullable=False),
    sa.Column('to_date', sa.Date(), nullable=False),
    sa.Column('room', sa.Integer(), nullable=True),
    sa.Column('user', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['room'], ['room.id'], ),
    sa.ForeignKeyConstraint(['user'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('booking',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('checked_in', sa.Boolean(), nullable=False),
    sa.Column('from_date', sa.Date(), nullable=False),
    sa.Column('to_date', sa.Date(), nullable=False),
    sa.Column('room', sa.Integer(), nullable=True),
    sa.Column('user', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['room'], ['room.id'], ),
    sa.ForeignKeyConstraint(['user'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('bookings',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('room', sa.Integer(), nullable=True),
    sa.Column('date', sa.Date(), nullable=False),
    sa.ForeignKeyConstraint(['room'], ['room.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('bookings')
    op.drop_table('booking')
    op.drop_table('archive')
    op.drop_table('room')
    op.drop_table('hotel')
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_table('user')
    op.drop_table('chain')
    op.drop_table('phone')
    op.drop_table('addr')
    # ### end Alembic commands ###
