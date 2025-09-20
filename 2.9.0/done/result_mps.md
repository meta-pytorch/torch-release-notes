# Release Notes worksheet mps

The main goal of this process is to rephrase all the commit messages below to make them **clear and easy to read** by the end user. You should follow the following instructions to do so:

* **Please clean up and format commit titles to be readable by the general PyTorch user.** Make sure you're [following the guidance here](https://docs.google.com/document/d/14OmgGBr1w6gl1VO47GGGdwrIaUNr92DFhQbY_NEk8mQ/edit)\! Your resulting notes must be consistent and easy to read.  
* Please sort commits into the following categories (you should not rename the categories\!), I tried to pre-sort these to ease your work, feel free to move commits around if the current categorization is not good.  
* Anything that is not public facing needs to be removed.  
* If anything is miscategorized/belongs to another domain, move it to `miscategorized.md`.  
* Please scan through `miscategorized.md` and handle any commits that belong within your domain according to these instructions.  
* We place a lot of emphasis on the “BC-breaking” and “deprecation” sections. Those should be where the most effort goes in. The “improvements” and “bug fixes” for Python API should be nice as well.  
* Once you are finished, move this very file from `todo/` to `done/` and submit a pull request.

The categories below are as follows:

* BC breaking: All commits that are BC-breaking. These are the most important commits. If any pre-sorted commit is actually BC-breaking, do move it to this section. Each commit should contain a paragraph explaining the rational behind the change as well as an example for how to update user code [BC-Guidelines](https://docs.google.com/document/d/14OmgGBr1w6gl1VO47GGGdwrIaUNr92DFhQbY_NEk8mQ/edit#heading=h.a9htwgvvec1m).  
* Deprecations: All commits introducing deprecation. Each commit should include a small example explaining what should be done to update user code.  
* new\_features: All commits introducing a new feature (new functions, new submodule, new supported platform etc)  
* improvements: All commits providing improvements to existing feature should be here (new backend for a function, new argument, better numerical stability)  
* bug fixes: All commits that fix bugs and behaviors that do not match the documentation  
* performance: All commits that are added mainly for performance (we separate this from improvements above to make it easier for users to look for it)  
* documentation: All commits that add/update documentation  
* Developers: All commits that are not end-user facing but still impact people that compile from source, develop into pytorch, extend pytorch, etc  
* not user facing: All commits that are not public end-user facing and hence should be dropped from the release notes

## mps

### bc breaking

- Build metal kernels of MacOS-14+ and remove all pre-MacOS-14 specific logic. Requires MacOS-14+ going forwards. ([\#159733](https://github.com/pytorch/pytorch/pull/159733), [\#159912](https://github.com/pytorch/pytorch/pull/159912))

### deprecation

### new features
- [Beta] Partial sparse support for MPS backend ([\#159729](https://github.com/pytorch/pytorch/pull/159729), [\#160254](https://github.com/pytorch/pytorch/pull/160254), [\#160223](https://github.com/pytorch/pytorch/pull/160223), [\#161846](https://github.com/pytorch/pytorch/pull/161846), [\#162007](https://github.com/pytorch/pytorch/pull/162007))

### improvements

- Add `shifted_chebyshev_polynomial_[tuvw]`, `igamma/igammac,grid_sampler_3d, native_dropout`/`native_dropout_backward`  ([\#157488](https://github.com/pytorch/pytorch/pull/157488), [\#161927](https://github.com/pytorch/pytorch/pull/161927), [\#160541](https://github.com/pytorch/pytorch/pull/160541), [\#162108](https://github.com/pytorch/pytorch/pull/162108))
- Extend atomic operations to all int types ([\#158179](https://github.com/pytorch/pytorch/pull/158179))  
- Extend `index_put` to complex types ([\#160159](https://github.com/pytorch/pytorch/pull/160159))  
- Extend addmm to integral types ([\#160270](https://github.com/pytorch/pytorch/pull/160270))  
- Add support for unsigned types ([\#159094](https://github.com/pytorch/pytorch/pull/159094))  
- Add API to query GPU core count ([\#160414](https://github.com/pytorch/pytorch/pull/160414))  
- Add `kthvalue` ([\#161817](https://github.com/pytorch/pytorch/pull/161817))
- Type-promote tensor-iterator common dtype ([\#160334](https://github.com/pytorch/pytorch/pull/160334))
- Implement logcumsumexp metal kernel ([\#156858](https://github.com/pytorch/pytorch/pull/156858))
- Enable dlpack integration ([\#158888](https://github.com/pytorch/pytorch/pull/158888))
- Dynamic reductions ([\#159355](https://github.com/pytorch/pytorch/pull/159355))
- Update `avg_pool2d` to use Metal kernel when `ceil_mode=True` ([\#161011](https://github.com/pytorch/pytorch/pull/161011))

### bug fixes

- Fix batch norm incorrect gradient ([\#156867](https://github.com/pytorch/pytorch/pull/156867))  
- Do not crash if tensor dim \> INT\_MAX ([\#158824](https://github.com/pytorch/pytorch/pull/158824))  
- Avoid outputing zeros from `exponential_` for MPS ([\#159386](https://github.com/pytorch/pytorch/pull/159386))  
- Fix MPS autocast for ConvTranspose3d ([\#160345](https://github.com/pytorch/pytorch/pull/160345))  
- Fix MPS conv3d autocast bias dtype mismatch ([\#160423](https://github.com/pytorch/pytorch/pull/160423))  
- Fix error check for torch.var on scalar ([\#160889](https://github.com/pytorch/pytorch/pull/160889))  
- Fix index\_add for complex \+ int64 ([\#160926](https://github.com/pytorch/pytorch/pull/160926))  
- Fix constant\_pad\_nd\_mps bug when pad is empty ([\#161149](https://github.com/pytorch/pytorch/pull/161149))  
- Fix index\_select for scalar\_types ([\#161206](https://github.com/pytorch/pytorch/pull/161206))  
- Fix `index_copy` for scalars ([\#161267](https://github.com/pytorch/pytorch/pull/161267))  
- Fix index\_copy for strided indices ([\#161333](https://github.com/pytorch/pytorch/pull/161333))  
- Fix index\_add for int64 input \+ zerodim index ([\#161511](https://github.com/pytorch/pytorch/pull/161511))  
- Ensure that tensors are contiguous before using MPS linear kernel ([\#161641](https://github.com/pytorch/pytorch/pull/161641))  
- Address NaNs if SDPA is called with all values masked from query ([\#157727](https://github.com/pytorch/pytorch/pull/157727))  
- Fix invalid formatting ([\#158436](https://github.com/pytorch/pytorch/pull/158436))  
- Fix empty input in posneg functions ([\#161824](https://github.com/pytorch/pytorch/pull/161824))
- Migrate round unary op to Metal ([\#161712](https://github.com/pytorch/pytorch/pull/161712))
- Type-promote tensor-iterator common dtype ([\#160334](https://github.com/pytorch/pytorch/pull/160334))

### performance

- Optimize cummin/cummax metal kernels ([\#156794](https://github.com/pytorch/pytorch/pull/156794))  
- Speedup torch.full for 1-byte types ([\#158874](https://github.com/pytorch/pytorch/pull/158874))  
- Speedup `argmax`/`argmin` ([\#159524](https://github.com/pytorch/pytorch/pull/159524))  
- Improve performance of max\_pool3d ([\#157875](https://github.com/pytorch/pytorch/pull/157875))  
- Avoid calling tensor ops in max\_pool3d impl ([\#157874](https://github.com/pytorch/pytorch/pull/157874))
- Move max\_pool2d to Metal for `stride != 1` ([\#157876](https://github.com/pytorch/pytorch/pull/157876))

### docs

### devs

### Untopiced

### not user facing

- Move sparsemps testing from test\_mps to test\_sparse ([\#161852](https://github.com/pytorch/pytorch/pull/161852))  
- Fix unused vars in GridSampler ([\#160850](https://github.com/pytorch/pytorch/pull/160850))  
- Delete `as_strided_tensorimpl_mps` ([\#157772](https://github.com/pytorch/pytorch/pull/157772))  
- Add benchmark for scan with indices ([\#156860](https://github.com/pytorch/pytorch/pull/156860))  
- Fix deduplication of kernels ([\#156843](https://github.com/pytorch/pytorch/pull/156843))  
- Move array def to `c10/metal/common.h` ([\#157746](https://github.com/pytorch/pytorch/pull/157746))  
- Use `simdgroup_size` constexpr ([\#157751](https://github.com/pytorch/pytorch/pull/157751))  
- Delete redundant header ([\#157966](https://github.com/pytorch/pytorch/pull/157966))  
- Move repeated code into helper functions ([\#158178](https://github.com/pytorch/pytorch/pull/158178))  
- Enable test\_aot\_inductor.py tests ([\#155598](https://github.com/pytorch/pytorch/pull/155598))  
- Enable test\_indexing on MPS ([\#158582](https://github.com/pytorch/pytorch/pull/158582))  
- Fix compilation warning in Pooling.metal ([\#158729](https://github.com/pytorch/pytorch/pull/158729))  
- Remove unused `ndArrayFromTensor` ([\#158823](https://github.com/pytorch/pytorch/pull/158823))  
- Fix cpu kernel generation ([\#158350](https://github.com/pytorch/pytorch/pull/158350))  
- Improve tabbing in cpp generation ([\#158351](https://github.com/pytorch/pytorch/pull/158351))  
- Enable more tests ([\#158703](https://github.com/pytorch/pytorch/pull/158703))  
- Fix compile benchmark correctness ([\#159731](https://github.com/pytorch/pytorch/pull/159731))  
- Remove unused size12 variable ([\#159832](https://github.com/pytorch/pytorch/pull/159832))  
- Combine all pre-MacOS14 xfail lists ([\#160228](https://github.com/pytorch/pytorch/pull/160228))
- Add `simd_[arg][max|min]` ([\#158990](https://github.com/pytorch/pytorch/pull/158990))
- Add fused\_rms and sdpa\_mps fallback ops for AOTInductor ([\#156844](https://github.com/pytorch/pytorch/pull/156844))
- Update `avg_pool3d` kernel to use `opmath_t` ([\#161071](https://github.com/pytorch/pytorch/pull/161071))

### security

