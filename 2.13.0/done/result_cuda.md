
# Release Notes worksheet cuda

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

## cuda
### bc breaking
### deprecation
### new features
- Add `CUDAGraph.get_graph_data()` for graph topology introspection ([#183165](https://github.com/pytorch/pytorch/pull/183165))
- Lightweight API to get private pool reserved memory bytes ([#178240](https://github.com/pytorch/pytorch/pull/178240))
### improvements
- Debugging tool to verify that external inputs to a cuda graph are alive before replay ([#174649](https://github.com/pytorch/pytorch/pull/174649))
- Add get/set/reset functions for BLAS workspace sizes ([#177912](https://github.com/pytorch/pytorch/pull/177912))
- Cleanup double import in `BinaryDivFloorKernel.cu` ([#179260](https://github.com/pytorch/pytorch/pull/179260))
- Return supported CUDA arch list when no GPU is present but GPU is compiled ([#180356](https://github.com/pytorch/pytorch/pull/180356))
- Detect and fix stale stream references in autograd during CUDA graph capture ([#180090](https://github.com/pytorch/pytorch/pull/180090))
- Use `opmath_t` in i1 and i1e CUDA kernels ([#183778](https://github.com/pytorch/pytorch/pull/183778))
- Support `resize_` with address hint ([#178215](https://github.com/pytorch/pytorch/pull/178215))
- Support bfloat16 in `_embedding_bag_per_sample_weights_backward` on CUDA ([#185889](https://github.com/pytorch/pytorch/pull/185889))
- Align `parsePerProcessMemoryFraction`'s return type with other parsers ([#185139](https://github.com/pytorch/pytorch/pull/185139))
- Improve error message when cuda-bindings version is too old ([#185990](https://github.com/pytorch/pytorch/pull/185990))
- Expose torch.cuda.current_solver_handle for cuSOLVER handle sharing ([#176705](https://github.com/pytorch/pytorch/pull/176705))
### bug fixes
- Workaround for `nvrtcCompileProgram` changing locale in CUDA < 12.6.2 ([#180569](https://github.com/pytorch/pytorch/pull/180569))
- Zero `total_weight` before accumulating in `nll_loss2d` ([#182082](https://github.com/pytorch/pytorch/pull/182082))
- Fix dtype promotion in max/min kernel ([#181505](https://github.com/pytorch/pytorch/pull/181505))
- Round per-process memory fraction cap to avoid spurious OOM ([#179444](https://github.com/pytorch/pytorch/pull/179444))
- Fix `torch.cuda.ExternalStream(0)` to wrap the NULL stream ([#183258](https://github.com/pytorch/pytorch/pull/183258))
- Fix stream pool collision in conditional graph nodes ([#185836](https://github.com/pytorch/pytorch/pull/185836))
### performance
- Fix CUDA version check gating warp merge sort ([#183527](https://github.com/pytorch/pytorch/pull/183527))
- Allow specifying nbits to radix sort in `embedding_dense_backward_cuda` (#183578) ([#183578](https://github.com/pytorch/pytorch/pull/183578))
### docs
### devs
### Untopiced
### not user facing
### security
