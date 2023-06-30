# Changelog

<!--next-version-placeholder-->

## v0.4.2 (2023-06-30)

### Fix

* **cicd:** Updated ci-cd workflow ([`24b253c`](https://github.com/Jon-Ting/sphractal/commit/24b253cac9a6d8b6df81751376415ba02b7806cb))

## v0.4.1 (2023-06-29)



## v0.4.0 (2023-06-30)

### Feature

* Added CI/CD workflow ([`8a78e22`](https://github.com/Jon-Ting/sphractal/commit/8a78e224634df7ee8ccbc75c6cb2b0f3944e8090))

### Fix

* **findSurf:** Fixed 'numNeigh' option in findSurf() ([`796d14c`](https://github.com/Jon-Ting/sphractal/commit/796d14cf05343b5004819be04a972826c277102c))
* **scanAllAtoms:** ScanAllAtoms() now prints 1/eps instead of magnFac ([`2c3b4a3`](https://github.com/Jon-Ting/sphractal/commit/2c3b4a30d9b126fb4bd6c8d8d5ec1e7f168221f1))
* **datasets:** GetExampleDataPath() returns str instead of PosixPath ([`6989942`](https://github.com/Jon-Ting/sphractal/commit/69899426fa6ae5406e322213930aea3e99ea2dfe))

### Documentation

* **readme:** Updated readme ([`3ab9697`](https://github.com/Jon-Ting/sphractal/commit/3ab969785424824cbe08af8ef84d56ba2cd26bb3))
* **mult:** Added recommendations for radMult and alphaMult to constants.py ([`90f31b4`](https://github.com/Jon-Ting/sphractal/commit/90f31b4379c2e81de9f8760121486fc8b96132a4))
* **example:** Completed example.ipynb ([`4b60535`](https://github.com/Jon-Ting/sphractal/commit/4b60535755e74b6e679daef80885a5c4a923a428))
* **findSurf:** Tidied up docstring for findSurf() ([`8bb5fb9`](https://github.com/Jon-Ting/sphractal/commit/8bb5fb925a425e55bbbffc953d96cf97e55577f0))
* **help:** Elaborated docstring to be returned from help() ([`543925b`](https://github.com/Jon-Ting/sphractal/commit/543925b95b7b43755a013b5e0d8c301eb66643eb))

## v0.3.0 (29/06/2023)

### Feature

- Added imports for more functions

### Documentation

- Updated readme and example in `docs/`

### Refactor

- Added compiled C++ GPU code

## v0.2.0 (29/06/2023)

### Feature

- Allowed `calcBL` to be specified for `findNN()`

### Documentation

- Updated readme
- Updated readme for C++ code
- Updated example in `docs/`
- Updated docstrings for surfPointClouds.py functions

### Build

- Updated poetry.lock

## v0.1.0 (27/06/2023)

- First release of `sphractal`
