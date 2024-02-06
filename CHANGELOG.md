# CHANGELOG



## v1.0.0 (2024-02-06)

### Breaking

* feat(cicd): updated ci-cd.yml

BREAKING CHANGE: release standard version. ([`0392a4a`](https://github.com/Jon-Ting/sphractal/commit/0392a4a5035a162c49f4a4d14b1bc3d7f2c17d17))


## v0.28.3 (2024-02-05)

### Fix

* fix(version): release standard version with publication
BREAKING CHANGE: first standard version. ([`26c4230`](https://github.com/Jon-Ting/sphractal/commit/26c423056c46f2a9a874189813afdad179b89b8b))


## v0.28.2 (2024-02-05)

### Unknown

* doc(readme): updated readme

BREAKING CHANGE: releasing first version with publication ([`3cd49bb`](https://github.com/Jon-Ting/sphractal/commit/3cd49bbe5ab42e6ee416457a06146078a7df3d42))


## v0.28.1 (2024-02-03)

### Fix

* fix(numCPUs): replaced cpu_count() by sched_getaffinity() ([`a3cfcf2`](https://github.com/Jon-Ting/sphractal/commit/a3cfcf237488c2abdd8292cfdc3c98deb61d28e1))

### Performance

* perf(maxBoxLenCPU): modified formula for nested parallelisation ([`79dfda7`](https://github.com/Jon-Ting/sphractal/commit/79dfda70505857eb7df5edcc2616c18eae0843e6))


## v0.28.0 (2024-02-02)

### Feature

* feat(voxel): renamed exePath as fastbcPath ([`3d7662f`](https://github.com/Jon-Ting/sphractal/commit/3d7662ff65372f754cffd5837722612908a50981))


## v0.27.2 (2024-02-02)

### Unknown

* doc(readme): rephrased sentences related to .exe files to emphasise platform agnosticity ([`abb73a6`](https://github.com/Jon-Ting/sphractal/commit/abb73a6400e6bcbf66e9c805c88a1a916c41bde4))


## v0.27.1 (2024-01-23)

### Build

* build(deps): bump pillow from 10.0.1 to 10.2.0 (#16)

Bumps [pillow](https://github.com/python-pillow/Pillow) from 10.0.1 to 10.2.0.
- [Release notes](https://github.com/python-pillow/Pillow/releases)
- [Changelog](https://github.com/python-pillow/Pillow/blob/main/CHANGES.rst)
- [Commits](https://github.com/python-pillow/Pillow/compare/10.0.1...10.2.0)

---
updated-dependencies:
- dependency-name: pillow
  dependency-type: indirect
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt;
Co-authored-by: dependabot[bot] &lt;49699333+dependabot[bot]@users.noreply.github.com&gt; ([`4729e86`](https://github.com/Jon-Ting/sphractal/commit/4729e86cd6f82eb3efb543a20c375e9b831f6deb))


## v0.27.0 (2024-01-19)

### Feature

* feat(findNN): capped the maximum indices for neighbour searching ([`db8a5e0`](https://github.com/Jon-Ting/sphractal/commit/db8a5e045de1ba7f6b3f680f0657f0722781a227))

### Performance

* perf(mkdir): avoid creating unnecessary directories ([`19139bf`](https://github.com/Jon-Ting/sphractal/commit/19139bf857bbcdc3323e751b4f77697ddfb855f0))


## v0.26.3 (2024-01-11)

### Build

* build(deps-dev): bump gitpython from 3.1.37 to 3.1.41 (#14)

Bumps [gitpython](https://github.com/gitpython-developers/GitPython) from 3.1.37 to 3.1.41.
- [Release notes](https://github.com/gitpython-developers/GitPython/releases)
- [Changelog](https://github.com/gitpython-developers/GitPython/blob/main/CHANGES)
- [Commits](https://github.com/gitpython-developers/GitPython/compare/3.1.37...3.1.41)

---
updated-dependencies:
- dependency-name: gitpython
  dependency-type: indirect
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt;
Co-authored-by: dependabot[bot] &lt;49699333+dependabot[bot]@users.noreply.github.com&gt; ([`200bd2f`](https://github.com/Jon-Ting/sphractal/commit/200bd2fbbe4904b6d628016ed59efbe65947168a))

* build(deps-dev): bump jinja2 from 3.1.2 to 3.1.3 (#15)

Bumps [jinja2](https://github.com/pallets/jinja) from 3.1.2 to 3.1.3.
- [Release notes](https://github.com/pallets/jinja/releases)
- [Changelog](https://github.com/pallets/jinja/blob/main/CHANGES.rst)
- [Commits](https://github.com/pallets/jinja/compare/3.1.2...3.1.3)

---
updated-dependencies:
- dependency-name: jinja2
  dependency-type: indirect
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt;
Co-authored-by: dependabot[bot] &lt;49699333+dependabot[bot]@users.noreply.github.com&gt; ([`b2ea74d`](https://github.com/Jon-Ting/sphractal/commit/b2ea74dfbc667a36909aa6c8d489b0f6f0894498))


## v0.26.2 (2024-01-10)

### Build

* build(deps): bump fonttools from 4.40.0 to 4.43.0 (#13)

Bumps [fonttools](https://github.com/fonttools/fonttools) from 4.40.0 to 4.43.0.
- [Release notes](https://github.com/fonttools/fonttools/releases)
- [Changelog](https://github.com/fonttools/fonttools/blob/main/NEWS.rst)
- [Commits](https://github.com/fonttools/fonttools/compare/4.40.0...4.43.0)

---
updated-dependencies:
- dependency-name: fonttools
  dependency-type: indirect
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt;
Co-authored-by: dependabot[bot] &lt;49699333+dependabot[bot]@users.noreply.github.com&gt; ([`00c8d10`](https://github.com/Jon-Ting/sphractal/commit/00c8d105630b683ce4750e16a7e2f7cd9269833c))


## v0.26.1 (2023-12-13)

### Build

* build(deps-dev): bump jupyter-server from 2.7.2 to 2.11.2 (#12)

Bumps [jupyter-server](https://github.com/jupyter-server/jupyter_server) from 2.7.2 to 2.11.2.
- [Release notes](https://github.com/jupyter-server/jupyter_server/releases)
- [Changelog](https://github.com/jupyter-server/jupyter_server/blob/main/CHANGELOG.md)
- [Commits](https://github.com/jupyter-server/jupyter_server/compare/v2.7.2...v2.11.2)

---
updated-dependencies:
- dependency-name: jupyter-server
  dependency-type: indirect
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt;
Co-authored-by: dependabot[bot] &lt;49699333+dependabot[bot]@users.noreply.github.com&gt; ([`f4f3304`](https://github.com/Jon-Ting/sphractal/commit/f4f33042d49eeaec29d64ce9a0d8ae2ef523eaad))


## v0.26.0 (2023-12-09)

### Feature

* feat(boxCnt): reverted back to version without the additional argument ([`620ed70`](https://github.com/Jon-Ting/sphractal/commit/620ed706d0efa75cf4566428aa9077cd5de3461e))

* feat(returnCoordsRange): fixed conflicts between new and old commits ([`b9b8b71`](https://github.com/Jon-Ting/sphractal/commit/b9b8b71f6941c6ad4ae16f1a177c019c2e6e714b))

* feat(runBoxCnt): added optional argument to return atomic coordinates ([`a230b08`](https://github.com/Jon-Ting/sphractal/commit/a230b084c342bc74718c7b6fe8c7b9f4f1c1485c))


## v0.25.2 (2023-11-30)

### Build

* build(deps-dev): bump cryptography from 41.0.4 to 41.0.6 (#11)

Bumps [cryptography](https://github.com/pyca/cryptography) from 41.0.4 to 41.0.6.
- [Changelog](https://github.com/pyca/cryptography/blob/main/CHANGELOG.rst)
- [Commits](https://github.com/pyca/cryptography/compare/41.0.4...41.0.6)

---
updated-dependencies:
- dependency-name: cryptography
  dependency-type: indirect
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt;
Co-authored-by: dependabot[bot] &lt;49699333+dependabot[bot]@users.noreply.github.com&gt; ([`7c2d342`](https://github.com/Jon-Ting/sphractal/commit/7c2d342fce5d0d687ad58f3d47d19ea92c58cedc))


## v0.25.1 (2023-11-15)

### Build

* build(ray): removed from package requirement ([`7c04dd6`](https://github.com/Jon-Ting/sphractal/commit/7c04dd659edac1b0e29300d945e525ee51585e00))


## v0.25.0 (2023-11-15)

### Feature

* feat(Pool): reverted back to concurrent.futures ([`4a6ea8b`](https://github.com/Jon-Ting/sphractal/commit/4a6ea8bdb5efe718ba533f5912a64b2d03468e86))


## v0.24.0 (2023-10-19)

### Build

* build(ray): added to dependency ([`3cc42c0`](https://github.com/Jon-Ting/sphractal/commit/3cc42c0b78804d7046dd6f376f20376a355fc1bf))

* build(mpi4py): added package to installation requirement ([`0ca6a56`](https://github.com/Jon-Ting/sphractal/commit/0ca6a56e474531d497eabd2e5dcc6cde005f4d02))

* build(deps-dev): bump urllib3 from 2.0.6 to 2.0.7 (#10)

Bumps [urllib3](https://github.com/urllib3/urllib3) from 2.0.6 to 2.0.7.
- [Release notes](https://github.com/urllib3/urllib3/releases)
- [Changelog](https://github.com/urllib3/urllib3/blob/main/CHANGES.rst)
- [Commits](https://github.com/urllib3/urllib3/compare/2.0.6...2.0.7)

---
updated-dependencies:
- dependency-name: urllib3
  dependency-type: indirect
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt;
Co-authored-by: dependabot[bot] &lt;49699333+dependabot[bot]@users.noreply.github.com&gt; ([`d77afa2`](https://github.com/Jon-Ting/sphractal/commit/d77afa2b9a6961bc7da35edea833e5e48f5b6221))

### Feature

* feat(ray): used Pool from ray ([`c07487f`](https://github.com/Jon-Ting/sphractal/commit/c07487fd16c849cb1b8194bc0bc9aa032a90e8ca))

* feat(Pool): replace concurrent.futures with mpi4py.futures ([`3276631`](https://github.com/Jon-Ting/sphractal/commit/3276631c8f6ece302ca6bcaa1bd6302196b5182d))


## v0.23.1 (2023-10-16)

### Build

* build(deps-dev): bump gitpython from 3.1.35 to 3.1.37 (#9)

Bumps [gitpython](https://github.com/gitpython-developers/GitPython) from 3.1.35 to 3.1.37.
- [Release notes](https://github.com/gitpython-developers/GitPython/releases)
- [Changelog](https://github.com/gitpython-developers/GitPython/blob/main/CHANGES)
- [Commits](https://github.com/gitpython-developers/GitPython/compare/3.1.35...3.1.37)

---
updated-dependencies:
- dependency-name: gitpython
  dependency-type: indirect
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt;
Co-authored-by: dependabot[bot] &lt;49699333+dependabot[bot]@users.noreply.github.com&gt; ([`8aaa6af`](https://github.com/Jon-Ting/sphractal/commit/8aaa6afd779364c64fff08d2332ddcf52fe54281))

### Unknown

* Merge branch &#39;main&#39; of github.com:Jon-Ting/sphractal into main ([`809c1f4`](https://github.com/Jon-Ting/sphractal/commit/809c1f438ad05a58011572ce79362bc514797139))

* Merge branch &#39;main&#39; of github.com:Jon-Ting/sphractal into main ([`87b16b7`](https://github.com/Jon-Ting/sphractal/commit/87b16b76f5d7452f1b7a5cdb6e0ce06c31cf3428))


## v0.23.0 (2023-10-16)

### Feature

* feat(findNN): removed ceil() from stepSize definition ([`aac4f34`](https://github.com/Jon-Ting/sphractal/commit/aac4f34c20c39f5c355bb56e4cdcfe8607e87add))


## v0.22.4 (2023-10-05)

### Build

* build(deps): bump pillow from 9.5.0 to 10.0.1 (#8)

Bumps [pillow](https://github.com/python-pillow/Pillow) from 9.5.0 to 10.0.1.
- [Release notes](https://github.com/python-pillow/Pillow/releases)
- [Changelog](https://github.com/python-pillow/Pillow/blob/main/CHANGES.rst)
- [Commits](https://github.com/python-pillow/Pillow/compare/9.5.0...10.0.1)

---
updated-dependencies:
- dependency-name: pillow
  dependency-type: indirect
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt;
Co-authored-by: dependabot[bot] &lt;49699333+dependabot[bot]@users.noreply.github.com&gt; ([`d83e100`](https://github.com/Jon-Ting/sphractal/commit/d83e10022445baeda52184731eb8fda589364e2f))

* build(deps-dev): bump urllib3 from 2.0.3 to 2.0.6 (#7)

Bumps [urllib3](https://github.com/urllib3/urllib3) from 2.0.3 to 2.0.6.
- [Release notes](https://github.com/urllib3/urllib3/releases)
- [Changelog](https://github.com/urllib3/urllib3/blob/main/CHANGES.rst)
- [Commits](https://github.com/urllib3/urllib3/compare/2.0.3...2.0.6)

---
updated-dependencies:
- dependency-name: urllib3
  dependency-type: indirect
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt;
Co-authored-by: dependabot[bot] &lt;49699333+dependabot[bot]@users.noreply.github.com&gt; ([`820e10d`](https://github.com/Jon-Ting/sphractal/commit/820e10d872df875cd56640bca87618f271f94c27))


## v0.22.3 (2023-09-22)

### Build

* build(deps-dev): bump gitpython from 3.1.32 to 3.1.35 (#5)

Bumps [gitpython](https://github.com/gitpython-developers/GitPython) from 3.1.32 to 3.1.35.
- [Release notes](https://github.com/gitpython-developers/GitPython/releases)
- [Changelog](https://github.com/gitpython-developers/GitPython/blob/main/CHANGES)
- [Commits](https://github.com/gitpython-developers/GitPython/compare/3.1.32...3.1.35)

---
updated-dependencies:
- dependency-name: gitpython
  dependency-type: indirect
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt;
Co-authored-by: dependabot[bot] &lt;49699333+dependabot[bot]@users.noreply.github.com&gt; ([`a679ded`](https://github.com/Jon-Ting/sphractal/commit/a679ded90e2a71af5403d4f26495dcdfed6ce5cc))

* build(deps-dev): bump cryptography from 41.0.3 to 41.0.4 (#6)

Bumps [cryptography](https://github.com/pyca/cryptography) from 41.0.3 to 41.0.4.
- [Changelog](https://github.com/pyca/cryptography/blob/main/CHANGELOG.rst)
- [Commits](https://github.com/pyca/cryptography/compare/41.0.3...41.0.4)

---
updated-dependencies:
- dependency-name: cryptography
  dependency-type: indirect
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt;
Co-authored-by: dependabot[bot] &lt;49699333+dependabot[bot]@users.noreply.github.com&gt; ([`92c2846`](https://github.com/Jon-Ting/sphractal/commit/92c28466676ac55eacd55013a2e611ad775f8e39))

* build: merge branch &#39;main&#39; of github.com:Jon-Ting/sphractal into main ([`71bbb6e`](https://github.com/Jon-Ting/sphractal/commit/71bbb6efa9af81d5f9b4d218dbb35df8258f814a))

### Refactor

* refactor(utils.py): added default value to findNN() radMult ([`f6d823e`](https://github.com/Jon-Ting/sphractal/commit/f6d823e62fdb79b182780a15cd11476e65f58cf3))

* refactor(utils): removed redundant comment ([`136ce36`](https://github.com/Jon-Ting/sphractal/commit/136ce36ea5eb21a6183240746dde0e1f6c89cb01))


## v0.22.2 (2023-09-13)

### Build

* build: merge branch &#39;main&#39; of github.com:Jon-Ting/sphractal into main ([`273e956`](https://github.com/Jon-Ting/sphractal/commit/273e956aa010a9b351e66c7fbcdf9e1ff650858c))

### Fix

* fix(findSlope): synchronised printing outputs with actual box-counting results when previous values are returned ([`7a9b15e`](https://github.com/Jon-Ting/sphractal/commit/7a9b15e2e860646d7522c954e2694e8a7cef2c2f))


## v0.22.1 (2023-09-12)

### Fix

* fix(findNN): enlarged stepSize to identify neighbours on surface with {100} packings ([`4f51e17`](https://github.com/Jon-Ting/sphractal/commit/4f51e17e3e2a25a829d21e8162977c4379b53042))

### Test

* test(findNN): updated related test function ([`7618001`](https://github.com/Jon-Ting/sphractal/commit/7618001b798a10a6c40a4b68beab63bd7363af40))


## v0.22.0 (2023-09-11)

### Feature

* feat(runBoxCnt): added bulkCN as optional argument ([`ddc8b7a`](https://github.com/Jon-Ting/sphractal/commit/ddc8b7aeba31b7503c81e0cfe783e5fed9df1daa))

* feat(runBoxCnt): added radMult as an optional argument ([`2464081`](https://github.com/Jon-Ting/sphractal/commit/246408149c5e90d5c24ac6254506bc577bdc8864))


## v0.21.2 (2023-09-05)

### Build

* build(deps-dev): bump jupyter-server from 2.7.0 to 2.7.2 (#3)

Bumps [jupyter-server](https://github.com/jupyter-server/jupyter_server) from 2.7.0 to 2.7.2.
- [Release notes](https://github.com/jupyter-server/jupyter_server/releases)
- [Changelog](https://github.com/jupyter-server/jupyter_server/blob/main/CHANGELOG.md)
- [Commits](https://github.com/jupyter-server/jupyter_server/compare/v2.7.0...v2.7.2)

---
updated-dependencies:
- dependency-name: jupyter-server
  dependency-type: indirect
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt;
Co-authored-by: dependabot[bot] &lt;49699333+dependabot[bot]@users.noreply.github.com&gt; ([`75625ef`](https://github.com/Jon-Ting/sphractal/commit/75625efa8f9e205f104d28d23d2e398f7214c8a2))


## v0.21.1 (2023-08-22)

### Build

* build(poetry.lock): resolved tornado dependabot alert ([`918e49d`](https://github.com/Jon-Ting/sphractal/commit/918e49d06dbcb3205b608dc75ef433f8a96f66d3))


## v0.21.0 (2023-08-16)

### Feature

* feat(findAtomsWithSurfNeighs): renamed findTargetAtoms() ([`e4ff459`](https://github.com/Jon-Ting/sphractal/commit/e4ff4595d01c5fc0f382a4c4144d245af505e704))

* feat(runBoxCnt): modified default value for minSample ([`866d551`](https://github.com/Jon-Ting/sphractal/commit/866d551ea5104f7d4b8a3dcd11d256fed67f553a))

### Fix

* fix(tests): updated test functions related to findTargetAtoms() ([`e0a2557`](https://github.com/Jon-Ting/sphractal/commit/e0a2557b5ab0b4588e7d8854816a89a1c4e7ce99))

### Performance

* perf(scanBox): removed redundant steps for inclusion of inner surface box counts ([`94da738`](https://github.com/Jon-Ting/sphractal/commit/94da73869ad4bcb8e9e6fee4595e9298162bb6e1))


## v0.20.13 (2023-08-12)

### Build

* build(ci-cd.yml): reverted back to usual publishing pipeline ([`bc1539a`](https://github.com/Jon-Ting/sphractal/commit/bc1539a05aebbea8f5fe0635c6d9c8c009fd8992))


## v0.20.12 (2023-08-12)

### Build

* build(ci-cd.yml): resolved conflicts ([`5bc16c7`](https://github.com/Jon-Ting/sphractal/commit/5bc16c7454aee1404e9e8226641e69d5bf39e3db))

* build(ci-cd.yml): added retrieve distribution step to publishing job ([`22b696b`](https://github.com/Jon-Ting/sphractal/commit/22b696bf76d6048175d7ff4833dd28d61e3767cd))


## v0.20.11 (2023-08-12)

### Build

* build(dist): ignored dist/ ([`2f9a9c5`](https://github.com/Jon-Ting/sphractal/commit/2f9a9c583db478146ff6595104f0323d274625c6))

### Fix

* fix(build): added dist/ ([`5f04a0d`](https://github.com/Jon-Ting/sphractal/commit/5f04a0d423bb53c8e33eb5543ff650ecab521017))


## v0.20.10 (2023-08-12)

### Fix

* fix(build): added dist/ ([`078c188`](https://github.com/Jon-Ting/sphractal/commit/078c188e3fb2f32e639529b6c4f6df2481b0c8e4))


## v0.20.9 (2023-08-12)

### Build

* build(.gitignore): stopped ignoring dist/ ([`fdcab07`](https://github.com/Jon-Ting/sphractal/commit/fdcab07aff1c6c2029fa6acc9ed89ed32f26601e))


## v0.20.8 (2023-08-12)

### Fix

* fix(ci-cd.yml): separate out a new pipeline for publishing

Signed-off-by: Jonathan Yik Chang Ting &lt;jonting97@gmail.com&gt; ([`f7a9989`](https://github.com/Jon-Ting/sphractal/commit/f7a9989a027f7c9b3e3f94973759f76932a855ca))

* fix(ci-cd.yml): added permission lines to specify trusted publishing flow

Signed-off-by: Jonathan Yik Chang Ting &lt;jonting97@gmail.com&gt; ([`589468b`](https://github.com/Jon-Ting/sphractal/commit/589468b0554cd6eb8bda7632cda0c0b6162b2b56))


## v0.20.7 (2023-08-12)

### Build

* build(ci-cd.yml): removed usernames and API tokens from file

Signed-off-by: Jonathan Yik Chang Ting &lt;jonting97@gmail.com&gt; ([`136659b`](https://github.com/Jon-Ting/sphractal/commit/136659be05eacbee562a6391aeaca1cf1ff84a9b))


## v0.20.6 (2023-08-12)

### Build

* build(ci-cd.yml): dealt with repository_url deprecation issue

Signed-off-by: Jonathan Yik Chang Ting &lt;jonting97@gmail.com&gt; ([`af9b5a7`](https://github.com/Jon-Ting/sphractal/commit/af9b5a712dbf6607710ab431fa900fc359df2ada))


## v0.20.5 (2023-08-12)

### Build

* build(ci-cd.yml): uncommented documentation building step

Signed-off-by: Jonathan Yik Chang Ting &lt;jonting97@gmail.com&gt; ([`5df24cc`](https://github.com/Jon-Ting/sphractal/commit/5df24cc00a6a70415abbcd95884a801828c804ee))


## v0.20.4 (2023-08-12)

### Build

* build(setup.py): made description on PyPI consistent with GitHub repo ([`d88a90e`](https://github.com/Jon-Ting/sphractal/commit/d88a90e0fb1279afe785b8b9362faa17776e428e))


## v0.20.3 (2023-08-12)

### Documentation

* docs(example): made sure all codes are visible in notebook ([`bc6db5c`](https://github.com/Jon-Ting/sphractal/commit/bc6db5c2904f045f105d0a0c71fe81cad38181a0))

* docs(readme): fixed pypi readme rendering issue ([`d6cf985`](https://github.com/Jon-Ting/sphractal/commit/d6cf98573c59fbb5cb5ab0fe31dd02254f83c770))


## v0.20.2 (2023-08-12)

### Documentation

* docs(readme): attempt to fix pypi readme rendering issue ([`ac8099a`](https://github.com/Jon-Ting/sphractal/commit/ac8099aa0644ba9203be9f0fe869d8b535f5a692))

* docs(example): updated example notebook ([`753e0f8`](https://github.com/Jon-Ting/sphractal/commit/753e0f851f8c6674011e8902068287e0d87ea4bd))

* docs: improved consistency of the docstrings for all functions ([`bbb613d`](https://github.com/Jon-Ting/sphractal/commit/bbb613d8ce7cd800226a5bb8bdcb899505a89069))

* docs(readme): made readme statements more concise ([`f1ef8ce`](https://github.com/Jon-Ting/sphractal/commit/f1ef8ce6b2779c749e09b84409cd43c0f99c8e01))

### Refactor

* refactor(findSlope): made sure estimation results are reported after all plots are shown ([`b490982`](https://github.com/Jon-Ting/sphractal/commit/b490982afba55ad8ed9a53839d1c4a97cae16936))


## v0.20.1 (2023-08-12)

### Documentation

* docs(readme): fixed position of first image

Signed-off-by: Jonathan Yik Chang Ting &lt;jonting97@gmail.com&gt; ([`fbfb2f5`](https://github.com/Jon-Ting/sphractal/commit/fbfb2f52ff468b2d026a50430f7bc1c7db123d07))


## v0.20.0 (2023-08-12)

### Build

* build: merge branch &#39;main&#39; of github.com:Jon-Ting/sphractal into main ([`60a51ef`](https://github.com/Jon-Ting/sphractal/commit/60a51ef146681887fd21b5734b6cd52d58f386d3))

### Documentation

* docs(findNN): added docstring for the function ([`7b22a4c`](https://github.com/Jon-Ting/sphractal/commit/7b22a4c159468db20e9eb66718d2edc23a5fe1fc))

### Feature

* feat(findSlope): modified while loop condition to better reflect the minSample specified ([`2805b74`](https://github.com/Jon-Ting/sphractal/commit/2805b745ec6b1b80f29853436bb9a8161a259dfe))

* feat(findSlope): modified while loop condition to better reflect the minSample specified ([`a7b7270`](https://github.com/Jon-Ting/sphractal/commit/a7b7270f095101f844b18120df23a663de1163c3))

### Fix

* fix(tests): removed redundant test combinations ([`374c5f1`](https://github.com/Jon-Ting/sphractal/commit/374c5f1a38f27be8a8197fdf6ba075d7dd31e6a8))

### Performance

* perf(findSlope): added assertion for minSample to make sure it&#39;s integer ([`ba6698d`](https://github.com/Jon-Ting/sphractal/commit/ba6698dba109e0cf6376d3a7a33d5a02e27bfc37))

### Unknown

* build(gitpython) : resolved dependency issue ([`fa8994f`](https://github.com/Jon-Ting/sphractal/commit/fa8994f5fc3bd51c5ce003e56fc4b4b8d716d485))


## v0.19.5 (2023-08-10)

### Fix

* fix(tests): corrected the function called to test getCaseStudyPaths() ([`8dcf30c`](https://github.com/Jon-Ting/sphractal/commit/8dcf30c76f55fe2bf022001f169669cadaa74d02))

* fix(test): corrected the number of case study coordinate files to be retrieved ([`84afd20`](https://github.com/Jon-Ting/sphractal/commit/84afd201c779065e3f9c995e0dc197e9b5ba94d5))

* fix(data): included the rhombic dodecahedron atomic coordinates as data ([`84edfb7`](https://github.com/Jon-Ting/sphractal/commit/84edfb7f902a8096b2e2c8ab664427a89d3778e6))

### Refactor

* refactor: merge branch &#39;main&#39; of github.com:Jon-Ting/sphractal into main ([`90d40f9`](https://github.com/Jon-Ting/sphractal/commit/90d40f94f96183b9466ef2ecee47cb54f3bfd15d))


## v0.19.4 (2023-08-09)

### Documentation

* docs(init): made documentations in __init__.py more concise ([`49dc087`](https://github.com/Jon-Ting/sphractal/commit/49dc0871c014d20f9113f7ce90639c38cb7136be))

### Fix

* fix(readthedocs): fixed the rendering errors on Sphinx documentations ([`850613a`](https://github.com/Jon-Ting/sphractal/commit/850613ac6f69e364de89d9e53523e00ad70c97f8))

### Refactor

* refactor(outDir): set default variable string to &#39;outputs&#39; ([`da0e7b2`](https://github.com/Jon-Ting/sphractal/commit/da0e7b29dbc8f29d7d9bf81b9c7882b23d5123ae))


## v0.19.3 (2023-08-09)

### Build

* build(ci-cd): commented out documentation re-rendering step from ci-cd.yml

Signed-off-by: Jonathan Yik Chang Ting &lt;jonting97@gmail.com&gt; ([`e7bcaa3`](https://github.com/Jon-Ting/sphractal/commit/e7bcaa3520e23bdd767aa0427278d6e2c5290374))


## v0.19.2 (2023-08-07)

### Fix

* fix(findSlope): fixed calling variable before assignment issue ([`6426881`](https://github.com/Jon-Ting/sphractal/commit/6426881373b156d853f326d0d4e8651d4f75e819))


## v0.19.1 (2023-08-07)

### Fix

* fix(findSlope): fixed calling variable before assignment issue ([`c5a94a4`](https://github.com/Jon-Ting/sphractal/commit/c5a94a481bb57bd5761b93d0ed623da1b4e84d7a))


## v0.19.0 (2023-08-07)

### Build

* build(gitignore): removed redundancies in .gitignore ([`be426cd`](https://github.com/Jon-Ting/sphractal/commit/be426cde18513acef4bf0f5f0f5568889fca5c90))

### Documentation

* docs(example): updated usage of findSlope() in example notebook ([`17f5b6f`](https://github.com/Jon-Ting/sphractal/commit/17f5b6f698b7d096411db6d3f3aa5b511de5ee4c))

### Feature

* feat(findSlope): returned final range of box lengths ([`a955fd4`](https://github.com/Jon-Ting/sphractal/commit/a955fd4de609ee30d9874062b59993f44ae839f0))

### Fix

* fix(test): fixed test function related to findSlope() ([`8a95cb3`](https://github.com/Jon-Ting/sphractal/commit/8a95cb3a245aeb453ff1827fe81db7dfdfe8439b))


## v0.18.4 (2023-08-04)

### Build

* build(poetry.lock): resolved dependencies vulnerability ([`216b0d3`](https://github.com/Jon-Ting/sphractal/commit/216b0d301c71c9af5bfc716064e46eae090f7775))

* build(dist): removed dist/ directory ([`043389f`](https://github.com/Jon-Ting/sphractal/commit/043389f9e29b1bfcc1fb5adec05729421b65579b))

* build(fastbc): ignored fastbc/ ([`3e0933a`](https://github.com/Jon-Ting/sphractal/commit/3e0933ad54ea40d737825f7af7a98b5360a71d03))

* build(poetry.lock): updated crytography package version ([`6962299`](https://github.com/Jon-Ting/sphractal/commit/6962299ef996e43b87aebf62de5517921c253424))

* build(fastbc): updated commits from fastbc/ repo ([`d32f9d3`](https://github.com/Jon-Ting/sphractal/commit/d32f9d318ecc4fa169726b3cdd787ea30d287b5a))

* build(condaforge): removed staged-recipes ([`e262310`](https://github.com/Jon-Ting/sphractal/commit/e262310578fac7d4ffc55ea46dc69f39bd1ad19c))

* build: allowed PSR to bump package version in setup.py as well ([`823f80b`](https://github.com/Jon-Ting/sphractal/commit/823f80b6df77b689560c450ae53e6923af69f416))

* build(condaforge): added staged-recipes for publication to conda-forge ([`0c09dab`](https://github.com/Jon-Ting/sphractal/commit/0c09dab457cee25c1086ac0da073594edd2a7db5))

* build(setup): included setup.py in pyproject.toml ([`4412644`](https://github.com/Jon-Ting/sphractal/commit/4412644a08a032e6f4aa520cfd625357e3837942))

* build: ignored dist/ ([`d3b183a`](https://github.com/Jon-Ting/sphractal/commit/d3b183a144f81284392852ae3b3222a52a126cf5))

* build: added information to be displayed for pip show in pyproject.toml ([`ef9a3c1`](https://github.com/Jon-Ting/sphractal/commit/ef9a3c1923153b45f38c6e829fd8e56071e6a101))

* build(setup): added setup.py ([`7c58f40`](https://github.com/Jon-Ting/sphractal/commit/7c58f403abe1bfd53d674ce02821f262690eec5e))

* build(dist): stopped ignoring dist/ ([`43f1264`](https://github.com/Jon-Ting/sphractal/commit/43f1264afd214395c309e4d9f0aadc758cd0714c))

* build: preparing for releasev0.3.0 ([`25ee6ba`](https://github.com/Jon-Ting/sphractal/commit/25ee6bac57dbd70951649b89292525e3b9dfd348))

* build: updated poetry.lock ([`1e1d824`](https://github.com/Jon-Ting/sphractal/commit/1e1d824ff00275e51210aff0d25297386ae63e5b))

* build: updated all dependencies ([`3af9a9e`](https://github.com/Jon-Ting/sphractal/commit/3af9a9ef0196ae93b31e345ea25b0181efb8180c))

* build: added dependencies ([`442a6ca`](https://github.com/Jon-Ting/sphractal/commit/442a6ca0c0a940b1297d3751152ae0ec57857602))

### Documentation

* docs(boxCnt): improved conciseness of the docstring for runBoxCnt() ([`083f977`](https://github.com/Jon-Ting/sphractal/commit/083f97732860fe71a357e8fca61ae911b43c259a))

* docs(example): explained the choice of numPoints in example.ipynb ([`8f45bd2`](https://github.com/Jon-Ting/sphractal/commit/8f45bd22e04cc6f2b56243d7a089f753d87349a5))

* docs(example): updated example.ipynb with recoloured and reoriented figures ([`9c17801`](https://github.com/Jon-Ting/sphractal/commit/9c17801f589184878ca39b0b26a188be50202183))

* docs(surfVoxel): simplified docstring for voxelBoxCnts() ([`4d7a395`](https://github.com/Jon-Ting/sphractal/commit/4d7a3950c75b69880881977aa2249507bf1015d8))

* docs(surfVoxel): updated recommendations of resource allocations for voxelBoxCnts() ([`e0eedb0`](https://github.com/Jon-Ting/sphractal/commit/e0eedb018ff919e3e7ee74a19610e78c23928ca4))

* docs(example): updated example.ipynb ([`578d85d`](https://github.com/Jon-Ting/sphractal/commit/578d85d5e996533c812ca919de7b11a75412ef9b))

* docs(readme): fixed paragraphing problems

Signed-off-by: Jonathan Yik Chang Ting &lt;jonting97@gmail.com&gt; ([`a637259`](https://github.com/Jon-Ting/sphractal/commit/a637259e1b4472fdc46fbd7201b0b6c18c0c3796))

* docs(readme): fixed fastbc repo link

Signed-off-by: Jonathan Yik Chang Ting &lt;jonting97@gmail.com&gt; ([`c43c213`](https://github.com/Jon-Ting/sphractal/commit/c43c213821bc83ac427ff082cd3bf69ce1ae21fa))

* docs(readme): added figures to readme

Signed-off-by: Jonathan Yik Chang Ting &lt;jonting97@gmail.com&gt; ([`813de14`](https://github.com/Jon-Ting/sphractal/commit/813de14bae48be15e960581f2a4673f98dafe949))

* docs(readme): removed dollar signs from readme ([`c6fc475`](https://github.com/Jon-Ting/sphractal/commit/c6fc475e537c5c3ef28029335942a25c70dd584d))

* docs(example): updated example notebook ([`76ecff9`](https://github.com/Jon-Ting/sphractal/commit/76ecff996e7ee04493c6aa5eeb4adf5baa932cbf))

* docs(readme): updated variable name change on readme ([`ff81621`](https://github.com/Jon-Ting/sphractal/commit/ff81621d7f8c19abc28e49f9d767e6e1cd77503f))

* docs(readme): added background section to readme ([`bcfbb62`](https://github.com/Jon-Ting/sphractal/commit/bcfbb62e4eb61beb0254ae24f72ccba1e890ef0a))

* docs(readme): omitted features under development ([`b9af10a`](https://github.com/Jon-Ting/sphractal/commit/b9af10aa6bc4b969ae9c30bbde5c3b1bb3f31baf))

* docs(example): fixed a typo in example.ipynb ([`157adc3`](https://github.com/Jon-Ting/sphractal/commit/157adc392b7400ac3ff152db55eafa706fdaf78a))

* docs(readme): fixed typo in readme ([`92b38b8`](https://github.com/Jon-Ting/sphractal/commit/92b38b85d33da568ab861cdb61350c69e8f9745c))

* docs(findSlope): added in-line comments for findSlope() ([`573a20c`](https://github.com/Jon-Ting/sphractal/commit/573a20c67d99c8afad5fa923660d5f437d0fbfa9))

* docs(example): updated example.ipynb with new figures ([`8341718`](https://github.com/Jon-Ting/sphractal/commit/83417184919473a3676f13e0fbbeca8c783783bb))

* docs(example): deleted .virtual_documents from docs/ ([`78dbe38`](https://github.com/Jon-Ting/sphractal/commit/78dbe382b2a2038b2978e3e1cb61c5a5631116ee))

* docs(example): updated example.ipynb to make sure fastBC executable could be detected ([`42cd8a6`](https://github.com/Jon-Ting/sphractal/commit/42cd8a6eef54158cfa39012cb0493db2f87f7c60))

* docs(readme): updated readme to specify the delay in point cloud functionalities ([`4d73e24`](https://github.com/Jon-Ting/sphractal/commit/4d73e24a911d82c7786c280b13b4258abf229446))

* docs(readme): updated readme ([`a5e3aa0`](https://github.com/Jon-Ting/sphractal/commit/a5e3aa0a36943d149143b2a23588d87585a2d2cd))

* docs(readme): updated readme ([`3ab9697`](https://github.com/Jon-Ting/sphractal/commit/3ab969785424824cbe08af8ef84d56ba2cd26bb3))

* docs(mult): added recommendations for radMult and alphaMult to constants.py ([`90f31b4`](https://github.com/Jon-Ting/sphractal/commit/90f31b4379c2e81de9f8760121486fc8b96132a4))

* docs(example): completed example.ipynb ([`4b60535`](https://github.com/Jon-Ting/sphractal/commit/4b60535755e74b6e679daef80885a5c4a923a428))

* docs(findSurf): tidied up docstring for findSurf() ([`8bb5fb9`](https://github.com/Jon-Ting/sphractal/commit/8bb5fb925a425e55bbbffc953d96cf97e55577f0))

* docs(help): elaborated docstring to be returned from help() ([`543925b`](https://github.com/Jon-Ting/sphractal/commit/543925b95b7b43755a013b5e0d8c301eb66643eb))

* docs: updated readme for C++ file and docstrings for surfPointClouds.py functions ([`a30fff9`](https://github.com/Jon-Ting/sphractal/commit/a30fff971e22f361adef86dbf32c6da43d1d78c2))

* docs: updated readme and example ([`c142036`](https://github.com/Jon-Ting/sphractal/commit/c14203621ac38e9da934456ab52e675d55a09dd0))

* docs: updated readme and example ([`47c4e72`](https://github.com/Jon-Ting/sphractal/commit/47c4e726c1a01eba5640bd06cae2476e94e8de66))

* docs: updated readme and example ([`476ff31`](https://github.com/Jon-Ting/sphractal/commit/476ff316a6bf157cc22e3b6bd8c2b35e4c511c32))

### Feature

* feat(datasets): added functions to access the case study atomic data ([`126b444`](https://github.com/Jon-Ting/sphractal/commit/126b444ea079828e0ca9759ea8761c65af3bdafe))

* feat(data): added atomic coordinates used for case studies ([`8111d48`](https://github.com/Jon-Ting/sphractal/commit/8111d4815017e22062401e1d49ebda269d9d79e5))

* feat(data): added validation data ([`7161b6e`](https://github.com/Jon-Ting/sphractal/commit/7161b6e3dcbb34fa78a9d3a742c5260cb98d24ea))

* feat(boxCnt): changed &#39;lenRange&#39; into  &#39;trimLen&#39; ([`8c9eeaf`](https://github.com/Jon-Ting/sphractal/commit/8c9eeaf8780a55fe7617d15a61d2b0a20536d3c6))

* feat(surfVoxel): implemented parallelisation functionalities for generation of point cloud representation of surface (#1)

* docs(boxCnt): updated docstrings of runBoxCnt()

* refactor(surfExact): renamed variables related to multiprocessings in surfExact.py

* docs(exactSurf): modified docstring for the &#39;exactSurf&#39; parameter of runBoxCnt()

* feat(surfVoxel): initialised parallelisation implementation for voxel representation

* build(fastbc): updated fastbc repo

* perf(surfVoxel): first stable version with parallelisation for surfVoxel functionalities

* build(fastbc): updated fastbc commits

* fix(surfVoxel): corrected the equation to get minAtomCPU

---------

Co-authored-by: Jonathan Ting &lt;jonathan.ting@anu.edu.au&gt;
Co-authored-by: github-actions &lt;github-actions@github.com&gt; ([`1a576ed`](https://github.com/Jon-Ting/sphractal/commit/1a576ed4f6fd133d1ecffa04aa2775200873c64a))

* feat(data): updated example xyz files for scaling tests ([`2e65389`](https://github.com/Jon-Ting/sphractal/commit/2e6538919b2c1c28f4e2298ec837c94644c3f16f))

* feat(boxLenConc): optimised resource allocations for more general cases ([`b107c07`](https://github.com/Jon-Ting/sphractal/commit/b107c078021c89c41e3674e8f7f5dd2cf43d4326))

* feat(data): unified and included more example data ([`c4cbe5e`](https://github.com/Jon-Ting/sphractal/commit/c4cbe5e54ee753a8cb640a36fe07b80384d90332))

* feat(data): added more example data and updated functionalities to get them ([`d65c3d2`](https://github.com/Jon-Ting/sphractal/commit/d65c3d21200a616208c2aa27c3001a3acbbec0ac))

* feat(findSlope): added notebook option to findSlope() plots ([`f6c6123`](https://github.com/Jon-Ting/sphractal/commit/f6c6123191d7d853fbd486f15049c526376da8da))

* feat(boxCnt): moved box-counting functions for each representation to respective modules ([`e8bbe38`](https://github.com/Jon-Ting/sphractal/commit/e8bbe38eb46dad1d2964569019f7c0a89c7604e3))

* feat: renamed modules, functions, variables to more concise names ([`0119301`](https://github.com/Jon-Ting/sphractal/commit/0119301cd857b5810d5689f6078ae4dd8dfd0dd6))

* feat(minValFromBound): added the input argument to related functionalities for exact surface representation ([`0ad3a49`](https://github.com/Jon-Ting/sphractal/commit/0ad3a496c2d954a10d8612ad9fcdb875c9c2585b))

* feat(figType): renamed options for figType based on seaborn style ([`f1a8fb1`](https://github.com/Jon-Ting/sphractal/commit/f1a8fb1ceacb23697ae30b7dd8e26e01745d1e94))

* feat(boxLenConc): implemented automatic parallelisation functionalities ([`b4f6c36`](https://github.com/Jon-Ting/sphractal/commit/b4f6c364c92ece88fa7bfea45ecaa565681c4647))

* feat(findSlope): added functionalities to generate publication-ready figures ([`5653519`](https://github.com/Jon-Ting/sphractal/commit/5653519a0fd49f12543eefcb7de96366113472ae))

* feat(pointcloud): implemented and provided clear instructions to use point cloud surface representation related functionalities ([`62d247c`](https://github.com/Jon-Ting/sphractal/commit/62d247c3fd277a3f4c96822f807bd0d56d392bbd))

* feat: added CI/CD workflow ([`8a78e22`](https://github.com/Jon-Ting/sphractal/commit/8a78e224634df7ee8ccbc75c6cb2b0f3944e8090))

* feat(init): added imports for more functions ([`f655fef`](https://github.com/Jon-Ting/sphractal/commit/f655fef441bf9c4ff426a35b3db6c65df89862d5))

* feat(findNN): allowed calcBL to be specified ([`b5c123c`](https://github.com/Jon-Ting/sphractal/commit/b5c123c183e0937a1e840c3b32be78c7cff285d5))

* feat(datasets): added example.xyz and new module to get its path ([`89f20dd`](https://github.com/Jon-Ting/sphractal/commit/89f20dd6ed9225c65b1be1b9c0fb1270d836506d))

* feat: add example data and datasets module ([`83e9473`](https://github.com/Jon-Ting/sphractal/commit/83e9473335279304d367b40e8d6691b9e30ee152))

* feat: added all source codes ([`f73f23c`](https://github.com/Jon-Ting/sphractal/commit/f73f23c7a21921925e43f3e553c3f000be90c2f6))

### Fix

* fix(readme): fixed readme broken links ([`dabe6e4`](https://github.com/Jon-Ting/sphractal/commit/dabe6e49094a196b8e280e15c2d60a1481747bb8))

* fix(tests): added test function for getCaseStudyDataPaths() ([`d324685`](https://github.com/Jon-Ting/sphractal/commit/d324685c489f9cb5a2cfbd1388d275f43a3bd37f))

* fix(surfVoxel): imported cpu_count() from multiprocessing ([`640025f`](https://github.com/Jon-Ting/sphractal/commit/640025ff9d869910f798654e74072d97ab0b3069))

* fix(test): updated ted test function for validation data ([`dcc47b9`](https://github.com/Jon-Ting/sphractal/commit/dcc47b9db5105a71dbc73be89ece49be0d904974))

* fix(findTargetAtoms): enabled the function to handle single atom case ([`2650e06`](https://github.com/Jon-Ting/sphractal/commit/2650e064a098e5681beb3e855474fb5eedc5f759))

* fix: enabled findNN() and findSurf() to handle single atom input ([`8cfdae4`](https://github.com/Jon-Ting/sphractal/commit/8cfdae4139e4772b8a5c0336accd5a8be852d3f4))

* fix(test): updated test functions related to example data ([`d40e923`](https://github.com/Jon-Ting/sphractal/commit/d40e92397dd78b09dd8a64d40a60fe1648e8a76b))

* fix(datasets): fixed a typo in getWeakScalingDataPaths() ([`533b5c7`](https://github.com/Jon-Ting/sphractal/commit/533b5c7b551bae0a9a59dd189e62e4d896432497))

* fix(datasets): added functions to get example data to package namespace ([`1302cdc`](https://github.com/Jon-Ting/sphractal/commit/1302cdc8b2f8942cd7380283c061fcc72c8df87b))

* fix(datasets): updated functions to get the xyz files used for scaling tests ([`05f61fb`](https://github.com/Jon-Ting/sphractal/commit/05f61fb4f7e0e9995e6d6f144ac0ca9ac2ff126b))

* fix(maxWorkers): fix zero cpu for parallelisation error ([`af00b98`](https://github.com/Jon-Ting/sphractal/commit/af00b989d8011afc48d7721632e4733167c30b7f))

* fix(boxLenScanMaxWorkers): fixed formula for resource allocations ([`165ec58`](https://github.com/Jon-Ting/sphractal/commit/165ec58e1d52a9836f9adecf4f1ef3455a64b42f))

* fix(fastbc): updated fastbc submodule name ([`43a9976`](https://github.com/Jon-Ting/sphractal/commit/43a9976d47b8d11648659bdea807c29d7eecc4a3))

* fix(findTargetAtoms): fixed the function for rmInSurf=False ([`c21fd67`](https://github.com/Jon-Ting/sphractal/commit/c21fd67a0b55618df06b5ab4e2701292e92161f5))

* fix(test): updated test functions ([`894d223`](https://github.com/Jon-Ting/sphractal/commit/894d2239a63cc88e4e85a76218c262fb733e8cc7))

* fix(readme): fixed broken links in readme ([`3e68a87`](https://github.com/Jon-Ting/sphractal/commit/3e68a87d75b0efb8584a8ad81a90824b61118834))

* fix(findSlope): reverted to producing figures with png format ([`a6ed73e`](https://github.com/Jon-Ting/sphractal/commit/a6ed73ee64c24cbba0f91d1f916d9ddba14d5f52))

* fix(version): fixed PSR not bumping pyproject.toml version mistake ([`e2e01bb`](https://github.com/Jon-Ting/sphractal/commit/e2e01bb6a9c19c366a8b890571516a7b5f546eb2))

* fix(version): updated pyproject.toml for PSR to bump version in it as well ([`2ce1374`](https://github.com/Jon-Ting/sphractal/commit/2ce1374580a85674e57b946e3d65f1eeafc51199))

* fix(setup): turned tuple for classifiers in setup.py into list ([`5fa7910`](https://github.com/Jon-Ting/sphractal/commit/5fa79104290534003656a63d3ba9d807bf27f6d6))

* fix(test): commented out tests for functionalities related to point cloud representation temporarily ([`86c5192`](https://github.com/Jon-Ting/sphractal/commit/86c5192be9bf8eca3721609d2f22e7e3fff615c8))

* fix(test): fixed missing directory error when running pytest from package root ([`062c4db`](https://github.com/Jon-Ting/sphractal/commit/062c4db2496d51491f9258a7fa0ab1fcef87a3e0))

* fix(mkdir): made sure that directories are generated before files are ([`c529767`](https://github.com/Jon-Ting/sphractal/commit/c529767b1dc168ead1932f19dd6a1191abeaaf7e))

* fix(cicd): updated ci-cd workflow ([`24b253c`](https://github.com/Jon-Ting/sphractal/commit/24b253cac9a6d8b6df81751376415ba02b7806cb))

* fix(findSurf): fixed &#39;numNeigh&#39; option in findSurf() ([`796d14c`](https://github.com/Jon-Ting/sphractal/commit/796d14cf05343b5004819be04a972826c277102c))

* fix(scanAllAtoms): scanAllAtoms() now prints 1/eps instead of magnFac ([`2c3b4a3`](https://github.com/Jon-Ting/sphractal/commit/2c3b4a30d9b126fb4bd6c8d8d5ec1e7f168221f1))

* fix(datasets): getExampleDataPath() returns str instead of PosixPath ([`6989942`](https://github.com/Jon-Ting/sphractal/commit/69899426fa6ae5406e322213930aea3e99ea2dfe))

### Performance

* perf(findSurf): sped up alpha shape algorithm ([`427536d`](https://github.com/Jon-Ting/sphractal/commit/427536d74b87bf9e445eb878baa7065c0f2e3f9d))

* perf(boxLenConc): reduced the number of times of calling cpu_counts() ([`c0911cf`](https://github.com/Jon-Ting/sphractal/commit/c0911cf1e04fde90be2ac38e8bd9004bf662caf2))

### Refactor

* refactor(datasets): added getCaseStudyDataPaths() to package namespace ([`47508f6`](https://github.com/Jon-Ting/sphractal/commit/47508f65d3dbcba0dad8e60df257272e2b581fa2))

* refactor(numPoints): made the variable name consistent across the package ([`4d419b9`](https://github.com/Jon-Ting/sphractal/commit/4d419b9fe3ed7d421a2d2dffdc25f317aef52ea9))

* refactor(boxCnt): made box count outputs printed more concise ([`47aacc3`](https://github.com/Jon-Ting/sphractal/commit/47aacc33144cde7526b3909f823c136bb2752e18))

* refactor(fastbc): updated fastbc submodule name ([`26a2f8d`](https://github.com/Jon-Ting/sphractal/commit/26a2f8d9d8a509913ddf271d95d448a73aefd658))

* refactor(findNN): removed unnecessary space and repeated codes ([`2dc8afd`](https://github.com/Jon-Ting/sphractal/commit/2dc8afd7ef515dc9423fd3921bfd026c4ef9c7e1))

* refactor(boxCnt): renamed PC to VX and ES to EX ([`ec9f93c`](https://github.com/Jon-Ting/sphractal/commit/ec9f93c9502b40b91a31c3a61a61e3bdf69e682a))

* refactor(surfPointClouds): renamed surfPointClouds.py to surfVoxel.py ([`1be2ab5`](https://github.com/Jon-Ting/sphractal/commit/1be2ab53b480e924201587cc98309ea176ff1df9))

* refactor: renamed alphaMult in findNN() to radMult ([`ba452d0`](https://github.com/Jon-Ting/sphractal/commit/ba452d0e7c0574e3dfbc643eef1c73f9f4f3a145))

* refactor(import): reordered import sequences following best practices ([`feeed14`](https://github.com/Jon-Ting/sphractal/commit/feeed14ae9be946dfe57cbb30f13205e69913359))

* refactor: reformatted the files to follow pep8 ([`8b54722`](https://github.com/Jon-Ting/sphractal/commit/8b54722254eab8fc3975407d5d4315748223bd1d))

* refactor(gitignore): ignored and removed files under development ([`312761a`](https://github.com/Jon-Ting/sphractal/commit/312761a60b888da4aa4e0076f33d583951da5bee))

* refactor: added sphractal-feedstock to .gitmodules ([`efa0361`](https://github.com/Jon-Ting/sphractal/commit/efa0361158fb17093f87768bbdb47fffb2df19f0))

* refactor(radType): changed default radType to &#39;atomic&#39; ([`d272ea9`](https://github.com/Jon-Ting/sphractal/commit/d272ea91bd1d7dcdf9954f14f7ee804822506347))

* refactor(bin): added compiled C++ GPU code ([`b6e6fb6`](https://github.com/Jon-Ting/sphractal/commit/b6e6fb6bdf91685669ed7e3917a4998da08004ce))

### Style

* style(exactBoxCnts): removed a print statement from the function ([`139b046`](https://github.com/Jon-Ting/sphractal/commit/139b0462566a2aeea0d296c2b15327d0935a3138))

* style: included more information in printing statements of getSphereBoxCnts() ([`e6bfcee`](https://github.com/Jon-Ting/sphractal/commit/e6bfcee17e41846f8157dfaefa05b3743cacfd30))

* style: added space in print statements for better visibility ([`1584c60`](https://github.com/Jon-Ting/sphractal/commit/1584c604f09b65c4b8afb1271c0a1d949a37b1db))

### Test

* test(trimLen): updated change in variable name ([`e442aa6`](https://github.com/Jon-Ting/sphractal/commit/e442aa60cc6fcc2a6bec0cabc681465f84482f5c))

* test(example): updated test functions for functions related to example data ([`fb1c8f0`](https://github.com/Jon-Ting/sphractal/commit/fb1c8f0d9ea213becab1243859459eb0ea5bec96))

* test: updated test functions and fixtures for findTargetAtoms() ([`35c7a55`](https://github.com/Jon-Ting/sphractal/commit/35c7a55058f53290663fead8975d36639d8ca56f))

* test(example): added test function for new example function ([`d07b85e`](https://github.com/Jon-Ting/sphractal/commit/d07b85e4bb0286f0e054ea00a86775e372b9cc2c))

* test: uncommented a test function for findSlope() ([`6d6b75b`](https://github.com/Jon-Ting/sphractal/commit/6d6b75bad07bdf261ac3634a4ca53c641aac802c))

* test: updated docstrings in test functions that are commented out ([`ed69a98`](https://github.com/Jon-Ting/sphractal/commit/ed69a98b639bbd7b086a33a3db100153c0527cf8))

* test: added unit tests for higher level functions ([`f1269a5`](https://github.com/Jon-Ting/sphractal/commit/f1269a53a6f873b8f08210934507d6f255eb4cfb))

* test: added tests for some functions ([`1350d4c`](https://github.com/Jon-Ting/sphractal/commit/1350d4caed38ab0b8b42e2422b75efa719e4a73c))

### Unknown

* Merge branch &#39;main&#39; of github.com:Jon-Ting/sphractal ([`3de0d64`](https://github.com/Jon-Ting/sphractal/commit/3de0d64a457b7e5bd7b5f16658edb26471658685))

* Merge branch &#39;main&#39; of github.com:Jon-Ting/sphractal ([`ff4fe90`](https://github.com/Jon-Ting/sphractal/commit/ff4fe90951a035d05b6c77916d8b598b87bc9941))

* Merge branch &#39;main&#39; of github.com:Jon-Ting/sphractal into main ([`2830ed3`](https://github.com/Jon-Ting/sphractal/commit/2830ed359aff0c5e828210d6f3bae70e219ecfcb))

* Merge branch &#39;main&#39; of github.com:Jon-Ting/sphractal into main ([`dacfae8`](https://github.com/Jon-Ting/sphractal/commit/dacfae8b4d2461dc93fe96b7a6aef8657779ce4e))

* feat(nexactBoxCnts: added numCPUs as input argument to the function ([`f1e01c9`](https://github.com/Jon-Ting/sphractal/commit/f1e01c9e3ce3d6c1af566784b5e09f0929e347c0))

* Merge branch &#39;main&#39; of github.com:Jon-Ting/sphractal into main ([`428347a`](https://github.com/Jon-Ting/sphractal/commit/428347a98ff17abe63e65ecb2f7bd2316d410fc5))

* Merge branch &#39;main&#39; of github.com:Jon-Ting/sphractal into main ([`d0577b6`](https://github.com/Jon-Ting/sphractal/commit/d0577b6bc22b23fae1a8d8dcaf3ec2ea26376913))

* Merge branch &#39;main&#39; of github.com:Jon-Ting/sphractal into main ([`be2f0ea`](https://github.com/Jon-Ting/sphractal/commit/be2f0ea10f6fa56b836dfc0fd707a00d4cdb91c8))

* Merge branch &#39;main&#39; of github.com:Jon-Ting/sphractal into main ([`7af5410`](https://github.com/Jon-Ting/sphractal/commit/7af5410639a9c5d361f7272b335a3b9e8d8afcdb))

* Update ci-cd.yml ([`fcd19ca`](https://github.com/Jon-Ting/sphractal/commit/fcd19cad0e0199ba5b9ceb484323a2edb07e2e62))

* initial package setup ([`268b378`](https://github.com/Jon-Ting/sphractal/commit/268b378604ebfef1151d52d52b42f4ca36613502))
