# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),


## [0.3.2] - 2024-02-10

### Updated
- fix ci/cd problems

### Todo
- use ruff
- fix publish action

## [0.3.0] - 2024-02-10

### Added
- Add validators for all classes
- Add Cleaner module
- Add StandardScaler implementation
- Manage problem of data drift train / test


### Updated
- Moove .utils to root folder
- Reshape entire module using transformer, cleaner, scaler, and selector
- Reshape pyproject and documentation

## [0.2.1] - 2024-02-09

### Added
- Full support for official documentation
- Add auto deploy documentation with GitHub pages
- Add notebooks to the documentation

### Updated
- Moove assets and utils to docs folder
- Restructure all package
- Update documentation to include usage examples
- Moove Changelog and Contributing to the docs folder
- Clean code files, remove unused imports, useless comments, and unused variables
- LogTransformer is now LogColumnTransformer
- BoolColumnTransformer and DropUniqueColumnTransformer now accept force_df_out attribute
- Rename modules logger to log

## [0.2.0] - 2024-02-08

### Added
- add BoolTransformer  to encode bool columns
- add UniqueTransformer to clean cols with unique values
- add pre-commit support for code formatting

### Updated

- Add utils to a separate module
- update CI/CD to include code formatting checks



## [0.1.0] - 2024-01-26

### Updated

- First public release
- Publish to PyPI
