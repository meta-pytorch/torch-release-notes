# PyTorch 2.8.0 Release Notes
- [Highlights](#highlights)
- [Backwards Incompatible Changes](#backwards-incompatible-changes)
- [Deprecations](#deprecations)
- [New Features](#new-features)
- [Improvements](#improvements)
- [Bug fixes](#bug-fixes)
- [Performance](#performance)
- [Documentation](#documentation)
- [Developers](#developers)
- [Security](#security)


# Highlights
TODO

For more details about these highlighted features, you can look at the release blogpost.
Below are the full release notes for this release.


# Backwards Incompatible Changes

### [Example] New interface for `GraphTransformObserver` to enable Node Level provenance tracking (#144277)
We now track a mapping between the nodes in the pre-grad and post-grad graph. See the issue for an example frontend to visualize the transformations. To update your `GraphTransformObserver` subclasses, instead of overriding `on_node_creation` and `on_node_erase`, there are new functions `get_node_creation_hook`, `get_node_erase_hook`, `get_node_replace_hook` and `get_deepcopy_hook`. These are registered on the `GraphModule` member of the `GraphTransformObserver` upon entry and exit of a `with` block

Version 2.6.0

```python
class MyPrintObserver(GraphTransformObserver):
    def on_node_creation(self, node: torch.fx.Node):
        print(node)
```
Version 2.7.0
```python
class MyPrintObserver(GraphTransformObserver):
    def get_node_creation_hook(self):
        def hook(node: torch.fx.Node):
            print(node)
        return hook
```


# Deprecations

### [Example] `torch.onnx.dynamo_export` is deprecated (#146425, #146639, #146923)

Users should use the `dynamo=True` option on `torch.onnx.export`.

Version 2.6.0

```py
torch.onnx.dynamo_export(model, *args, **kwargs)
```

Version 2.7.0

```py
torch.onnx.export(model, args, kwargs=kwargs, dynamo=True)
```


# New features

## Release Engineering
## Python Frontend
## Autograd
## Dataloader
## Linear Algebra
## Nested Tensor (NJT)
## torch.nn
## torch.optim
## Build Frontend
## C++ Frontend
## Distributed
#### Distributed Checkpoint (DCP)
#### DTensor
#### c10d
#### DistributedDataParallel (DDP)
#### FullyShardedDataParallel2 (FSDP2)
#### ...
## CPU
#### x86
#### aarch64
## CUDA
## MPS
## ROCm
## XPU
## Profiler
## torch.compile
#### Dynamo
#### AOTDispatcher
#### Inductor
## torch.fx
## torch.export
## Quantization
## ONNX
## JIT
## Lazy Tensor
## torch.package


# Improvements
<same ordering as in new features>

# Bug fixes
<same ordering as in new features>


# Performance
<same ordering as in new features>


# Documentation
<same ordering as in new features>

# Security
<same ordering as in new features>
