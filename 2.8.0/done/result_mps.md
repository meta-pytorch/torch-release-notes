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

### deprecation

### new features

### Improvements

- Add support for operations: `i0e`, `i1e,` `torch.special.bessel_[jy][01], modified_bessel_i1, bicubic2d_aa, modified_bessel_k0, modified_bessel_k1, scaled_modified_bessel_k0, scaled_modified_bessel_k1, nanmedian, hermite_polynomial_h, hermite_polynomial_he, rsub, index_copy, hardshrink, upsample_trilinear, erfc, isin_Scalar_Tensor, isin_Tensor_Scalar, chebyshev_polynomial_t, col2im, nearest_3d, chebyshev_polynomial_[uvw]` ([\#149174](https://github.com/pytorch/pytorch/pull/149174), [\#149203](https://github.com/pytorch/pytorch/pull/149203) [\#149123](https://github.com/pytorch/pytorch/pull/149123), [\#149368](https://github.com/pytorch/pytorch/pull/149368), [\#149378](https://github.com/pytorch/pytorch/pull/149378), [\#149563](https://github.com/pytorch/pytorch/pull/149563), [\#149687](https://github.com/pytorch/pytorch/pull/149687), [\#149705](https://github.com/pytorch/pytorch/pull/149705), [\#149783](https://github.com/pytorch/pytorch/pull/149783), [\#149407](https://github.com/pytorch/pytorch/pull/149407)/[\#149680](https://github.com/pytorch/pytorch/pull/149680), [\#150279](https://github.com/pytorch/pytorch/pull/150279), [\#151754](https://github.com/pytorch/pytorch/pull/151754), [\#153786](https://github.com/pytorch/pytorch/pull/153786), [\#154326](https://github.com/pytorch/pytorch/pull/154326), [\#155304](https://github.com/pytorch/pytorch/pull/155304), [\#156263](https://github.com/pytorch/pytorch/pull/156263), [\#155382](https://github.com/pytorch/pytorch/pull/155382), [\#154010](https://github.com/pytorch/pytorch/pull/154010), [\#149816](https://github.com/pytorch/pytorch/pull/149816), [\#152282](https://github.com/pytorch/pytorch/pull/152282), [\#156090](https://github.com/pytorch/pytorch/pull/156090), [\#150060](https://github.com/pytorch/pytorch/pull/150060))  
    
    
- Add MPSInductor support for:  `modified_bessel_i0, pow, log2, floorToInt, hermite_polynomial_he, modified_bessel_k1, i0e, i1e,` ([\#149342](https://github.com/pytorch/pytorch/pull/149342), [\#151449](https://github.com/pytorch/pytorch/pull/151449), [\#151754](https://github.com/pytorch/pytorch/pull/151754), [\#149687](https://github.com/pytorch/pytorch/pull/149687), [\#149180](https://github.com/pytorch/pytorch/pull/149180), [\#149221](https://github.com/pytorch/pytorch/pull/149221))  
    
- Extending dtype support for:  
  * index\_put to half precision floats ([\#151869](https://github.com/pytorch/pytorch/pull/151869))  
  * ConvTranspose3D for FP32 and complex ([\#154696](https://github.com/pytorch/pytorch/pull/154696))  
  * Extend index\_copy support to complex dtypes ([\#154671](https://github.com/pytorch/pytorch/pull/154671))  
  * Extend torch.special. to integer dtypes ([\#155002](https://github.com/pytorch/pytorch/pull/155002))  
  * Enable log1p and sigmoid for int64 ([\#151791](https://github.com/pytorch/pytorch/pull/151791))  
- Support ArgumentBuffer bindings from C++/Python ([\#150780](https://github.com/pytorch/pytorch/pull/150780))  
- Migrate div rounding modes ([\#152758](https://github.com/pytorch/pytorch/pull/152758))  
- Support numpy scalars handling in MPSInductor ([\#153598](https://github.com/pytorch/pytorch/pull/153598))  
- Improve error message for CUDAGuardImpl, MPSGuardImpl, XPUGuardImpl ([\#149838](https://github.com/pytorch/pytorch/pull/149838))  
- More descriptive error message for torch.nanmean() with complex dtypes ([\#153252](https://github.com/pytorch/pytorch/pull/153252))  
- Grad Scaler implementation ([\#150255](https://github.com/pytorch/pytorch/pull/150255))  
- Add error message with assert to topK if ndims() \- dim \> 4 ([\#155475](https://github.com/pytorch/pytorch/pull/155475))  
- Activation kernels: do compute at float precision ([\#155735](https://github.com/pytorch/pytorch/pull/155735))


### Bug fixes

- Fix codegen for nested multistage reductions in MPSInductor ([\#154578](https://github.com/pytorch/pytorch/pull/154578))  
- Fix torch.arange bound validation for large float inputs ([\#154320](https://github.com/pytorch/pytorch/pull/154320))  
- Fix larger-than-threadgroup Welford reductions ([\#151152](https://github.com/pytorch/pytorch/pull/151152))  
- Specify `max_total_threads_per_threadgroup` ([\#150247](https://github.com/pytorch/pytorch/pull/150247))  
- Fix `determine_backend_memory_format` logic ([\#151042](https://github.com/pytorch/pytorch/pull/151042))  
- Fix silent correctness in bitcast ([\#151272](https://github.com/pytorch/pytorch/pull/151272))  
- Adjust memory format detection ([\#151288](https://github.com/pytorch/pytorch/pull/151288))  
- Make fused rms\_norm traceable ([\#150661](https://github.com/pytorch/pytorch/pull/150661))  
- Allow isin for mixed types ([\#151600](https://github.com/pytorch/pytorch/pull/151600))  
- Implement `atomic_add` store mode ([\#151871](https://github.com/pytorch/pytorch/pull/151871))  
- Make sure sizevars are computed ([\#152436](https://github.com/pytorch/pytorch/pull/152436))  
- Fix lerp for complex numbers ([\#152479](https://github.com/pytorch/pytorch/pull/152479))  
- Fix `truncdiv` implementation ([\#152788](https://github.com/pytorch/pytorch/pull/152788))  
- Fix multistage reduction suffixes ([\#153362](https://github.com/pytorch/pytorch/pull/153362))  
- Fix float64 scalar tensor handling ([\#153582](https://github.com/pytorch/pytorch/pull/153582))  
- Fix conv\_transpose channels last ([\#153787](https://github.com/pytorch/pytorch/pull/153787))  
- Fix indexing calculation ([\#153997](https://github.com/pytorch/pytorch/pull/153997))  
- Fix memory leaks in mps\_linear\_nograph ([\#154765](https://github.com/pytorch/pytorch/pull/154765))  
- Fix complex scalar binding to Metal tensors ([\#155184](https://github.com/pytorch/pytorch/pull/155184))  
- Fix unary/binary ops for 2\*\*32+ elem tensors ([\#155183](https://github.com/pytorch/pytorch/pull/155183))  
- Fix remainder implementation for int types ([\#155891](https://github.com/pytorch/pytorch/pull/155891))  
- Fix bug in 3d coords calculation ([\#156375](https://github.com/pytorch/pytorch/pull/156375))  
- Fix nested loop var elimination ([\#156566](https://github.com/pytorch/pytorch/pull/156566))  
- Fix multistage reduction check ([\#156567](https://github.com/pytorch/pytorch/pull/156567))  
- Fix type promotion for `torch.floor_divide` ([\#149233](https://github.com/pytorch/pytorch/pull/149233))  
- Add assertion to align with cuda ([\#153233](https://github.com/pytorch/pytorch/pull/153233))  
- Fix inverse bug for N\>1024 ([\#146754](https://github.com/pytorch/pytorch/pull/146754))  
- Fix where ([\#151176](https://github.com/pytorch/pytorch/pull/151176))  
- Fix logit output for half/bfloat ([\#151282](https://github.com/pytorch/pytorch/pull/151282))  
- Fix ICE for entr bool instantiation on M1/M2 ([\#152204](https://github.com/pytorch/pytorch/pull/152204))  
- Fix the approximation of polygamma for n \== 0\. ([\#152214](https://github.com/pytorch/pytorch/pull/152214))  
- Fix memory leak in SDPA float32 ([\#152371](https://github.com/pytorch/pytorch/pull/152371))  
- Fix metal ops with different dtypes ([\#149974](https://github.com/pytorch/pytorch/pull/149974))


### Performance

- Layernorm forward speedup with new kernel  ([\#152010](https://github.com/pytorch/pytorch/pull/152010))  
- Disable mm/bmm decompositions ([\#150541](https://github.com/pytorch/pytorch/pull/150541))  
- Speedup `sum`/`prod` reductions ([\#150566](https://github.com/pytorch/pytorch/pull/150566))  
- Implement metal kernel for basic MPS arithmetic ops using TensorIterator ([\#147644](https://github.com/pytorch/pytorch/pull/147644))  
- Replace indexed with strided flavor ([\#149730](https://github.com/pytorch/pytorch/pull/149730))  
- SDPA specialized kernels ([\#152781](https://github.com/pytorch/pytorch/pull/152781))  
- Move mps\_linear forward to use MPS kernels directly instead of MPSGraph ([\#152210](https://github.com/pytorch/pytorch/pull/152210))


### docs

### devs

### Untopiced

### Not user facing

- Migrate following ops to TensorIterator: `lerp.Scalar.out, complex_mul, mul, neg/exp/exp2/rsqrt/tanh/sin/cos/tan/sinc` ([\#152514](https://github.com/pytorch/pytorch/pull/152514), [\#149728](https://github.com/pytorch/pytorch/pull/149728), [\#152515](https://github.com/pytorch/pytorch/pull/152515), [\#152876](https://github.com/pytorch/pytorch/pull/152876))  
    
- Migrate following ops to use Metal kernels: `hardsigmoid, hardswish, softshrink, log1p/log10/log2/log, add/sub, div, sigmoid, abs, expm1, leaky_relu, sinh/cosh, fmod/remainder` ([\#155462](https://github.com/pytorch/pytorch/pull/155462), [\#155479](https://github.com/pytorch/pytorch/pull/155479), [\#155586](https://github.com/pytorch/pytorch/pull/155586), [\#154936](https://github.com/pytorch/pytorch/pull/154936)/[\#153398](https://github.com/pytorch/pytorch/pull/153398), [\#152510](https://github.com/pytorch/pytorch/pull/152510), [\#152743](https://github.com/pytorch/pytorch/pull/152743), [\#155080](https://github.com/pytorch/pytorch/pull/155080), [\#155474](https://github.com/pytorch/pytorch/pull/155474), [\#155611](https://github.com/pytorch/pytorch/pull/155611), [\#155571](https://github.com/pytorch/pytorch/pull/155571), [\#154465](https://github.com/pytorch/pytorch/pull/154465), [\#154280](https://github.com/pytorch/pytorch/pull/154280))  
    
- Implement scan metal kernels ([\#156100](https://github.com/pytorch/pytorch/pull/156100))  
- Migrate `torch.complex` to binary\_functor ([\#149727](https://github.com/pytorch/pytorch/pull/149727))  
- Migrate `bitwise_not` to unary operator ([\#151460](https://github.com/pytorch/pytorch/pull/151460))  
- Do not dispatch empty kernels ([\#152663](https://github.com/pytorch/pytorch/pull/152663))  
- Speed-up time spent in generating shaped str keys ([\#152202](https://github.com/pytorch/pytorch/pull/152202))  
- Use `auto` in MPS codebase more ([\#150000](https://github.com/pytorch/pytorch/pull/150000))  
- Preserve in/out dtypes in binary\_op name ([\#150024](https://github.com/pytorch/pytorch/pull/150024))  
- Reuse format\_size utils ([\#149383](https://github.com/pytorch/pytorch/pull/149383))  
- Move atomic ops to c10/metal/atomic.h ([\#151868](https://github.com/pytorch/pytorch/pull/151868))  
- Move common binary ops macros to indexing.h ([\#149263](https://github.com/pytorch/pytorch/pull/149263))  
- Fix i0e test to test the correct function. ([\#149204](https://github.com/pytorch/pytorch/pull/149204))  
- Reuse `result_of` from `c10/metal/utils.h` ([\#149262](https://github.com/pytorch/pytorch/pull/149262))  
- Add inline to function definition. ([\#149704](https://github.com/pytorch/pytorch/pull/149704))  
- Get rid of `supports_dense` flag ([\#149729](https://github.com/pytorch/pytorch/pull/149729))  
- Move `polar`/`complex` to stubs ([\#149752](https://github.com/pytorch/pytorch/pull/149752))  
- Add `c10/metal/common.h` ([\#149955](https://github.com/pytorch/pytorch/pull/149955))  
- Fix signed/unsigned comparison warning ([\#150246](https://github.com/pytorch/pytorch/pull/150246))  
- Test bf16 perf of few unary and binary ops ([\#150382](https://github.com/pytorch/pytorch/pull/150382))  
- Benchmark reduction ops ([\#150452](https://github.com/pytorch/pytorch/pull/150452))  
- Implement reduction caching ([\#151151](https://github.com/pytorch/pytorch/pull/151151))  
- Start benchmarking compile results ([\#151155](https://github.com/pytorch/pytorch/pull/151155))  
- Move ops modifiers to testing utils so other tests can reuse ([\#151781](https://github.com/pytorch/pytorch/pull/151781))  
- Implement \_print\_Trunc\_to\_Int ([\#151964](https://github.com/pytorch/pytorch/pull/151964))  
- Delete unused lerp functors ([\#152443](https://github.com/pytorch/pytorch/pull/152443))  
- Introduce `c10::metal::mul` ([\#152466](https://github.com/pytorch/pytorch/pull/152466))  
- Extend typecasted op support to complex dtypes ([\#152504](https://github.com/pytorch/pytorch/pull/152504))  
- Remove `exec_binary_alpha_kernel` ([\#152485](https://github.com/pytorch/pytorch/pull/152485))  
- Pass `alpha` by reference ([\#152737](https://github.com/pytorch/pytorch/pull/152737))  
- Use `squeeze`/`unsqueeze` in Linear ([\#153288](https://github.com/pytorch/pytorch/pull/153288))  
- Speedup test\_large\_bmm ([\#153562](https://github.com/pytorch/pytorch/pull/153562))  
- Add GoogleFnet, YituTechConvBert and Super\_SloMo to benchmarks ([\#153658](https://github.com/pytorch/pytorch/pull/153658))  
- Cleanup log ops migration ([\#153727](https://github.com/pytorch/pytorch/pull/153727))  
- Replace size() checks with empty() ([\#153805](https://github.com/pytorch/pytorch/pull/153805))  
- Delete unused `complex_mul_out` ([\#154175](https://github.com/pytorch/pytorch/pull/154175))  
- Delete `complex_div` ([\#154275](https://github.com/pytorch/pytorch/pull/154275))  
- Code deduplication ([\#154290](https://github.com/pytorch/pytorch/pull/154290))  
- Do not copy sizes/strides unnecesserily ([\#154670](https://github.com/pytorch/pytorch/pull/154670))  
- Define `REGISTER_UNARY_TI_DISPATCH` ([\#155081](https://github.com/pytorch/pytorch/pull/155081))  
- Better error messages ([\#155150](https://github.com/pytorch/pytorch/pull/155150))  
- Some refactor in preparation for 64-bit iterators ([\#155178](https://github.com/pytorch/pytorch/pull/155178))  
- Parametrize `test_scaled_dot_product_attention_autocast` ([\#155005](https://github.com/pytorch/pytorch/pull/155005))  
- Extend ndim\_and\_dtypes to 4 elements ([\#155272](https://github.com/pytorch/pytorch/pull/155272))  
- Enable optimizer tests affected by addcdiv ([\#155437](https://github.com/pytorch/pytorch/pull/155437))  
- Enable RProp test for non-contiguous ([\#155439](https://github.com/pytorch/pytorch/pull/155439))  
- Refactor round\_decimals shader code to leverage new macro ([\#155316](https://github.com/pytorch/pytorch/pull/155316))  
- Fix binary builds ([\#155733](https://github.com/pytorch/pytorch/pull/155733))  
- Fix tests to use common function ([\#155752](https://github.com/pytorch/pytorch/pull/155752))  
- Fix dynamic dispatch size ([\#155582](https://github.com/pytorch/pytorch/pull/155582))  
- Use cpp sym-expr printer ([\#155646](https://github.com/pytorch/pytorch/pull/155646))  
- Add benchmark for scan operations ([\#156241](https://github.com/pytorch/pytorch/pull/156241))  
- Refactor core matmul logic into matmul\_core ([\#155969](https://github.com/pytorch/pytorch/pull/155969))

### security

