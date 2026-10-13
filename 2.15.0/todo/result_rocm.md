
# Release Notes worksheet rocm

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

## rocm
### bc breaking
### deprecation
### new features
### improvements
### bug fixes
- [ROCm] Reject unregistered host pointers in getDeviceFromPtr ([#192193](https://github.com/pytorch/pytorch/pull/192193))
- [ROCm] Build CK flash dropout seed tensors from host values ([#197563](https://github.com/pytorch/pytorch/pull/197563))
### performance
### docs
### devs
### Untopiced
- [ROCm] Fix "Ignoring invalid value for boolean flag AMD_SERIALIZE_KERNEL: 3" ([#186652](https://github.com/pytorch/pytorch/pull/186652))
- Disabling Origami for ROCm 10.0 and above. ([#193843](https://github.com/pytorch/pytorch/pull/193843))
- Fix pdist and cdist launch failure past 2^24 outputs on ROCm ([#188006](https://github.com/pytorch/pytorch/pull/188006))
- [ROCm] Fix CK SDPA flash attention on gfx1200/gfx1201 (RDNA4) ([#188114](https://github.com/pytorch/pytorch/pull/188114))
- [ROCm] Guard native BMM outer-product launches against the HIP work-item limit ([#194131](https://github.com/pytorch/pytorch/pull/194131))
- [ROCm] Add document SDPA BSHD layout performance on gfx1151 iGPU ([#190771](https://github.com/pytorch/pytorch/pull/190771))
- [ROCm] Fall back to native RNN when MIOpen RNN fails at runtime ([#189658](https://github.com/pytorch/pytorch/pull/189658))
- [ROCm] Fix CK SDPA flash attention on gfx1200/gfx1201 (RDNA4) ([#188114](https://github.com/pytorch/pytorch/pull/188114))
- [ROCm][inductor] gfx1250 TDM support for dense mm/addmm ([#191166](https://github.com/pytorch/pytorch/pull/191166))
- [ROCm] Check AOTriton attention errors at the originating callsite ([#194100](https://github.com/pytorch/pytorch/pull/194100))
- [ROCm] Cache BMM outer-product warp size ([#196368](https://github.com/pytorch/pytorch/pull/196368))
- [ROCm] Map hsa_queue kineto metadata and unskip its parity test ([#196487](https://github.com/pytorch/pytorch/pull/196487))
- [ROCm] Update GDS doc to include hipFile ([#195478](https://github.com/pytorch/pytorch/pull/195478))
- [ROCm][inductor] gfx1250 TDM support for generic descriptor codegen ([#196525](https://github.com/pytorch/pytorch/pull/196525))
- [ROCm] Increase default hipBLASLt workspace to 80 MiB ([#197201](https://github.com/pytorch/pytorch/pull/197201))
- Move the miopen_batch_norm decomposition to the core table ([#197160](https://github.com/pytorch/pytorch/pull/197160))
- [ROCm] Allow all scaled_mm layouts for fp8 tensorwise scaling  ([#196884](https://github.com/pytorch/pytorch/pull/196884))
- [ROCm] Free rocFFT plans ([#197425](https://github.com/pytorch/pytorch/pull/197425))
- [ROCm] Bump AOTriton to 0.14b ([#197747](https://github.com/pytorch/pytorch/pull/197747))
- [ROCm] Build and test the cublas and cusolver cpp extensions ([#197816](https://github.com/pytorch/pytorch/pull/197816))
- [ROCm] Add MI355X device info entry ([#196365](https://github.com/pytorch/pytorch/pull/196365))
- [ROCm] Restore the caller's device in ~CUDAGraph ([#197903](https://github.com/pytorch/pytorch/pull/197903))
- [ROCm][inductor] gfx1250 TDM support for flex attention forward and decode ([#197329](https://github.com/pytorch/pytorch/pull/197329))
- [ROCm] Return early from memory-efficient attention on empty inputs and unskip its tests ([#198022](https://github.com/pytorch/pytorch/pull/198022))
- [ROCm] Bump AOTriton to 0.14b ([#197747](https://github.com/pytorch/pytorch/pull/197747))
- [ROCm] Bump AOTriton to 0.14.1b ([#197747](https://github.com/pytorch/pytorch/pull/197747))
- [ROCm] Honor depthwise_kernel="native" where the native kernel applies ([#198221](https://github.com/pytorch/pytorch/pull/198221))
- [ROCm] Bump AOTriton to 0.14.2b ([#197747](https://github.com/pytorch/pytorch/pull/197747))
- Note MI300 accuracy issues in set_float32_matmul_precision ([#190736](https://github.com/pytorch/pytorch/pull/190736))
- [ROCm] Preserve amdsmi library selection during import ([#197482](https://github.com/pytorch/pytorch/pull/197482))
- [ROCm] Always eagerly allocate hipBLAS(Lt) workspaces ([#196920](https://github.com/pytorch/pytorch/pull/196920))
- [ROCm] Stop hipify from rewriting std::max/std::min to ::max/::min ([#199444](https://github.com/pytorch/pytorch/pull/199444))
- [ROCm] Make single-block topk gather deterministic ([#199425](https://github.com/pytorch/pytorch/pull/199425))
- [Inductor][ROCm] Fall back for BF16 atomic accumulation ([#198199](https://github.com/pytorch/pytorch/pull/198199))
### not user facing
- [ROCm] Add gfx950 pre-swizzled MX FP4/FP8 scale layout for scaled_mm ([#190290](https://github.com/pytorch/pytorch/pull/190290))
- [ROCm] Add gfx950 pre-swizzled MX FP4/FP8 scale layout for scaled_mm ([#190290](https://github.com/pytorch/pytorch/pull/190290))
### security
