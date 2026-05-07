
# Release Notes worksheet functorch

## functorch
### bc breaking
### deprecation
### new features
### improvements
### bug fixes
- Fixed `grad`/`vjp`/`jvp` returning zeros under `inference_mode` ([#177596](https://github.com/pytorch/pytorch/pull/177596))
- Fixed `vmap` batch rules for `group_norm` backward operator ([#176272](https://github.com/pytorch/pytorch/pull/176272))
- [functorch] Fix double-pop in popDynamicLayerStackToDepth ([#177585](https://github.com/pytorch/pytorch/pull/177585))
### performance
- [FUNCTORCH] Use [] instead of list() for improved performance ([#175491](https://github.com/pytorch/pytorch/pull/175491))
### docs
### devs
### not user facing
### security
