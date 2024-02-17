"""
https://strftime.org/

https://docs.python.org/3/library/datetime.html#datetime.datetime.timestamp

https://www.ietf.org/archive/id/draft-peabody-dispatch-new-uuid-format-01.html#name-uuidv7-layout-and-bit-order

https://news.ycombinator.com/item?id=36102801

https://github.com/oittaa/uuid6-python/issues/28

class Meta is not inherited
"""

from django.conf import settings  # DEPRECATED ?

from django.db import models  # DEPRECATED
from django.db.models import DateTimeField, UUIDField

import uuid6  # DEPRECATED
from uuid6 import uuid7


class Foundation(models.Model):

    uuid = UUIDField(primary_key=True, editable=False, default=uuid7,
        verbose_name='UUID v7'
    )

    row_add = DateTimeField(auto_now_add=True, verbose_name='Row Added Timestamp')

    row_mod = DateTimeField(auto_now=True, verbose_name='Row Modified Timestamp')

    class Meta:
        abstract = True

    def get_edit_path(self):
        app = self._meta.app_label
        model = self._meta.model_name
        return f"{app}/{model}/{self.pk}/change/"

# ==============================================================================
# OLDER ITERATIONS (for legacy models)
# ==============================================================================

class Timestamps(models.Model):

    # row_updated = models.BooleanField(default = False)
    # theoretically this column should be redundant with a UUID v7 column, alas
    # thusfar dates extracted from the UUID v7 value are only valid in the
    # Python REPL, not in Django model methods

    # row_add_ts
    row_add = models.DateTimeField(auto_now_add=True,
        verbose_name='Row Added Timestamp'
    )

    # row_updated_timestamp = models.DateTimeField(auto_now=True)
    row_mod = models.DateTimeField(auto_now=True,
        verbose_name='Row Modified Timestamp'
    )


    class Meta:
        abstract = True




    """
    # UPDATED TIME VARIANTS
    def row_updated_ts_pretty(self):
        return self.row_updated_ts_auto.strftime(
            settings.TIMESTAMP_WITH_ZONE_PRETTY)

    def row_updated_ts_ugly(self):
        return self.row_updated_ts_auto.strftime(settings.TIMESTAMP_WITH_ZONE)

    def row_updated_ts_unix(self):
        return self.row_updated_ts_auto.strftime('%s')

    def row_updated(self):
        return self.row_updated_ts_auto.strftime(settings.DATE_SHORT)

    # CREATED TIME VARIANTS
    def row_created_ts_pretty(self):
        return self.row_created_ts_auto.strftime(
            settings.TIMESTAMP_WITH_ZONE_PRETTY)

    def row_created_ts_ugly(self):
        return self.row_created_ts_auto.strftime(settings.TIMESTAMP_WITH_ZONE)

    def row_created_ts_unix(self):
        return self.row_created_ts_auto.strftime('%s')

    def row_created(self):
        return self.row_created_ts_auto.strftime(settings.DATE_SHORT)
    """

# ------------------------------------------------

class EditLink(models.Model):

    class Meta:
        abstract = True

    def get_edit_path(self):
        app = self._meta.app_label
        model = self._meta.model_name
        return f"{app}/{model}/{self.pk}/change/"

# ------------------------------------------------

class EditLinkWithTS(Timestamps):

    class Meta:
        abstract = True

    def get_edit_path(self):
        app = self._meta.app_label
        model = self._meta.model_name
        return f"{app}/{model}/{self.pk}/change/"

# ------------------------------------------------

class UUIDpk(models.Model):
    # using parens for the default value function, e.g.
    #    default=uuid6.uuid7()
    # causes the same migration to be created infinitely in Django models. In
    # contrast, parens are required in the Python REPL. So is an incorrect epoch
    # being encoded into the id when used in Django models? Notably, the
    # extraction of UTC timestamps from UUID v7 only seems accurate in the REPL,
    # but NOT in Django model methods. So for now we're just relying on UUID v7
    # for a unique, sortable primary key compatible with distributed environments.
    uuid = models.UUIDField(primary_key=True, editable=False, 
        default=uuid6.uuid7, verbose_name="UUID v7"
    )

    class Meta:
        abstract = True
