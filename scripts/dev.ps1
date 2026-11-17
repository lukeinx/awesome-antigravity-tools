<#
.SYNOPSIS
    Developer task runner for awesome-antigravity-tools on Windows PowerShell.
.EXAMPLE
    pwsh .\scripts\dev.ps1 -Task all
    pwsh .\scripts\dev.ps1 -Task serve
#>
[CmdletBinding()]
param(
    [ValidateSet('all', 'validate', 'generate', 'export', 'build-site', 'test', 'audit', 'discover', 'serve')]
    [string]$Task = 'all',
    [int]$Port = 8765
)

$ErrorActionPreference = 'Stop'
$repoRoot = Split-Path -Parent $PSScriptRoot
Push-Location $repoRoot

try {
    switch ($Task) {
        'validate' {
            python scripts/validate_catalog.py --check-sync --strict-warnings
            python scripts/build_site.py --check
            python scripts/export_catalog.py --check
        }
        'generate' {
            python scripts/validate_catalog.py --fix-order
            python scripts/generate_badges.py
            python scripts/generate_docs.py
            python scripts/export_catalog.py
            python scripts/build_site.py
        }
        'export' {
            python scripts/export_catalog.py
        }
        'build-site' {
            python scripts/build_site.py
        }
        'test' {
            python -m unittest discover -s tests -v
            node --check docs/catalog-logic.js
            node --check docs/insights.js
            node --check docs/app.js
            node --test tests/test_web.mjs
        }
        'audit' {
            python scripts/health-check.py --use-gh-cli
            python scripts/generate_badges.py
            python scripts/generate_docs.py
            python scripts/export_catalog.py
            python scripts/build_site.py
        }
        'discover' {
            python scripts/discover_candidates.py --use-gh-cli --limit 15
        }
        'serve' {
            Write-Host "Serving docs/ at http://127.0.0.1:$Port/ (Ctrl+C to stop)" -ForegroundColor Cyan
            python -m http.server $Port --directory docs
        }
        'all' {
            python scripts/validate_catalog.py --fix-order
            python scripts/generate_badges.py
            python scripts/generate_docs.py
            python scripts/export_catalog.py
            python scripts/build_site.py
            python scripts/validate_catalog.py --check-sync --strict-warnings
            python scripts/build_site.py --check
            python scripts/export_catalog.py --check
            python -m unittest discover -s tests -v
            node --test tests/test_web.mjs
        }
    }
} finally {
    Pop-Location
}
