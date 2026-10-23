# Miscategorized PRs

PRs that ended up in the wrong worksheet, organized by which area they belong to.

- Improve the error when a symbolic size reaches an op expecting concrete ints: report the offending index and value, and suggest common dynamic-shape causes ([#186082](https://github.com/pytorch/pytorch/pull/186082))
- Speed up `FunctionalTensor` creation with dynamic shapes by reusing the inner tensor's storage size (about 1s less compile time on one model) ([#193416](https://github.com/pytorch/pytorch/pull/193416))
- Honor explicit MTIA activity filters in the profiler: `COLLECTIVE_COMM` is now a selectable MTIA activity, and combining a non-empty `custom_profiler_config` with an explicit MTIA `activity_filter` is rejected ([#194920](https://github.com/pytorch/pytorch/pull/194920))
- Speed up the chunked CUDA `torch.nn.functional.linear_cross_entropy` backward with one fused CuTeDSL kernel when the CuTeDSL runtime is installed (0.61-0.87x of eager time on H100, 0.30-0.78x on B200, at lower peak memory) ([#195829](https://github.com/pytorch/pytorch/pull/195829))
