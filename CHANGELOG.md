# CHANGELOG



## v1.4.1 (2024-01-13)

### Build

* build: bump version os python used on workflows to 3.11 ([`853d23b`](https://github.com/danielmbomfim/PyYep/commit/853d23b95fc1954ae32738be72f0cb030ad5771e))

### Documentation

* docs: updates doc strings ([`3a5a807`](https://github.com/danielmbomfim/PyYep/commit/3a5a8074b685e615dc80e90dfa8e966acc71c2fe))

### Fix

* fix: fix path of nested validation errors ([`2bf196f`](https://github.com/danielmbomfim/PyYep/commit/2bf196fdbb4be3219efe8331c8bda0c8a11c6b95))

* fix: fixes typing errors ([`32be752`](https://github.com/danielmbomfim/PyYep/commit/32be7521df2f8c1eb7bf6a0141fa4977488de0bb))

### Refactor

* refactor: change the name of some attributes and methods to make them more explicit ([`a536283`](https://github.com/danielmbomfim/PyYep/commit/a53628334db0ce939127e9de5b6395be3e242068))

### Style

* style: fix flake8 style erros ([`d8b1eab`](https://github.com/danielmbomfim/PyYep/commit/d8b1eab048bd2a9d4c0dd9cc1f286c1b9f205a5e))


## v1.4.0 (2023-12-09)

### Chore

* chore(release): [skip ci] Release v1.4.0 ([`57dcfef`](https://github.com/danielmbomfim/PyYep/commit/57dcfefbd92e44557fdbe72146027302c251ec0c))

### Documentation

* docs: updates README.md ([`84733ae`](https://github.com/danielmbomfim/PyYep/commit/84733aeb00bc15170b9a2adda92feeabfcea2410))

### Feature

* feat: adds support for implicit schemas on dict validation ([`2a51746`](https://github.com/danielmbomfim/PyYep/commit/2a5174631da1b4c0ac87901cfcf3d7f123fd48c8))


## v1.3.0 (2023-12-02)

### Chore

* chore(release): [skip ci] Release v1.3.0 ([`2ace7e9`](https://github.com/danielmbomfim/PyYep/commit/2ace7e9c670174045e3dc41f16a8af0676303bb6))

### Feature

* feat: implements a validator for dicts ([`10cf63e`](https://github.com/danielmbomfim/PyYep/commit/10cf63e7d3794d2fba829b6173d1e93ddcd60e98))

### Fix

* fix: validation on the &#34;of&#34; method of the array validation wont stop at the first error anymore ([`e948375`](https://github.com/danielmbomfim/PyYep/commit/e948375e8c10367666ecc970c817407486457897))


## v1.2.0 (2023-11-28)

### Chore

* chore(release): [skip ci] Release v1.2.0 ([`6a6a1eb`](https://github.com/danielmbomfim/PyYep/commit/6a6a1eb8b5cd61d4f3197fe28db4d2865bafca85))

### Feature

* feat: adds a validation method to array validator to test if an item is included on a iterable ([`d5b3da0`](https://github.com/danielmbomfim/PyYep/commit/d5b3da0acfdc2fb3a5c7e14f5ccd23aa01d68ba4))


## v1.1.0 (2023-11-26)

### Chore

* chore(release): [skip ci] Release v1.1.0 ([`c2aba5e`](https://github.com/danielmbomfim/PyYep/commit/c2aba5e96c38cdfffe0fc02f0ab4b339365f5561))

* chore: implements semantic release ([`75e3ed6`](https://github.com/danielmbomfim/PyYep/commit/75e3ed697697bd71359995960dad761ea4f94c47))

### Ci

* ci: split code analyze and build in different actions ([`c4d9229`](https://github.com/danielmbomfim/PyYep/commit/c4d9229bc4efc0d82418e1bfa13a5015d274f39a))

### Documentation

* docs: update docstrings of validation methods ([`ce7b979`](https://github.com/danielmbomfim/PyYep/commit/ce7b979f03f152968b1439a75cfa2eb42bc10744))

### Feature

* feat: adds a option to validate the items of an array ([`aafd94f`](https://github.com/danielmbomfim/PyYep/commit/aafd94f007314ef492050004c6641aaf12d0d0cf))

### Fix

* fix: fixes bug when passing Validators instances as arguments to validation methods ([`2168fe6`](https://github.com/danielmbomfim/PyYep/commit/2168fe6e511d8e9f3e0f59bcc8819e96013ced2a))

### Refactor

* refactor: updates ArrayValidator type hints ([`066bd06`](https://github.com/danielmbomfim/PyYep/commit/066bd0662ae406a92b83d374e00247d031f3216e))

* refactor: refactors validatorMethod decorator to make it more legible ([`2625be7`](https://github.com/danielmbomfim/PyYep/commit/2625be7d3d6e1c00ee5b05a83a6f332d7eb36e7c))

* refactor: replaces the Any type by TypeVars ([`7dba2ab`](https://github.com/danielmbomfim/PyYep/commit/7dba2ab01b08224fa5d2140eb27fdfdb6bfa3caf))

* refactor: removes unused code ([`30c4b57`](https://github.com/danielmbomfim/PyYep/commit/30c4b5758a752e45f75a467f71c13f2d2b0272f1))

* refactor: splits the validators on individual files ([`1a0b08d`](https://github.com/danielmbomfim/PyYep/commit/1a0b08d2b532791606bf3cb1caa81934efca1cd0))

### Style

* style: applies python&#39;s recommended styling rules ([`b024e17`](https://github.com/danielmbomfim/PyYep/commit/b024e17d8b9cda2ad081050fa835ca4e9c14b1a0))

### Unknown

* Update README.md ([`ad565f0`](https://github.com/danielmbomfim/PyYep/commit/ad565f051c907a9eb8b676ea9b39c41c844e5348))

* tests: expands tests coverage ([`5ba13e0`](https://github.com/danielmbomfim/PyYep/commit/5ba13e05c3f00bcf6642e53f815fa4d2ccd86be3))


## v1.0.1 (2023-11-24)

### Feature

* feat: adds simple valudation to arrays ([`cb4e0d6`](https://github.com/danielmbomfim/PyYep/commit/cb4e0d6d47141fffe1ef7eb0497466e272120a99))

### Unknown

* Merge pull request #1 from danielmbomfim/feat/array-validation

feat: adds simple valudation to arrays ([`879bcc2`](https://github.com/danielmbomfim/PyYep/commit/879bcc2080403458090bd3a6066136743f6abb79))

* fixing docstrings ([`0f8c8f9`](https://github.com/danielmbomfim/PyYep/commit/0f8c8f9a8c1e4140d1cf2a22f8a09c4228f01c3c))

* added a modifier method to allow modifications on values after validation ([`41cd097`](https://github.com/danielmbomfim/PyYep/commit/41cd0978fb60850c3323dbce2c91a6ea8ed1718c))

* added a condition method to allow the conditional execution of validators ([`846b165`](https://github.com/danielmbomfim/PyYep/commit/846b165db2727d87479a5ce031f2858be5b70342))

* added some validators for brazilian documents ([`13b4d2b`](https://github.com/danielmbomfim/PyYep/commit/13b4d2bcff9029c70ed1251120b662d16f0221ce))

* fixing validators docstrings ([`987abf5`](https://github.com/danielmbomfim/PyYep/commit/987abf5a071bb62f0d2fc457b6f761daeb5e1a6b))

* created a decorator to abstract the validators registry and adding new default validation method in_ ([`b921970`](https://github.com/danielmbomfim/PyYep/commit/b9219708e7e09a2809180cd08562c7040e1f2ffd))

* added the option of using a success hook on the input items ([`575d915`](https://github.com/danielmbomfim/PyYep/commit/575d915415d11162e25a86d72c4feaafd7496b84))

* changed container used on build from windows to Linux (ubuntu) ([`88da2f4`](https://github.com/danielmbomfim/PyYep/commit/88da2f43a9f366f4be4076e392d1330f4d6f2c0a))

* added basic documentation ([`893f773`](https://github.com/danielmbomfim/PyYep/commit/893f77374c4d91e0dfb520ea400768a5570dbbd7))

* added test and build files ([`89917a3`](https://github.com/danielmbomfim/PyYep/commit/89917a3690d5bfb33e3e5ece923bf69ebf9b7bb0))

* created the base for the project ([`5c3b112`](https://github.com/danielmbomfim/PyYep/commit/5c3b1129f690c130f7c8cda5fe1179bc085b83ac))
