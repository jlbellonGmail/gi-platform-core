import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "release-readiness.ps1"


def run(*args):
    return subprocess.run(["pwsh", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(SCRIPT), *args], cwd=ROOT, text=True, capture_output=True)


def test_release_gate_is_safe_for_the_current_v200_candidate():
    result = run("-Version", "v2.0.0", "-DryRun")
    assert result.returncode != 0
    assert "manifiesto de alcance" in result.stderr


def test_release_gate_uses_the_current_release_manifest_not_historical_template_phases():
    content = SCRIPT.read_text(encoding="utf-8")
    assert "18-status-observabilidad" not in content
    assert "19-unidades-paralelizacion" not in content
    assert "20-releases-evolucion" not in content
    assert "21-validacion-integral-v2" not in content
    assert "22-auditoria-release-v2" not in content
    assert "manifest.json" in content
    assert "roadmapItems" in content


def test_release_gate_rejects_invalid_semver():
    result = run("-Version", "2.0.0", "-DryRun")
    assert result.returncode != 0
    assert "SemVer" in result.stderr


def test_release_script_is_read_only():
    content = SCRIPT.read_text(encoding="utf-8")
    assert "git tag" not in content
    assert "gh release create" not in content
    assert "git push" not in content
