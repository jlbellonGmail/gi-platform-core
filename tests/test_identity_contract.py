import json
from pathlib import Path


def test_identity_contract_manifest_is_json_and_compatible():
    root = Path(__file__).parents[1]
    schema = json.loads((root / "contracts/core-api-v0.2.0.json").read_text(encoding="utf-8"))
    manifest = json.loads((root / "contracts/core-api-v0.2.0.manifest.json").read_text(encoding="utf-8"))
    assert schema["version"] == manifest["contract_version"] == "0.2.0"
    assert manifest["compatible_with"] == ["0.1.0"]
    assert {item["name"] for item in manifest["operations"]} == {"validate_identity", "link_identity", "unlink_identity"}
