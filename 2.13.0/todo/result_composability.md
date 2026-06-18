
# Release Notes worksheet composability

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

## composability
### bc breaking
### deprecation
### new features
### improvements
### bug fixes
### performance
### docs
### devs
### Untopiced
- Formalize inplace operators with Tag.inplace ([#181099](https://github.com/pytorch/pytorch/pull/181099))
- Support inplace-tagged custom operators in torch.compile ([#181100](https://github.com/pytorch/pytorch/pull/181100))
- Fix typos in comments and docstrings across distributed, decomp, and fx modules ([#181979](https://github.com/pytorch/pytorch/pull/181979))
- Fix typos in comments and error messages ([#181965](https://github.com/pytorch/pytorch/pull/181965))
- Fix torch.empty(..., out=...) shape validation under torch.compile ([#182349](https://github.com/pytorch/pytorch/pull/182349))
- Fix frac decomposition signed zero handling ([#183640](https://github.com/pytorch/pytorch/pull/183640))
- Fix pad_sequence mixed dtype padding decomp ([#184173](https://github.com/pytorch/pytorch/pull/184173))
- Fix istft fake tensor length padding ([#184532](https://github.com/pytorch/pytorch/pull/184532))
- Fix unfold_backward decomposition for overlapping windows ([#183996](https://github.com/pytorch/pytorch/pull/183996))
- Use int32 indices for grid sampler lowering ([#184269](https://github.com/pytorch/pytorch/pull/184269))
- Fix Inductor split Tensor decomposition ([#184134](https://github.com/pytorch/pytorch/pull/184134))
- fix flash sdpa activation dtype mismatched between meta and cpu implementation ([#185573](https://github.com/pytorch/pytorch/pull/185573))
- Fix Inductor embedding negative indices ([#184107](https://github.com/pytorch/pytorch/pull/184107))
- Preserve 5D nearest upsample decomposition layout ([#184553](https://github.com/pytorch/pytorch/pull/184553))
- change most HOPs to use @register_fake instad of py_impl(FakeTensorMode) ([#186247](https://github.com/pytorch/pytorch/pull/186247))
- Fix addmv decomposition dtype validation ([#184140](https://github.com/pytorch/pytorch/pull/184140))
- Preserve aten.hardtanh meta semantics for export ([#185298](https://github.com/pytorch/pytorch/pull/185298))
- Validate MaxUnpool output sizes ([#184706](https://github.com/pytorch/pytorch/pull/184706))
- Fix _fused_dropout decomposition at keep probability zero ([#184979](https://github.com/pytorch/pytorch/pull/184979))
- Add op_overloads to OpOverloadPacket and use it ([#182993](https://github.com/pytorch/pytorch/pull/182993))
### not user facing
- [decomp] Fix addmm decomposition crash with out_dtype under FakeTensorMode ([#179634](https://github.com/pytorch/pytorch/pull/179634))
- [decomp] Fix torch.split decomposition for empty dim with nonzero split_size ([#181493](https://github.com/pytorch/pytorch/pull/181493))
- [PyTorch] Update _cslt_sparse_mm meta registration for hipSPARSELt (#181609) ([#181609](https://github.com/pytorch/pytorch/pull/181609))
- Fix fill_ meta to validate value tensor is 0-dimensional ([#179363](https://github.com/pytorch/pytorch/pull/179363))
- Fix torch.distribution.Gamma in compile ([#174090](https://github.com/pytorch/pytorch/pull/174090))
- Fix _weight_int8pack_mm meta to validate inner dims and scales ([#179364](https://github.com/pytorch/pytorch/pull/179364))
- Fix miopen_batch_norm meta save_mean/save_var dtype ([#179365](https://github.com/pytorch/pytorch/pull/179365))
- Fix torch.compile wrong output shape for norm() with negative dim ([#182405](https://github.com/pytorch/pytorch/pull/182405))
- [custom-ops] Enable opcheck stride checking for CPU tensors ([#183002](https://github.com/pytorch/pytorch/pull/183002))
- Fix for #183002 ([#183353](https://github.com/pytorch/pytorch/pull/183353))
- [meta tensors] Fix conv2d kernel size validation for meta and symbolic shapes ([#180448](https://github.com/pytorch/pytorch/pull/180448))
- [compile] add _transformer_encoder_layer_fwd fake tensor support ([#183916](https://github.com/pytorch/pytorch/pull/183916))
- Fix reflection/replication pad stride mismatch under torch.compile ([#179837](https://github.com/pytorch/pytorch/pull/179837))
- [aot_autograd] Genericize graphsafe RNG to support non-CUDA device backends ([#182391](https://github.com/pytorch/pytorch/pull/182391))
- [xpu][fix] Fix reflection/replication pad output memory format to match eager behavior ([#184484](https://github.com/pytorch/pytorch/pull/184484))
- Use torch.var_mean to fuse paired var/mean reductions ([#184843](https://github.com/pytorch/pytorch/pull/184843))
- Fix symbolic float lp_pool2d compilation ([#184000](https://github.com/pytorch/pytorch/pull/184000))
- Use torch.sigmoid() in silu_backward decomposition ([#185041](https://github.com/pytorch/pytorch/pull/185041))
- [DDE] Fix data-dependent errors in pooling meta functions ([#183774](https://github.com/pytorch/pytorch/pull/183774))
- [decomp] Compare in opmath in hardtanh_backward ([#185840](https://github.com/pytorch/pytorch/pull/185840))
- [torch] use sym_eq for unbacked-safe shape compare in is_same_shape (#184943) ([#184943](https://github.com/pytorch/pytorch/pull/184943))
- Fix index_copy decomposition shape checks ([#184338](https://github.com/pytorch/pytorch/pull/184338))
- Fix LSTM export hidden state metadata ([#185716](https://github.com/pytorch/pytorch/pull/185716))
- Fix private convolution fake symint handling ([#185081](https://github.com/pytorch/pytorch/pull/185081))
- Mark graphsafe_run_with_rng_state as cacheable for FxGraphCache ([#185562](https://github.com/pytorch/pytorch/pull/185562))
- Preserve strides in meta zero ([#185360](https://github.com/pytorch/pytorch/pull/185360))
- fix runtime for non_overlapping_and_dense ([#186785](https://github.com/pytorch/pytorch/pull/186785))
### security
