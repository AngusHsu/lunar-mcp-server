# Astronomy dependency upgrade for v1.2.1

Issue #12 isolates the calculation-sensitive astronomy dependency changes for
the v1.2.1 patch release.

## Resolution

| Package | Before | After | Decision |
| --- | ---: | ---: | --- |
| `skyfield` | 1.53 | 1.54 | Upgraded and constrained to `>=1.54,<2`. |
| `ephem` | 4.2 | 4.2.1 | Upgraded and constrained to `>=4.2.1,<5`. |
| `astropy` | 7.1.0 | removed | Removed because neither runtime code nor tests import it. |
| `jplephem` | 2.23 | 2.24 | Required by the targeted Skyfield resolution. |
| `sgp4` | 2.25 | 2.27 | Required by the targeted Skyfield resolution. |
| `numpy` | 2.3.3 | 2.4.6 on Python 3.11; 2.5.1 on Python 3.12+ | Required by the targeted Skyfield resolution. |

Removing unused Astropy also removes its exclusive transitives `pyerfa` and
`astropy-iers-data`. No public lunar calculation uses those packages.

## Compatibility review

- [Skyfield 1.54's changelog](https://rhodesmill.org/skyfield/installation.html#changelog)
  records an updated Earth-orientation table, optional light-deflection
  controls, faster rise/setting searches, array subtraction support, and a
  topocentric-deflection bug fix. This project does not call the changed
  apparent-position or rise/setting APIs. The `Loader`, timescale, vector,
  observation, and angle APIs used here remain compatible, and the exact
  golden outputs below remain unchanged.
- [Ephem 4.2.1](https://pypi.org/project/ephem/4.2.1/) is a patch update. The
  project only probes the import today; it does not use Ephem to produce public
  results.
- Astropy 8.0.1 requires Python 3.11+, but upgrading it would retain a large,
  unused dependency tree. Removal is lower risk than an unused major upgrade.

## Golden-output policy

Golden fixtures were captured on the pre-upgrade lock and were not regenerated
after upgrading. They cover the labels and rounded illumination/angle values at
new-moon, quarter, and full-moon boundaries, plus consecutive UTC date inputs
using Asia/Taipei coordinates. Values are asserted exactly at the API's current
three-decimal illumination and one-decimal angle precision.

The API currently evaluates each input date at 00:00 UTC. Coordinates are
normalized and returned, while rise/set values remain placeholders and no
timezone parameter is supported. Issue #12 preserves this behavior rather than
mixing feature or algorithm changes into a dependency patch.

## Offline ephemeris behavior

Previously, `load("de421.bsp")` depended on the process working directory and a
clean wheel omitted the file, allowing Skyfield to attempt a network download.
DE421 is now package data and is resolved with `importlib.resources`. A test
changes to an empty working directory, rejects every Skyfield download attempt,
and initializes the calculator from the bundled ephemeris. Both wheel and sdist
contents are checked during release validation.
