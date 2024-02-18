# Changelog

## v1.4.1 (2023-09-29)

#### Fixes

* fix type annotation in PoolBar constructor

## v1.4.0 (2023-09-29)

#### New Features

* add thread/process pool executor and ProgBar integration class

## v1.3.1 (2023-06-10)

#### Fixes

* add exception handling to prevent crashing when there is no terminal
#### Refactorings

* make ProgBar.bar a property
#### Docs

* update readme
* update and improve docstrings
## v1.3.0 (2023-06-03)

#### New Features

* add movement to Spinner
* sequence width will update when the terminal width changes
#### Refactorings

* default character sequence is assigned as parameter default
* change width parameter to width_ratio
#### Others

* add missing version prefix


## v1.2.0 (2023-04-25)

#### New Features

* implement Spinner class
* add context manager functionality
* add runtime property to ProgBar
* implement update_frequency functionality
#### Fixes

* fix bug where bar display exceeds width_ratio if counter goes above total
#### Performance improvements

* remove leading space when no prefix is passed to display
#### Refactorings

* remove total property and start counter at 1 instead of 0
* improve type annotations
#### Docs

* update readme
* improve display() doc string


## v1.1.0 (2023-04-16)

#### Fixes

* update minimum python version required


## v1.0.2 (2023-03-22)

#### Others

* build v1.0.2
* update readme


## v1.0.1 (2023-02-13)

#### Fixes

* fix counter_override in error in ProgBar.display() if passed value is 0
#### Others

* build v1.0.1
* update changelog