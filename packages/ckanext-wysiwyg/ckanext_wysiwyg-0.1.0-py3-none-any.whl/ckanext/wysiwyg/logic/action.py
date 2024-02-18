from __future__ import annotations

import logging

from ckan.logic import validate
from ckan.plugins import toolkit as tk


log = logging.getLogger(__name__)


# @validate(cron_schema.add_cron_job)
@tk.side_effect_free
def ckeditor5_image_upload(context, data_dict):
    pass
