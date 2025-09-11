
# Release Notes worksheet mps

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

## mps
### bc breaking
- [BE][MPS] Build metal kernels of MacOS-14+ ([#159733](https://github.com/pytorch/pytorch/pull/159733))
- [MPS] Remove all pre-MacOS14 logic ([#159912](https://github.com/pytorch/pytorch/pull/159912))
### deprecation
### new features
### improvements
- [MPS] Add `shifted_chebyshev_polynomial_[tuvw]` ([#157488](https://github.com/pytorch/pytorch/pull/157488))
- [MPS] Add `shifted_chebyshev_polynomial_[tuvw]` ([#157488](https://github.com/pytorch/pytorch/pull/157488))
- [MPS] Extend atomic operations to all int types ([#158179](https://github.com/pytorch/pytorch/pull/158179))
- [MPS] Speedup torch.full for 1-byte types ([#158874](https://github.com/pytorch/pytorch/pull/158874))
- [MPS] Add support for unsigned types ([#159094](https://github.com/pytorch/pytorch/pull/159094))
- [MPS] Add `simd_[arg][max|min]` ([#158990](https://github.com/pytorch/pytorch/pull/158990))
- [MPS] Speedup `argmax`/`argmin` ([#159524](https://github.com/pytorch/pytorch/pull/159524))
- [MPS] Move max_pool2d to Metal for `stride != 1` ([#157876](https://github.com/pytorch/pytorch/pull/157876))
- [MPS] Extend `index_put` to complex types ([#160159](https://github.com/pytorch/pytorch/pull/160159))
- [MPS] Add API to query GPU core count ([#160414](https://github.com/pytorch/pytorch/pull/160414))
- [MPS] Update `avg_pool3d` kernel to use `opmath_t` ([#161071](https://github.com/pytorch/pytorch/pull/161071))
- [MPS] Add slow version of `kthvalue` ([#161817](https://github.com/pytorch/pytorch/pull/161817))
- [MPS] Add `igamma/igammac` ops ([#161927](https://github.com/pytorch/pytorch/pull/161927))
- [MPS] enable cat op for sparse ([#162007](https://github.com/pytorch/pytorch/pull/162007))
### bug fixes
- [MPS][BE] Delete `as_strided_tensorimpl_mps` ([#157772](https://github.com/pytorch/pytorch/pull/157772))
- [MPS] Do not crash if tensor dim > INT_MAX ([#158824](https://github.com/pytorch/pytorch/pull/158824))
- [MPS] Avoid outputing zeros from `exponential_` for MPS ([#159386](https://github.com/pytorch/pytorch/pull/159386))
- [MPS] Extend addmm to integral types ([#160270](https://github.com/pytorch/pytorch/pull/160270))
- [MPS] Type-promote tensor-iterator common dtype ([#160334](https://github.com/pytorch/pytorch/pull/160334))
- Fix MPS autocast for ConvTranspose3d ([#160345](https://github.com/pytorch/pytorch/pull/160345))
- Fix MPS conv3d autocast bias dtype mismatch ([#160423](https://github.com/pytorch/pytorch/pull/160423))
- [MPS] Fix error check for torch.var on scalar ([#160889](https://github.com/pytorch/pytorch/pull/160889))
- [MPS] Fix index_add for complex + int64 ([#160926](https://github.com/pytorch/pytorch/pull/160926))
- Fix constant_pad_nd_mps bug when pad is empty ([#161149](https://github.com/pytorch/pytorch/pull/161149))
- [MPS] Fix index_select for scalar_types ([#161206](https://github.com/pytorch/pytorch/pull/161206))
- [MPS] Fix `index_copy` for scalars ([#161267](https://github.com/pytorch/pytorch/pull/161267))
- [MPS] Fix index_copy for strided indices ([#161333](https://github.com/pytorch/pytorch/pull/161333))
- Fix index_add for int64 input + zerodim index ([#161511](https://github.com/pytorch/pytorch/pull/161511))
- Ensure that tensors are contiguous before using no-graph MPS impl ([#161641](https://github.com/pytorch/pytorch/pull/161641))
- [MPS] Migrate round unary op to Metal ([#161712](https://github.com/pytorch/pytorch/pull/161712))
### performance
- [MPS] Optimize cummin/cummax metal kernels ([#156794](https://github.com/pytorch/pytorch/pull/156794))
### docs
### devs
### Untopiced
- [MPS] Fix batch norm incorrect gradient ([#156867](https://github.com/pytorch/pytorch/pull/156867))
- [aoti][mps] Add fused_rms and sdpa_mps fallback ops ([#156844](https://github.com/pytorch/pytorch/pull/156844))
- [MPS] Implement logcumsumexp metal kernel ([#156858](https://github.com/pytorch/pytorch/pull/156858))
- [MPS] Avoid calling tensor ops in max_pool3d impl ([#157874](https://github.com/pytorch/pytorch/pull/157874))
- Address NaNs if SDPA is called with all values masked from query ([#157727](https://github.com/pytorch/pytorch/pull/157727))
- Fix invalid formatting ([#158436](https://github.com/pytorch/pytorch/pull/158436))
- [MPS] Improve performance of max_pool3d ([#157875](https://github.com/pytorch/pytorch/pull/157875))
- [MPS] coalesce for sparse tensors ([#159729](https://github.com/pytorch/pytorch/pull/159729))
- [MPS] Sparse coalesce more dtypes to match cpu ([#160254](https://github.com/pytorch/pytorch/pull/160254))
- [MPS] Add mps keys to `indices` and `values` ops ([#160223](https://github.com/pytorch/pytorch/pull/160223))
- [MPS] Add `grid_sampler_3d` for MPS ([#160541](https://github.com/pytorch/pytorch/pull/160541))
- [MPS][BE] Fix unused vars in GridSampler ([#160850](https://github.com/pytorch/pytorch/pull/160850))
- [MPS] Update `avg_pool2d` to use Metal kernel when `ceil_mode=True` ([#161011](https://github.com/pytorch/pytorch/pull/161011))
- [MPS] fix empty input in posneg functions ([#161824](https://github.com/pytorch/pytorch/pull/161824))
- [MPS] add bunch of unary funcs for sparse tensors ([#161846](https://github.com/pytorch/pytorch/pull/161846))
- [MPS] Move sparsemps testing from test_mps to test_sparse ([#161852](https://github.com/pytorch/pytorch/pull/161852))
- [MPS] Add `native_dropout` and `native_dropout_backward` ([#162108](https://github.com/pytorch/pytorch/pull/162108))
### not user facing
- [MPS] Add benchmark for scan with indices ([#156860](https://github.com/pytorch/pytorch/pull/156860))
- [aoti][mps] Fix deduplication of kernels ([#156843](https://github.com/pytorch/pytorch/pull/156843))
- [EZ][BE] Move array def to `c10/metal/common.h` ([#157746](https://github.com/pytorch/pytorch/pull/157746))
- [BE] Use `simdgroup_size` constexpr ([#157751](https://github.com/pytorch/pytorch/pull/157751))
- [EZ][BE] Delete redundant header ([#157966](https://github.com/pytorch/pytorch/pull/157966))
- [BE] Move repeated code into helper functions ([#158178](https://github.com/pytorch/pytorch/pull/158178))
- [aoti][mps] Enable test_aot_inductor.py tests ([#155598](https://github.com/pytorch/pytorch/pull/155598))
- [CI][MPS] Enable test_indexing on MPS ([#158582](https://github.com/pytorch/pytorch/pull/158582))
- [EZ][BE] Fix compilation warning in Pooling.metal ([#158729](https://github.com/pytorch/pytorch/pull/158729))
- [EZ][BE][MPS] Remove unused `ndArrayFromTensor` ([#158823](https://github.com/pytorch/pytorch/pull/158823))
- [aoti][mps] Fix cpu kernel generation ([#158350](https://github.com/pytorch/pytorch/pull/158350))
- [aoti][mps] Improve tabbing in cpp generation ([#158351](https://github.com/pytorch/pytorch/pull/158351))
- [aoti][mps] Enable more tests ([#158703](https://github.com/pytorch/pytorch/pull/158703))
- [MPS] Enable dlpack integration ([#158888](https://github.com/pytorch/pytorch/pull/158888))
- [aoti][mps] Dynamic reductions ([#159355](https://github.com/pytorch/pytorch/pull/159355))
- [CI][MPS] Fix compile benchmark correctness ([#159731](https://github.com/pytorch/pytorch/pull/159731))
- [BE][MPS] Remove unused size12 variable ([#159832](https://github.com/pytorch/pytorch/pull/159832))
- [MPS][BE] Combine all pre-MacOS14 xfail lists ([#160228](https://github.com/pytorch/pytorch/pull/160228))
### security
