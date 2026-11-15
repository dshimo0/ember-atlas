# Local acquisition and calibration

Python 3.10+; standard library only. Run from the repository root on Windows,
macOS or Linux. No GPU or deep-learning training is needed. This performs statistical
calibration and evaluation. Download sizes and duration depend on region, period and
FIRMS quota; start with Chilecito. No files are automatically published to Vercel.

## PowerShell

Enter the key privately in this terminal session:

```powershell
$secret = Read-Host 'FIRMS MAP KEY' -AsSecureString
$env:FIRMS_MAP_KEY = [System.Net.NetworkCredential]::new('', $secret).Password
python scripts/firms.py availability
python scripts/regional_calibration.py plan --region chilecito
python scripts/regional_calibration.py fetch --region chilecito
python scripts/regional_calibration.py evaluate --region chilecito
Remove-Item Env:FIRMS_MAP_KEY
```

Check availability before fetching. Default fit window is 2020–2022; evaluation
2023–2024. These are protocol defaults, not an assertion of available complete inputs
or a new blind holdout for previously inspected regions. Do not tune using the evaluation
results and then describe them as independent confirmation.

On an explicit FIRMS transaction-quota error, the script waits 11 minutes with
minute-by-minute progress and retries up to three times. Other failures stop immediately.
After exhausted retries the script records the failed window and exits
nonzero. Remaining planned windows are unattempted. Correct availability/quota issues
and rerun the identical command: verified payloads are reused. Keep start/end identical
when resuming. Different windows have separate output directories.

## History and event review

After checking source availability, request earlier MODIS separately:

```powershell
python scripts/regional_calibration.py plan --region chilecito --sources MODIS_SP --start 2001-01-01 --end 2019-12-31
python scripts/regional_calibration.py fetch --region chilecito --sources MODIS_SP --start 2001-01-01 --end 2019-12-31
```

For the author's July 2026 case, check availability of SP and archived NRT first.
The following is only a plan until the availability review confirms these dates:

```powershell
python scripts/regional_calibration.py plan --region chilecito --sources MODIS_NRT,VIIRS_NOAA20_NRT --start 2026-07-20 --end 2026-08-05
```

Replace `plan` with `fetch` only for an available product/window. If unavailable,
use an official archive acquisition workflow and retain manifests; this runner does
not invent archive results or import arbitrary archive formats automatically.
NRT cannot be calibrated by this runner or silently appended to SP.

Use `--region` for any of the eight existing region IDs. Run one region at a time.
The nine-region list is visible in `--help`. Chilecito's provisional rectangle is
defined in the script and spec 004; it is not yet a published preset or official boundary.

## Outputs and review

Under `data/local-calibration/<region>/<start>_<end>/`:

- Original CSV and SHA manifests, acquisition plan/status.
- `daily.csv`: counts and occupied cells per product/day; no row for missing retrieval.
- `validation.json`: seasonal fit, all monthly pairs, excluded months and support gate.
- `comparison.json`: raw/scalar/seasonal held-out errors and peak-month comparison,
  produced only when support is sufficient. The scalar is estimated on training only.

Inspect bias, peaks and baseline comparison before approving a transfer. A successful
legacy seasonal gate does not prove improvement over the scalar or approve deployment.
Review zero-activity regions and coordinate validity. Hash-verified empty retrievals
do not establish cloud-free observation. Preserve original frozen Pantanal artifacts.

Integration is a separate task: verified input import, regional registry, local map
fallback, model selection protocol, UI and export wiring, then end-to-end tests.
Never copy a regional model into the Pantanal validation file.
