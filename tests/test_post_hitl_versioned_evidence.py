from pathlib import Path


WORKFLOW = Path(".github/workflows/post-hitl-merge-gate.yml")


def _evidence_path(version: str, slug: str, filename: str) -> str:
    return f"runs/{version}/{slug}/{filename}"


def test_post_hitl_gate_resolves_evidence_from_feature_outputs():
    content = WORKFLOW.read_text(encoding="utf-8")

    assert "runs/v2.0.0/" not in content
    assert 'runs/${{ steps.feature.outputs.version }}/${{ steps.feature.outputs.slug }}/human-authorization.md' in content
    assert 'runs/${{ steps.feature.outputs.version }}/${{ steps.feature.outputs.slug }}/independent-review.md' in content
    assert 'runs/${{ steps.feature.outputs.version }}/${{ steps.feature.outputs.slug }}/integrity-evidence.md' in content


def test_feature_versions_resolve_to_distinct_evidence_directories():
    slug = "02-supabase-gi-dev-validation"

    v010 = _evidence_path("v0.1.0", slug, "human-authorization.md")
    v200 = _evidence_path("v2.0.0", slug, "human-authorization.md")

    assert v010 == "runs/v0.1.0/02-supabase-gi-dev-validation/human-authorization.md"
    assert v200 == "runs/v2.0.0/02-supabase-gi-dev-validation/human-authorization.md"
    assert v010 != v200
