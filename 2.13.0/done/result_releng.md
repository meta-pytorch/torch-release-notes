
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
- Bazel build support has been removed ([#180883](https://github.com/pytorch/pytorch/pull/180883))

  The Bazel build was never broadly adopted and still depended on the antiquated Bazel 6,
  while the wider ecosystem has since moved to Bazel 9. All Bazel build files and CI jobs have
  been removed. Users building PyTorch with Bazel should migrate to the supported CMake/`pip install`
  build flow.

  Version 2.12:
  ```bash
  # Build PyTorch with Bazel
  bazel build //:torch
  ```

  Version 2.13:
  ```bash
  # Bazel build files have been removed; build from source with pip instead
  pip install --no-build-isolation -e .
  ```

- CPython 3.13t (free-threaded) binaries are no longer built ([#182951](https://github.com/pytorch/pytorch/pull/182951))

  Upstream `pypa/manylinux` removed CPython 3.13t (free-threaded) on 2026-05-07, because 3.13t
  was experimental and has been superseded by the now-non-experimental CPython 3.14t. As a result,
  PyTorch 2.13 no longer ships `cp313t` wheels (Linux, Triton, and related artifacts). Users on the
  free-threaded interpreter should move to Python 3.14t.

  Version 2.12:
  ```bash
  # cp313t (free-threaded 3.13) wheels were available
  python3.13t -m pip install torch
  ```

  Version 2.13:
  ```bash
  # Use free-threaded Python 3.14t instead
  python3.14t -m pip install torch
  ```

### deprecation
### new features
- Add Python 3.15 wheel builds across Linux (CPU/CUDA), Triton, ROCm, and XPU ([#182954](https://github.com/pytorch/pytorch/pull/182954), [#184600](https://github.com/pytorch/pytorch/pull/184600), [#185409](https://github.com/pytorch/pytorch/pull/185409), [#184829](https://github.com/pytorch/pytorch/pull/184829), [#184891](https://github.com/pytorch/pytorch/pull/184891), [#184906](https://github.com/pytorch/pytorch/pull/184906), [#185094](https://github.com/pytorch/pytorch/pull/185094))
### improvements
- CUDA Linux wheels are now always built as "small wheels" that depend on the NVIDIA CUDA pip packages instead of bundling the CUDA shared libraries, and the unused CUDA 12.8/12.9 build paths were removed ([#180612](https://github.com/pytorch/pytorch/pull/180612))
- Remove the bundled `ptxas` from CUDA 13 binaries now that the upstream Triton fix has landed, reducing wheel size ([#174716](https://github.com/pytorch/pytorch/pull/174716))
- Upgrade ROCm CI/CD images to 7.2.3 ([#181288](https://github.com/pytorch/pytorch/pull/181288))
- Move the NCCL pin to 2.30 ([#181313](https://github.com/pytorch/pytorch/pull/181313))
- Advance the Triton pin to 3.7.1 ([#181001](https://github.com/pytorch/pytorch/pull/181001), [#186792](https://github.com/pytorch/pytorch/pull/186792))
- Upgrade the XPU support package to 2026.0 ([#182003](https://github.com/pytorch/pytorch/pull/182003))
- Add a configurable threshold to avoid power-of-two rounding for large pinned memory allocations ([#171662](https://github.com/pytorch/pytorch/pull/171662))
### bug fixes
### performance
- Add an operator microbenchmark comparison workflow for PRs ([#179476](https://github.com/pytorch/pytorch/pull/179476))
- Add a batch-invariant accuracy mode for benchmark perf tests ([#180610](https://github.com/pytorch/pytorch/pull/180610))
### docs
### devs
- Migrate the build to CMake / scikit-build-core: move NCCL checkout, source-file mirroring, header wrapping, `compile_commands` merging, and the `torch._C` extension/`version.py` build out of `setup.py` and into CMake ([#181450](https://github.com/pytorch/pytorch/pull/181450), [#177642](https://github.com/pytorch/pytorch/pull/177642), [#177643](https://github.com/pytorch/pytorch/pull/177643), [#177644](https://github.com/pytorch/pytorch/pull/177644), [#180243](https://github.com/pytorch/pytorch/pull/180243))
- Drop the setuptools `concat_license_files` hook and adopt PEP 639 `license-files`; replace deprecated `distutils` usage ([#180237](https://github.com/pytorch/pytorch/pull/180237), [#182120](https://github.com/pytorch/pytorch/pull/182120))
- Install `libaotriton_v2.so` via cmake install for wheel packaging ([#180242](https://github.com/pytorch/pytorch/pull/180242))
- Embed the macOS OpenMP runtime in `PostBuildSteps` ([#180239](https://github.com/pytorch/pytorch/pull/180239))
### not user facing
- Remove unused noqa directives in non-torch/, batch 1 ([#180140](https://github.com/pytorch/pytorch/pull/180140))
- [CI] Remove runtime Chocolatey installs from Windows CI (3a893377d9a)
- Bump lxml from 6.0.2 to 6.1.0 in /.ci/docker (75b947d3fc8)
- [Dependabot] Update(deps): Bump transformers from 5.5.3 to 5.6.1 in /.ci/docker/ci_commit_pins (8d595a30550)
- [BE][Docs] Error out rather than hang if workflow is missing credentials ([#181433](https://github.com/pytorch/pytorch/pull/181433))
- Revert "Change runner to linux.12xlarge for nightly doc push (#181256)" ([#181459](https://github.com/pytorch/pytorch/pull/181459))
- Bump gitpython from 3.1.45 to 3.1.47 in /.ci/lumen_cli (a528959cac4)
- [Dependabot] Update(deps): Bump transformers from 5.6.1 to 5.7.0 in /.ci/docker/ci_commit_pins (2a1f7f19f28)
- Bump pytest from 7.3.2 to 9.0.3 in /.ci/docker (2ddaba93ea0)
- [CD] Refactor manywheel build scripts (split env setup, deps, wheel, repair) ([#182409](https://github.com/pytorch/pytorch/pull/182409))
- Update FA3 wheel to be the official cuda 13 variant ([#182695](https://github.com/pytorch/pytorch/pull/182695))
- Bump gitpython from 3.1.47 to 3.1.50 in /.ci/lumen_cli (142a2f2542c)
- [CD] Port XPU manywheel build to the Python pipeline ([#182942](https://github.com/pytorch/pytorch/pull/182942))
- [CD] Port ROCm manywheel build to the Python pipeline ([#182696](https://github.com/pytorch/pytorch/pull/182696))
- [ci] Fix tlparse artifact collection and enable torch trace on A100/B200 perf jobs ([#183340](https://github.com/pytorch/pytorch/pull/183340))
- Bump pip from 26.0.1 to 26.1 in /.ci/docker (95e38306137)
- Update vllm pin and rename test_llm_with_multi_loras ([#183846](https://github.com/pytorch/pytorch/pull/183846))
- Add basic pyrefly infer command ([#173647](https://github.com/pytorch/pytorch/pull/173647))
- [CD] Raise timeout for x86 cuda builds to 280 mins ([#185560](https://github.com/pytorch/pytorch/pull/185560))
- torchtitan: track CUDA_STABLE for build/test env and nightly wheel channel ([#186014](https://github.com/pytorch/pytorch/pull/186014))
- Remove references to torch_tpu.api ([#186083](https://github.com/pytorch/pytorch/pull/186083))
- Use normalized name spmd-types in wheel Requires-Dist ([#186545](https://github.com/pytorch/pytorch/pull/186545))
- Disable custom op aliasing errors for vLLM CI ([#184638](https://github.com/pytorch/pytorch/pull/184638))
- Remove XNNPACK availability check from binary smoke test ([#186662](https://github.com/pytorch/pytorch/pull/186662))
- [Dependabot] Update(deps): Bump transformers from 5.9.0 to 5.10.1 in /.ci/docker/ci_commit_pins (34ccd6b3cbe)
- update spmd_types to 0.2.1 ([#186803](https://github.com/pytorch/pytorch/pull/186803))
- [Dependabot] Update(deps): Bump transformers from 5.7.0 to 5.9.0 in /.ci/docker/ci_commit_pins (696ebd85f52)
- [release 2.13] Apply Release only changes to 2.13 branch (1f706b96385)
- [release 2.13] Remove docker image pinning from s390x manywheel builds (da8ca4eb91c)
- Fetch tags in unified manywheel build job so release tags are detected (d7a7b7d02c2)
- [AArch64][CI]Add m8g as an option for nightly Inductor benchmark instances for AArch64 ([#174100](https://github.com/pytorch/pytorch/pull/174100))
- [CI] Fix checkout path conflict in TD indexer workflow ([#180476](https://github.com/pytorch/pytorch/pull/180476))
- [runner_determinator] Support per-user rollout percentage for runner experiments ([#180510](https://github.com/pytorch/pytorch/pull/180510))
- [vision hash update] update the pinned vision hash ([#180517](https://github.com/pytorch/pytorch/pull/180517))
- [BE] Skip submodule checkout in docker image build workflows ([#180572](https://github.com/pytorch/pytorch/pull/180572))
- Add the new accelerator (Ascend NPU) to allowlist.yml ([#180352](https://github.com/pytorch/pytorch/pull/180352))
- Fix libtorch build writing outside workspace ([#180598](https://github.com/pytorch/pytorch/pull/180598))
- [CI] Align vLLM wheel build CUDA versions with PyTorch nightly ([#180607](https://github.com/pytorch/pytorch/pull/180607))
- [OSDC] Enable trunk workflow on OSDC runners ([#180537](https://github.com/pytorch/pytorch/pull/180537))
- Fix GDS smoke test failure on CUDA 13.2 ([#180577](https://github.com/pytorch/pytorch/pull/180577))
- Correct the Repo Name in allowlist.yaml ([#180794](https://github.com/pytorch/pytorch/pull/180794))
- [CI] Fix target-determination-indexer pytorch checkout path ([#180711](https://github.com/pytorch/pytorch/pull/180711))
- [ROCm][CI] Modify permissions in nightly workflow ([#180877](https://github.com/pytorch/pytorch/pull/180877))
- Allow pytorch-bot to trigger Claude Autorevert Advisor workflow ([#180932](https://github.com/pytorch/pytorch/pull/180932))
- [RISCV] disable cuda-bingings on riscv64 CI ([#173663](https://github.com/pytorch/pytorch/pull/173663))
- [CI] Use portable jemalloc path lookup in build.sh ([#180983](https://github.com/pytorch/pytorch/pull/180983))
- [vllm hash update] update the pinned vllm hash ([#180516](https://github.com/pytorch/pytorch/pull/180516))
- [ROCm][CI] Use env vars and clean up docker-cache-rocm.yml ([#180710](https://github.com/pytorch/pytorch/pull/180710))
- [s390x CI] Disable scheduled s390x-periodic runs ([#181005](https://github.com/pytorch/pytorch/pull/181005))
- [vllm hash update] update the pinned vllm hash ([#181048](https://github.com/pytorch/pytorch/pull/181048))
- [Benchmark] Fix xpu benchmark workflow issue ([#180825](https://github.com/pytorch/pytorch/pull/180825))
- [BE] Make macos_binary_build_workflow.yml use matrix ([#181153](https://github.com/pytorch/pytorch/pull/181153))
- [ROCm][CI] Update permissions in rocm-mi200.yml for build-osdc step ([#180755](https://github.com/pytorch/pytorch/pull/180755))
- [vision hash update] update the pinned vision hash ([#181049](https://github.com/pytorch/pytorch/pull/181049))
- [vllm hash update] update the pinned vllm hash ([#181197](https://github.com/pytorch/pytorch/pull/181197))
- [BE] Drop unused CUDA 12.8 and ROCm 7.0 Docker image builds ([#181273](https://github.com/pytorch/pytorch/pull/181273))
- trymerge: allowlist facebook-github-tools for skip_internal_checks ([#181246](https://github.com/pytorch/pytorch/pull/181246))
- [BE] Use sparse checkout for runner-determinator job ([#181311](https://github.com/pytorch/pytorch/pull/181311))
- [BE] Build all macOS Python wheels on a single runner ([#181171](https://github.com/pytorch/pytorch/pull/181171))
- [BE] Add sparse-checkout input to checkout-pytorch action ([#181317](https://github.com/pytorch/pytorch/pull/181317))
- [BE] Use sparse checkout for binary upload job ([#181312](https://github.com/pytorch/pytorch/pull/181312))
- Temporarily disable XPU workflow on pull ([#181408](https://github.com/pytorch/pytorch/pull/181408))
- Allow more time and bigger runner for docs workflow ([#181427](https://github.com/pytorch/pytorch/pull/181427))
- Change runner to linux.12xlarge for nightly doc push ([#181256](https://github.com/pytorch/pytorch/pull/181256))
- Use full clone for docs build to fix nightly hang ([#181456](https://github.com/pytorch/pytorch/pull/181456))
- [CI] Migrate 12.8 CI jobs to 13.0 ([#180052](https://github.com/pytorch/pytorch/pull/180052))
- Reenable XPU workflows ([#181437](https://github.com/pytorch/pytorch/pull/181437))
- mergebot: identify failing PR in ghstack merge rule errors ([#181506](https://github.com/pytorch/pytorch/pull/181506))
- [docs] Use nproc instead of -j auto so worker count respects cgroups ([#181543](https://github.com/pytorch/pytorch/pull/181543))
- [vision hash update] update the pinned vision hash ([#181315](https://github.com/pytorch/pytorch/pull/181315))
- [vllm hash update] update the pinned vllm hash ([#181316](https://github.com/pytorch/pytorch/pull/181316))
- [xla hash update] update the pinned xla hash ([#181558](https://github.com/pytorch/pytorch/pull/181558))
- Migrate smoke test on B200 to OSDC ([#181544](https://github.com/pytorch/pytorch/pull/181544))
- [ROCm][CI] Add distributed and inductor test configs to rocm-nightly ([#179628](https://github.com/pytorch/pytorch/pull/179628))
- [CI] Restrict mkl installation to x86 systems only ([#178778](https://github.com/pytorch/pytorch/pull/178778))
- [BE] Slim Jinja templates: render matrix-driven binary workflows ([#181586](https://github.com/pytorch/pytorch/pull/181586))
- Bump pytest to 9.0.3 without breaking the host Python 3.9 install ([#181668](https://github.com/pytorch/pytorch/pull/181668))
- Add riseproject-dev/pytorch as L1 cross repo CI relay ([#181739](https://github.com/pytorch/pytorch/pull/181739))
- ci: add torchcomms to distributed CI ([#181662](https://github.com/pytorch/pytorch/pull/181662))
- [xpu][fix] Skip test_device_capability_supported_dtypes on XPU ([#180660](https://github.com/pytorch/pytorch/pull/180660))
- [vllm hash update] update the pinned vllm hash ([#181679](https://github.com/pytorch/pytorch/pull/181679))
- Use container: directive for linux binary build/test workflows ([#181599](https://github.com/pytorch/pytorch/pull/181599))
- [OSDC]Migrate slow.yml jobs to OSDC (ARC) via dial-up pattern ([#181799](https://github.com/pytorch/pytorch/pull/181799))
- [BE] Unify s390x and other linux binary build/test workflows ([#182018](https://github.com/pytorch/pytorch/pull/182018))
- Update assigntome-docathon.yml for 2026 Docathon ([#181264](https://github.com/pytorch/pytorch/pull/181264))
- [MergeRules] Make Metamates group explicit ([#176303](https://github.com/pytorch/pytorch/pull/176303))
- Fix NumPy 2.0 `np.string_` removal in test_monitor and test_tensorboard and unskip test_writer ([#168252](https://github.com/pytorch/pytorch/pull/168252))
- Update label check for docathon-2026 ([#182128](https://github.com/pytorch/pytorch/pull/182128))
- [OSDC]Migrate nightly.yml docs-build to OSDC (ARC) via dial-up pattern ([#181802](https://github.com/pytorch/pytorch/pull/181802))
- Reset .ci/docker tree to known good Docker configuration ([#182305](https://github.com/pytorch/pytorch/pull/182305))
- Fwd fix linter after revert ([#182309](https://github.com/pytorch/pytorch/pull/182309))
- [MergeBot] Add negative patterns ([#182322](https://github.com/pytorch/pytorch/pull/182322))
- [CD] Restore 420-minute timeout for ROCm linux manywheel builds ([#182335](https://github.com/pytorch/pytorch/pull/182335))
- [BE] Reduce build_vars duplication ([#182390](https://github.com/pytorch/pytorch/pull/182390))
- [OSDC] Migrate H100 workflows to OSDC via dial-up pattern ([#182198](https://github.com/pytorch/pytorch/pull/182198))
- Forward CMake 4 policy minimum to host-protoc ([#182118](https://github.com/pytorch/pytorch/pull/182118))
- [BE] Allow handling of `UNKNOWN` DrCI status ([#182568](https://github.com/pytorch/pytorch/pull/182568))
- Change cross repo CI relay to riseproject-dev/pytorch-ci ([#181977](https://github.com/pytorch/pytorch/pull/181977))
- Fix XPU compilation check ([#182280](https://github.com/pytorch/pytorch/pull/182280))
- [CI] Increase ROCm MI355 test shards to reduce timeout pressure ([#182646](https://github.com/pytorch/pytorch/pull/182646))
- Add svekars to Metamates ([#182692](https://github.com/pytorch/pytorch/pull/182692))
- Run dynamo-unittest on every commit to main ([#182674](https://github.com/pytorch/pytorch/pull/182674))
- [osdc] Migrate inductor-unittest.yml to OSDC (ARC) via dial-up pattern ([#181919](https://github.com/pytorch/pytorch/pull/181919))
- [ROCm][CI] Fix docker rebuild: explicit pip in conda env, fail-fast install_rocm_drm.sh ([#182616](https://github.com/pytorch/pytorch/pull/182616))
- [CI] Fix windows-arm64-build-test by porting #179024 fixes to .ps1 script ([#182647](https://github.com/pytorch/pytorch/pull/182647))
- [CI] Check installed git version during Docker build (#182228) ([#182750](https://github.com/pytorch/pytorch/pull/182750))
- Remove quantization-periodic workflow ([#182878](https://github.com/pytorch/pytorch/pull/182878))
- Compute .ci/docker tree hash to runner_determinator ([#182579](https://github.com/pytorch/pytorch/pull/182579))
- [CI] Add A100 OSDC mapping and migrate inductor A100 perf nightly ([#182753](https://github.com/pytorch/pytorch/pull/182753))
- [CI] Refresh HF cache on workflow_dispatch runs ([#182889](https://github.com/pytorch/pytorch/pull/182889))
- [CI] Migrate operator_microbenchmark A100/H100 jobs to OSDC ([#182754](https://github.com/pytorch/pytorch/pull/182754))
- [CI] Migrate attention_op_microbenchmark A100/H100 jobs to OSDC ([#182755](https://github.com/pytorch/pytorch/pull/182755))
- [CI] Migrate inductor-micro-benchmark to OSDC ARC ([#182756](https://github.com/pytorch/pytorch/pull/182756))
- [CI] Migrate inductor-A100-perf-compare to OSDC ARC ([#182757](https://github.com/pytorch/pytorch/pull/182757))
- [CI] Remove unused torchbench workflow ([#182758](https://github.com/pytorch/pytorch/pull/182758))
- Remove nitpicker workflow ([#182879](https://github.com/pytorch/pytorch/pull/182879))
- [CI] Disable NCCL NVLS on H100 distributed CI job ([#182888](https://github.com/pytorch/pytorch/pull/182888))
- [ci] Fix torchtitan test flake from ciflow tag collision ([#182875](https://github.com/pytorch/pytorch/pull/182875))
- Fix nightly docs push by giving OSDC job access to pytorchbot-env ([#182922](https://github.com/pytorch/pytorch/pull/182922))
- [CI] Enlarge runner size for xpu build ([#181196](https://github.com/pytorch/pytorch/pull/181196))
- [CI][ARC] Propagate ci-docker-hash to calculate-docker-image calls ([#182843](https://github.com/pytorch/pytorch/pull/182843))
- Fix TD changed file detection for ghstack PRs ([#182957](https://github.com/pytorch/pytorch/pull/182957))
- [OSDC] Migrate nightly inductor H100 perf workflow to OSDC via dial-up pattern ([#182591](https://github.com/pytorch/pytorch/pull/182591))
- Bump gitpython from 3.1.47 to 3.1.50 in /.ci/lumen_cli (6a7d27c182c)
- Auto-label .ci/docker changes with no-runner-experiments ([#183244](https://github.com/pytorch/pytorch/pull/183244))
- [CD] [BE] Trim build_env_setup.py OS-package install to zip+openssl ([#183320](https://github.com/pytorch/pytorch/pull/183320))
- Always run EC2 route on pull requests in _linux-build/_linux-test ([#183243](https://github.com/pytorch/pytorch/pull/183243))
- [OSDC] Migrate dtensor.yml to OSDC (ARC) via dial-up pattern ([#182581](https://github.com/pytorch/pytorch/pull/182581))
- Upgrade numba to 0.64.0 ([#182081](https://github.com/pytorch/pytorch/pull/182081))
- Cpython dynamo test org ([#169856](https://github.com/pytorch/pytorch/pull/169856))
- [CI] Plumb ci-docker-hash through OSDC-migrated workflows ([#183492](https://github.com/pytorch/pytorch/pull/183492))
- AArch64 inductor benchmark: revert benchmarking on 16 cores ([#183467](https://github.com/pytorch/pytorch/pull/183467))
- [CI] Migrate periodic workflow to OSDC ([#183493](https://github.com/pytorch/pytorch/pull/183493))
- [CI] Migrate inductor-micro-benchmark-x86 workflow to OSDC ([#183496](https://github.com/pytorch/pytorch/pull/183496))
- [XPU][CI] Fix setup-xpu permission error from leftover root-owned artifacts ([#183572](https://github.com/pytorch/pytorch/pull/183572))
- [CI] Migrate dynamo-unittest workflow to OSDC ([#183494](https://github.com/pytorch/pytorch/pull/183494))
- Use pytorch/test-infra setup-uv wrapper in macOS binary build ([#183643](https://github.com/pytorch/pytorch/pull/183643))
- [ci] Fix ENABLE_TORCH_TRACE on OSDC runners and perf_cli H100/B200 support ([#183718](https://github.com/pytorch/pytorch/pull/183718))
- ci: fail docker-builds GHCR push step on first error ([#183782](https://github.com/pytorch/pytorch/pull/183782))
- Update pytorch_sphinx_theme2 version to 0.4.10 ([#183505](https://github.com/pytorch/pytorch/pull/183505))
- [OSDC] Migrate operator_benchmark.yml to OSDC (ARC) via dial-up pattern ([#182886](https://github.com/pytorch/pytorch/pull/182886))
- Make docs preview upload faster ([#183380](https://github.com/pytorch/pytorch/pull/183380))
- [OSDC] Migrate torchtitan.yml to OSDC (ARC) via dial-up pattern ([#182899](https://github.com/pytorch/pytorch/pull/182899))
- [ROCm][CI] Remove sandbox distributed jobs; restore periodic-rocm-mi200 cron schedule ([#183914](https://github.com/pytorch/pytorch/pull/183914))
- Remove pins for deprecated multipy and torchtext ([#183872](https://github.com/pytorch/pytorch/pull/183872))
- [BE] Build all aarch64 + x86 CPU wheels on a single runner ([#183931](https://github.com/pytorch/pytorch/pull/183931))
- [OSDC] Migrate inductor.yml to OSDC (ARC) via dial-up pattern ([#183646](https://github.com/pytorch/pytorch/pull/183646))
- [OSDC] Migrate inductor-periodic.yml to OSDC (ARC) via dial-up pattern ([#183647](https://github.com/pytorch/pytorch/pull/183647))
- [OSDC] Migrate inductor-nightly.yml to OSDC (ARC) via dial-up pattern ([#183648](https://github.com/pytorch/pytorch/pull/183648))
- [OSDC] Migrate h100-cutlass-backend.yml to OSDC (ARC) via dial-up pattern ([#183650](https://github.com/pytorch/pytorch/pull/183650))
- [BE] Build all CUDA wheels per (arch, cuda) on a single runner ([#184045](https://github.com/pytorch/pytorch/pull/184045))
- [ROCm][CI] Increase shards for trunk-rocm-sandbox workflow ([#183905](https://github.com/pytorch/pytorch/pull/183905))
- [ROCm][CI] Run rocm-mi200 PR workflows on k8s ([#184210](https://github.com/pytorch/pytorch/pull/184210))
- [OSDC] Fall back to GHA artifacts for TD download ([#184289](https://github.com/pytorch/pytorch/pull/184289))
- Add pytorch/crcr-test repo to allowlist ([#184433](https://github.com/pytorch/pytorch/pull/184433))
- Add pytorch/crcr-test to L2 allowlist ([#184482](https://github.com/pytorch/pytorch/pull/184482))
- Bump pytorch_sphinx_theme to 0.4.11 ([#184425](https://github.com/pytorch/pytorch/pull/184425))
- [OSDC] Point linux.arm64.m7g.metal at the Graviton3 bare-metal pool ([#184291](https://github.com/pytorch/pytorch/pull/184291))
- Add @rtimpe to Dynamo merge rules ([#184594](https://github.com/pytorch/pytorch/pull/184594))
- [ROCm][CI] Remove test-matrix from pull workflow ROCm build ([#184557](https://github.com/pytorch/pytorch/pull/184557))
- Use shutil instead of rsync in reuse_old_whl to fix OSDC builds ([#184834](https://github.com/pytorch/pytorch/pull/184834))
- Use dtensor-build's docker-image output in dtensor-test ([#185158](https://github.com/pytorch/pytorch/pull/185158))
- Cancel in-progress docker-builds on new commits to a ciflow PR ([#185188](https://github.com/pytorch/pytorch/pull/185188))
- [BE] Stop running mem_leak_check on CI ([#185265](https://github.com/pytorch/pytorch/pull/185265))
- [ROCm] enable test-weekly MI355 inductor dashboard job ([#183538](https://github.com/pytorch/pytorch/pull/183538))
- [CI] Abort builds/tests for 10+ deep ghstacks ([#185290](https://github.com/pytorch/pytorch/pull/185290))
- [ROCm][CI] Simplify ROCm workflow - Removes user perm changes (unnecessary due to .ci/pytorch/test.sh) ([#183570](https://github.com/pytorch/pytorch/pull/183570))
- Wrap up OSDC/EC2 shadow-traffic experiment ([#185181](https://github.com/pytorch/pytorch/pull/185181))
- Add @trichmo to dynamo merge_rules ([#185244](https://github.com/pytorch/pytorch/pull/185244))
- [ROCm][CI] Restore workspace owner after ROCm test container runs for navi31s ([#185444](https://github.com/pytorch/pytorch/pull/185444))
- Make profiler resilient to duplicate flow start IDs ([#184792](https://github.com/pytorch/pytorch/pull/184792))
- Migrate h100-distributed workflow to OSDC ([#185180](https://github.com/pytorch/pytorch/pull/185180))
- Fix the missing arc experiment in inductor-pallas and tsan workflows ([#185538](https://github.com/pytorch/pytorch/pull/185538))
- [CI] Nuke all the dynamo_eager and aot_eager integration tests ([#185224](https://github.com/pytorch/pytorch/pull/185224))
- Update runner determinator to support exclusion syntax ([#185580](https://github.com/pytorch/pytorch/pull/185580))
- [CI] Fix Windows pip install command ([#185662](https://github.com/pytorch/pytorch/pull/185662))
- Fix condition for upload-docs-preview job ([#185685](https://github.com/pytorch/pytorch/pull/185685))
- Decouple aoti cross-compile shard from main cuda13 test job ([#185680](https://github.com/pytorch/pytorch/pull/185680))
- Publish docs preview from a standalone docs-build workflow ([#185688](https://github.com/pytorch/pytorch/pull/185688))
- Generalize flex flash vectorization config for mask mods ([#185020](https://github.com/pytorch/pytorch/pull/185020))
- Update torch_tpu.txt ([#185679](https://github.com/pytorch/pytorch/pull/185679))
- [vllm hash update] update the pinned vllm hash ([#183068](https://github.com/pytorch/pytorch/pull/183068))
- add spmd_types==0.2.0 to pytorch ([#180880](https://github.com/pytorch/pytorch/pull/180880))
- Enable CuTeDSL op overrides in CI: accept cutlass-dsl 4.5.2, install tvm-ffi ([#186081](https://github.com/pytorch/pytorch/pull/186081))
- Update allowlist.yml ([#186062](https://github.com/pytorch/pytorch/pull/186062))
- Use CUDA_STABLE for vLLM test torch-backend channel ([#186108](https://github.com/pytorch/pytorch/pull/186108))
- Add hidden experimental CUPTI monitor API ([#186034](https://github.com/pytorch/pytorch/pull/186034))
- Bring in gemm kernels form quack and CI testing for patch set ([#186284](https://github.com/pytorch/pytorch/pull/186284))
- [CI] Route aarch64 docker-builds jobs to an aarch64 runner ([#186317](https://github.com/pytorch/pytorch/pull/186317))
- [CI] Use a shared registry build cache for docker-builds ([#186297](https://github.com/pytorch/pytorch/pull/186297))
- Update torch-xpu-ops commit pin ([#186208](https://github.com/pytorch/pytorch/pull/186208))
- [vllm hash update] update the pinned vllm hash ([#186165](https://github.com/pytorch/pytorch/pull/186165))
- [ROCm][CI] Decrease ROCm shards of trunk.yml & remove triggers from extraneous workflows ([#186401](https://github.com/pytorch/pytorch/pull/186401))
- Update merge_rules.yaml to include `torch._C._dynamo.*` ([#186628](https://github.com/pytorch/pytorch/pull/186628))
- [XPU] Add pyzes==0.1.1 to XPU nightly wheel extra install requirements ([#185969](https://github.com/pytorch/pytorch/pull/185969))
- Don't skip linux cpu/cuda binary tests when ROCm/XPU builds fail ([#186651](https://github.com/pytorch/pytorch/pull/186651))
- Make TORCH_TRACE fork-safe and preserve tlparse logs ([#184772](https://github.com/pytorch/pytorch/pull/184772))
- [Windows CI] Pin openssl=3.5.6 to fix Windows cert-store ASN.1 failure ([#186846](https://github.com/pytorch/pytorch/pull/186846))
- Update torch-xpu-ops commit pin ([#186768](https://github.com/pytorch/pytorch/pull/186768))
- Full git fetch on tag pushes so release manywheel builds detect the tag ([#187042](https://github.com/pytorch/pytorch/pull/187042))
- Followup - Full git fetch on tag pushes so release manywheel builds detect the tag ([#187047](https://github.com/pytorch/pytorch/pull/187047))
- Full git fetch on tag pushes so macOS release wheel builds detect the tag ([#187139](https://github.com/pytorch/pytorch/pull/187139))
### security
