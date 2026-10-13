
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
### improvements
### bug fixes
- [XPU][Aten] Fix memory format detection for conv backward overrideable ([#194328](https://github.com/pytorch/pytorch/pull/194328))
### performance
### docs
### devs
### Untopiced
- [Reland] Add IPC support for XPUEvent (#191182) ([#193399](https://github.com/pytorch/pytorch/pull/193399))
- Add IPC support for torch.xpu.Event ([#192495](https://github.com/pytorch/pytorch/pull/192495))
- Register SparseXPU dispatch for aten::linalg_vector_norm ([#194165](https://github.com/pytorch/pytorch/pull/194165))
- Add XPU dispatch for linalg.polar ([#188253](https://github.com/pytorch/pytorch/pull/188253))
- Support torch.xpu.Event in torch.multiprocessing ([#192514](https://github.com/pytorch/pytorch/pull/192514))
- [XPU] Register _spsolve for SparseCsrXPU backend ([#189372](https://github.com/pytorch/pytorch/pull/189372))
- [xpu] Add non split pool support on xpu caching allcoator ([#192033](https://github.com/pytorch/pytorch/pull/192033))
- [xpu] Add use_oom support on xpu caching allcoator ([#192038](https://github.com/pytorch/pytorch/pull/192038))
- [xpu] Remove allocator property from MemPool ([#192041](https://github.com/pytorch/pytorch/pull/192041))
- [xpu] Refine and improve MemPool functionality ([#192048](https://github.com/pytorch/pytorch/pull/192048))
- Refine error message for torch.xpu.utilization() on Xe2+ ([#197210](https://github.com/pytorch/pytorch/pull/197210))
- Unify LazyLevelZero stub macro into a single ZE_STUB ([#197209](https://github.com/pytorch/pytorch/pull/197209))
- [xpu] Improve pyzes error message on Xe2+ ([#197494](https://github.com/pytorch/pytorch/pull/197494))
- [xpu] Compensate for UMD headroom in free_memory on SYCL 2026.2 ([#195987](https://github.com/pytorch/pytorch/pull/195987))
- Add XPU caching allocator checkpoint pool state bindings ([#188259](https://github.com/pytorch/pytorch/pull/188259))
- Refine reusable event usage scope on XPUEvent ([#197396](https://github.com/pytorch/pytorch/pull/197396))
- Revert "Add Reuseable Event support on c10::Event on XPU (#191165)" ([#197401](https://github.com/pytorch/pytorch/pull/197401))
- [inductor][eager] Resolve which distribution provides the importable Triton module ([#195022](https://github.com/pytorch/pytorch/pull/195022))
- [XPU] Allow pure MQA in overrideable SDPA backend without enable_gqa ([#196731](https://github.com/pytorch/pytorch/pull/196731))
- [xpu] Compensate for UMD headroom in free_memory on SYCL 2026.2 ([#195987](https://github.com/pytorch/pytorch/pull/195987))
- [xpu] Support torch.xpu.mem_get_info on pluggable allocator ([#197412](https://github.com/pytorch/pytorch/pull/197412))
- [XPU] Register linalg._powsum and _foreach_powsum.Scalar for XPU ([#189238](https://github.com/pytorch/pytorch/pull/189238))
- [xpu] Correctly filter visiable device to align SYCL ([#198336](https://github.com/pytorch/pytorch/pull/198336))
### not user facing
- Update torch-xpu-ops commit pin ([#193929](https://github.com/pytorch/pytorch/pull/193929))
### security
