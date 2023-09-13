# Changelog

<!--next-version-placeholder-->

## v0.22.2 (2023-09-13)

### Fix

* **findSlope:** Synchronised printing outputs with actual box-counting results when previous values are returned ([`7a9b15e`](https://github.com/Jon-Ting/sphractal/commit/7a9b15e2e860646d7522c954e2694e8a7cef2c2f))

## v0.22.1 (2023-09-12)

### Fix

* **findNN:** Enlarged stepSize to identify neighbours on surface with {100} packings ([`4f51e17`](https://github.com/Jon-Ting/sphractal/commit/4f51e17e3e2a25a829d21e8162977c4379b53042))

## v0.22.0 (2023-09-11)

### Feature

* **runBoxCnt:** Added bulkCN as optional argument ([`ddc8b7a`](https://github.com/Jon-Ting/sphractal/commit/ddc8b7aeba31b7503c81e0cfe783e5fed9df1daa))
* **runBoxCnt:** Added radMult as an optional argument ([`2464081`](https://github.com/Jon-Ting/sphractal/commit/246408149c5e90d5c24ac6254506bc577bdc8864))

## v0.21.2 (2023-09-05)



## v0.21.1 (2023-08-22)



## v0.21.0 (2023-08-16)

### Feature

* **findAtomsWithSurfNeighs:** Renamed findTargetAtoms() ([`e4ff459`](https://github.com/Jon-Ting/sphractal/commit/e4ff4595d01c5fc0f382a4c4144d245af505e704))
* **runBoxCnt:** Modified default value for minSample ([`866d551`](https://github.com/Jon-Ting/sphractal/commit/866d551ea5104f7d4b8a3dcd11d256fed67f553a))

### Fix

* **tests:** Updated test functions related to findTargetAtoms() ([`e0a2557`](https://github.com/Jon-Ting/sphractal/commit/e0a2557b5ab0b4588e7d8854816a89a1c4e7ce99))

### Performance

* **scanBox:** Removed redundant steps for inclusion of inner surface box counts ([`94da738`](https://github.com/Jon-Ting/sphractal/commit/94da73869ad4bcb8e9e6fee4595e9298162bb6e1))

## v0.20.13 (2023-08-12)



## v0.20.12 (2023-08-12)



## v0.20.11 (2023-08-12)

### Fix

* **build:** Added dist/ ([`5f04a0d`](https://github.com/Jon-Ting/sphractal/commit/5f04a0d423bb53c8e33eb5543ff650ecab521017))

## v0.20.10 (2023-08-12)

### Fix

* **build:** Added dist/ ([`078c188`](https://github.com/Jon-Ting/sphractal/commit/078c188e3fb2f32e639529b6c4f6df2481b0c8e4))

## v0.20.9 (2023-08-12)



## v0.20.8 (2023-08-12)

### Fix

* **ci-cd.yml:** Separate out a new pipeline for publishing ([`f7a9989`](https://github.com/Jon-Ting/sphractal/commit/f7a9989a027f7c9b3e3f94973759f76932a855ca))
* **ci-cd.yml:** Added permission lines to specify trusted publishing flow ([`589468b`](https://github.com/Jon-Ting/sphractal/commit/589468b0554cd6eb8bda7632cda0c0b6162b2b56))

## v0.20.7 (2023-08-12)



## v0.20.6 (2023-08-12)



## v0.20.5 (2023-08-12)



## v0.20.4 (2023-08-12)



## v0.20.3 (2023-08-12)

### Documentation

* **example:** Made sure all codes are visible in notebook ([`bc6db5c`](https://github.com/Jon-Ting/sphractal/commit/bc6db5c2904f045f105d0a0c71fe81cad38181a0))
* **readme:** Fixed pypi readme rendering issue ([`d6cf985`](https://github.com/Jon-Ting/sphractal/commit/d6cf98573c59fbb5cb5ab0fe31dd02254f83c770))

## v0.20.2 (2023-08-12)

### Documentation

* **readme:** Attempt to fix pypi readme rendering issue ([`ac8099a`](https://github.com/Jon-Ting/sphractal/commit/ac8099aa0644ba9203be9f0fe869d8b535f5a692))
* **example:** Updated example notebook ([`753e0f8`](https://github.com/Jon-Ting/sphractal/commit/753e0f851f8c6674011e8902068287e0d87ea4bd))
* Improved consistency of the docstrings for all functions ([`bbb613d`](https://github.com/Jon-Ting/sphractal/commit/bbb613d8ce7cd800226a5bb8bdcb899505a89069))
* **readme:** Made readme statements more concise ([`f1ef8ce`](https://github.com/Jon-Ting/sphractal/commit/f1ef8ce6b2779c749e09b84409cd43c0f99c8e01))

## v0.20.1 (2023-08-12)

### Documentation

* **readme:** Fixed position of first image ([`fbfb2f5`](https://github.com/Jon-Ting/sphractal/commit/fbfb2f52ff468b2d026a50430f7bc1c7db123d07))

## v0.20.0 (2023-08-12)

### Feature

* **findSlope:** Modified while loop condition to better reflect the minSample specified ([`2805b74`](https://github.com/Jon-Ting/sphractal/commit/2805b745ec6b1b80f29853436bb9a8161a259dfe))
* **findSlope:** Modified while loop condition to better reflect the minSample specified ([`a7b7270`](https://github.com/Jon-Ting/sphractal/commit/a7b7270f095101f844b18120df23a663de1163c3))

### Fix

* **tests:** Removed redundant test combinations ([`374c5f1`](https://github.com/Jon-Ting/sphractal/commit/374c5f1a38f27be8a8197fdf6ba075d7dd31e6a8))

### Documentation

* **findNN:** Added docstring for the function ([`7b22a4c`](https://github.com/Jon-Ting/sphractal/commit/7b22a4c159468db20e9eb66718d2edc23a5fe1fc))

### Performance

* **findSlope:** Added assertion for minSample to make sure it's integer ([`ba6698d`](https://github.com/Jon-Ting/sphractal/commit/ba6698dba109e0cf6376d3a7a33d5a02e27bfc37))

## v0.19.5 (2023-08-10)

### Fix

* **tests:** Corrected the function called to test getCaseStudyPaths() ([`8dcf30c`](https://github.com/Jon-Ting/sphractal/commit/8dcf30c76f55fe2bf022001f169669cadaa74d02))
* **test:** Corrected the number of case study coordinate files to be retrieved ([`84afd20`](https://github.com/Jon-Ting/sphractal/commit/84afd201c779065e3f9c995e0dc197e9b5ba94d5))
* **data:** Included the rhombic dodecahedron atomic coordinates as data ([`84edfb7`](https://github.com/Jon-Ting/sphractal/commit/84edfb7f902a8096b2e2c8ab664427a89d3778e6))

## v0.19.4 (2023-08-09)

### Fix

* **readthedocs:** Fixed the rendering errors on Sphinx documentations ([`850613a`](https://github.com/Jon-Ting/sphractal/commit/850613ac6f69e364de89d9e53523e00ad70c97f8))

### Documentation

* **init:** Made documentations in __init__.py more concise ([`49dc087`](https://github.com/Jon-Ting/sphractal/commit/49dc0871c014d20f9113f7ce90639c38cb7136be))

## v0.19.3 (2023-08-09)



## v0.19.2 (2023-08-07)

### Fix

* **findSlope:** Fixed calling variable before assignment issue ([`6426881`](https://github.com/Jon-Ting/sphractal/commit/6426881373b156d853f326d0d4e8651d4f75e819))

## v0.19.1 (2023-08-07)

### Fix

* **findSlope:** Fixed calling variable before assignment issue ([`c5a94a4`](https://github.com/Jon-Ting/sphractal/commit/c5a94a481bb57bd5761b93d0ed623da1b4e84d7a))

## v0.19.0 (2023-08-07)

### Feature

* **findSlope:** Returned final range of box lengths ([`a955fd4`](https://github.com/Jon-Ting/sphractal/commit/a955fd4de609ee30d9874062b59993f44ae839f0))

### Fix

* **test:** Fixed test function related to findSlope() ([`8a95cb3`](https://github.com/Jon-Ting/sphractal/commit/8a95cb3a245aeb453ff1827fe81db7dfdfe8439b))

### Documentation

* **example:** Updated usage of findSlope() in example notebook ([`17f5b6f`](https://github.com/Jon-Ting/sphractal/commit/17f5b6f698b7d096411db6d3f3aa5b511de5ee4c))

## v0.18.4 (2023-08-04)



## v0.18.3 (2023-08-04)



## v0.18.2 (2023-08-02)

### Documentation

* **boxCnt:** Improved conciseness of the docstring for runBoxCnt() ([`083f977`](https://github.com/Jon-Ting/sphractal/commit/083f97732860fe71a357e8fca61ae911b43c259a))

## v0.18.1 (2023-08-02)

### Fix

* **readme:** Fixed readme broken links ([`dabe6e4`](https://github.com/Jon-Ting/sphractal/commit/dabe6e49094a196b8e280e15c2d60a1481747bb8))

## v0.18.0 (2023-07-30)

### Feature

* **datasets:** Added functions to access the case study atomic data ([`126b444`](https://github.com/Jon-Ting/sphractal/commit/126b444ea079828e0ca9759ea8761c65af3bdafe))
* **data:** Added atomic coordinates used for case studies ([`8111d48`](https://github.com/Jon-Ting/sphractal/commit/8111d4815017e22062401e1d49ebda269d9d79e5))

### Fix

* **tests:** Added test function for getCaseStudyDataPaths() ([`d324685`](https://github.com/Jon-Ting/sphractal/commit/d324685c489f9cb5a2cfbd1388d275f43a3bd37f))

### Documentation

* **example:** Explained the choice of numPoints in example.ipynb ([`8f45bd2`](https://github.com/Jon-Ting/sphractal/commit/8f45bd22e04cc6f2b56243d7a089f753d87349a5))

## v0.17.3 (2023-07-29)



## v0.17.2 (2023-07-29)

### Fix

* **surfVoxel:** Imported cpu_count() from multiprocessing ([`640025f`](https://github.com/Jon-Ting/sphractal/commit/640025ff9d869910f798654e74072d97ab0b3069))

### Documentation

* **example:** Updated example.ipynb with recoloured and reoriented figures ([`9c17801`](https://github.com/Jon-Ting/sphractal/commit/9c17801f589184878ca39b0b26a188be50202183))

## v0.17.1 (2023-07-29)

### Documentation

* **surfVoxel:** Simplified docstring for voxelBoxCnts() ([`4d7a395`](https://github.com/Jon-Ting/sphractal/commit/4d7a3950c75b69880881977aa2249507bf1015d8))

## v0.17.0 (2023-07-28)

### Feature

* **data:** Added validation data ([`7161b6e`](https://github.com/Jon-Ting/sphractal/commit/7161b6e3dcbb34fa78a9d3a742c5260cb98d24ea))

### Fix

* **test:** Updated ted test function for validation data ([`dcc47b9`](https://github.com/Jon-Ting/sphractal/commit/dcc47b9db5105a71dbc73be89ece49be0d904974))
* **findTargetAtoms:** Enabled the function to handle single atom case ([`2650e06`](https://github.com/Jon-Ting/sphractal/commit/2650e064a098e5681beb3e855474fb5eedc5f759))
* Enabled findNN() and findSurf() to handle single atom input ([`8cfdae4`](https://github.com/Jon-Ting/sphractal/commit/8cfdae4139e4772b8a5c0336accd5a8be852d3f4))

### Documentation

* **surfVoxel:** Updated recommendations of resource allocations for voxelBoxCnts() ([`e0eedb0`](https://github.com/Jon-Ting/sphractal/commit/e0eedb018ff919e3e7ee74a19610e78c23928ca4))

## v0.16.0 (2023-07-27)

### Feature

* **boxCnt:** Changed 'lenRange' into  'trimLen' ([`8c9eeaf`](https://github.com/Jon-Ting/sphractal/commit/8c9eeaf8780a55fe7617d15a61d2b0a20536d3c6))

## v0.15.1 (2023-07-25)



## v0.15.0 (2023-07-24)

### Feature

* **surfVoxel:** Implemented parallelisation functionalities for generation of point cloud representation of surface ([#1](https://github.com/Jon-Ting/sphractal/issues/1)) ([`1a576ed`](https://github.com/Jon-Ting/sphractal/commit/1a576ed4f6fd133d1ecffa04aa2775200873c64a))

## v0.14.1 (2023-07-19)

### Documentation

* **example:** Updated example.ipynb ([`578d85d`](https://github.com/Jon-Ting/sphractal/commit/578d85d5e996533c812ca919de7b11a75412ef9b))

## v0.14.0 (2023-07-18)

### Feature

* **data:** Updated example xyz files for scaling tests ([`2e65389`](https://github.com/Jon-Ting/sphractal/commit/2e6538919b2c1c28f4e2298ec837c94644c3f16f))

### Fix

* **test:** Updated test functions related to example data ([`d40e923`](https://github.com/Jon-Ting/sphractal/commit/d40e92397dd78b09dd8a64d40a60fe1648e8a76b))
* **datasets:** Fixed a typo in getWeakScalingDataPaths() ([`533b5c7`](https://github.com/Jon-Ting/sphractal/commit/533b5c7b551bae0a9a59dd189e62e4d896432497))
* **datasets:** Added functions to get example data to package namespace ([`1302cdc`](https://github.com/Jon-Ting/sphractal/commit/1302cdc8b2f8942cd7380283c061fcc72c8df87b))
* **datasets:** Updated functions to get the xyz files used for scaling tests ([`05f61fb`](https://github.com/Jon-Ting/sphractal/commit/05f61fb4f7e0e9995e6d6f144ac0ca9ac2ff126b))

## v0.13.1 (2023-07-17)

### Fix

* **maxWorkers:** Fix zero cpu for parallelisation error ([`af00b98`](https://github.com/Jon-Ting/sphractal/commit/af00b989d8011afc48d7721632e4733167c30b7f))

## v0.13.0 (2023-07-17)

### Feature

* **boxLenConc:** Optimised resource allocations for more general cases ([`b107c07`](https://github.com/Jon-Ting/sphractal/commit/b107c078021c89c41e3674e8f7f5dd2cf43d4326))

## v0.12.4 (2023-07-17)

### Fix

* **boxLenScanMaxWorkers:** Fixed formula for resource allocations ([`165ec58`](https://github.com/Jon-Ting/sphractal/commit/165ec58e1d52a9836f9adecf4f1ef3455a64b42f))

## v0.12.3 (2023-07-16)



## v0.12.2 (2023-07-15)

### Documentation

* **readme:** Fixed paragraphing problems ([`a637259`](https://github.com/Jon-Ting/sphractal/commit/a637259e1b4472fdc46fbd7201b0b6c18c0c3796))
* **readme:** Fixed fastbc repo link ([`c43c213`](https://github.com/Jon-Ting/sphractal/commit/c43c213821bc83ac427ff082cd3bf69ce1ae21fa))
* **readme:** Added figures to readme ([`813de14`](https://github.com/Jon-Ting/sphractal/commit/813de14bae48be15e960581f2a4673f98dafe949))

## v0.12.1 (2023-07-14)

### Fix

* **fastbc:** Updated fastbc submodule name ([`43a9976`](https://github.com/Jon-Ting/sphractal/commit/43a9976d47b8d11648659bdea807c29d7eecc4a3))

### Documentation

* **readme:** Removed dollar signs from readme ([`c6fc475`](https://github.com/Jon-Ting/sphractal/commit/c6fc475e537c5c3ef28029335942a25c70dd584d))

## v0.12.0 (2023-07-14)

### Feature

* **data:** Unified and included more example data ([`c4cbe5e`](https://github.com/Jon-Ting/sphractal/commit/c4cbe5e54ee753a8cb640a36fe07b80384d90332))

### Fix

* **findTargetAtoms:** Fixed the function for rmInSurf=False ([`c21fd67`](https://github.com/Jon-Ting/sphractal/commit/c21fd67a0b55618df06b5ab4e2701292e92161f5))

### Performance

* **findSurf:** Sped up alpha shape algorithm ([`427536d`](https://github.com/Jon-Ting/sphractal/commit/427536d74b87bf9e445eb878baa7065c0f2e3f9d))

## v0.11.0 (2023-07-13)

### Feature

* **data:** Added more example data and updated functionalities to get them ([`d65c3d2`](https://github.com/Jon-Ting/sphractal/commit/d65c3d21200a616208c2aa27c3001a3acbbec0ac))

## v0.10.0 (2023-07-12)

### Feature

* **findSlope:** Added notebook option to findSlope() plots ([`f6c6123`](https://github.com/Jon-Ting/sphractal/commit/f6c6123191d7d853fbd486f15049c526376da8da))
* **boxCnt:** Moved box-counting functions for each representation to respective modules ([`e8bbe38`](https://github.com/Jon-Ting/sphractal/commit/e8bbe38eb46dad1d2964569019f7c0a89c7604e3))
* Renamed modules, functions, variables to more concise names ([`0119301`](https://github.com/Jon-Ting/sphractal/commit/0119301cd857b5810d5689f6078ae4dd8dfd0dd6))

### Fix

* **test:** Updated test functions ([`894d223`](https://github.com/Jon-Ting/sphractal/commit/894d2239a63cc88e4e85a76218c262fb733e8cc7))

### Documentation

* **example:** Updated example notebook ([`76ecff9`](https://github.com/Jon-Ting/sphractal/commit/76ecff996e7ee04493c6aa5eeb4adf5baa932cbf))
* **readme:** Updated variable name change on readme ([`ff81621`](https://github.com/Jon-Ting/sphractal/commit/ff81621d7f8c19abc28e49f9d767e6e1cd77503f))

## v0.9.1 (2023-07-11)

### Documentation

* **readme:** Added background section to readme ([`bcfbb62`](https://github.com/Jon-Ting/sphractal/commit/bcfbb62e4eb61beb0254ae24f72ccba1e890ef0a))
* **readme:** Omitted features under development ([`b9af10a`](https://github.com/Jon-Ting/sphractal/commit/b9af10aa6bc4b969ae9c30bbde5c3b1bb3f31baf))

## v0.9.0 (2023-07-10)

### Feature

* **minValFromBound:** Added the input argument to related functionalities for exact surface representation ([`0ad3a49`](https://github.com/Jon-Ting/sphractal/commit/0ad3a496c2d954a10d8612ad9fcdb875c9c2585b))

## v0.8.1 (2023-07-08)

### Documentation

* **example:** Fixed a typo in example.ipynb ([`157adc3`](https://github.com/Jon-Ting/sphractal/commit/157adc392b7400ac3ff152db55eafa706fdaf78a))

## v0.8.0 (2023-07-07)

### Feature

* **figType:** Renamed options for figType based on seaborn style ([`f1a8fb1`](https://github.com/Jon-Ting/sphractal/commit/f1a8fb1ceacb23697ae30b7dd8e26e01745d1e94))

### Documentation

* **readme:** Fixed typo in readme ([`92b38b8`](https://github.com/Jon-Ting/sphractal/commit/92b38b85d33da568ab861cdb61350c69e8f9745c))

## v0.7.1 (2023-07-05)



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
