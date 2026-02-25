
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
- [CD] Exclude Volta from CUDA-12.8 and 12.9 builds ([#172598](https://github.com/pytorch/pytorch/pull/172598))
### deprecation
### new features
### improvements
### bug fixes
### performance
### docs
- Fix stable cpp docs rendering ([#171957](https://github.com/pytorch/pytorch/pull/171957))
### devs
- clarify needs repro and edge cases ([#174028](https://github.com/pytorch/pytorch/pull/174028))
### Untopiced
- Bump filelock from 3.18.0 to 3.20.1 in /.ci/docker (df0ac1b506e)
- Add normalization and activation ops to operator benchmarks ([#169544](https://github.com/pytorch/pytorch/pull/169544))
- Add benchmarks for scaled_mm and scaled_grouped_mm ([#170909](https://github.com/pytorch/pytorch/pull/170909))
- Bump aiohttp from 3.13.2 to 3.13.3 in /.ci/docker (3dd897e669a)
- Fix FA3 wheel stats and tests ([#172030](https://github.com/pytorch/pytorch/pull/172030))
- Bump aiohttp from 3.13.2 to 3.13.3 in /.ci/docker (3bfdf85fe5f)
- Bump filelock from 3.20.1 to 3.20.3 in /.ci/docker (75fd1a27b67)
- Build FA3 wheels for linux ([#172654](https://github.com/pytorch/pytorch/pull/172654))
- [FA3 wheel] build cuda 13 x ARM + submodule bump ([#173214](https://github.com/pytorch/pytorch/pull/173214))
- [BE] Enable HF cache on all CI jobs ([#173477](https://github.com/pytorch/pytorch/pull/173477))
- Fix macosx wheel metadata ([#173541](https://github.com/pytorch/pytorch/pull/173541))
- Use an openmp built for macos-11.0 ([#173666](https://github.com/pytorch/pytorch/pull/173666))
- fix wheel name ([#173945](https://github.com/pytorch/pytorch/pull/173945))
- [einops] Don't register einops ops with `allow_in_graph` ([#173611](https://github.com/pytorch/pytorch/pull/173611))
- Bump protobuf from 6.33.2 to 6.33.5 in /.ci/docker (595db20168b)
- [CD] Update xpu support package version to 2025.3.2 ([#173199](https://github.com/pytorch/pytorch/pull/173199))
- clean up FA3 linux build script ([#174206](https://github.com/pytorch/pytorch/pull/174206))
- add env vars to FA3 linux build script ([#174476](https://github.com/pytorch/pytorch/pull/174476))
- [RELEASE 2.11] Release only changes (af5c4ec030d)
- [release-only] Remove +ptx from cuda 13.0 builds (a2813af6564)
### not user facing
- [ROCm][CI] upgrade wheels to 7.1.1 patch release ([#170101](https://github.com/pytorch/pytorch/pull/170101))
- ci: Modify workflows to use new ecr-login action ([#169962](https://github.com/pytorch/pytorch/pull/169962))
- Consolidate NCCL version for different CUDA; 2.28.9 ([#169927](https://github.com/pytorch/pytorch/pull/169927))
- ci: Fix aws-region default in ecr-login action ([#170193](https://github.com/pytorch/pytorch/pull/170193))
- ci: Remove workspace deletion in binary build/test workflows ([#170192](https://github.com/pytorch/pytorch/pull/170192))
- ci: install local dependencies in setup-linux action ([#169968](https://github.com/pytorch/pytorch/pull/169968))
- ci: Revert setup-rocm to not use ecr-login ([#170260](https://github.com/pytorch/pytorch/pull/170260))
- ci: Use uv tool install to install pip ([#170272](https://github.com/pytorch/pytorch/pull/170272))
- ci: Add check-tpu composite action for TPU detection ([#170269](https://github.com/pytorch/pytorch/pull/170269))
- ci: Ensure we pass through TPU env variables (REDO) ([#170270](https://github.com/pytorch/pytorch/pull/170270))
- ci: Fix has_profile check, remove cross-account ([#170267](https://github.com/pytorch/pytorch/pull/170267))
- Unpin patch version of nvidia-cuda-runtime for CUDA 13.0 builds ([#170331](https://github.com/pytorch/pytorch/pull/170331))
- ci: Move upload-test-artifacts to use uv + python ([#169969](https://github.com/pytorch/pytorch/pull/169969))
- ci: Switch everything over to use temp envs + uv ([#170316](https://github.com/pytorch/pytorch/pull/170316))
- Fix GPU_FLAG setting logic on B200  ([#170375](https://github.com/pytorch/pytorch/pull/170375))
- [vllm hash update] update the pinned vllm hash ([#169733](https://github.com/pytorch/pytorch/pull/169733))
- [vllm hash update] update the pinned vllm hash ([#170391](https://github.com/pytorch/pytorch/pull/170391))
- [audio hash update] update the pinned audio hash ([#169795](https://github.com/pytorch/pytorch/pull/169795))
- ci: Try s3 first, fall back to gha for upload-test-artifacts ([#170439](https://github.com/pytorch/pytorch/pull/170439))
- [BE] Cleanup some deprecated steps in _linux-test ([#170377](https://github.com/pytorch/pytorch/pull/170377))
- [CI] Create inductor pallas TPU CI job ([#169776](https://github.com/pytorch/pytorch/pull/169776))
- Instrument trunk and pull wfs (linux) with job and test filtering ([#168201](https://github.com/pytorch/pytorch/pull/168201))
- [cd] Validate Docker release builds only when WITH_PUSH ([#170473](https://github.com/pytorch/pytorch/pull/170473))
- ci: Split out pallas tpu + gpu ([#170478](https://github.com/pytorch/pytorch/pull/170478))
- [audio hash update] update the pinned audio hash ([#170409](https://github.com/pytorch/pytorch/pull/170409))
- [vllm hash update] update the pinned vllm hash ([#170408](https://github.com/pytorch/pytorch/pull/170408))
- assert removal in ci, github, numpy ref, wo, backends, nn and onnx ([#170328](https://github.com/pytorch/pytorch/pull/170328))
- ci: Switch inductor-pallas to autolabel ([#170620](https://github.com/pytorch/pytorch/pull/170620))
- [vllm hash update] update the pinned vllm hash ([#170628](https://github.com/pytorch/pytorch/pull/170628))
- Shorten the file names in libtorch_agnostic tests ([#170664](https://github.com/pytorch/pytorch/pull/170664))
- [CI] Swap TPUs from v6 to v7 ([#170690](https://github.com/pytorch/pytorch/pull/170690))
- [audio hash update] update the pinned audio hash ([#170727](https://github.com/pytorch/pytorch/pull/170727))
- [CI] Enable ecr-login for ROCm workflows ([#170700](https://github.com/pytorch/pytorch/pull/170700))
- [ROCm][CI] Remove MI300 docker image caching ([#170793](https://github.com/pytorch/pytorch/pull/170793))
- [ROCm][CI] Remove ciflow/rocm and ciflow/inductor-rocm triggers ([#170797](https://github.com/pytorch/pytorch/pull/170797))
- [vllm hash update] update the pinned vllm hash ([#170725](https://github.com/pytorch/pytorch/pull/170725))
- Update triton 3.6 to include  triton-lang/triton#8959 ([#170712](https://github.com/pytorch/pytorch/pull/170712))
- [ROCM][CI] Update ECR login action to use pytorch repository ([#170879](https://github.com/pytorch/pytorch/pull/170879))
- [vision hash update] update the pinned vision hash ([#170833](https://github.com/pytorch/pytorch/pull/170833))
- [audio hash update] update the pinned audio hash ([#170966](https://github.com/pytorch/pytorch/pull/170966))
- [vllm hash update] update the pinned vllm hash ([#170925](https://github.com/pytorch/pytorch/pull/170925))
- [xla hash update] update the pinned xla hash ([#170422](https://github.com/pytorch/pytorch/pull/170422))
- Remove concurrency limits in workflows for workflow_dispatches ([#171132](https://github.com/pytorch/pytorch/pull/171132))
- Update triton 3.6 to latest ([#171115](https://github.com/pytorch/pytorch/pull/171115))
- [vllm hash update] update the pinned vllm hash ([#171009](https://github.com/pytorch/pytorch/pull/171009))
- Setup vLLM benchmark ([#170466](https://github.com/pytorch/pytorch/pull/170466))
- Use r7i for debug-build job ([#170213](https://github.com/pytorch/pytorch/pull/170213))
- [CI] Update job-filter dependencies for cross-compile-linux-test job ([#171166](https://github.com/pytorch/pytorch/pull/171166))
- Use c7i.2xlarge for RISC64 build ([#168094](https://github.com/pytorch/pytorch/pull/168094))
- Switch ASAN build to c7i.4xlarge ([#170219](https://github.com/pytorch/pytorch/pull/170219))
- [vllm hash update] update the pinned vllm hash ([#171146](https://github.com/pytorch/pytorch/pull/171146))
- Set a separate build env for each inductor build ([#171197](https://github.com/pytorch/pytorch/pull/171197))
- [vLLM] Fail the benchmark when there is no results ([#171155](https://github.com/pytorch/pytorch/pull/171155))
- [vllm hash update] update the pinned vllm hash ([#171281](https://github.com/pytorch/pytorch/pull/171281))
- [vllm hash update] update the pinned vllm hash ([#171431](https://github.com/pytorch/pytorch/pull/171431))
- Enable test_utils for CI test on linux aarch64 ([#170447](https://github.com/pytorch/pytorch/pull/170447))
- [vllm hash update] update the pinned vllm hash ([#171491](https://github.com/pytorch/pytorch/pull/171491))
- Bump torchbench version ([#171490](https://github.com/pytorch/pytorch/pull/171490))
- [vllm hash update] update the pinned vllm hash ([#171557](https://github.com/pytorch/pytorch/pull/171557))
- Assert in github, docs, setup and top ([#170598](https://github.com/pytorch/pytorch/pull/170598))
- [vllm hash update] update the pinned vllm hash ([#171589](https://github.com/pytorch/pytorch/pull/171589))
- [vision hash update] update the pinned vision hash ([#171757](https://github.com/pytorch/pytorch/pull/171757))
- [CD] Update CuDNN version to 9.15 for 12.9 builds ([#171793](https://github.com/pytorch/pytorch/pull/171793))
- [vLLM] Run PyTorch x vLLM compilation unit tests on B200 ([#171426](https://github.com/pytorch/pytorch/pull/171426))
- [vllm hash update] update the pinned vllm hash ([#171841](https://github.com/pytorch/pytorch/pull/171841))
- Upgrade submodule oneDNN to v3.10.2 ([#165887](https://github.com/pytorch/pytorch/pull/165887))
- [vllm hash update] update the pinned vllm hash ([#171946](https://github.com/pytorch/pytorch/pull/171946))
- [audio hash update] update the pinned audio hash ([#171658](https://github.com/pytorch/pytorch/pull/171658))
- [vllm hash update] update the pinned vllm hash ([#172043](https://github.com/pytorch/pytorch/pull/172043))
- [CI] Run slow tests during MPS shard run ([#172052](https://github.com/pytorch/pytorch/pull/172052))
- [AMD] Bump magma library revision for fix cholesky API, part 1 ([#172083](https://github.com/pytorch/pytorch/pull/172083))
- [ROCm][AMD] Bump magma library revision for fix cholesky API, part 2 (#172083) ([#172112](https://github.com/pytorch/pytorch/pull/172112))
- [vllm hash update] update the pinned vllm hash ([#172151](https://github.com/pytorch/pytorch/pull/172151))
- [ROCm] Increase the timeout value for ops microbenchmark ([#172158](https://github.com/pytorch/pytorch/pull/172158))
- [BE] Remove libstdcxx conda-forge hack from Docker builds ([#172260](https://github.com/pytorch/pytorch/pull/172260))
- [DTensor] Automatically set release_notes label ([#172121](https://github.com/pytorch/pytorch/pull/172121))
- [vllm hash update] update the pinned vllm hash ([#172175](https://github.com/pytorch/pytorch/pull/172175))
- docker build disable ucc cpp warning ([#172279](https://github.com/pytorch/pytorch/pull/172279))
- [Reland] FBGEMM_GENAI -> MSLK ([#172224](https://github.com/pytorch/pytorch/pull/172224))
- Add docs preview for cpp docs built with ciflow/nightly (doxygen-enabled) ([#172120](https://github.com/pytorch/pytorch/pull/172120))
- [vLLM] Retry vLLM tests with a delay ([#172323](https://github.com/pytorch/pytorch/pull/172323))
- ci: Use buildx directly ([#172243](https://github.com/pytorch/pytorch/pull/172243))
- [xpu][feature] Enable BHSD layout and add deterministic check for SDPA XPU FlashAttention backend ([#170414](https://github.com/pytorch/pytorch/pull/170414))
- ci: Give root the ability to run apt ([#172244](https://github.com/pytorch/pytorch/pull/172244))
- [vllm hash update] update the pinned vllm hash ([#172291](https://github.com/pytorch/pytorch/pull/172291))
- [CI] Run unit tests for XPU without timeout ([#171968](https://github.com/pytorch/pytorch/pull/171968))
- Skip broken BW compat test in our fa3 smoke tests ([#172452](https://github.com/pytorch/pytorch/pull/172452))
- Update tlparse instructions in  pt2 bug report template  ([#172392](https://github.com/pytorch/pytorch/pull/172392))
- Redirect setup ([#172035](https://github.com/pytorch/pytorch/pull/172035))
- [vision hash update] update the pinned vision hash ([#171842](https://github.com/pytorch/pytorch/pull/171842))
- [vllm hash update] update the pinned vllm hash ([#172518](https://github.com/pytorch/pytorch/pull/172518))
- Fix libuv build error in windows-arm64-build-test. ([#172203](https://github.com/pytorch/pytorch/pull/172203))
- [CD] Update smoke test, enable torch compile testing for py 3.14 and 3.14t ([#172656](https://github.com/pytorch/pytorch/pull/172656))
- Add Claude Code GitHub Action workflow configuration ([#172686](https://github.com/pytorch/pytorch/pull/172686))
- ultrathink ([#172691](https://github.com/pytorch/pytorch/pull/172691))
- fix ultrathink ([#172698](https://github.com/pytorch/pytorch/pull/172698))
- [ci] Unpin python ([#169907](https://github.com/pytorch/pytorch/pull/169907))
- [EZ] Update CuDNN to 9.15.1 for CUDA-12.8 binary builds ([#172680](https://github.com/pytorch/pytorch/pull/172680))
- [vllm hash update] update the pinned vllm hash ([#172695](https://github.com/pytorch/pytorch/pull/172695))
- [vllm hash update] update the pinned vllm hash ([#172749](https://github.com/pytorch/pytorch/pull/172749))
- [vLLM] Fail the benchmark when the results are all zero ([#172616](https://github.com/pytorch/pytorch/pull/172616))
- [CI] Remove ninja version pin from test.sh ([#172817](https://github.com/pytorch/pytorch/pull/172817))
- [BE][CI] Remove explicit uv install from lintrunner.sh ([#172920](https://github.com/pytorch/pytorch/pull/172920))
- ci: Use test-infra setup-uv wrapper ([#172974](https://github.com/pytorch/pytorch/pull/172974))
- [CI] Collect eager performance when benchmarking vLLM ([#172979](https://github.com/pytorch/pytorch/pull/172979))
- Enable triggering s390x nightly wheels build with ciflow/s390x label ([#172983](https://github.com/pytorch/pytorch/pull/172983))
- [ROCm][CI] create ROCm7.2 images with no magma - 1/N ([#173096](https://github.com/pytorch/pytorch/pull/173096))
- Bump transformers to 4.57.5 ([#172996](https://github.com/pytorch/pytorch/pull/172996))
- [ROCm][CI] Create ROCm 7.2 magma tarball - 2/N ([#173106](https://github.com/pytorch/pytorch/pull/173106))
- [vllm hash update] update the pinned vllm hash ([#172800](https://github.com/pytorch/pytorch/pull/172800))
- [vLLM] Install deep_gemm ([#172412](https://github.com/pytorch/pytorch/pull/172412))
- [ROCm][CI] create ROCm 7.2 images for binary builds - 3/N ([#173187](https://github.com/pytorch/pytorch/pull/173187))
- [CLAUDE]Add nice error message for forked repos ([#172963](https://github.com/pytorch/pytorch/pull/172963))
- Label PRs With Reviewers with triaged ([#172676](https://github.com/pytorch/pytorch/pull/172676))
- Update torchao pinned commit ([#172410](https://github.com/pytorch/pytorch/pull/172410))
- [vision hash update] update the pinned vision hash ([#173124](https://github.com/pytorch/pytorch/pull/173124))
- [audio hash update] update the pinned audio hash ([#173022](https://github.com/pytorch/pytorch/pull/173022))
- [vllm hash update] update the pinned vllm hash ([#173230](https://github.com/pytorch/pytorch/pull/173230))
- [ROCm][CI] Enable upload of S3 artifacts for inductor-perf-nightly-rocm* workflows ([#171468](https://github.com/pytorch/pytorch/pull/171468))
- Add cu130 to flash attention 3 upload ([#173398](https://github.com/pytorch/pytorch/pull/173398))
- Fix forked pr merges skips ([#173400](https://github.com/pytorch/pytorch/pull/173400))
- Run vLLM jobs in HF offline mode by default ([#172300](https://github.com/pytorch/pytorch/pull/172300))
- [ROCm][CI] Use MI350 test runners ([#173407](https://github.com/pytorch/pytorch/pull/173407))
- Add action to upload claude code action usage metrics ([#173418](https://github.com/pytorch/pytorch/pull/173418))
- [CLAUDE BOT] respond to autorevert inquiries ([#173422](https://github.com/pytorch/pytorch/pull/173422))
- Delete check-labels workflow ([#173445](https://github.com/pytorch/pytorch/pull/173445))
- [CI] Change xpu ci test with long time support driver ([#172820](https://github.com/pytorch/pytorch/pull/172820))
- [vllm hash update] update the pinned vllm hash ([#173305](https://github.com/pytorch/pytorch/pull/173305))
- [ROCm][CI] Enable permission change step for gfx950 runners ([#173503](https://github.com/pytorch/pytorch/pull/173503))
- Disable ROCM jobs on trunk ([#173573](https://github.com/pytorch/pytorch/pull/173573))
- [BE] Delete unused `centos-rocm` ([#173587](https://github.com/pytorch/pytorch/pull/173587))
- [BE] Remove Python-2.6.9 copy-pasta ([#173588](https://github.com/pytorch/pytorch/pull/173588))
- [audio hash update] update the pinned audio hash ([#173457](https://github.com/pytorch/pytorch/pull/173457))
- [vision hash update] update the pinned vision hash ([#173595](https://github.com/pytorch/pytorch/pull/173595))
- [vllm hash update] update the pinned vllm hash ([#173594](https://github.com/pytorch/pytorch/pull/173594))
- [BE] Update XPU installation scripts for Linux CICD ([#173507](https://github.com/pytorch/pytorch/pull/173507))
- Add treeless checkout ability to checkout-pytorch ([#172544](https://github.com/pytorch/pytorch/pull/172544))
- Add py3.14t to ci ([#167407](https://github.com/pytorch/pytorch/pull/167407))
- [CI] Optimize the inductor CPU test jobs ([#169038](https://github.com/pytorch/pytorch/pull/169038))
- Use spin in ci ([#169374](https://github.com/pytorch/pytorch/pull/169374))
- Add myself (jane) to be able to try claude code on GH ([#173674](https://github.com/pytorch/pytorch/pull/173674))
- Add auto triage claude workflow ([#173530](https://github.com/pytorch/pytorch/pull/173530))
- [CI] Bump jax version ([#173403](https://github.com/pytorch/pytorch/pull/173403))
- Ai policy and template updates ([#173670](https://github.com/pytorch/pytorch/pull/173670))
- remove assert in hop and trymerge script ([#172480](https://github.com/pytorch/pytorch/pull/172480))
- Allow claude bot react to bot queries ([#173819](https://github.com/pytorch/pytorch/pull/173819))
- [ROCm][CI] Update ROCm CI to MI350 runners ([#173209](https://github.com/pytorch/pytorch/pull/173209))
- Enable support for fork PRs in Claude Code GitHub Action ([#173748](https://github.com/pytorch/pytorch/pull/173748))
- Add two stage flow to fix OSS issues ([#173725](https://github.com/pytorch/pytorch/pull/173725))
- [vision hash update] update the pinned vision hash ([#173875](https://github.com/pytorch/pytorch/pull/173875))
- [vllm hash update] update the pinned vllm hash ([#173874](https://github.com/pytorch/pytorch/pull/173874))
- [smoke_test] Add option to test only torch+torchvision ([#173925](https://github.com/pytorch/pytorch/pull/173925))
- Remove duplicate Jinja2 requirement in CI dependencies ([#173919](https://github.com/pytorch/pytorch/pull/173919))
- build FA3 wheels for Windows ([#173564](https://github.com/pytorch/pytorch/pull/173564))
- remove pr trigger ([#173963](https://github.com/pytorch/pytorch/pull/173963))
- Rename FA3 wheel workflow files to begin with _binary ([#173973](https://github.com/pytorch/pytorch/pull/173973))
- [BE] Setup HF cache for vLLM benchmark ([#173609](https://github.com/pytorch/pytorch/pull/173609))
- [ROCm][CI] Enable pre- and post-merge `default` and `distributed` config ROCm CI jobs on trunk.yml ([#170294](https://github.com/pytorch/pytorch/pull/170294))
- [vision hash update] update the pinned vision hash ([#174022](https://github.com/pytorch/pytorch/pull/174022))
- Adds SherlockNoMad to the list of allowed claudebot users ([#174139](https://github.com/pytorch/pytorch/pull/174139))
- [BE] Cleanup windows CUDA, CPU, XPU builds scripts ([#174236](https://github.com/pytorch/pytorch/pull/174236))
- [vllm hash update] update the pinned vllm hash ([#174004](https://github.com/pytorch/pytorch/pull/174004))
- [CI] Update onnxscript version to 0.6.0 ([#173828](https://github.com/pytorch/pytorch/pull/173828))
- Upgrade NCCL to 2.29.3 ([#174338](https://github.com/pytorch/pytorch/pull/174338))
- Update auto_request_review.yml ([#174118](https://github.com/pytorch/pytorch/pull/174118))
- Add new users to Claude workflow condition ([#174429](https://github.com/pytorch/pytorch/pull/174429))
- Use cuda-toolkit for multiple linux cuda packages ([#174390](https://github.com/pytorch/pytorch/pull/174390))
- [ROCm] Create ROCm7.2 binaries - 5/N ([#174234](https://github.com/pytorch/pytorch/pull/174234))
- [vision hash update] update the pinned vision hash ([#174349](https://github.com/pytorch/pytorch/pull/174349))
- [Pallas TPU] Configure CI for TPU mahcines. ([#173870](https://github.com/pytorch/pytorch/pull/173870))
- clean up windows fa3 build script ([#174294](https://github.com/pytorch/pytorch/pull/174294))
- Pin setuptools<82 to fix pkg_resources removal breakage ([#174631](https://github.com/pytorch/pytorch/pull/174631))
- [BE] Update pandas version for python-3.12 to 2.2.3 ([#174634](https://github.com/pytorch/pytorch/pull/174634))
- bump commit hash for FA3 windows build ([#174656](https://github.com/pytorch/pytorch/pull/174656))
- [Pallas TPU] Bump up the version of TorchTpu used in Torch CI. ([#174705](https://github.com/pytorch/pytorch/pull/174705))
- [CD] update ocloc patch version on Windows ([#174744](https://github.com/pytorch/pytorch/pull/174744))
- Add Natalia and make list easier to read ([#174841](https://github.com/pytorch/pytorch/pull/174841))
- [ROCm][CI] install patched libdrm for updated amdgpu.ids file ([#174811](https://github.com/pytorch/pytorch/pull/174811))
- copy FA3 wheels to CUDA minor version subfolders ([#174803](https://github.com/pytorch/pytorch/pull/174803))
- Manually revert #174338 ([#174838](https://github.com/pytorch/pytorch/pull/174838))
- [ONNX] Use OpSignature from onnx_ir ([#174740](https://github.com/pytorch/pytorch/pull/174740))
- Add fp16/bf16 dtype to Conv3d benchmark ([#172884](https://github.com/pytorch/pytorch/pull/172884))
- Add myself to claude review list ([#174973](https://github.com/pytorch/pytorch/pull/174973))
- Move upload FA3 job to a separate workflow ([#174975](https://github.com/pytorch/pytorch/pull/174975))
- Update pytorch_sphinx_theme2 version to 0.4.3 ([#174806](https://github.com/pytorch/pytorch/pull/174806))
- [xpu][feature][FlexAttention] Enable tensor descriptor for FlexAttention backward ([#166927](https://github.com/pytorch/pytorch/pull/166927))
- Add Github Secret Token to Upload FA3 Wheels Job ([#175009](https://github.com/pytorch/pytorch/pull/175009))
- [pallas backend] Use native tensor allocation on the TPU ([#175007](https://github.com/pytorch/pytorch/pull/175007))
- Update merge rule for Accelerator ([#174962](https://github.com/pytorch/pytorch/pull/174962))
- Pin setuptools<82 in inductor benchmark docker build ([#175035](https://github.com/pytorch/pytorch/pull/175035))
- Fix macOS arm64 libtorch release upload failure ([#175100](https://github.com/pytorch/pytorch/pull/175100))
- [CI] Move CUDA 12.8 GPU tests from per-commit trunk to periodic ([#175067](https://github.com/pytorch/pytorch/pull/175067))
- [BE] Remove cuda 12.4 periodic tests ([#175170](https://github.com/pytorch/pytorch/pull/175170))
- [CI] Add CUDA 13 periodic tests ([#174850](https://github.com/pytorch/pytorch/pull/174850))
### security
