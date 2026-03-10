
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
- Async error reporting from GPU operations ([#170002](https://github.com/pytorch/pytorch/pull/170002), [#170050](https://github.com/pytorch/pytorch/pull/170050))
    ```python
    import torch
    x=torch.rand(10, 1, 10, device='mps')
    y=x[:, [1]]
    torch.mps.synchronize()  # will raise index out of bounds error
    ```
- Added support for Metal 4 ([#172229](https://github.com/pytorch/pytorch/pull/172229), [#172230](https://github.com/pytorch/pytorch/pull/172230))
### improvements
- Improved support for distributions operations ([#172187](https://github.com/pytorch/pytorch/pull/172187), [#172675](https://github.com/pytorch/pytorch/pull/172675), [#173287](https://github.com/pytorch/pytorch/pull/173287))
- Enabling `index_fill` backward pass ([#174238](https://github.com/pytorch/pytorch/pull/174238))
- Extended `baddbmm` and `addbmm` to integer and complex types ([#170895](https://github.com/pytorch/pytorch/pull/170895))
- Improved error messages for distributed ops on MPS ([#173954](https://github.com/pytorch/pytorch/pull/173954))
- Added MPS support for `torch.special.erfcx` (scaled complementary error function) ([#172910](https://github.com/pytorch/pytorch/pull/172910))
### bug fixes
- Fixed non-contiguous grid sampler on MPS ([#171619](https://github.com/pytorch/pytorch/pull/171619))
- Fixed large reductions when compiling for MPS ([#171479](https://github.com/pytorch/pytorch/pull/171479))
- Fixed MPS Inductor `tanh` implementation ([#172406](https://github.com/pytorch/pytorch/pull/172406))
- Fixed complex to real power scalar on MPS ([#174147](https://github.com/pytorch/pytorch/pull/174147))
- Fixed masked op logic in MPS Inductor ([#170134](https://github.com/pytorch/pytorch/pull/170134))
- Fixed `orgqr` race condition on MPS ([#174143](https://github.com/pytorch/pytorch/pull/174143))
- Fixed 2-pass SDPA memory corruption by forcing float accumulators, resolving nondeterministic/corrupt results with bf16/fp16 and GQA when seq_len > 1023 ([#174945](https://github.com/pytorch/pytorch/pull/174945))
### performance
- Migrated `atan2` to native MPS Metal kernel ([#173405](https://github.com/pytorch/pytorch/pull/173405))
- Migrated `pow_tensor_scalar` and `reciprocal` to Metal shaders ([#170077](https://github.com/pytorch/pytorch/pull/170077))
- Reimplemented Cauchy distribution with native Metal kernel ([#174062](https://github.com/pytorch/pytorch/pull/174062))
- Rewrote `log_normal` and `geometric` distributions as Metal shaders ([#174189](https://github.com/pytorch/pytorch/pull/174189))
- Migrated `grid_sampler_2d` to Metal ([#174343](https://github.com/pytorch/pytorch/pull/174343))
### docs
### devs
- Migrated `_local_scalar_dense_mps` to DispatchV2 ([#172967](https://github.com/pytorch/pytorch/pull/172967))
### Untopiced
### not user facing
- Do not use deprecated `isIntegralType` method ([#171200](https://github.com/pytorch/pytorch/pull/171200))
- Take reference after a null check in `MPSStream::checkLastError` ([#171786](https://github.com/pytorch/pytorch/pull/171786))
- Add OpInfo skips and dtypes for MPS ops (1/N through 16/N) ([#170122](https://github.com/pytorch/pytorch/pull/170122), [#170454](https://github.com/pytorch/pytorch/pull/170454), [#170820](https://github.com/pytorch/pytorch/pull/170820), [#171952](https://github.com/pytorch/pytorch/pull/171952), [#171953](https://github.com/pytorch/pytorch/pull/171953), [#172269](https://github.com/pytorch/pytorch/pull/172269), [#172270](https://github.com/pytorch/pytorch/pull/172270), [#172569](https://github.com/pytorch/pytorch/pull/172569), [#172570](https://github.com/pytorch/pytorch/pull/172570), [#172571](https://github.com/pytorch/pytorch/pull/172571), [#172572](https://github.com/pytorch/pytorch/pull/172572), [#172573](https://github.com/pytorch/pytorch/pull/172573), [#172574](https://github.com/pytorch/pytorch/pull/172574), [#172575](https://github.com/pytorch/pytorch/pull/172575), [#172891](https://github.com/pytorch/pytorch/pull/172891), [#172892](https://github.com/pytorch/pytorch/pull/172892))
- Remove cholesky inverse redundant test ([#172264](https://github.com/pytorch/pytorch/pull/172264))
- Extend `test_output` match to support upcasts ([#172591](https://github.com/pytorch/pytorch/pull/172591))
- Fix unused variable warning ([#172950](https://github.com/pytorch/pytorch/pull/172950))
- Replace `test_dtypes` xfails with `dtypesIfMPS` where applicable ([#172788](https://github.com/pytorch/pytorch/pull/172788))
- Enable per-sample seed in `test_output_grad_match` ([#173328](https://github.com/pytorch/pytorch/pull/173328))
- Unimplement `gcd` for `torch.bool` ([#173600](https://github.com/pytorch/pytorch/pull/173600))
- Skip `test_non_standard_bool_values` and remove xfails ([#173560](https://github.com/pytorch/pytorch/pull/173560))
- Update opinfos for recently changed ops and other CI failures ([#173025](https://github.com/pytorch/pytorch/pull/173025))
- Enable `test_ops.py` for MPS for macOS 15+ ([#169018](https://github.com/pytorch/pytorch/pull/169018))
- Move tolerance overrides to OpInfo ([#174411](https://github.com/pytorch/pytorch/pull/174411))
- Add macOS Tahoe testing shard ([#174484](https://github.com/pytorch/pytorch/pull/174484))
- Enable test for `nn.TransformerEncoderLayer` ([#174865](https://github.com/pytorch/pytorch/pull/174865))
- MPS Inductor now uses precise flavors of trigonometric functions for improved numerical accuracy ([#172466](https://github.com/pytorch/pytorch/pull/172466))
- Metal distribution shaders now use precise math for improved numerical accuracy ([#174240](https://github.com/pytorch/pytorch/pull/174240))
### security
