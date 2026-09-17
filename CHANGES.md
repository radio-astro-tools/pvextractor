## v0.5 - 2026-09-17

<!-- Release notes generated using configuration in .github/release.yml at v0.5 -->
### What's Changed

#### Other Changes

* Bump the actions group in /.github/workflows with 5 updates by @dependabot[bot] in https://github.com/radio-astro-tools/pvextractor/pull/123
* Remove unused distutils import by @smaret in https://github.com/radio-astro-tools/pvextractor/pull/129
* fix: Address flake8 W605: SyntaxError: invalid escape sequence '('. by @Hellseher in https://github.com/radio-astro-tools/pvextractor/pull/125
* CI updates by @e-koch in https://github.com/radio-astro-tools/pvextractor/pull/130
* Bump the actions group in /.github/workflows with 2 updates by @dependabot[bot] in https://github.com/radio-astro-tools/pvextractor/pull/131
* Update badges  in README.rst by @keflavich in https://github.com/radio-astro-tools/pvextractor/pull/132
* Remove e-mail address from author by @keflavich in https://github.com/radio-astro-tools/pvextractor/pull/133
* Bump actions/download-artifact from 4 to 5 in /.github/workflows in the actions group by @dependabot[bot] in https://github.com/radio-astro-tools/pvextractor/pull/134
* Bump actions/checkout from 4 to 5 in /.github/workflows in the actions group by @dependabot[bot] in https://github.com/radio-astro-tools/pvextractor/pull/135
* Bump actions/setup-python from 5 to 6 in /.github/workflows in the actions group by @dependabot[bot] in https://github.com/radio-astro-tools/pvextractor/pull/136
* Bump the actions group across 1 directory with 3 updates by @dependabot[bot] in https://github.com/radio-astro-tools/pvextractor/pull/138
* Bump actions/checkout from 5 to 6 in /.github/workflows in the actions group by @dependabot[bot] in https://github.com/radio-astro-tools/pvextractor/pull/139
* Bump the actions group in /.github/workflows with 2 updates by @dependabot[bot] in https://github.com/radio-astro-tools/pvextractor/pull/140
* Bump the actions group in /.github/workflows with 2 updates by @dependabot[bot] in https://github.com/radio-astro-tools/pvextractor/pull/141
* Bump actions/checkout from 6 to 7 in /.github/workflows in the actions group by @dependabot[bot] in https://github.com/radio-astro-tools/pvextractor/pull/143
* Bump the actions group across 1 directory with 2 updates by @dependabot[bot] in https://github.com/radio-astro-tools/pvextractor/pull/145
* CI: add weekly cron test run and switch to PyPI trusted publishing by @e-koch in https://github.com/radio-astro-tools/pvextractor/pull/146
* Docs once-over: fix stale links, broken example, typos by @e-koch in https://github.com/radio-astro-tools/pvextractor/pull/147
* Bump minimum spectral-cube and radio-beam by @e-koch in https://github.com/radio-astro-tools/pvextractor/pull/148
* Install nightly builds in dev CI jobs by @e-koch in https://github.com/radio-astro-tools/pvextractor/pull/149

### New Contributors

* @dependabot[bot] made their first contribution in https://github.com/radio-astro-tools/pvextractor/pull/123
* @smaret made their first contribution in https://github.com/radio-astro-tools/pvextractor/pull/129
* @Hellseher made their first contribution in https://github.com/radio-astro-tools/pvextractor/pull/125
* @e-koch made their first contribution in https://github.com/radio-astro-tools/pvextractor/pull/130

**Full Changelog**: https://github.com/radio-astro-tools/pvextractor/compare/v0.4...v0.5

## v0.4 - 2023-11-16

<!-- Release notes generated using configuration in .github/release.yml at main -->
### What's Changed

#### New Features

- Fix for 107: allow user to ignore non-square pixel error by @keflavich in https://github.com/radio-astro-tools/pvextractor/pull/113

#### Bug Fixes

- issubclass replaced by isinstance in PVSlicer by @lpda in https://github.com/radio-astro-tools/pvextractor/pull/112
- Non-square bug in get_spatial_scale fixed by @lpda in https://github.com/radio-astro-tools/pvextractor/pull/110
- bugfix: undeclared variable by @keflavich in https://github.com/radio-astro-tools/pvextractor/pull/118
- Issue108: URL broken in the example use case by @lpda in https://github.com/radio-astro-tools/pvextractor/pull/109

#### Other Changes

- Fix compatibility with latest version of astropy and update infrastructure by @astrofrog in https://github.com/radio-astro-tools/pvextractor/pull/120

### New Contributors

- @lpda made their first contribution in https://github.com/radio-astro-tools/pvextractor/pull/112

**Full Changelog**: https://github.com/radio-astro-tools/pvextractor/compare/v0.3...v0.4

## v0.3 (2022-03-31)

### What's Changed

- Plot docs and convenience tools by @keflavich in https://github.com/radio-astro-tools/pvextractor/pull/102
- Add gh actions by @keflavich in https://github.com/radio-astro-tools/pvextractor/pull/103
- try to fix grid by removing 'novis' by @keflavich in https://github.com/radio-astro-tools/pvextractor/pull/105
- allow DaskSpectralCube, etc. to work by @keflavich in https://github.com/radio-astro-tools/pvextractor/pull/99

**Full Changelog**: https://github.com/radio-astro-tools/pvextractor/compare/v0.2...v0.3

## v0.2 (2020-04-19)

- Update package infrastructure. #93, #96
- Fix compatibility with the latest versions of Python and Matplotlib. #89, #95
- Added `return_area` option for `extract_poly_slices`. #59
- Fix error that occurred when WCS did not have a PC matrix defined. #90

## v0.1 (2018-01-26)

- First official release.
