
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
- Remove the `allocator` property from `torch.xpu.MemPool` to match CUDA; `pool.allocator` now raises `AttributeError` ([#192041](https://github.com/pytorch/pytorch/pull/192041))

  ```python
  alloc = my_allocator  # keep your own reference
  ```

### deprecation
### new features
- `torch.xpu.Event(interprocess=True)` can now be shared across processes through `torch.multiprocessing` or `ipc_handle()` / `from_ipc_handle()`, matching `torch.cuda.Event` ([#192495](https://github.com/pytorch/pytorch/pull/192495), [#193399](https://github.com/pytorch/pytorch/pull/193399), [#192514](https://github.com/pytorch/pytorch/pull/192514))

### improvements
- Add `no_split` and `use_on_oom` support to `torch.xpu.MemPool` ([#192048](https://github.com/pytorch/pytorch/pull/192048), [#192033](https://github.com/pytorch/pytorch/pull/192033), [#192038](https://github.com/pytorch/pytorch/pull/192038))
- Support `torch.xpu.mem_get_info` with a pluggable XPU allocator ([#197412](https://github.com/pytorch/pytorch/pull/197412))
- Add XPU support for `linalg.polar`, `linalg.qr` (out), `geqrf`, `linalg.householder_product`, `sparse.spsolve` and sparse `vector_norm` ([#188253](https://github.com/pytorch/pytorch/pull/188253), [#187564](https://github.com/pytorch/pytorch/pull/187564), [#189372](https://github.com/pytorch/pytorch/pull/189372), [#194165](https://github.com/pytorch/pytorch/pull/194165), [#189238](https://github.com/pytorch/pytorch/pull/189238))
- Use the XPU SDPA backend for multi-query attention without `enable_gqa=True` ([#196731](https://github.com/pytorch/pytorch/pull/196731))
### bug fixes
- Fix wrong XPU results in `conv1d` backward ([#194328](https://github.com/pytorch/pytorch/pull/194328)), batch norm, `fft` on empty batches, norm reductions ([#193929](https://github.com/pytorch/pytorch/pull/193929)), and bf16/fp16 `addmm`/`baddbmm` with `alpha`/`beta` ([#174864](https://github.com/pytorch/pytorch/pull/174864))
- Fix `torch.xpu.mem_get_info` under-reporting free memory on Xe2 and later ([#195987](https://github.com/pytorch/pytorch/pull/195987))
- Fix XPU device indices not matching SYCL's order when an integrated GPU is listed first ([#198336](https://github.com/pytorch/pytorch/pull/198336))
- Fix oneDNN SDPA with grouped-query attention and head-broadcast masks ([#194973](https://github.com/pytorch/pytorch/pull/194973))
### performance
- Faster SDPA training ([#195419](https://github.com/pytorch/pytorch/pull/195419))
### docs
- Clarify Intel GPU prerequisites ([#198820](https://github.com/pytorch/pytorch/pull/198820))
### devs
### Untopiced
### not user facing
- Unify LazyLevelZero stub macro into a single ZE_STUB ([#197209](https://github.com/pytorch/pytorch/pull/197209))
- Add XPU caching allocator checkpoint pool state bindings ([#188259](https://github.com/pytorch/pytorch/pull/188259))
- Improve error messages from `torch.xpu.utilization()` and other Level Zero Sysman queries on Xe2 and later GPUs when the process lacks the required permissions ([#197210](https://github.com/pytorch/pytorch/pull/197210), [#197494](https://github.com/pytorch/pytorch/pull/197494)) (cut for length)
- Fix "An event cannot be enqueued for signaling or waiting behind a command which is not enqueued in the backend" errors with oneCCL on BMG ([#197396](https://github.com/pytorch/pytorch/pull/197396)) (cut for length)
- Fix `torch.xpu.Event.record()` submitting twice on first use, which could lose profiling timestamps ([#194609](https://github.com/pytorch/pytorch/pull/194609)) (cut for length)
### security
