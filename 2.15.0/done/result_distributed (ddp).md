
# Release Notes worksheet distributed (ddp)

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

## distributed (ddp)
### bc breaking
### deprecation
### new features
- Add caller-controlled backward finalization to `DistributedDataParallel`. Setting `ddp.require_manual_backward_finalization = True` stops DDP from waiting on gradient all-reduces and writing reduced gradients back at the end of backward; the caller then calls `ddp.finalize_backward()` exactly once per synchronized backward, either after `backward()` returns or from a backward hook once all buckets are ready (`ddp.should_finalize_after_backward` says which is required). This lets other work, such as sparse backward or communication, overlap the in-flight all-reduce, or lets `optimizer.step()` start before backward fully returns ([#196651](https://github.com/pytorch/pytorch/pull/196651))
- Add a `lazy_bucket_allocation` option (default `False`) to `DistributedDataParallel`. When enabled, DDP allocates each dense gradient bucket when its gradients become ready during backward and releases the bucket storage after backward, instead of keeping all buckets allocated across iterations. This lowers peak memory because the buckets no longer overlap with forward activations ([#199110](https://github.com/pytorch/pytorch/pull/199110))
### improvements
### bug fixes
### performance
- With `batched_grad_copy=True`, `DistributedDataParallel` now also batches the copy of reduced buckets back into `.grad` into one `_foreach_copy_` per bucket. This applies when `gradient_as_bucket_view=False` and removes one copy kernel launch per parameter ([#190524](https://github.com/pytorch/pytorch/pull/190524))
### docs
### devs
### Untopiced
### not user facing
### security
