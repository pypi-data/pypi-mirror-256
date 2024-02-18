## v0.7.1 (2024-02-12)

### Fix

- **MetisAPI**: match *data_source_ids* to *data_sources*

## v0.7.0 (2024-02-06)

### Feat

- camel case <-> snake case autoconversion

### Refactor

- code dedup

## v0.6.0 (2023-09-23)

### Feat

- **MetisAPI**: support collections visibility

### Fix

- **helpers**: runtime type checks

## v0.5.0 (2023-07-27)

### Feat

- **namespaces**: check that engine is supported

## v0.4.0 (2023-06-25)

### Feat

- **namespaces**: implements /calculations namespace, deprecate get_engines()
- **MetisAPI**: timeouts

### Refactor

- **namespaces**: scope v0 namespaces into v0

## v0.3.0 (2023-05-19)

### Feat

- *input* calculation parameter support

## v0.2.0 (2023-05-02)

### Feat

- **calculations**: wait and get results of calculation
- **MetisCalculationDTO**: add parent field
- **datasources**: get, get_parents, get_children methods
- **MetisDataSourceDTO**: parents-children fields
- **datasources**: DataSourceType

### Fix

- **MetisCalculationDTO**: remove nonexistent field

## v0.1.0 (2023-05-02)

### Feat

- more verbose exceptions

### Fix

- examples
- fix __repr__ for TypedDict
- linting
- client tests

## v0.0.3 (2023-03-02)

### Feat

- tests GH action
- full API coverage and refactor to TypedDicts
- sync client
- implement all endpoints and more user-friendly async API
- lint github action
- setup linters
- setup dependabot

### Fix

- remove hardcoded type flavors
