# Ember Atlas — owner review copy

Status: technical implementation in progress; not ready to submit as a validated release.

## Summary

Ember Atlas addresses how changes from MODIS to VIIRS can alter the apparent fire activity record in the Pantanal. It implements a NASA FIRMS ingestion pipeline, an occupied cell-day comparison, and a calendar interface linking sensor-specific observations to downloadable evidence.

## Project Details

Fire and land managers need to distinguish unusually active seasons from a change in sensor sensitivity. Ember Atlas places thermal anomaly detections on a globally anchored 0.05-degree grid per UTC day within the Pantanal study rectangle (59°W–54°W, 23°S–15°S). The target products are MODIS Standard Processing and VIIRS NOAA-20 Standard Processing. These are intended sources, not yet acquired observations in this release.

The reproducible seasonal transfer uses a chronological training/holdout split, requires at least three training and two holdout years, and compares monthly MAE and signed bias in occupied cell-days. No empirical validation or unusually active-season conclusion is currently available. Calibration remains unavailable. Cloud, sampling and overpass differences limit comparability; hotspots do not measure unique fires or burned area.

The first intended user is a regional fire or land-management organization preparing recurring seasonal reviews. A pilot would measure analyst time per review and reproducibility of exported evidence. Demand and willingness to pay are untested. Managed AOIs and scheduled reports are possible service hypotheses; NASA observations remain public resources.

## Use of Artificial Intelligence

OpenAI Codex assisted with repository inspection, software implementation, tests and documentation. No generated observations or synthetic public data were used. Tests use isolated fixtures. The team must review source correctness and verify real NASA observations and measured results before submission.

## Links and completion gates

Repository: https://github.com/dshimo0/ember-atlas

Project and Project Demonstration fields: pending verified scientific release and public media. Do not paste this draft as a completed project. Team Owner must reconcile current field limits and publish verified URLs, coverage, measured performance and team contributions before final submission. Terms acceptance and Submit for Judging remain solely with the Team Owner.
