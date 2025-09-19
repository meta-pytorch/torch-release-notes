
# Release Notes worksheet quantization

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

## quantization
### bc breaking
### deprecation
### new features
- Enable cpu fp8 qlinear ([#155678](https://github.com/pytorch/pytorch/pull/155678))
- Enable cpu fp8 qconv ([#157076](https://github.com/pytorch/pytorch/pull/157076))

### improvements
- Avoid getting model device once per node for pt2e quantization flow ([#159901](https://github.com/pytorch/pytorch/pull/159901))
- Fixes bug in implementation of `HistogramObserver` ([#156457](https://github.com/pytorch/pytorch/pull/156457))
- Support `bias=None` for `fbgemm_linear_fp16_weight` CPU op ([#158535](https://github.com/pytorch/pytorch/pull/158535))
- Add Static Dispatch Kernel for `wrapped_fbgemm_linear_fp16_weight` for Sigmoid ([#160451](https://github.com/pytorch/pytorch/pull/160451))


### bug fixes
- Avoid NaN in fp8 output of CPU qlinear and qconv ops ([#160957](https://github.com/pytorch/pytorch/pull/160957))
- Fix segmentation fault when `choose_qparams_optimized` ([#161966](https://github.com/pytorch/pytorch/pull/161966))
### performance
### docs
### devs
- Revamp dtype documentation ([#156087](https://github.com/pytorch/pytorch/pull/156087))
- Use new type statement to fix public API of types ([#158487](https://github.com/pytorch/pytorch/pull/158487))

### Untopiced

### not user facing
- [BE][Ez]: Update ruff to 0.12.2 ([#157937](https://github.com/pytorch/pytorch/pull/157937))
- [BE][3/6] fix typos in test/ ([#157637](https://github.com/pytorch/pytorch/pull/157637))
- Addressing some linter errors ([#158670](https://github.com/pytorch/pytorch/pull/158670))
- Remove the uncessary empty file ([#160728](https://github.com/pytorch/pytorch/pull/160728))
- [BE][13/16] fix typos in torch/ (torch/ao/) ([#156603](https://github.com/pytorch/pytorch/pull/156603))
- [inductor] Add typing to _inductor/ir.py ([#149958](https://github.com/pytorch/pytorch/pull/149958))
- [remove untyped defs] batch 1 ([#157011](https://github.com/pytorch/pytorch/pull/157011))
- [BE][PYFMT] migrate PYFMT for `torch/[a-c]*/` to `ruff format` ([#144554](https://github.com/pytorch/pytorch/pull/144554))
- Fix typo: 'paramter' → 'parameter' in quantization model report test ([#157646](https://github.com/pytorch/pytorch/pull/157646))
- remove allow-untyped-defs from torch/ao/nn/quantized/modules/rnn.py ([#157234](https://github.com/pytorch/pytorch/pull/157234))
- Update'unit_batch_dynamic_prepacked' tests to use ASSERT_NEAR instead of ASSERT_EQ (#157860) ([#157861](https://github.com/pytorch/pytorch/pull/157861))
- Remove pytorch quant docs since we are moving to torchao ([#157766](https://github.com/pytorch/pytorch/pull/157766))
- remove allow-untyped-defs from torch/ao/nn/intrinsic/quantized/dynamic/modules/linear_relu.py ([#157848](https://github.com/pytorch/pytorch/pull/157848))
- [Inductor][Float8] Add float8_e4m3fn into assertion dtype list. ([#157684](https://github.com/pytorch/pytorch/pull/157684))
- Avoid AOTAutogradCache.load in stack trace on cache miss path ([#158149](https://github.com/pytorch/pytorch/pull/158149))
- Inline dispatch_and_compile into its call site. ([#158150](https://github.com/pytorch/pytorch/pull/158150))
- Pipeline _create_aot_dispatcher_function ([#158173](https://github.com/pytorch/pytorch/pull/158173))
- Hoist choose_dispatcher to top level, remove unnecessary returns ([#158176](https://github.com/pytorch/pytorch/pull/158176))
- Introduce stages to aot_dispatch ([#158213](https://github.com/pytorch/pytorch/pull/158213))
- Move functions from torch._functorch.aot_autograd that are not frontend functions to frontend_utils ([#158251](https://github.com/pytorch/pytorch/pull/158251))
- [BE][3/5] fix typos in aten/ (aten/src/ATen/native/) ([#157552](https://github.com/pytorch/pytorch/pull/157552))
- [BE] Fix extra-semi warnings ([#158730](https://github.com/pytorch/pytorch/pull/158730))
- [BE] fix remaining flake8 v7 warnings ([#159044](https://github.com/pytorch/pytorch/pull/159044))
- [BE][PYFMT] migrate PYFMT for `test/[i-z]*/` to `ruff format` ([#144556](https://github.com/pytorch/pytorch/pull/144556))
- Ensure export joint with descriptors + compile works ([#159337](https://github.com/pytorch/pytorch/pull/159337))
- [CPU] Fix bias dtype issue for FP8 qlinear ([#159125](https://github.com/pytorch/pytorch/pull/159125))
- Use boxed_nop_preserve_node_meta for aot_export_joint_with_descriptors ([#159545](https://github.com/pytorch/pytorch/pull/159545))
- unskipped mobilenet_v3 quantization and mobilenet_v2 quantization plus tests from https://github.com/pytorch/pytorch/issues/125438 ([#157786](https://github.com/pytorch/pytorch/pull/157786))
- [BE][PYFMT] migrate PYFMT for `torch/[p-z]*/` to `ruff format` ([#144552](https://github.com/pytorch/pytorch/pull/144552))
- Fix qembeddingbag_byte_prepack_meta to use sym_sizes ([#159985](https://github.com/pytorch/pytorch/pull/159985))
- Using std::make_unique<T>() instead of unique<T>(new T()) ([#160723](https://github.com/pytorch/pytorch/pull/160723))
- Using std::vector or c10::SmallVector instead of CArray ([#160959](https://github.com/pytorch/pytorch/pull/160959))
- Enable more nightly tests on s390x ([#160893](https://github.com/pytorch/pytorch/pull/160893))
### security
