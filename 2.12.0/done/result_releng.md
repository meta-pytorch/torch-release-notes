
# Release Notes worksheet releng

You should:

1. ensure commit categorization is correct
2. write up major features, bc-breaking changes, deprecations in detail
3. summarize the other sections

## 1. Ensure commit categorization is correct

* Please sort commits into the following categories (you should not rename the categories!), I tried to pre-sort these to ease your work, feel free to move commits around if the current categorization is not good.
* Anything that is not public facing needs to be removed.
* If anything is miscategorized/belongs to another domain, move it to `miscategorized.md`.
* Please scan through `miscategorized.md` and handle any commits that belong within your domain according to these instructions.

The categories below are as follows:

* BC breaking: All commits that are BC-breaking. These are the most important commits. If any pre-sorted commit is actually BC-breaking, do move it to this section. Each commit should contain a paragraph explaining the rational behind the change as well as an example for how to update user code [BC-Guidelines](https://docs.google.com/document/d/14OmgGBr1w6gl1VO47GGGdwrIaUNr92DFhQbY_NEk8mQ/edit#heading=h.a9htwgvvec1m).
* Deprecations: All commits introducing deprecation. Each commit should include a small example explaining what should be done to update user code.
* new_features: All commits introducing a new feature (new functions, new submodule, new supported platform etc)
* improvements: All commits providing improvements to existing feature should be here (new backend for a function, new argument, better numerical stability)
* bug fixes: All commits that fix bugs and behaviors that do not match the documentation
* performance: All commits that are added mainly for performance (we separate this from improvements above to make it easier for users to look for it)
* documentation: All commits that add/update documentation
* Developers: All commits that are not end-user facing but still impact people that compile from source, develop into pytorch, extend pytorch, etc
* not user facing: All commits that are not public end-user facing and hence should be dropped from the release notes

## 2. Major features, BC-breaking changes, deprecations

The main goal of this process is to rephrase all the commit messages below to make them **clear and easy to read** by the end user. You should follow the following instructions to do so:

* **Please clean up and format commit titles to be readable by the general PyTorch user.** Make sure you're [following the guidance here](https://docs.google.com/document/d/14OmgGBr1w6gl1VO47GGGdwrIaUNr92DFhQbY_NEk8mQ/edit)! Your resulting notes must be consistent and easy to read.
* We place a lot of emphasis on the “BC-breaking” and “deprecation” sections. Those should be where the most effort goes in. The “improvements” and “bug fixes” for Python API should be nice as well.

## 3. Summarize the other sections

For the other sections (improvements, bug fixes, performance, documentation, developers, not user facing) - use your
judgement to summarize the key PRs. You do not need to make every commit description perfect
(changed in v2.10 to simplify the process).

Once you are finished, move this very file from `todo/` to `done/` and submit a pull request.

Feel free to use https://github.com/pytorch/pytorch/releases/tag/v2.10.0 as an example.

## releng
### bc breaking
### deprecation
- Deprecate CUDA 12.8 builds in favor of CUDA 13.0 ([#179072](https://github.com/pytorch/pytorch/pull/179072))

  CUDA 12.8 binaries have been removed from the PyTorch binary build matrix. CUDA 13.0 is now the stable default and CUDA 12.6 remains available for users on older drivers. Users explicitly pinning the `cu128` index URL will need to switch to `cu130` (recommended) or `cu126`.

  Version 2.11:
  ```bash
  pip install torch --index-url https://download.pytorch.org/whl/cu128
  ```

  Version 2.12:
  ```bash
  # Use CUDA 13.0 (default on PyPI):
  pip install torch
  # Or explicitly:
  pip install torch --index-url https://download.pytorch.org/whl/cu130
  # Older driver fallback:
  pip install torch --index-url https://download.pytorch.org/whl/cu126
  ```
- Compatibility with CMake < 3.10 will be removed in a future release ([#166259](https://github.com/pytorch/pytorch/pull/166259))

  Source builds against CMake versions older than 3.10 now emit a deprecation warning. A future release will require CMake 3.10 or newer; please upgrade CMake before then.
### new features
- Add Claude-powered autorevert AI advisor workflow ([#177404](https://github.com/pytorch/pytorch/pull/177404), [#178810](https://github.com/pytorch/pytorch/pull/178810))
- Add torchtitan tests to PyTorch CI ([#175901](https://github.com/pytorch/pytorch/pull/175901), [#176774](https://github.com/pytorch/pytorch/pull/176774), [#179749](https://github.com/pytorch/pytorch/pull/179749), [#177572](https://github.com/pytorch/pytorch/pull/177572))
- Add Pallas TPU CI configuration ([#173870](https://github.com/pytorch/pytorch/pull/173870), [#174532](https://github.com/pytorch/pytorch/pull/174532), [#175650](https://github.com/pytorch/pytorch/pull/175650), [#175590](https://github.com/pytorch/pytorch/pull/175590))
- Add downloadable profiler traces and TLParse output from CI runs ([#178488](https://github.com/pytorch/pytorch/pull/178488))
- Enable full AArch64 unit testing for pull requests, with periodic m7g coverage maintained on trunk ([#178270](https://github.com/pytorch/pytorch/pull/178270))
### improvements
- Add support for CUDA 13.2 in CI/CD including binary builds, magma builds, and Windows CD workflows; update binaries to CUDA 13.2.1 ([#177083](https://github.com/pytorch/pytorch/pull/177083), [#177197](https://github.com/pytorch/pytorch/pull/177197), [#177918](https://github.com/pytorch/pytorch/pull/177918), [#178660](https://github.com/pytorch/pytorch/pull/178660), [#180288](https://github.com/pytorch/pytorch/pull/180288), [#177975](https://github.com/pytorch/pytorch/pull/177975), [#177567](https://github.com/pytorch/pytorch/pull/177567), [#180293](https://github.com/pytorch/pytorch/pull/180293))
- Upgrade Triton to 3.7 ([#174896](https://github.com/pytorch/pytorch/pull/174896), [#178821](https://github.com/pytorch/pytorch/pull/178821), [#179586](https://github.com/pytorch/pytorch/pull/179586), [#179971](https://github.com/pytorch/pytorch/pull/179971), [#177364](https://github.com/pytorch/pytorch/pull/177364), [#177723](https://github.com/pytorch/pytorch/pull/177723))
- Upgrade NCCL to 2.29.7 ([#176299](https://github.com/pytorch/pytorch/pull/176299))
- Upgrade cusparseLt to 0.8.1 for CUDA 12.9 / 13.0 builds ([#177456](https://github.com/pytorch/pytorch/pull/177456))
- Migrate clang15 CI jobs to clang18 and consolidate ASAN/ONNX images ([#178801](https://github.com/pytorch/pytorch/pull/178801), [#178803](https://github.com/pytorch/pytorch/pull/178803), [#178928](https://github.com/pytorch/pytorch/pull/178928))
- Bump MACOSX_DEPLOYMENT_TARGET to 14.0 ([#179083](https://github.com/pytorch/pytorch/pull/179083))
- Bump numpy pin to 2.3.4 for Python 3.14 builds ([#179720](https://github.com/pytorch/pytorch/pull/179720))
- Add macOS wheel platform tag vs dylib minos validation ([#177609](https://github.com/pytorch/pytorch/pull/177609), [#177993](https://github.com/pytorch/pytorch/pull/177993))
- Enable Metal-4 shaders offline compilation ([#179378](https://github.com/pytorch/pytorch/pull/179378))
- Migrate lint and other workflows from EC2 to k8s ARC runners (OSDC) ([#177431](https://github.com/pytorch/pytorch/pull/177431), [#177899](https://github.com/pytorch/pytorch/pull/177899), [#177950](https://github.com/pytorch/pytorch/pull/177950), [#177953](https://github.com/pytorch/pytorch/pull/177953), [#177954](https://github.com/pytorch/pytorch/pull/177954), [#178585](https://github.com/pytorch/pytorch/pull/178585), [#178973](https://github.com/pytorch/pytorch/pull/178973), [#179058](https://github.com/pytorch/pytorch/pull/179058))
- Add XPU client docker image and CI tests ([#174188](https://github.com/pytorch/pytorch/pull/174188), [#177831](https://github.com/pytorch/pytorch/pull/177831), [#178380](https://github.com/pytorch/pytorch/pull/178380), [#178383](https://github.com/pytorch/pytorch/pull/178383), [#178143](https://github.com/pytorch/pytorch/pull/178143), [#179786](https://github.com/pytorch/pytorch/pull/179786))
- Merge majority of libtorch builds into wheel CD builds ([#174753](https://github.com/pytorch/pytorch/pull/174753), [#177802](https://github.com/pytorch/pytorch/pull/177802))
- Enable R2/S3 dual upload for torch nightly packages ([#175352](https://github.com/pytorch/pytorch/pull/175352), [#175570](https://github.com/pytorch/pytorch/pull/175570))
### bug fixes
- Fix periodic inductor CI silently skipping all tests ([#177695](https://github.com/pytorch/pytorch/pull/177695))
- Fix python docs build hanging in CI ([#180177](https://github.com/pytorch/pytorch/pull/180177))
- Avoid installing test dll into Windows wheel and fix libuv copy path ([#179024](https://github.com/pytorch/pytorch/pull/179024))
- Fix aarch64 build-osdc using x86 runner on ARC ([#179783](https://github.com/pytorch/pytorch/pull/179783))
### performance
- Add deterministic mode for benchmark perf tests ([#178233](https://github.com/pytorch/pytorch/pull/178233))
- Fix subprocess benchmark crash for addmm with input_reorder ([#177930](https://github.com/pytorch/pytorch/pull/177930))
- Add unbacked perf testing to inductor periodic ([#177034](https://github.com/pytorch/pytorch/pull/177034))
### docs
- Auto-detect missing doc redirects for moved/deleted files ([#173805](https://github.com/pytorch/pytorch/pull/173805))
- Add `.nojekyll` file creation in CPP doc push script ([#179721](https://github.com/pytorch/pytorch/pull/179721))
- Simplify condition for linux-docs job ([#180391](https://github.com/pytorch/pytorch/pull/180391))
### devs
- Update CXX_STANDARD to C++20 across build targets ([#178343](https://github.com/pytorch/pytorch/pull/178343))
- Remove legacy_nvidia_driver code ([#175363](https://github.com/pytorch/pytorch/pull/175363))
- Change default CUDA arch list to sm_7.5 ([#175574](https://github.com/pytorch/pytorch/pull/175574))
- Move binary build scripts from `.circleci/` to `.ci/pytorch/` and clean up old copies ([#175930](https://github.com/pytorch/pytorch/pull/175930), [#175915](https://github.com/pytorch/pytorch/pull/175915), [#175917](https://github.com/pytorch/pytorch/pull/175917))
- Add ARC runner label mapping config and experiment support to runner determinator ([#177803](https://github.com/pytorch/pytorch/pull/177803), [#177804](https://github.com/pytorch/pytorch/pull/177804))
- Use sccache when available for faster builds ([#175556](https://github.com/pytorch/pytorch/pull/175556))
- Standardize ninja installation to PyPI ([#179508](https://github.com/pytorch/pytorch/pull/179508))
- Remove ancient OpenSSL 1.1.1k build ([#179513](https://github.com/pytorch/pytorch/pull/179513))
- Remove stale CentOS-7 references ([#179507](https://github.com/pytorch/pytorch/pull/179507))
- Remove UCC/UCX from Docker builds ([#175607](https://github.com/pytorch/pytorch/pull/175607))
### Untopiced
### not user facing
- [vision hash update] update the pinned vision hash ([#174642](https://github.com/pytorch/pytorch/pull/174642))
- Use treeless checkout in linux build and test workflows ([#172545](https://github.com/pytorch/pytorch/pull/172545))
- Remove Claude Code conclusions from mergeability checks to prevent blocking merges ([#174814](https://github.com/pytorch/pytorch/pull/174814))
- [vision hash update] update the pinned vision hash ([#175214](https://github.com/pytorch/pytorch/pull/175214))
- Update zlib version on RISC-V Docker image ([#175237](https://github.com/pytorch/pytorch/pull/175237))
- Fix TPU test artifacts upload ([#174455](https://github.com/pytorch/pytorch/pull/174455))
- [vision hash update] update the pinned vision hash ([#175296](https://github.com/pytorch/pytorch/pull/175296))
- [CI] Enable HF cache when updating TorchInductor pinned commits ([#175400](https://github.com/pytorch/pytorch/pull/175400))
- [CI] Enable strict mode in vLLM benchmark ([#175399](https://github.com/pytorch/pytorch/pull/175399))
- [xpu][fix][Inductor] Catch Intel Triton compilation/runtime error as IntelGPUError ([#169167](https://github.com/pytorch/pytorch/pull/169167))
- [vision hash update] update the pinned vision hash ([#175465](https://github.com/pytorch/pytorch/pull/175465))
- [CI] Remove unused pytorch-linux-jammy-aarch64-py3.10-clang21 Docker image ([#175457](https://github.com/pytorch/pytorch/pull/175457))
- [audio hash update] update the pinned audio hash ([#175386](https://github.com/pytorch/pytorch/pull/175386))
- Improve inductor-pallas labeler ([#175664](https://github.com/pytorch/pytorch/pull/175664))
- [vllm hash update] update the pinned vllm hash ([#174347](https://github.com/pytorch/pytorch/pull/174347))
- [CI] Modify binaries to use correct GHA workspace ([#174290](https://github.com/pytorch/pytorch/pull/174290))
- Claude code review workflow improvements ([#176027](https://github.com/pytorch/pytorch/pull/176027))
- [vllm hash update] update the pinned vllm hash ([#176036](https://github.com/pytorch/pytorch/pull/176036))
- [Ci][VLLM] Add disabling vllm tests in ci ([#175649](https://github.com/pytorch/pytorch/pull/175649))
- [vllm hash update] update the pinned vllm hash ([#176079](https://github.com/pytorch/pytorch/pull/176079))
- [vllm hash update] update the pinned vllm hash ([#176108](https://github.com/pytorch/pytorch/pull/176108))
- Update core maintainers in merge_rules ([#175977](https://github.com/pytorch/pytorch/pull/175977))
- Make kulinseth and albanD emeritus for MPS/Metal backend ([#176437](https://github.com/pytorch/pytorch/pull/176437))
- [BE] Add error handling to get-changed-files workflow ([#176212](https://github.com/pytorch/pytorch/pull/176212))
- [CI] Remove the "Apply lint suggestions" workflow ([#176189](https://github.com/pytorch/pytorch/pull/176189))
- [Mergerules] Remove `NVFuser` group ([#176301](https://github.com/pytorch/pytorch/pull/176301))
- [MergeRules] Remove dagitses from OSS CI merge rules ([#176302](https://github.com/pytorch/pytorch/pull/176302))
- [MergeRules] Add kurtamohler to MPS rule ([#176304](https://github.com/pytorch/pytorch/pull/176304))
- [ci] Add --compilation-config support to vLLM benchmark workflow ([#175976](https://github.com/pytorch/pytorch/pull/175976))
- [claude code review] Add CONTRIBUTOR role to Claude Code precheck conditions ([#176522](https://github.com/pytorch/pytorch/pull/176522))
- [CI] Disable TRANSFORMERS_OFFLINE for nightly vLLM benchmark runs ([#176553](https://github.com/pytorch/pytorch/pull/176553))
- [vllm hash update] update the pinned vllm hash ([#176242](https://github.com/pytorch/pytorch/pull/176242))
- [claude] Enable pr-review skill for @claude GitHub bot ([#176490](https://github.com/pytorch/pytorch/pull/176490))
- [Fix] Revert support for pull request review comments in Claude Code review workflow ([#176652](https://github.com/pytorch/pytorch/pull/176652))
- [GHF] Update MPS mergerules ([#176654](https://github.com/pytorch/pytorch/pull/176654))
- [CI] Add `apply-lint.yml` workflow ([#176665](https://github.com/pytorch/pytorch/pull/176665))
- [claude] Fix mode detection bug: move prompt to CLAUDE.md ([#176750](https://github.com/pytorch/pytorch/pull/176750))
- Use reusable Claude Code workflow from test-infra ([#176724](https://github.com/pytorch/pytorch/pull/176724))
- [CI] Cache flashinfer cubins on mounted volume in vLLM benchmark ([#176697](https://github.com/pytorch/pytorch/pull/176697))
- [Apply-Lint] Extend it to support ghstack ([#176769](https://github.com/pytorch/pytorch/pull/176769))
- [torchtitan hash update] update the pinned torchtitan hash ([#176768](https://github.com/pytorch/pytorch/pull/176768))
- [torchtitan hash update] update the pinned torchtitan hash ([#176850](https://github.com/pytorch/pytorch/pull/176850))
- AArch64 xFail for failing tests in inductor/test_cpu_repro ([#171095](https://github.com/pytorch/pytorch/pull/171095))
- [BE] Add in-place collect_env execution ([#176904](https://github.com/pytorch/pytorch/pull/176904))
- Update torchbenchmark pin to latest ([#176933](https://github.com/pytorch/pytorch/pull/176933))
- Install `flash-attn-4` and `cutlass_api` w/o `-e` option ([#177150](https://github.com/pytorch/pytorch/pull/177150))
- [CI][CUDA] Add test_fused_attention to have better CuDNN test coverage ([#173965](https://github.com/pytorch/pytorch/pull/173965))
- Revert "[BE] Remove `Optional` and `Union` usage repo wide (#176918)" ([#177184](https://github.com/pytorch/pytorch/pull/177184))
- Reapply "[BE] Remove Optional and Union usage repo wide (#176918)" ([#177314](https://github.com/pytorch/pytorch/pull/177314))
- [BE] Remove Optional and Union usage repo wide ([#176918](https://github.com/pytorch/pytorch/pull/176918))
- [CI] add dtensor workflow ([#177329](https://github.com/pytorch/pytorch/pull/177329))
- [torchtitan hash update] update the pinned torchtitan hash ([#176956](https://github.com/pytorch/pytorch/pull/176956))
- [vllm hash update] update the pinned vllm hash ([#177104](https://github.com/pytorch/pytorch/pull/177104))
- [torchtitan hash update] update the pinned torchtitan hash ([#177464](https://github.com/pytorch/pytorch/pull/177464))
- [Storage] Add swap_data_ptr for safe storage data pointer transfer ([#177449](https://github.com/pytorch/pytorch/pull/177449))
- [CI] Work around H100 FabricManager failure causing multicast failure ([#177472](https://github.com/pytorch/pytorch/pull/177472))
- [vllm hash update] update the pinned vllm hash ([#177465](https://github.com/pytorch/pytorch/pull/177465))
- [torchtitan hash update] update the pinned torchtitan hash ([#177500](https://github.com/pytorch/pytorch/pull/177500))
- [torchtitan hash update] update the pinned torchtitan hash ([#177601](https://github.com/pytorch/pytorch/pull/177601))
- [vllm hash update] update the pinned vllm hash ([#177602](https://github.com/pytorch/pytorch/pull/177602))
- [CI] Disable HF offline mode for nightly scheduled benchmark runs ([#177667](https://github.com/pytorch/pytorch/pull/177667))
- [vision hash update] update the pinned vision hash ([#175593](https://github.com/pytorch/pytorch/pull/175593))
- [torchtitan hash update] update the pinned torchtitan hash ([#177706](https://github.com/pytorch/pytorch/pull/177706))
- [BE][CI] Check for passwordless sudo instead of hardcoding BUILD_ENVIRONMENT exclusions ([#177914](https://github.com/pytorch/pytorch/pull/177914))
- [BE][Docker] Clean up `manywheel/build_scripts` ([#177800](https://github.com/pytorch/pytorch/pull/177800))
- submodule init `third_party/cutlass` in `test_h100_cutlass_backend` ([#177941](https://github.com/pytorch/pytorch/pull/177941))
- [torchtitan hash update] update the pinned torchtitan hash ([#177923](https://github.com/pytorch/pytorch/pull/177923))
- [CI] Clean up runner-determinator: use script directly instead of inline YAML ([#178012](https://github.com/pytorch/pytorch/pull/178012))
- [CI] Add --include-inductor-graph-partition to vllm benchmarking ([#178272](https://github.com/pytorch/pytorch/pull/178272))
- Use official wheels for fa4 ([#178438](https://github.com/pytorch/pytorch/pull/178438))
- [vision hash update] update the pinned vision hash ([#177925](https://github.com/pytorch/pytorch/pull/177925))
- [CI] Update setup-linux to simplify compiler setup ([#178361](https://github.com/pytorch/pytorch/pull/178361))
- [BE] Move some common CI steps to setup-linux ([#178580](https://github.com/pytorch/pytorch/pull/178580))
- [torchtitan hash update] update the pinned torchtitan hash ([#178453](https://github.com/pytorch/pytorch/pull/178453))
- [BE] Cleanup rust installation after sccache build ([#178789](https://github.com/pytorch/pytorch/pull/178789))
- [BE] Clean conda cache before publishing image ([#178790](https://github.com/pytorch/pytorch/pull/178790))
- [Bugfix] Use setup-linux everywhere ([#178831](https://github.com/pytorch/pytorch/pull/178831))
- [BE] When push image to ghcr.io also push a tag without sha suffix ([#178949](https://github.com/pytorch/pytorch/pull/178949))
- [BE] Delete unused linux-test action ([#178994](https://github.com/pytorch/pytorch/pull/178994))
- [CI] Add zip package into CI images ([#178983](https://github.com/pytorch/pytorch/pull/178983))
- [Bugfix] Cleanup setup-python on B200 in _linux-test ([#178832](https://github.com/pytorch/pytorch/pull/178832))
- [BE] Only keep runner mapping used by PyTorch CI ([#178982](https://github.com/pytorch/pytorch/pull/178982))
- [CI] Add git-core PPA to Docker base image for newer git ([#179025](https://github.com/pytorch/pytorch/pull/179025))
- [CI] Purge pip cache after uninstalling nightly torch in ONNX setup ([#179027](https://github.com/pytorch/pytorch/pull/179027))
- [BE] Remove cuda 12.9 from docker. Use linux.arm64.4xlarge for Linux aarch64 cuda builds ([#179158](https://github.com/pytorch/pytorch/pull/179158))
- [BE] Clean up some irregularities in pull workflows ([#179171](https://github.com/pytorch/pytorch/pull/179171))
- Remove cuda 12.9 cd builds ([#179155](https://github.com/pytorch/pytorch/pull/179155))
- Fix FA3 test which currently fails and times out ([#179183](https://github.com/pytorch/pytorch/pull/179183))
- Use full path to GHA in FA3 stable workflow ([#179187](https://github.com/pytorch/pytorch/pull/179187))
- Remove unused pytorch/llvm:9.0.1 from CI Docker images ([#179179](https://github.com/pytorch/pytorch/pull/179179))
- [mergebot] Allow facebook-github-tools bot to issue reverts ([#179108](https://github.com/pytorch/pytorch/pull/179108))
- Remove unused mkl dynamic library package from CI requirements ([#179186](https://github.com/pytorch/pytorch/pull/179186))
- [vision hash update] update the pinned vision hash ([#178838](https://github.com/pytorch/pytorch/pull/178838))
- [audio hash update] update the pinned audio hash ([#178951](https://github.com/pytorch/pytorch/pull/178951))
- [CI] Handle GitHub API error when getting the list of changed files ([#179339](https://github.com/pytorch/pytorch/pull/179339))
- [vllm hash update] update the pinned vllm hash ([#179439](https://github.com/pytorch/pytorch/pull/179439))
- Add append_system_prompt to Claude Code workflow for PR reviews ([#179289](https://github.com/pytorch/pytorch/pull/179289))
- [vllm hash update] update the pinned vllm hash ([#179531](https://github.com/pytorch/pytorch/pull/179531))
- [BE] Create upload-build-artifacts action, mirror download-build-artifacts ([#179612](https://github.com/pytorch/pytorch/pull/179612))
- [CI] Fix use-gha input string truthiness bug in artifact actions ([#179654](https://github.com/pytorch/pytorch/pull/179654))
- Add allowlist.yml file for Cross Repo CI Relay ([#178681](https://github.com/pytorch/pytorch/pull/178681))
- Pin claude-code-action to v1.0.89 to fix Bedrock auth regression ([#179726](https://github.com/pytorch/pytorch/pull/179726))
- [vision hash update] update the pinned vision hash ([#179775](https://github.com/pytorch/pytorch/pull/179775))
- [vllm hash update] update the pinned vllm hash ([#179650](https://github.com/pytorch/pytorch/pull/179650))
- [BE] Clean up duplicated checkout PyTorch step ([#178700](https://github.com/pytorch/pytorch/pull/178700))
- torch_tpu: point to new repo location ([#178811](https://github.com/pytorch/pytorch/pull/178811))
- [retrybot] Add Initialize containers to retryable step names ([#180082](https://github.com/pytorch/pytorch/pull/180082))
- [Dependabot] Update(deps): Bump transformers from 5.2.0 to 5.5.3 in /.ci/docker/ci_commit_pins ([#179913](https://github.com/pytorch/pytorch/pull/179913))
- [CI] Upgrade py3.14t dynamo_wrapped runners to linux.4xlarge to fix OOM ([#180231](https://github.com/pytorch/pytorch/pull/180231))
- [CI] Run torchbench install as jenkins user instead of chowning ([#180180](https://github.com/pytorch/pytorch/pull/180180))
- [vision hash update] update the pinned vision hash ([#179873](https://github.com/pytorch/pytorch/pull/179873))
- [CI] Delete `pch` test workflow ([#175592](https://github.com/pytorch/pytorch/pull/175592))
- [CI] Remove unused Java/JNI detection from CI build script ([#175894](https://github.com/pytorch/pytorch/pull/175894))
- Move dill uninstall from Docker build time to test time ([#179320](https://github.com/pytorch/pytorch/pull/179320))
- Reland D97799113: [CK SDPA] Add CK backend support for varlen attention ([#178729](https://github.com/pytorch/pytorch/pull/178729))
- Bump pillow from 11.0.0 to 12.1.1 in /.ci/docker (ac5db1c0b0e)
- Always checkout submodules on MacOS (fb4f0be3869)
- Fix claude-autorevert-advisor to allow pytorch-auto-revert bot (f4d23bec429)
- Bump requests from 2.32.4 to 2.33.0 in /.github (1c0fd99bc15)
- Bump aiohttp from 3.13.3 to 3.13.4 in /.ci/docker (01f5dbbbd56)
- Update CMake version in Dockerfile to 3.18.4.post1 (d6bd40f6a2a)
- Bump onnx from 1.20.0 to 1.21.0 in /.ci/docker (dfc51cfd414)
- Bump pygments from 2.15.0 to 2.20.0 in /.ci/docker (d58620a11f6)
- Bump uv from 0.9.6 to 0.11.6 in /.ci/lumen_cli (672d6d9b5db)
- Bump pillow from 12.1.1 to 12.2.0 in /.ci/docker (d3f8120e366)
- Bump pytest from 7.3.2 to 9.0.3 in /.ci/lumen_cli (58db28e4140)
### security
- Pin third-party GitHub Actions to SHA and extract unsafe expressions ([#178638](https://github.com/pytorch/pytorch/pull/178638))
