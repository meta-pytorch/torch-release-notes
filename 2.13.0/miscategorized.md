# Miscategorized PRs

PRs that ended up in the wrong worksheet, organized by which area they belong to.

## cuda
- Expose torch.cuda.current_solver_handle for cuSOLVER handle sharing ([#176705](https://github.com/pytorch/pytorch/pull/176705)) (from dynamo; labeled `release notes: cuda`)

## export
- Make functorch JVP operator torch.exportable ([#179686](https://github.com/pytorch/pytorch/pull/179686)) (from dynamo; labeled `release notes: export`)

## autograd
- Add torch.autograd.graph.region_activation_memory_budget ([#185979](https://github.com/pytorch/pytorch/pull/185979)) (from dynamo; labeled `release notes: autograd`)

## mps
(from inductor (aoti) — these are pure MPS kernel changes that also carried a `release notes: inductor (aoti)` label)
- [MPS] grid_sampler_3d backward pass ([#179388](https://github.com/pytorch/pytorch/pull/179388))
- [MPS] Flatten 5D tensors to 4D in batch_norm for performance ([#180335](https://github.com/pytorch/pytorch/pull/180335))
