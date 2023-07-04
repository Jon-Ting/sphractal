# Changelog

<!--next-version-placeholder-->

## v0.7.0 (2023-07-04)

### Feature

* **boxLenConc:** Implemented automatic parallelisation functionalities ([`b4f6c36`](https://github.com/Jon-Ting/sphractal/commit/b4f6c364c92ece88fa7bfea45ecaa565681c4647))

### Performance

* **boxLenConc:** Reduced the number of times of calling cpu_counts() ([`c0911cf`](https://github.com/Jon-Ting/sphractal/commit/c0911cf1e04fde90be2ac38e8bd9004bf662caf2))

## v0.6.1 (2023-07-04)

### Fix

* **readme:** Fixed broken links in readme ([`3e68a87`](https://github.com/Jon-Ting/sphractal/commit/3e68a87d75b0efb8584a8ad81a90824b61118834))

### Documentation

* **findSlope:** Added in-line comments for findSlope() ([`573a20c`](https://github.com/Jon-Ting/sphractal/commit/573a20c67d99c8afad5fa923660d5f437d0fbfa9))

## v0.6.0 (2023-07-04)

### Feature

* **findSlope:** Added functionalities to generate publication-ready figures ([`5653519`](https://github.com/Jon-Ting/sphractal/commit/5653519a0fd49f12543eefcb7de96366113472ae))

### Fix

* **findSlope:** Reverted to producing figures with png format ([`a6ed73e`](https://github.com/Jon-Ting/sphractal/commit/a6ed73ee64c24cbba0f91d1f916d9ddba14d5f52))

### Documentation

* **example:** Updated example.ipynb with new figures ([`8341718`](https://github.com/Jon-Ting/sphractal/commit/83417184919473a3676f13e0fbbeca8c783783bb))

## v0.5.0 (2023-07-03)

### Feature

* **pointcloud:** Implemented and provided clear instructions to use point cloud surface representation related functionalities ([`62d247c`](https://github.com/Jon-Ting/sphractal/commit/62d247c3fd277a3f4c96822f807bd0d56d392bbd))

### Fix

* **setup:** Turned tuple for classifiers in setup.py into list ([`5fa7910`](https://github.com/Jon-Ting/sphractal/commit/5fa79104290534003656a63d3ba9d807bf27f6d6))

### Documentation

* **example:** Deleted .virtual_documents from docs/ ([`78dbe38`](https://github.com/Jon-Ting/sphractal/commit/78dbe382b2a2038b2978e3e1cb61c5a5631116ee))
* **example:** Updated example.ipynb to make sure fastBC executable could be detected ([`42cd8a6`](https://github.com/Jon-Ting/sphractal/commit/42cd8a6eef54158cfa39012cb0493db2f87f7c60))

## v0.4.4 (2023-07-01)

### Documentation

* **readme:** Updated readme to specify the delay in point cloud functionalities ([`4d73e24`](https://github.com/Jon-Ting/sphractal/commit/4d73e24a911d82c7786c280b13b4258abf229446))

## v0.4.3 (2023-07-01)

### Fix

* **test:** Commented out tests for functionalities related to point cloud representation temporarily ([`86c5192`](https://github.com/Jon-Ting/sphractal/commit/86c5192be9bf8eca3721609d2f22e7e3fff615c8))
* **test:** Fixed missing directory error when running pytest from package root ([`062c4db`](https://github.com/Jon-Ting/sphractal/commit/062c4db2496d51491f9258a7fa0ab1fcef87a3e0))
* **mkdir:** Made sure that directories are generated before files are ([`c529767`](https://github.com/Jon-Ting/sphractal/commit/c529767b1dc168ead1932f19dd6a1191abeaaf7e))

### Documentation

* **readme:** Updated readme ([`a5e3aa0`](https://github.com/Jon-Ting/sphractal/commit/a5e3aa0a36943d149143b2a23588d87585a2d2cd))

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

* Added imports for more functions

### Documentation

* Updated readme and example in `docs/`

### Refactor

* Added compiled C++ GPU code

## v0.2.0 (29/06/2023)

### Feature

* Allowed `calcBL` to be specified for `findNN()`

### Documentation

* Updated readme
* Updated readme for C++ code
* Updated example in `docs/`
* Updated docstrings for surfPointClouds.py functions

### Build

* Updated poetry.lock

## v0.1.0 (27/06/2023)

* First release of `sphractal`
