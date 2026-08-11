
# Release Notes worksheet inductor (aoti)

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

## inductor (aoti)
### bc breaking
### deprecation
### new features
- [user-streams][aoti] Support explicit user streams in cpp_wrapper (#182971) ([#182971](https://github.com/pytorch/pytorch/pull/182971))
### improvements
- [AOTI] Support AOTI lazy autotune with dual-wrapper ([#184735](https://github.com/pytorch/pytorch/pull/184735))
- [AOTI] Wire torch.cond and torch.while_loop into AOTI dual-wrapper ([#184736](https://github.com/pytorch/pytorch/pull/184736))
- c10 OptionalArrayRef: add C10_LIFETIMEBOUND to borrowing constructors ([#190076](https://github.com/pytorch/pytorch/pull/190076))
### bug fixes
### performance
### docs
### devs
### Untopiced
- [FakeTensor] Add hinted symbolic storage size metadata ([#183839](https://github.com/pytorch/pytorch/pull/183839))
- [xpu][yaml] Migrate XPU ATen Ops registrations to native_functions.yaml ([#181233](https://github.com/pytorch/pytorch/pull/181233))
- move c10/util/win32-headers.h to torch/headeronly, move aoti usage ([#186962](https://github.com/pytorch/pytorch/pull/186962))
- [PyTorch][AOTI] Env-gated timing/diagnostic logging for the AOTI model-loading pipeline (#186309) ([#186309](https://github.com/pytorch/pytorch/pull/186309))
- [AOTI] Fix S638065: sync default stream after AOTI constant copy (AMD) (#186963) ([#186963](https://github.com/pytorch/pytorch/pull/186963))
- Fix hardcoded CUDA device in OSSProxyExecutor ([#184741](https://github.com/pytorch/pytorch/pull/184741))
- Fix the potential global range overflow issue ([#187307](https://github.com/pytorch/pytorch/pull/187307))
- [AOTInductor] Fix input-handle GPU memory leak when run_impl throws on an input runtime check (#189503) ([#189503](https://github.com/pytorch/pytorch/pull/189503))
- [AOTInductor] Free un-transferred folded constants on error in run_const_fold (#189505) ([#189505](https://github.com/pytorch/pytorch/pull/189505))
- [XPU] Refactor and refine sycl_runtime_wrappers.h (and xpu.cpp) ([#190143](https://github.com/pytorch/pytorch/pull/190143))
- Also include manual AOTI shims in our linter ([#191266](https://github.com/pytorch/pytorch/pull/191266))
### not user facing
- Fix partitioner SymInt bindings for backward ([#185473](https://github.com/pytorch/pytorch/pull/185473))
- Fix partitioner SymInt bindings for backward ([#185473](https://github.com/pytorch/pytorch/pull/185473))
- [inductor] Add TritonMeta TypedDict for the Triton-launch metadata bag ([#188759](https://github.com/pytorch/pytorch/pull/188759))
- [inductor] Group deferred input size asserts ([#184752](https://github.com/pytorch/pytorch/pull/184752))
- [inductor] Add InductorMeta TypedDict for the runtime kernel-config bag ([#189036](https://github.com/pytorch/pytorch/pull/189036))
- Remove obsolete Python wrapper symbol extraction ([#184460](https://github.com/pytorch/pytorch/pull/184460))
- [inductor] Fix inductor dropping ordering dep between effectful ops with different kernel types ([#188301](https://github.com/pytorch/pytorch/pull/188301))
- [XPU][AOTInductor] Fix SIGSEGV in run_const_fold when stream is nullptr ([#189517](https://github.com/pytorch/pytorch/pull/189517))
- [inductor] device-aware cpp-wrapper debug sync (fix ROCm regression) ([#190071](https://github.com/pytorch/pytorch/pull/190071))
- [inductor] drop no-op hipify wrapper on CUDA debug-sync path ([#190472](https://github.com/pytorch/pytorch/pull/190472))
- [HOP] Inductor lowering for switch (1/2) ([#188976](https://github.com/pytorch/pytorch/pull/188976))
- [AOTI] Error-code-check the scatter/index_put fallback shim calls ([#190909](https://github.com/pytorch/pytorch/pull/190909))
- [AOTI] Error-code-check remaining clone/new_tensor_handle shim calls ([#190910](https://github.com/pytorch/pytorch/pull/190910))
- [AOTI] Fix const-graph missing CUDA header in DualWrapper ([#191050](https://github.com/pytorch/pytorch/pull/191050))
- [inductor] Fix inductor dropping ordering dep between effectful ops with different kernel types ([#188301](https://github.com/pytorch/pytorch/pull/188301))
- [XPU] Skip CUDA stream event codegen in AOTI cpp_wrapper for XPU ([#190637](https://github.com/pytorch/pytorch/pull/190637))
### security
