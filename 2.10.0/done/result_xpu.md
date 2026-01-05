
# Release Notes worksheet xpu

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

## xpu
### bc breaking
### deprecation
### new features
- Support ATen operators `scaled_mm` and `scaled_mm_v2` for Intel GPU ([#166056](https://github.com/pytorch/pytorch/pull/166056))
- Support ATen operator `_weight_int8pack_mm` for Intel GPU ([#160938](https://github.com/pytorch/pytorch/pull/160938))
- Extend SYCL support in PyTorch CPP Extension API to allow users to implement new custom operators on Windows ([#162579](https://github.com/pytorch/pytorch/pull/162579))
- Add API `torch.xpu.get_per_process_memory_fraction` for Intel GPU ([#165511](https://github.com/pytorch/pytorch/pull/165511))
- Add API `torch.xpu.set_per_process_memory_fraction` for Intel GPU ([#165510](https://github.com/pytorch/pytorch/pull/165510))
- Add API `torch.xpu.is_tf32_supported` for Intel GPU ([#163141](https://github.com/pytorch/pytorch/pull/163141))
- Add API `torch.xpu.can_device_access_peer` for Intel GPU ([#162705](https://github.com/pytorch/pytorch/pull/162705))
- Add API `torch.accelerator.get_memory_info` for Intel GPU ([#162564](https://github.com/pytorch/pytorch/pull/162564))
### improvements
- Support `--nproc-per-node` torchrun option for Intel GPU ([#159474](https://github.com/pytorch/pytorch/pull/159474))
- Support complex dtype of Aten operator Matmul for Intel GPU ([#160867](https://github.com/pytorch/pytorch/pull/160867))
- Add SYCL-TLA implementation for aten flash attention ([#169101](https://github.com/pytorch/pytorch/pull/169101))

### bug fixes
- Fix OneDNN deconvolution with `output_padding` on Intel GPU ([#169176](https://github.com/pytorch/pytorch/pull/169176))
- Fix conv1d precision error on Intel GPU ([#162944](https://github.com/pytorch/pytorch/pull/162944))
- Fix incorrect FLOPs counting of `convolution_overrideable` on Intel GPU([#166839](https://github.com/pytorch/pytorch/pull/166839))
- Fix performance drop in AOTI on Intel GPU ([#163315](https://github.com/pytorch/pytorch/pull/163315))

### performance
### docs
- Add new supported client GPU Panther Lake in "Get Started with XPU" page ([#170517](https://github.com/pytorch/pytorch/pull/170517))

### devs
- Upgrade Intel GPU software stack package to intel-deep-learning-essentials-2025.3 ([#166829](https://github.com/pytorch/pytorch/pull/166829))

### Untopiced
### not user facing
### security
