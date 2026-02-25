
# Release Notes worksheet mps

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

## mps
### bc breaking
### deprecation
### new features
### improvements
- [MPS] Add shader error reporting mechanism from Python ([#170002](https://github.com/pytorch/pytorch/pull/170002))
- [MPS] Migrate pow_tensor_scalar/reciprocal ops to Metal shaders ([#170077](https://github.com/pytorch/pytorch/pull/170077))
- [MPS] Extend baddbmm and addbmm for integer and complex types ([#170895](https://github.com/pytorch/pytorch/pull/170895))
- [MPS][BE] Add checks for MacOS-26 ([#172229](https://github.com/pytorch/pytorch/pull/172229))
- [MPS] Compile shaders using latest OS capabilities ([#172230](https://github.com/pytorch/pytorch/pull/172230))
- [BE][MPSInductor] Use `::precise::` flavors of trigonometic functions ([#172466](https://github.com/pytorch/pytorch/pull/172466))
- [MPS] log normal implementation ([#172187](https://github.com/pytorch/pytorch/pull/172187))
- [MPSInductor] Fix masked op logic ([#170134](https://github.com/pytorch/pytorch/pull/170134))
- [MPSInductor] Report out-of-bounds from torch.compiled code ([#170050](https://github.com/pytorch/pytorch/pull/170050))
- [MPS] Add dummy vdot implementation ([#172840](https://github.com/pytorch/pytorch/pull/172840))
- [MPS] Implement erfcx ([#172910](https://github.com/pytorch/pytorch/pull/172910))
- [MPS] Add dummy vdot implementation ([#172840](https://github.com/pytorch/pytorch/pull/172840))
- [MPS] cauchy implementation ([#172675](https://github.com/pytorch/pytorch/pull/172675))
- [BE] Migrated `_local_scalar_dense_mps` to DispatchV2 ([#172967](https://github.com/pytorch/pytorch/pull/172967))
- [MPS] geometric distribution implementation ([#173287](https://github.com/pytorch/pytorch/pull/173287))
- [MPS] cauchy with metal kernel ([#174062](https://github.com/pytorch/pytorch/pull/174062))
- [MPS] rewrite log normal and geometric to metal shaders ([#174189](https://github.com/pytorch/pytorch/pull/174189))
- [MPS] Add `_unique` aten op ([#174238](https://github.com/pytorch/pytorch/pull/174238))
- [MPS] update to metal precise in distributions.metal ([#174240](https://github.com/pytorch/pytorch/pull/174240))
- [BE][MPS] Migrate grid_sampler_2d to Metal ([#174343](https://github.com/pytorch/pytorch/pull/174343))
- [MPS] Fix `abs` complex overflow/underflow ([#174346](https://github.com/pytorch/pytorch/pull/174346))
### bug fixes
- [MPS] fix non contiguous grid sampler ([#171619](https://github.com/pytorch/pytorch/pull/171619))
- [MPS] fix large reductions when compiling ([#171479](https://github.com/pytorch/pytorch/pull/171479))
- Fix MPS Inductor for tanh implementation ([#172406](https://github.com/pytorch/pytorch/pull/172406))
- [MPS] Fix complex to real power scalar ([#174147](https://github.com/pytorch/pytorch/pull/174147))
### performance
- [MPS] Migrate atan2 to MPS kernel ([#173405](https://github.com/pytorch/pytorch/pull/173405))
### docs
### devs
### Untopiced
- [MPS] Fix `orgqr` race condition ([#174143](https://github.com/pytorch/pytorch/pull/174143))
- [MPS] Fix 2-pass SDPA memory corruption by forcing float accumulators ([#174945](https://github.com/pytorch/pytorch/pull/174945))
### not user facing
- [MPS][BE] Do not use deprecated `isIntegralType` method ([#171200](https://github.com/pytorch/pytorch/pull/171200))
- [BE] Take reference after a null check in MPSStream::checkLastError ([#171786](https://github.com/pytorch/pytorch/pull/171786))
- [MPS] Add OpInfo skips and dtypes for MPS ops (1/N) ([#170122](https://github.com/pytorch/pytorch/pull/170122))
- [MPS] Add OpInfo skips and dtypes for MPS ops (2/N) ([#170454](https://github.com/pytorch/pytorch/pull/170454))
- [MPS] Add OpInfo skips and dtypes for MPS ops (3/N) ([#170820](https://github.com/pytorch/pytorch/pull/170820))
- [MPS] remove cholesky inverse redundant test ([#172264](https://github.com/pytorch/pytorch/pull/172264))
- [MPS] Add OpInfo skips and dtypes for MPS ops (4/N) ([#171952](https://github.com/pytorch/pytorch/pull/171952))
- [MPS] Add OpInfo skips and dtypes for MPS ops (5/N) ([#171953](https://github.com/pytorch/pytorch/pull/171953))
- [MPS] Add OpInfo skips and dtypes for MPS ops (6/N) ([#172269](https://github.com/pytorch/pytorch/pull/172269))
- [MPS] Add OpInfo skips and dtypes for MPS ops (7/N) ([#172270](https://github.com/pytorch/pytorch/pull/172270))
- [CI][MPS] Extend test_output match to support upcasts ([#172591](https://github.com/pytorch/pytorch/pull/172591))
- [BE][MPS] Fix unused variable warning ([#172950](https://github.com/pytorch/pytorch/pull/172950))
- [MPS] Add OpInfo skips and dtypes for MPS ops (8/N) ([#172569](https://github.com/pytorch/pytorch/pull/172569))
- [MPS] Add OpInfo skips and dtypes for MPS ops (9/N) ([#172570](https://github.com/pytorch/pytorch/pull/172570))
- [MPS] Add OpInfo skips and dtypes for MPS ops (10/N) ([#172571](https://github.com/pytorch/pytorch/pull/172571))
- [MPS] Add OpInfo skips and dtypes for MPS ops (11/N) ([#172572](https://github.com/pytorch/pytorch/pull/172572))
- [MPS] Add OpInfo skips and dtypes for MPS ops (12/N) ([#172573](https://github.com/pytorch/pytorch/pull/172573))
- [MPS] Add OpInfo skips and dtypes for MPS ops (13/N) ([#172574](https://github.com/pytorch/pytorch/pull/172574))
- [MPS] Add OpInfo skips and dtypes for MPS ops (14/N) ([#172575](https://github.com/pytorch/pytorch/pull/172575))
- [MPS] Replace `test_dtypes` xfails with `dtypesIfMPS` where applicable ([#172788](https://github.com/pytorch/pytorch/pull/172788))
- [MPS] Add OpInfo skips and dtypes for MPS ops (15/N) ([#172891](https://github.com/pytorch/pytorch/pull/172891))
- [MPS] Add OpInfo skips and dtypes for MPS ops (16/N) ([#172892](https://github.com/pytorch/pytorch/pull/172892))
- [BE][MPS] Enable per-sample seed in test_output_grad_match ([#173328](https://github.com/pytorch/pytorch/pull/173328))
- [BE][MPS] Unimplement gcd for torch.bool ([#173600](https://github.com/pytorch/pytorch/pull/173600))
- [BE][MPS] Print better error message about distribtued ops ([#173954](https://github.com/pytorch/pytorch/pull/173954))
- [MPS] Skip `test_non_standard_bool_values` and remove xfails ([#173560](https://github.com/pytorch/pytorch/pull/173560))
- [MPS] Update opinfos for recently changed ops and other CI failures ([#173025](https://github.com/pytorch/pytorch/pull/173025))
- [MPS] Enable `test_ops.py` for MPS for MacOS 15+ ([#169018](https://github.com/pytorch/pytorch/pull/169018))
- [BE][MPS] Move tolerance overrides to OpInfo ([#174411](https://github.com/pytorch/pytorch/pull/174411))
- [MPS] Add MacOS Tahoe testing shard ([#174484](https://github.com/pytorch/pytorch/pull/174484))
- [MPS] Enable test for `nn.TransformerEncoderLayer` ([#174865](https://github.com/pytorch/pytorch/pull/174865))
### security
