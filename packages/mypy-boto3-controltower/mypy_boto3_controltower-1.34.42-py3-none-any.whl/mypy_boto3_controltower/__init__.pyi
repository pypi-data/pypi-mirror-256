"""
Main interface for controltower service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_controltower import (
        Client,
        ControlTowerClient,
        ListBaselinesPaginator,
        ListEnabledBaselinesPaginator,
        ListEnabledControlsPaginator,
        ListLandingZonesPaginator,
    )

    session = Session()
    client: ControlTowerClient = session.client("controltower")

    list_baselines_paginator: ListBaselinesPaginator = client.get_paginator("list_baselines")
    list_enabled_baselines_paginator: ListEnabledBaselinesPaginator = client.get_paginator("list_enabled_baselines")
    list_enabled_controls_paginator: ListEnabledControlsPaginator = client.get_paginator("list_enabled_controls")
    list_landing_zones_paginator: ListLandingZonesPaginator = client.get_paginator("list_landing_zones")
    ```
"""

from .client import ControlTowerClient
from .paginator import (
    ListBaselinesPaginator,
    ListEnabledBaselinesPaginator,
    ListEnabledControlsPaginator,
    ListLandingZonesPaginator,
)

Client = ControlTowerClient

__all__ = (
    "Client",
    "ControlTowerClient",
    "ListBaselinesPaginator",
    "ListEnabledBaselinesPaginator",
    "ListEnabledControlsPaginator",
    "ListLandingZonesPaginator",
)
