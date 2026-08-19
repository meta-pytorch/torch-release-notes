
# Release Notes worksheet quantization

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

## quantization
### bc breaking
### deprecation
### new features
### improvements
### bug fixes
- Fix a divide-by-zero crash (`SIGFPE`) in `torch.quantize_per_channel` on the per-channel `float_qparams` path for the `qint32` dtype; whole-byte quantized types now pack correctly instead of underflowing the packing factor to zero ([#186767](https://github.com/pytorch/pytorch/pull/186767))
- Add the missing overflow check to the FBGEMM build of the ARM `quantize_val` path, fixing incorrect quantized values that showed up as quantization test failures on some hardware ([#187481](https://github.com/pytorch/pytorch/pull/187481))
- Fix a GPU memory access fault that aborted quantized `embedding_bag` byte and 4-bit rowwise lookups on ROCm, caused by a bitwise-AND typo in the bit-field extraction primitive ([#192571](https://github.com/pytorch/pytorch/pull/192571))
### performance
- Add a bias-add fast path to fp16 dynamic quantized linear (`PackedLinearWeightFp16`), speeding up the bias addition step by 10–49× on representative shapes (roughly a 5% overall CPU reduction) ([#189943](https://github.com/pytorch/pytorch/pull/189943))
### docs
### devs
- Update the vendored XNNPACK to github revision f6486e3e1d ([#191206](https://github.com/pytorch/pytorch/pull/191206))
### Untopiced
### not user facing
- Use `std::clamp` in the quantizer CPU kernels ([#185490](https://github.com/pytorch/pytorch/pull/185490), [#185552](https://github.com/pytorch/pytorch/pull/185552))
- Fix typos in comments and docstrings ([#187543](https://github.com/pytorch/pytorch/pull/187543), [#188814](https://github.com/pytorch/pytorch/pull/188814), [#190374](https://github.com/pytorch/pytorch/pull/190374), [#190722](https://github.com/pytorch/pytorch/pull/190722))
- Use const_data_ptr for read-only weight_norm and qnnpack sites ([#187819](https://github.com/pytorch/pytorch/pull/187819))
- Use const_data_ptr for read-only quantized sites ([#187817](https://github.com/pytorch/pytorch/pull/187817))
- [BE][Ez]: Apply missing std::move calls via clang-tidy ([#189583](https://github.com/pytorch/pytorch/pull/189583))
- Cleanup dead code across tests ([#188573](https://github.com/pytorch/pytorch/pull/188573))
- [BE][Ez]: Apply some more missing moves ([#189907](https://github.com/pytorch/pytorch/pull/189907))
- Remove stale Caffe2 references from docs ([#190430](https://github.com/pytorch/pytorch/pull/190430))
- Make uncaught doctest warnings a hard error, after quieting the noise ([#191416](https://github.com/pytorch/pytorch/pull/191416))
- [1/N][Test] Refactor `TestBaseStructuredSparsifier` in `torch_ao_sparsity.py` ([#191199](https://github.com/pytorch/pytorch/pull/191199))
- [BE][Ez]: Add missing qnnpack test to OSS build ([#192373](https://github.com/pytorch/pytorch/pull/192373))
### security
