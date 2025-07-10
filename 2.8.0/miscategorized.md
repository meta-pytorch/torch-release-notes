# Miscategorized commits

Welcome to the Pool of Miscategorized commits.
Add any commits that were miscategorized for your domain below.
Handle any commits that actually do belong to your domain and remove them from this list.

## Compiled Autograd
- [ca] default on in CI, with fallback for tests in test/compiled_autograd_skips/ ([#155480](https://github.com/pytorch/pytorch/pull/155480))


- partitioner: ensure collectives saved by SAC that are actually unused in the bw are properly not saved ([#149652](https://github.com/pytorch/pytorch/pull/149652))
- partitioner/SAC: fix recompute tag propagation for ops with list[tensor] inputs ([#152195](https://github.com/pytorch/pytorch/pull/152195))
- add min/max_seqlen to non_differentiable ([#151750](https://github.com/pytorch/pytorch/pull/151750))
- bf16 grouped gemm ([#150374](https://github.com/pytorch/pytorch/pull/150374))
- [dynamic shapes] support SymInt inputs for kthvalue ([#152151](https://github.com/pytorch/pytorch/pull/152151))
- support multinomial for dynamic num_samples ([#149463](https://github.com/pytorch/pytorch/pull/149463))

- [partitioner] always ban compiler-driven recompute of collectives by default ([#147561](https://github.com/pytorch/pytorch/pull/147561))
- Support subclass constructor capturing in export ([#147014](https://github.com/pytorch/pytorch/pull/147014))
- [AOTI][reland] Update test runner to use the new APIs ([#149412](https://github.com/pytorch/pytorch/pull/149412))
- [export] specialize for aten.to ([#149235](https://github.com/pytorch/pytorch/pull/149235))
- [1/N] Use internal linkage in torch/csrc C++ files. ([#150930](https://github.com/pytorch/pytorch/pull/150930))
- Reland fast gather and index implementation ([#151917](https://github.com/pytorch/pytorch/pull/151917))
- Support XPU in memory tracker ([#150703](https://github.com/pytorch/pytorch/pull/150703))
- Fix xrefs ([#151888](https://github.com/pytorch/pytorch/pull/151888))
- Add option to use mempool on OOM ([#151487](https://github.com/pytorch/pytorch/pull/151487))
- [ca] Functionalize AccumulateGrad ([#155521](https://github.com/pytorch/pytorch/pull/155521))
- [pt2d] Add reorder_comms_preserving_peak_memory pass ([#146562](https://github.com/pytorch/pytorch/pull/146562))
- fix numpy compatibility for 2d small list indices ([#154806](https://github.com/pytorch/pytorch/pull/154806))
- Resubmit Remove MemPoolContext  (#154042) ([#154746](https://github.com/pytorch/pytorch/pull/154746))

## not user facing
