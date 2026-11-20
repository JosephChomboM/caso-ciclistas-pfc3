from alembic import context

from app.core.db import Base, engine
from app.modules.billing.models import Invoice, Subscription  # noqa: F401
from app.modules.cycleways.models import Cycleway  # noqa: F401
from app.modules.parking.models import Favorite, Parking  # noqa: F401
from app.modules.reports.models import ModerationAction, Report  # noqa: F401
from app.modules.users.models import User  # noqa: F401

if context.is_offline_mode():
    context.configure(url=str(engine.url), target_metadata=Base.metadata, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()
else:
    with engine.connect() as connection:
        context.configure(connection=connection, target_metadata=Base.metadata)
        with context.begin_transaction():
            context.run_migrations()
