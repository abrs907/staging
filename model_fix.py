"""
This file defines the database models
"""

from pydal.validators import *

from .common import Field, db

db.define_table("cars",
                Field("car_make", "string", help="Car Make & Model",
                      required=True, unique=True,
                      format="%(car_make)s")
                )

db.define_table("owner",
                Field("owner_name", "string", required=True),
                Field("cars", "list:reference cars", multiple=True)
                )


# --- Workaround: make "cars" display as a list of car names ---
# This pydal version does not derive <table>._format from a field's format,
# and list:reference fields do not get a default represent/validator here.
# Set them explicitly so Grids and Forms render a list of cars instead of ids.
db.cars._format = lambda r: r.get("car_make") or r.id
db.owner.cars.requires = IS_IN_DB(db, "cars.id", db.cars._format, multiple=True)
db.owner.cars.represent = (
    lambda value, row=None: ", ".join(
        db.cars._format(db.cars(v)) for v in (value or [])
    )
    if value
    else ""
)

db.commit()


# Define your table below
#
# db.define_table('thing', Field('name'))
#
# always commit your models to avoid problems later
#
# db.commit()
#
