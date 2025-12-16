
# Release Notes worksheet linalg_frontend

The main goal of this process is to rephrase all the commit messages below to make them **clear and easy to read** by the end user. You should follow the following instructions to do so:

* **Please clean up and format commit titles to be readable by the general PyTorch user.** Make sure you're [following the guidance here](https://docs.google.com/document/d/14OmgGBr1w6gl1VO47GGGdwrIaUNr92DFhQbY_NEk8mQ/edit)! Your resulting notes must be consistent and easy to read.
* Please sort commits into the following categories (you should not rename the categories!), I tried to pre-sort these to ease your work, feel free to move commits around if the current categorization is not good.
* Anything that is not public facing needs to be removed.
* If anything is miscategorized/belongs to another domain, move it to `miscategorized.md`.
* Please scan through `miscategorized.md` and handle any commits that belong within your domain according to these instructions.
* We place a lot of emphasis on the “BC-breaking” and “deprecation” sections. Those should be where the most effort goes in. The “improvements” and “bug fixes” for Python API should be nice as well.
* Once you are finished, move this very file from `todo/` to `done/` and submit a pull request.

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

## linalg_frontend
### bc breaking
- [BC-Breaking] Remove long-deprecated casting functions from native_functions.yaml ([#164641](https://github.com/pytorch/pytorch/pull/164641))
- Remove long-deprecated casting functions from some ONNX files ([#164641](https://github.com/pytorch/pytorch/pull/164641))
### deprecation
### new features
### improvements
### bug fixes
- [BE] Check that swizzle arguments are passed to the call ([#167869](https://github.com/pytorch/pytorch/pull/167869))
### performance
### docs
### devs
### Untopiced
- Fix the regression issue caused by non-arrch64 platforms not hitting the MKLDNN path. ([#162168](https://github.com/pytorch/pytorch/pull/162168))
- Remove C++ and test branches for CUDA<12 ([#163443](https://github.com/pytorch/pytorch/pull/163443))
- Add initial suppressions for pyrefly ([#164177](https://github.com/pytorch/pytorch/pull/164177))
- [ROCm][tunableop] Modified Online Tuning Mode to add Instant Logging ([#163965](https://github.com/pytorch/pytorch/pull/163965))
- [ROCm][tunableop] Improvements to tunableop Numerical Check ([#163079](https://github.com/pytorch/pytorch/pull/163079))
- [cuda] fix triu/tril int32 overflow for large matrices ([#164705](https://github.com/pytorch/pytorch/pull/164705))
- Remove unused exception parameter from some files, to work with -Wunused-exception-parameter ([#165770](https://github.com/pytorch/pytorch/pull/165770))
- docs: fix typos ([#164879](https://github.com/pytorch/pytorch/pull/164879))
- [ROCm][tunableop] Fixed Offline Tuning file writing ([#166074](https://github.com/pytorch/pytorch/pull/166074))
- [CUDA][cuBLASLt] addmm -- extend bias fusions to cases with (1 by n) shapes ([#166307](https://github.com/pytorch/pytorch/pull/166307))
- [2/N] Change C-style casts to static_cast or reinterpret_cast ([#165891](https://github.com/pytorch/pytorch/pull/165891))
- MatMal - fix folding logic ([#166891](https://github.com/pytorch/pytorch/pull/166891))
- Back out "MatMal - fix folding logic" ([#167884](https://github.com/pytorch/pytorch/pull/167884))
- Logaddexp complex inconsistent bw cpu and cuda ([#163509](https://github.com/pytorch/pytorch/pull/163509))
- Update linalg.norm to match numpy's handling of degenerate inputs ([#168086](https://github.com/pytorch/pytorch/pull/168086))
- Eliminate GPU to CPU sync in linalg.eig for CUDA tensors ([#168283](https://github.com/pytorch/pytorch/pull/168283))
### not user facing
- Fix integer overflow bug in triu/tril for large diagonal values ([#153240](https://github.com/pytorch/pytorch/pull/153240))
- Remove test conditions for CUDA<12 ([#163495](https://github.com/pytorch/pytorch/pull/163495))
- Adding check for square matrix for input tensor in matrix_exp backwar… ([#163357](https://github.com/pytorch/pytorch/pull/163357))
- Enable several unit tests on ROCm ([#163087](https://github.com/pytorch/pytorch/pull/163087))
- Remove old ROCm version check in tests ([#164245](https://github.com/pytorch/pytorch/pull/164245))
- [ROCm][tunableop] Fixes flaky test issue ([#166084](https://github.com/pytorch/pytorch/pull/166084))
- Improve eig tests in preparation for new eig backends ([#166322](https://github.com/pytorch/pytorch/pull/166322))
- [ROCm][CI] remove relaxed tolerance for tf32 tests ([#166478](https://github.com/pytorch/pytorch/pull/166478))
- [CUDA][cuBLASLt] addmm -- enable 2D bias in the Lt path when followed by an activation ([#165548](https://github.com/pytorch/pytorch/pull/165548))
### security
