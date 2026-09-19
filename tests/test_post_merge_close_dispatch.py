from pathlib import Path


WORKFLOW = Path(".github/workflows/post-merge-close-feature.yml")


def test_close_workflow_supports_validated_manual_dispatch():
    content = WORKFLOW.read_text(encoding="utf-8")

    assert "workflow_dispatch:" in content
    assert "pr_number:" in content
    assert "branch:" in content
    assert "version:" in content
    assert "slug:" in content
    assert "workflow_dispatch inputs no corresponden" in content
    assert 'github.event_name == \'workflow_dispatch\'' in content


def test_manual_dispatch_still_uses_official_close_script_and_pr_validation():
    content = WORKFLOW.read_text(encoding="utf-8")

    assert "./scripts/close-feature.ps1" in content
    assert "-PrNumber ${{ steps.feature.outputs.pr_number }}" in content
    assert "-SkipLocalCleanup" in content
