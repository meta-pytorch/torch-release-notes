
# Release Notes worksheet aotdispatcher

## aotdispatcher
### bc breaking
### deprecation
### new features
### improvements
### bug fixes
- Fixed AOTAutograd crash on `no_grad` views of differentiable intermediates ([#175673](https://github.com/pytorch/pytorch/pull/175673))
- Fixed inplace checks in autograd backward functions during functionalization ([#177213](https://github.com/pytorch/pytorch/pull/177213))
### performance
### docs
- Documented supported input and output dtypes for custom ops ([#175452](https://github.com/pytorch/pytorch/pull/175452))
### devs
- Codegen `AOTDispatchSubclassWrapper` ([#176741](https://github.com/pytorch/pytorch/pull/176741))
- Added UUID-based cache key support for pre-grad custom passes ([#177403](https://github.com/pytorch/pytorch/pull/177403)) _(from miscategorized)_
### not user facing
- Add cache key test for multiple outputs ([#178174](https://github.com/pytorch/pytorch/pull/178174))
- Add autograd_cache_key to compile_fx with tests ([#178172](https://github.com/pytorch/pytorch/pull/178172)) _(from miscategorized)_
- Add autograd_cache_key to standalone_compile with tests ([#178173](https://github.com/pytorch/pytorch/pull/178173)) _(from miscategorized)_
### security
