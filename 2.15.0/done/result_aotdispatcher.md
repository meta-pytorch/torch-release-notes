
# Release Notes worksheet aotdispatcher

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

## aotdispatcher
### bc breaking
### deprecation
### new features
### improvements
- Stop bypassing the AOTAutograd cache for graphs that contain a `torch.inference_mode` region or a `torch.tensor(...)` call built from data-dependent scalars ([#191409](https://github.com/pytorch/pytorch/pull/191409))
### bug fixes
- Fix compiling code that calls a matmul or view op on a plain `torch.Tensor` subclass with no `__torch_dispatch__`, which failed with a dispatch error under Inductor and `aot_eager` ([#193968](https://github.com/pytorch/pytorch/pull/193968))
- Fix the wrong tensor being copied back into a mutated input when, with `keep_inference_input_mutations`, a function returns an input whose mutation stays in the graph alongside other inputs mutated outside it ([#198622](https://github.com/pytorch/pytorch/pull/198622))
- Fix persistent AOTAutograd cache misses across processes for tensor subclasses whose metadata contains a `set` or `frozenset`, by making the cache key independent of `PYTHONHASHSEED` ([#193419](https://github.com/pytorch/pytorch/pull/193419))
- Fix `PendingUnbackedSymbolNotFound` when a compiled `saved_tensors_hooks` pack hook allocates unbacked SymInts ([#193258](https://github.com/pytorch/pytorch/pull/193258))
- Fix opaque constants being corrupted when a compiled graph has tensor-subclass outputs, on both cold compile and cache hit ([#193190](https://github.com/pytorch/pytorch/pull/193190))
- Fix an AOTAutograd cache-key crash, `AttributeError: Can't get local object 'WeakValueDictionary.__init__.<locals>.remove'`, for tensor subclasses whose `__tensor_flatten__` metadata contains a `WeakValueDictionary` ([#190080](https://github.com/pytorch/pytorch/pull/190080))
- Fix the min-cut partitioner crashing with `RuntimeError: Unknown metadata type <class 'torch.device'>` on graphs with device-valued nodes ([#196146](https://github.com/pytorch/pytorch/pull/196146))
- Fix static-input indices being left shifted after effect tokens are removed from an inference graph, which could make Inductor skip the alignment check for a regular input and pass a misaligned view to a kernel that assumes 16-byte alignment ([#198005](https://github.com/pytorch/pytorch/pull/198005))
- Fix ranks that share a cache and seed the Python RNG identically generating the same AOT precompile fallback cache key, by using a UUID instead of `random.random()` ([#191427](https://github.com/pytorch/pytorch/pull/191427))
### performance
### docs
### devs
### Untopiced
### not user facing
### security
