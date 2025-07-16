
# Release Notes worksheet cuda

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

## cuda
### bc breaking
### deprecation
### new features
- Support capture of event record and wait in cuda graphs for timing ([#155372](https://github.com/pytorch/pytorch/pull/155372))
### improvements
- Support large batch sizes in memory-efficient SDPA backend forward ([#154029](https://github.com/pytorch/pytorch/pull/154029))
- Memory-efficient attention backward indexing fix (produced an illegal memory access) ([#155397](https://github.com/pytorch/pytorch/pull/155397))
- Support large batch sizes in memory-efficient SDPA backend backward ([#154663](https://github.com/pytorch/pytorch/pull/154663))
- CUTLASS update to 3.9.2 ([#152779](https://github.com/pytorch/pytorch/pull/152779))
- Report the correct tensor that needs to be GPU in FusedSgdKernel error message ([#153074](https://github.com/pytorch/pytorch/pull/153074))
- Support SDPA attention backends on sm121 (DGX Spark) ([#152314](https://github.com/pytorch/pytorch/pull/152314))
- Always initialize a CUDA context when torch.cuda.set_device() is called by the user ([#155900](https://github.com/pytorch/pytorch/pull/155900))
- Add torch.cuda._compile_kernel() to support building inline user CUDA kernels live at runtime ([#151484](https://github.com/pytorch/pytorch/pull/151484))
- Add FP8 row-wise scaled-mm for sm12x (GeForce Blackwell) ([#155991](https://github.com/pytorch/pytorch/pull/155991))
- Use 4 elements per thread in no-cast elementwise kernel to reduce binary size ([#154558](https://github.com/pytorch/pytorch/pull/154558))
- Add Clear History Flag to cleanup memory snapshots ([#149352](https://github.com/pytorch/pytorch/pull/149352))
- Use cutlass native BroadcastPtrArray in scaled group gemm to simplify implementation ([#152404](https://github.com/pytorch/pytorch/pull/152404))
### bug fixes
- Fix deterministic indexing with broadcast ([#154296](https://github.com/pytorch/pytorch/pull/154296))
- Fix `torch.backends.cuda.matmul.allow_fp16_accumulation` crash when using cuBLASLt ([#153083](https://github.com/pytorch/pytorch/pull/153083))
- Enable AsyncMM on Blackwell ([#153519](https://github.com/pytorch/pytorch/pull/153519))
- Fix torch.cuda.MemPool for multithreaded use-cases ([#153356](https://github.com/pytorch/pytorch/pull/153356))
- Properly clean up hooks in `torch.cuda.memory._record_memory_history` ([#153839](https://github.com/pytorch/pytorch/pull/153839))
- Fix to avoid calling `sum()` on a default-constructed gamma / beta in `layer_norm` ([#156600](https://github.com/pytorch/pytorch/pull/156600))
- Avoid hangs by erroring out for negative offsets or K=0 in grouped GEMMs ([#153226](https://github.com/pytorch/pytorch/pull/153226))
### performance
- 8 bytes aligned vector loads for bf16 and fp16 dtypes in torch.cat ([#150233](https://github.com/pytorch/pytorch/pull/150233))
- Enable vectorized 8byte copy for fp16/bf16 for index select kernel ([#152380](https://github.com/pytorch/pytorch/pull/152380))
- Use gather in index_select to improve performance ([#151715](https://github.com/pytorch/pytorch/pull/151715))
### docs
- Fix deprecated amp APIs in docs ([#154553](https://github.com/pytorch/pytorch/pull/154553))
- Document device memory apis in correct module ([#155126](https://github.com/pytorch/pytorch/pull/155126))
- Document non-pytorch CUDA memory allocation and how to query it ([#150880](https://github.com/pytorch/pytorch/pull/150880))
### devs
### Untopiced
### not user facing
- Fix missing field initializer warning in build ([#149597](https://github.com/pytorch/pytorch/pull/149597))
- [Easy][Building] Fix the warning of int4mm.cu when building ([#151427](https://github.com/pytorch/pytorch/pull/151427))
### security
