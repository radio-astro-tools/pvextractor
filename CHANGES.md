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
