
# Release Notes worksheet xpu

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

## xpu
### bc breaking
### deprecation
### new features
- Introduce XPUGraph a runtime optimization feature designed to reduce kernels host overhead on XPU devices, detail in: [design](https://github.com/pytorch/pytorch/issues/162143]) and [usage](https://docs.pytorch.org/docs/2.11/xpu.html#graphs). ([#166285](https://github.com/pytorch/pytorch/pull/166285), [#174041](https://github.com/pytorch/pytorch/pull/174041), [#174351](https://github.com/pytorch/pytorch/pull/174351), [#174059](https://github.com/pytorch/pytorch/pull/174059), [#174046](https://github.com/pytorch/pytorch/pull/174046), [#166843](https://github.com/pytorch/pytorch/pull/166843))

### improvements
- Add `torch.xpu._dump_snapshot` API ([#170186](https://github.com/pytorch/pytorch/pull/170186))
- Add `torch.xpu._record_memory_history` API ([#169559](https://github.com/pytorch/pytorch/pull/169559))
- Add `torch.xpu.memory_snapshot` ([#169442](https://github.com/pytorch/pytorch/pull/169442))
- Add `local_mem_size` to XPU device properties ([#172314](https://github.com/pytorch/pytorch/pull/172314))
- Support `torch.accelerator.get_device_capability` on XPU ([#170747](https://github.com/pytorch/pytorch/pull/170747))
 Enable Triton online softmax kernels on XPU ([#163251](https://github.com/pytorch/pytorch/pull/163251))
- Support woq_int8 Inductor pattern on Intel GPU ([#163615](https://github.com/pytorch/pytorch/pull/163615))
- Add XPU ATen GEMM overloads with output dtype ([#170523](https://github.com/pytorch/pytorch/pull/170523))
- Support `aot_inductor.emit_multi_arch_kernel` on XPU ([#171432](https://github.com/pytorch/pytorch/pull/171432))
- Improve Inductor UT coverage for XPU ([#171280](https://github.com/pytorch/pytorch/pull/171280), [#166376](https://github.com/pytorch/pytorch/pull/166376), [#169181](https://github.com/pytorch/pytorch/pull/169181), [#166504](https://github.com/pytorch/pytorch/pull/166504))
- Enable Triton mm template `decompose_k` choice for XPU ([#170541](https://github.com/pytorch/pytorch/pull/170541))
- Support AOTInductor standalone compile API for XPU ([#171450](https://github.com/pytorch/pytorch/pull/171450))

### bug fixes
- Fix T5 model SDPA pattern matcher on XPU ([#171774](https://github.com/pytorch/pytorch/pull/171774))
- Fix `torch.xpu.memory_allocated` / `torch.xpu.memory_reserved` reporting incorrect memory sizes ([#171453](https://github.com/pytorch/pytorch/pull/171453))

### performance
- Optimize `int_mm` performance on Intel GPU when `mat2` is non-contiguous ([#169555](https://github.com/pytorch/pytorch/pull/169555))
- Enable static Triton kernel launcher for XPU backend to reduce model compilation time ([#169938](https://github.com/pytorch/pytorch/pull/169938))

### docs
- Update XPU Get Started guide with new client GPU and formatting ([#169810](https://github.com/pytorch/pytorch/pull/169810))
- Document previous version of Torch XPU installation ([#174453](https://github.com/pytorch/pytorch/pull/174453))
- Update previous version 2.10 installation in get start xpu ([#176141](https://github.com/pytorch/pytorch/pull/176141))

### devs
- Switch Intel Triton compiled kernel format from `spv` to `zebin` ([#167972](https://github.com/pytorch/pytorch/pull/167972))

### Untopiced
### not user facing
- [test] Enable more Inductor UT for XPU ([#171773](https://github.com/pytorch/pytorch/pull/171773))
- Enable BHSD layout and add deterministic check for SDPA XPU FlashAttention backend ([#170414](https://github.com/pytorch/pytorch/pull/170414))
- Enable tensor descriptor for FlexAttention backward ([#166927](https://github.com/pytorch/pytorch/pull/166927))
- Fix SyclExtension Windows build for oneAPI 2025.3+ breaking change ([#170701](https://github.com/pytorch/pytorch/pull/170701))
### security
