
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
- [MPS] Allocating all tensors in unified memory ([#175818](https://github.com/pytorch/pytorch/pull/175818))
- [MPS] Allocating all tensors in unified memory ([#175818](https://github.com/pytorch/pytorch/pull/175818))
### deprecation
### new features
### improvements
- [MPS] Fix `abs` complex overflow/underflow ([#174346](https://github.com/pytorch/pytorch/pull/174346))
- [MPS] Migrate `index_fill_` to Metal ([#175822](https://github.com/pytorch/pytorch/pull/175822))
- [MPS] Implement linalg_qr for MPS ([#172536](https://github.com/pytorch/pytorch/pull/172536))
- [EZ][MPS] Extend histogram to float/bfloat ([#176913](https://github.com/pytorch/pytorch/pull/176913))
- [MPS] Add cholesky_solve support ([#176703](https://github.com/pytorch/pytorch/pull/176703))
- [MPS] Extend unfold_backward to torch.complex64 ([#177274](https://github.com/pytorch/pytorch/pull/177274))
- [MPS] Support complex inputs to `scatter` and `gather` ([#177794](https://github.com/pytorch/pytorch/pull/177794))
- [MPS] Migrate Lerp to metal kernel ([#177093](https://github.com/pytorch/pytorch/pull/177093))
- [MPS] Register DeviceCapability for MPS backend ([#178180](https://github.com/pytorch/pytorch/pull/178180))
- [Accelerator] Register DeviceCapability for MPS backend ([#178180](https://github.com/pytorch/pytorch/pull/178180))
- [MPS] Migrate Eye to metal ([#178683](https://github.com/pytorch/pytorch/pull/178683))
- [MPS] Migrate RELU to metal ([#178866](https://github.com/pytorch/pytorch/pull/178866))
- [MPS] Migrate Silu to metal ([#179071](https://github.com/pytorch/pytorch/pull/179071))
- [MPS] Implement `torch.distributions.Gamma` (fwd + bwd) ([#179228](https://github.com/pytorch/pytorch/pull/179228))
- [MPS] switch exponential distribution to metal ([#174277](https://github.com/pytorch/pytorch/pull/174277))
- [MPS] Migrate fill_ to native Metal kernels ([#176101](https://github.com/pytorch/pytorch/pull/176101))
- [MPS] RMSNorm speedup ([#180173](https://github.com/pytorch/pytorch/pull/180173))
- [MPS] remove .item sync in _amp_non_finite_check_and_unscale_mps_single_impl ([#180267](https://github.com/pytorch/pytorch/pull/180267))
### bug fixes
- [MPS] Fix AvgPool for channels last + offs ([#175235](https://github.com/pytorch/pytorch/pull/175235))
- [MPS] Return pivots from `linalg_solve_out_mps_impl` ([#175284](https://github.com/pytorch/pytorch/pull/175284))
- [MPS] Fix lu_solve for broadcasted bias ([#175332](https://github.com/pytorch/pytorch/pull/175332))
- [MPS] addmm & mm implementations must return zero filled matrix if one of inputs are empty ([#175905](https://github.com/pytorch/pytorch/pull/175905))
- [MPS] Fix index_reduce atomic misalignment for sub-32-bit types ([#176009](https://github.com/pytorch/pytorch/pull/176009))
- [MPS] Fix masked_fill for non-contig outputs ([#176171](https://github.com/pytorch/pytorch/pull/176171))
- [MPS] Support noncontiguous bias in `layer_norm` ([#176238](https://github.com/pytorch/pytorch/pull/176238))
- [MPS] Add unsigned int types to Metal cast opertions ([#176343](https://github.com/pytorch/pytorch/pull/176343))
- [MPS] Fix noncontiguous behavior for `solve_triangular` ([#176335](https://github.com/pytorch/pytorch/pull/176335))
- [MPS] Support noncontiguous weight for histogram/histogramdd ([#175906](https://github.com/pytorch/pytorch/pull/175906))
- Fix MPS memory leak in getStridedMPSNDArray: autorelease NSArray copies ([#176648](https://github.com/pytorch/pytorch/pull/176648))
- [MPS] Add error checking for bmm ([#176771](https://github.com/pytorch/pytorch/pull/176771))
- [Inductor][MPS] Fix half-precision type mismatches in Metal shader codegen ([#176436](https://github.com/pytorch/pytorch/pull/176436))
- [MPS] Fix SDPA output shape when value head dim differs ([#176843](https://github.com/pytorch/pytorch/pull/176843))
- [MPS] Error out if one tries to create `torch.cdouble` tensor ([#176985](https://github.com/pytorch/pytorch/pull/176985))
- [MPS] Error out if one tries to create `torch.cdouble` tensor ([#176985](https://github.com/pytorch/pytorch/pull/176985))
- [MPS] Fix `_copy_from_and_resize` logic ([#177606](https://github.com/pytorch/pytorch/pull/177606))
- [MPS] Fix linear backward crash with channels_last grad ([#178278](https://github.com/pytorch/pytorch/pull/178278))
- Detect mm padding overflow and incorrect alignment conditions and dispatch to metal_mm ([#178203](https://github.com/pytorch/pytorch/pull/178203))
- [MPS] Fix nested ops.masked variable name collisions in Metal codegen ([#178304](https://github.com/pytorch/pytorch/pull/178304))
- [MPS] Replace MPSGraph nonzero with native Metal prefix-sum + scatter ([#178484](https://github.com/pytorch/pytorch/pull/178484))
- [MPS] fix in-place self.add_(other, alpha) RuntimeErrors with type promotion ([#178724](https://github.com/pytorch/pytorch/pull/178724))
- [MPS] Fix BatchNorm with mixed input/weight dtypes (#178770) ([#178775](https://github.com/pytorch/pytorch/pull/178775))
- [MPS] Fix hi/lo swap typo in Metal Philox RNG single_round ([#179227](https://github.com/pytorch/pytorch/pull/179227))
- [MPS] Allow getMPSScalar construction for uint64 ([#179230](https://github.com/pytorch/pytorch/pull/179230))
- [MPS] Fix mm with stride-0 inputs on macOS < 26.4 ([#180236](https://github.com/pytorch/pytorch/pull/180236))
### performance
- [MPS] Reimplement cross operation as single stage Metal kernel ([#175498](https://github.com/pytorch/pytorch/pull/175498))
- [MPS] Reimplement cross operation as single stage Metal kernel ([#175498](https://github.com/pytorch/pytorch/pull/175498))
### docs
### devs
### Untopiced
- [MPS] Fix `masked_scatter` side-effect and align behavior with CPU ([#175622](https://github.com/pytorch/pytorch/pull/175622))
- [MPS] Fix `lgamma/digamma/polygamma` noncontiguous behavior ([#175603](https://github.com/pytorch/pytorch/pull/175603))
- [MPS] Add `index_reduce` ([#174936](https://github.com/pytorch/pytorch/pull/174936))
- [MPS] Fix masked_scatter to preserve scalar tensor shape ([#174381](https://github.com/pytorch/pytorch/pull/174381))
- [MPS] Migrate xlogy from MPSGraph to native Metal ([#177749](https://github.com/pytorch/pytorch/pull/177749))
- [MPS] Migrate `norm` to metal kernel ([#177328](https://github.com/pytorch/pytorch/pull/177328))
- [MPS] Support complex inputs for `repeat` ([#178198](https://github.com/pytorch/pytorch/pull/178198))
- [MPS][BE] Replace `.count(hash) = 0` with `.contains(hash)` ([#178337](https://github.com/pytorch/pytorch/pull/178337))
- [MPS] Support complex inputs to `cumsum` ([#178328](https://github.com/pytorch/pytorch/pull/178328))
- [MPS] Support complex inputs to `logcumsumexp` ([#178411](https://github.com/pytorch/pytorch/pull/178411))
- [MPS] Support complex inputs to `cumprod` ([#178436](https://github.com/pytorch/pytorch/pull/178436))
- [MPS] Support complex inputs to `nn.functional.linear` ([#178799](https://github.com/pytorch/pytorch/pull/178799))
- [BE] [MPS] Improve call site of `_scaled_dot_product_attention_math_mps` ([#179309](https://github.com/pytorch/pytorch/pull/179309))
- [MPS] Enable `mvlgamma` ([#178914](https://github.com/pytorch/pytorch/pull/178914))
- [MPS] Standardize Metal kernel compilation around AsyncCompile ([#179838](https://github.com/pytorch/pytorch/pull/179838))
### not user facing
- [BE][MPS] Use `fmt::format` to compute key ([#175249](https://github.com/pytorch/pytorch/pull/175249))
- [BE][MPS] Add `_3d` suffix `grid_sampler` kernel ([#175060](https://github.com/pytorch/pytorch/pull/175060))
- [MPS] Update `test_noncontiguous_samples` decorators and error comments ([#176348](https://github.com/pytorch/pytorch/pull/176348))
- [MPS] Migrate minimum/maximum from MPSGraph to native Metal ([#177747](https://github.com/pytorch/pytorch/pull/177747))
- [MPS] Remove some usages of double dtype in MPS tests ([#177766](https://github.com/pytorch/pytorch/pull/177766))
- [BE] Fix compilation warning in Indexing.metal ([#178507](https://github.com/pytorch/pytorch/pull/178507))
- [MPS] bundled shared library typo ([#179447](https://github.com/pytorch/pytorch/pull/179447))
- [BE] Refactor shared interpolation helpers into SamplingHelpers.h ([#179751](https://github.com/pytorch/pytorch/pull/179751))
- [MPS] Support instrumentation of Objective-C++ ([#178702](https://github.com/pytorch/pytorch/pull/178702))
### security
