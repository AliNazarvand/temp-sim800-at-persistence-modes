# SIM800 AT Persistence Modes - full pipeline bootstrap
# Usage: pwsh -File scripts/bootstrap.ps1
param(
    [switch]$SkipExtract,
    [switch]$SkipBuild
)

$ErrorActionPreference = "Stop"
$script:fail = $false
$root = Split-Path -Parent $PSScriptRoot
Set-Location -LiteralPath $root

$py = "python"

function Step {
    param([string]$Name, [scriptblock]$Action)
    Write-Host "==== $Name ===="
    try {
        & $Action
        if ($LASTEXITCODE -ne 0) {
            Write-Host "FAIL: $Name (exit $LASTEXITCODE)" -ForegroundColor Red
            $script:fail = $true
        } else {
            Write-Host "OK:   $Name" -ForegroundColor Green
        }
    } catch {
        Write-Host "FAIL: $Name - $_" -ForegroundColor Red
        $script:fail = $true
    }
}

# Correct pipeline order: extract -> validate -> generate -> check -> test -> build -> reports
Step "1. Download PDFs" { & $py scripts/fetch_sources.py }
if (-not $SkipExtract) {
    Step "2. Extract persistence (best-effort)" { & $py scripts/extract_persistence.py }
}
Step "3. Validate" { & $py scripts/validate.py }
Step "4. Generate headers" { & $py scripts/generate_headers.py }
Step "5. Check brace balance" { & $py scripts/check_brace_balance.py }
Step "6. Doc examples check" { & $py scripts/check_doc_examples.py }
Step "7. Python tests" { & $py -m pytest tests/test_validation.py -q }
Step "8. Generate reports" { & $py scripts/generate_reports.py }

if (-not $SkipBuild) {
    Step "9. Configure CMake" {
        if (-not (Test-Path "build")) {
            cmake -B build -G "MinGW Makefiles" .
            if ($LASTEXITCODE -ne 0) { cmake -B build . }
        }
    }
    Step "10. Build" { cmake --build build }
    Step "11. ctest" { ctest --test-dir build --output-on-failure }
}

if ($script:fail) {
    Write-Host "Pipeline finished with FAILURES." -ForegroundColor Red
    exit 1
}
Write-Host "Pipeline finished successfully." -ForegroundColor Green
exit 0