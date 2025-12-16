
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
### deprecation
### new features
### improvements
- [MPS] mps sparse mul op implementation ([#162349](https://github.com/pytorch/pytorch/pull/162349))
- [MPS] mps sparse mul op implementation ([#162349](https://github.com/pytorch/pytorch/pull/162349))
- [MPS] enable cat op for sparse ([#162007](https://github.com/pytorch/pytorch/pull/162007))
- [MPS] enable empty like and unsqueeze for SparseMPS ([#162910](https://github.com/pytorch/pytorch/pull/162910))
- [MPS] sparse mps any ([#162885](https://github.com/pytorch/pytorch/pull/162885))
- [MPS] zeros like, narrow and enable tests ([#163011](https://github.com/pytorch/pytorch/pull/163011))
- [MPS] [Sparse] unique_dim and sparse broadcast ([#163694](https://github.com/pytorch/pytorch/pull/163694))
- [MPS] sparse norm ([#164961](https://github.com/pytorch/pytorch/pull/164961))
- [MPS] sparse mask implementation ([#165102](https://github.com/pytorch/pytorch/pull/165102))
- [MPS] Move `torch.cat` impl to Metal ([#165373](https://github.com/pytorch/pytorch/pull/165373))
- [MPS] sparse matmuls ([#165232](https://github.com/pytorch/pytorch/pull/165232))
- [MPS] slightly faster cholesky ([#165867](https://github.com/pytorch/pytorch/pull/165867))
- [MPS] Add `linalg.householder_product` for MPS ([#166090](https://github.com/pytorch/pytorch/pull/166090))
- [MPS] Refactor `torch.cat` and add fast path for contiguous inputs ([#166556](https://github.com/pytorch/pytorch/pull/166556))
- [MPS] empty matrix x vec mul fix ([#166561](https://github.com/pytorch/pytorch/pull/166561))
- [MPS] SparseMps mv op ([#166708](https://github.com/pytorch/pytorch/pull/166708))
- [MPS] erfinv for sparse mps ([#166711](https://github.com/pytorch/pytorch/pull/166711))
- [MPS] sparse sparse mm ([#167013](https://github.com/pytorch/pytorch/pull/167013))
- [MPS] Add mechanism for reporting asserts from kernels ([#166615](https://github.com/pytorch/pytorch/pull/166615))
- [MPS] SparseMps mv op ([#166708](https://github.com/pytorch/pytorch/pull/166708))
- [MPS] mm out sparse ([#167908](https://github.com/pytorch/pytorch/pull/167908))
- [MPS] permute op for sparse tensors ([#168154](https://github.com/pytorch/pytorch/pull/168154))
- [BE][MPS] Add out-of-bounds checks for embedding_bag ([#168930](https://github.com/pytorch/pytorch/pull/168930))
- [MPS] Add `linalg.lu_solve` and `linalg.lu` ([#167569](https://github.com/pytorch/pytorch/pull/167569))
- [MPS] Migrate `lu_unpack` to Metal and fix `lu_solve` backward ([#168120](https://github.com/pytorch/pytorch/pull/168120))
- [MPS] sparse softmax/logsoftmax ([#169125](https://github.com/pytorch/pytorch/pull/169125))
- [MPS] Migrate remaining `clamp` ops to Metal ([#169478](https://github.com/pytorch/pytorch/pull/169478))
- [MPS] Index select mps sparse ([#169368](https://github.com/pytorch/pytorch/pull/169368))
### bug fixes
- [MPS] Fix `[nan]median` output for empty tensors ([#162846](https://github.com/pytorch/pytorch/pull/162846))
- Fix invalid indices bug for max_unpool2d/3d on MPS ([#163036](https://github.com/pytorch/pytorch/pull/163036))
- [MPS] Fix compile linalg inv ([#163452](https://github.com/pytorch/pytorch/pull/163452))
- [MPS] Fix conv layout handling ([#162776](https://github.com/pytorch/pytorch/pull/162776))
- [MPS] Fix nan behavior in `grid_sampler_3d` ([#163881](https://github.com/pytorch/pytorch/pull/163881))
- [MPSHooks] Release pending command encoder ([#164093](https://github.com/pytorch/pytorch/pull/164093))
- [MPS] Chunk fillBuffer into 4Gb slices ([#164108](https://github.com/pytorch/pytorch/pull/164108))
- [MPS] fix empty dot op crash ([#165237](https://github.com/pytorch/pytorch/pull/165237))
- [MPS] Improve `index_fill_` error handling ([#165594](https://github.com/pytorch/pytorch/pull/165594))
- [MPS] Fix internal assertion in torch.linalg.solve for singular matrices ([#165254](https://github.com/pytorch/pytorch/pull/165254))
- [MPS] Fix SDPA fp16 overflow ([#165961](https://github.com/pytorch/pytorch/pull/165961))
- [EZ][MPS] Improve distribution error checking ([#166425](https://github.com/pytorch/pytorch/pull/166425))
- [MPS] Fix random in-place ops on non-contiguous tensors ([#165267](https://github.com/pytorch/pytorch/pull/165267))
- [MPS] Improve index_select error checking ([#166468](https://github.com/pytorch/pytorch/pull/166468))
- [MPS] Fix crash when max/min ops called for complex types ([#166214](https://github.com/pytorch/pytorch/pull/166214))
- [MPS] Error out when BatchNorm is called for Complex ([#166215](https://github.com/pytorch/pytorch/pull/166215))
- [MPS] Error out when BatchNorm is called for Complex ([#166215](https://github.com/pytorch/pytorch/pull/166215))
- [MPS] Fix crash in BCELoss backwards with reduction="none" and inputs with trailing 1s in shape ([#166786](https://github.com/pytorch/pytorch/pull/166786))
- [MPS] Add Metal complex mm implementation ([#167755](https://github.com/pytorch/pytorch/pull/167755))
- [MPS] addmm complex fix ([#167826](https://github.com/pytorch/pytorch/pull/167826))
- MPS: Fix clamp scalar cache key to store floats in hex representation ([#167777](https://github.com/pytorch/pytorch/pull/167777))
- Fix clamp broadcasting on MPS (Fixes #160734) ([#165058](https://github.com/pytorch/pytorch/pull/165058))
- [MPS] Fix repeat_interleave with slices ([#167961](https://github.com/pytorch/pytorch/pull/167961))
- [MPS] Move `elu` impl to Metal ([#166903](https://github.com/pytorch/pytorch/pull/166903))
- [MPS][1/N] Fix unsupported dtypes error checking for some MPS ops ([#166273](https://github.com/pytorch/pytorch/pull/166273))
- [MPS] fix broadcasting issues for mul on sparse tensors ([#168112](https://github.com/pytorch/pytorch/pull/168112))
- [MPS] Fix dlpack exports/imports for sliced tensors ([#169272](https://github.com/pytorch/pytorch/pull/169272))
- [MPS] Fix dlpack exports/imports for sliced tensors ([#169272](https://github.com/pytorch/pytorch/pull/169272))
- [MPS] Add input/indices shape validation for MaxUnpool{1,2,3}d ([#169261](https://github.com/pytorch/pytorch/pull/169261))
- [MPS][Inductor] Add _print_Where method to MetalExprPrinter for ReflectionPad support ([#169648](https://github.com/pytorch/pytorch/pull/169648))
### performance
### docs
### devs
### Untopiced
- [BE] Use `fmt::format` to define Conv key ([#162925](https://github.com/pytorch/pytorch/pull/162925))
- [mps] Take into account offset ([#163021](https://github.com/pytorch/pytorch/pull/163021))
- [MPS] Add `embedding_bag` forward pass ([#163012](https://github.com/pytorch/pytorch/pull/163012))
- [BUG] MaxUnpool2d/3d should check output dim before accessing its elements ([#163507](https://github.com/pytorch/pytorch/pull/163507))
- [MPS] Compute `offset2bag/bag_size/max_indices` in `_embedding_bag` ([#163281](https://github.com/pytorch/pytorch/pull/163281))
- [SDPA] [MPS] Fixes regression in 2.8.0 for scaled_dot_product_attention using mps ([#163598](https://github.com/pytorch/pytorch/pull/163598))
- [EZ][BE] Fix unused parameter warnings in EmbeddingBag ([#164135](https://github.com/pytorch/pytorch/pull/164135))
- [MPS] Add backward pass for `embedding_bag` ([#163931](https://github.com/pytorch/pytorch/pull/163931))
- [MPS] Update OS version in error message ([#164946](https://github.com/pytorch/pytorch/pull/164946))
- [MPS] Support large tensors in `torch.cat` ([#164416](https://github.com/pytorch/pytorch/pull/164416))
- [MPS] Fix parity between CPU and MPS on singular matrices in linalg.lu_factor ([#165871](https://github.com/pytorch/pytorch/pull/165871))
- [MPS] Move hypot to Metal ([#166216](https://github.com/pytorch/pytorch/pull/166216))
- [MPS] Better error checking for FFT ops ([#166272](https://github.com/pytorch/pytorch/pull/166272))
- [MPS] Move `logaddexp/logaddexp2` to Metal and support complex ([#166670](https://github.com/pytorch/pytorch/pull/166670))
- [MPS] Migrate `clamp.Tensor_out` to Metal ([#169407](https://github.com/pytorch/pytorch/pull/169407))
- [MPS] Fix `test_ops.py` crashes ([#169017](https://github.com/pytorch/pytorch/pull/169017))
### not user facing
- [BE] Delete [Ventura|Sonoma]Ops header ([#162921](https://github.com/pytorch/pytorch/pull/162921))
- [BE] Use `output_t` directly ([#163518](https://github.com/pytorch/pytorch/pull/163518))
- [MPS] test sparse add MPS dtypes so we get proper expected failure ([#163951](https://github.com/pytorch/pytorch/pull/163951))
- [BE] Fix unused parameter warning ([#165272](https://github.com/pytorch/pytorch/pull/165272))
- [MPS] fix comment for normcdf ([#165233](https://github.com/pytorch/pytorch/pull/165233))
- Turn some const variables into constexpr in C++ code ([#165401](https://github.com/pytorch/pytorch/pull/165401))
- [MPS][BE] Fix unused variable warning ([#165726](https://github.com/pytorch/pytorch/pull/165726))
- Turn some const variables into constexpr in C++ code ([#165401](https://github.com/pytorch/pytorch/pull/165401))
- [MPS] Migrate `angle` to Metal ops ([#166210](https://github.com/pytorch/pytorch/pull/166210))
- [BE] Fix metal compilation warnings ([#166315](https://github.com/pytorch/pytorch/pull/166315))
- [MPS] fix large matmul test device ([#166271](https://github.com/pytorch/pytorch/pull/166271))
- Add back Windows and macOS to tensorboard tests ([#166389](https://github.com/pytorch/pytorch/pull/166389))
- [Fix] Optimize max unpooling index validation using aminmax ([#165394](https://github.com/pytorch/pytorch/pull/165394))
- [MPS] Move `dispatch_sync_with_rethrow` to MPSStream ([#167445](https://github.com/pytorch/pytorch/pull/167445))
- [MPS] remove expected failure for a test ([#167922](https://github.com/pytorch/pytorch/pull/167922))
- [MPS] enable sparse mm test ([#168156](https://github.com/pytorch/pytorch/pull/168156))
- [MPS] Modify eps for gradcheck for float32 dtypes ([#168902](https://github.com/pytorch/pytorch/pull/168902))
- [MPS][BugFix] Fix MaxPool2d/MaxPool3d output size validation (Issue #168246) ([#168332](https://github.com/pytorch/pytorch/pull/168332))
### security
