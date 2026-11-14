# Release checklist

Checked 2026-11-14 UTC. Status is evidence-based; no final submission was attempted.

| Gate | Status | Owner / evidence / next action |
|---|---|---|
| Existing repository preserved | Verified | Clean main at 0785c3e before new feature branch; original history retained |
| Existing automated tests | Verified | 3 initial tests passed |
| FIRMS public documentation reachable | Verified | HTTP 200 with authorized network access |
| FIRMS secret and availability | Pending | Owner configures FIRMS_MAP_KEY as runtime ingestion secret; then run availability |
| Real paired slice and matched years | Pending | Run runbook acquisition after availability; pin manifests |
| Empirical holdout and sensitivity results | Pending | Run evaluation on real data; review grid/confidence/platform diagnostics |
| Anonymous complete data workflow | Pending | Real snapshot needed; browser CSV, map and calendar checks outstanding |
| Historical comparison and calibration evidence | Pending | Adequate complete matched years needed |
| English UI and source materials | Verified | Authored interface and submission documentation are English |
| Public media and demonstration format | Pending | No recording; owner verifies current official guide independently of pitch |
| No minors / subtitle review | Pending | Review finished recording; no people assets currently used |
| Current official resources and challenge links | Pending | HTTP errors encountered; current portal and guide need owner inspection |
| Product/version/rights inventory | Pending | Resource inventory distinguishes intended sources from used data |
| Member registration/event/waitlist | Pending | Team Owner checks private portal records |
| Pre-existing work eligibility | Pending | Owner consults Local Lead; history predates this session and must not be relabeled |
| Deadline and local pitch cutoff | Pending | Addendum states Nov 15 2026 23:59 São Paulo; owner must independently confirm |
| AI disclosure | Verified | Draft identifies Codex assistance and fixture-only synthetic data |
| Save portal, preview links and submit | Pending | Team Owner accepts terms and explicitly selects Submit for Judging; capture private confirmation |

## Executed verification update

- Nine unit tests pass; JavaScript syntax check passes.
- Local Chromium verified unavailable-data state, disabled download, area/sensor/month controls and 1440px/390px layouts without page errors or horizontal overflow. Actual captures: `interface-desktop.png`, `interface-mobile.png`. These show the current unavailable-data interface, not a scientific demonstration.
- Vercel creation request returned HTTP 403: “You don't have permission to create a project.” No live URL exists. No CLI fallback is installed. Owner must provide an existing accessible project or project-creation permission.
- Official resources and challenge pages returned HTTP 503 on 2026-11-14. Demo format and current portal fields remain unverified.
- Draft pull request: https://github.com/dshimo0/ember-atlas/pull/1 ; main has not been merged or changed.
