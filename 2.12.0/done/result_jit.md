
# Release Notes worksheet jit

## jit
### bc breaking
### deprecation
### new features
- Added input-independent graph optimization API ([#179393](https://github.com/pytorch/pytorch/pull/179393))
### improvements
### bug fixes
- Silenced CPython 3.13.8 `inspect.getsourcelines()` bug ([#179066](https://github.com/pytorch/pytorch/pull/179066))
- Fixed data race in opaque type registry ([#175694](https://github.com/pytorch/pytorch/pull/175694))
- Fixed xplat build: use `PyObjectType::get()` directly ([#178786](https://github.com/pytorch/pytorch/pull/178786))
### performance
- Cached `can_compile_class` and short-circuited type inference for ProcessGroup ([#179396](https://github.com/pytorch/pytorch/pull/179396))
### docs
### devs
- Removed `torch/csrc/utils/six.h` ([#179110](https://github.com/pytorch/pytorch/pull/179110))
- Upgraded runtime JIT/Inductor codegen to C++20 ([#176502](https://github.com/pytorch/pytorch/pull/176502))
### not user facing
- [BE] Use namespace alias in ir.h ([#175382](https://github.com/pytorch/pytorch/pull/175382))
- Remove ir.h from `jit/api/` headers include chain ([#175413](https://github.com/pytorch/pytorch/pull/175413))
- Reorder type declarations and move definitions to fix Windows builds with TheRock ([#176207](https://github.com/pytorch/pytorch/pull/176207))
- [BE] Apply up007 and up045 to directories from headeronly through nn ([#176229](https://github.com/pytorch/pytorch/pull/176229))
- [BE][JIT] Replace LOG(FATAL) with TORCH_INTERNAL_ASSERT ([#178291](https://github.com/pytorch/pytorch/pull/178291))
- [distributed] Handle FakeScriptObject wrapping of ProcessGroup in pybind ([#178692](https://github.com/pytorch/pytorch/pull/178692))
- Replace erase-remove idiom with `std::erase_if` ([#179231](https://github.com/pytorch/pytorch/pull/179231))
### security
