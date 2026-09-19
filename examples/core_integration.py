"""Minimal host-side consumption example for GI-PLATFORM-CORE.

The host application owns configuration and chooses the persistence adapter.
Dental-specific entities and rules must remain outside this example.
"""

from gi_platform_core import CoreApi, CoreService, InMemoryCoreStore


def build_core() -> CoreApi:
    store = InMemoryCoreStore()
    service = CoreService(store)
    service.create_permission("location:read", "Read locations")
    return CoreApi(service)


if __name__ == "__main__":
    api = build_core()
    organization = api.create_organization("Example organization")
    user = api.create_user("example-subject", "Example user")
    membership = api.add_membership(user["id"], organization["id"])
    role = api.create_role(organization["id"], "reader", {"location:read"})
    api.assign_role(membership["id"], role["id"])
    location = api.create_location(organization["id"], "Main location")
    api.grant_location_access(membership["id"], location["id"])
    print(api.authorize(user["id"], organization["id"], "location:read", location["id"]))
