
# Release Notes worksheet onnx

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

## onnx
### bc breaking

- Default opset in `torch.onnx.export` is now 18 ([#156023](https://github.com/pytorch/pytorch/pull/156023))

When `dynamo=False`, the default ONNX opset version has been updated from 17 to 18. Users can set `opset_version` to explicitly select an opset version.

Version 2.7

```py
# opset_version=17
torch.onnx.export(...)
```

Version 2.8

```py
# To preserve the original behavior
torch.onnx.export(..., opset_version=17)

# New: opset_version=18
torch.onnx.export(...)
```

- The `JitTraceConvertStrategy` has been removed ([#152556](https://github.com/pytorch/pytorch/pull/152556))

Support for JIT traced and scripted modules in the ONNX exporter when `dynamo=True` has been removed. You are encouraged to export an nn.Module directly, or create an `ExportedProgram` using `torch.export` before exporting to ONNX.

- `onnxscript>=0.3.1` is required for the `dynamo=True` option ([#157017](https://github.com/pytorch/pytorch/pull/157017))

You must upgrade `onnxscript` to version 0.3.1 or higher for it to be compatible with PyTorch 2.8.

### deprecation

- The `dynamo=False` (current default) option is deprecated ([#152478](https://github.com/pytorch/pytorch/pull/152478) and [#155580](https://github.com/pytorch/pytorch/pull/155580))

The default will be `dynamo=True` starting from PyTorch 2.9. You are encouraged to migrate to use the `dynamo=True` option in `torch.onnx.export`. This flag makes `torch.export.export` the default export path, replacing `TorchScript`, as `TorchScript` is nearing end-of-life"

To maintain the old behavior, set `dynamo=False`. You are encouraged to also experiment with the `fallback=True` option that will make the exporter fall back to the `dynamo=False` path if there are errors.

### new features

- Additional opsets (>18) are supported when `dynamo=True` ([#149901](https://github.com/pytorch/pytorch/pull/149901), [#154596](https://github.com/pytorch/pytorch/pull/154596))

Opsets 18-23 are supported with `dynamo=True`. Importantly, you will be able to leverage the `Attention` ONNX operator when setting `opset` to 23.

- Support for symbolic operators in the `dynamo=True` export path ([#148905](https://github.com/pytorch/pytorch/pull/148905), [#149678](https://github.com/pytorch/pytorch/pull/149678), [#150038](https://github.com/pytorch/pytorch/pull/150038))

Two operators `torch.onnx.ops.symbolic` and `torch.onnx.ops.symbolic_multi_out` are defined to allow you to create symbolic ONNX operators directly in your PyTorch models. You can use them in a `forward` method:

```py
def forward(self, x: torch.Tensor) -> torch.Tensor:
    # Optionally use is_in_onnx_export to control the behavior during onnx export

    if torch.onnx.is_in_onnx_export():
        # Create a symbolic ONNX operator with the name "CustomOp" in the "custom_domain" domain.
        # The output tensor will have the specified dtype and shape
        return torch.onnx.ops.symbolic(
            "custom_domain::CustomOp",
            (x,),
            dict(attr_key="attr_value"),
            dtype=x.dtype,
            shape=x.shape,
            version=1,
        )
    else:
        return x
```

To learn more, refer to the [docs](https://docs.pytorch.org/docs/main/onnx_ops.html#symbolic-operators).

- ONNX operators as native PyTorch ops ([#156431](https://github.com/pytorch/pytorch/pull/156431), [#156367](https://github.com/pytorch/pytorch/pull/156367), [#154745](https://github.com/pytorch/pytorch/pull/154745))

You can now use the ONNX operators `Attention-23` and `RotaryEmbedding-23` as native PyTorch operators in your nn.Module, which will be converted directly in the exported ONNX models. You can use them in your `forward` methods like so:

```py
def forward(
    self, input_data, cos_cache_data, sin_cache_data, position_ids_data
):
    return torch.onnx.ops.rotary_embedding(
        input_data,
        cos_cache_data,
        sin_cache_data,
        position_ids_data,
    )
```

To learn more, refer to the [docs](https://docs.pytorch.org/docs/main/onnx_ops.html#onnx-operators).

- Support for `torch.scan` ([#154513](https://github.com/pytorch/pytorch/pull/154513))

Uses of `torch.scan` can now be converted to ONNX.

- Support 0/1-sized example inputs on dynamic dimensions ([#155717](https://github.com/pytorch/pytorch/pull/155717))

You may now use a size 1 dimension in example inputs on the dynamic dimensions. Prior to this release, users were required to provide size>=2 example inputs on the dynamic dimensions due to the [0/1 specialization behavior in torch.export](https://docs.google.com/document/d/16VPOa3d-Liikf48teAOmxLc92rgvJdfosIy-yoT38Io)

- New strategy `draft_export` ([#147529](https://github.com/pytorch/pytorch/pull/147529))

`draft_export` is added as the last strategy for obtaining an ExportedProgram in `torch.onnx.export` to provide debugging information when there are data dependent / constraint errors. You may learn more in the [docs](https://docs.pytorch.org/docs/main/draft_export.html)


- Others
  - Support sym_float ([#153200](https://github.com/pytorch/pytorch/pull/153200))
  - Update ONNX to 1.18 ([#152200](https://github.com/pytorch/pytorch/pull/152200))
  - Support float4 ([#151069](https://github.com/pytorch/pytorch/pull/151069), [#156353](https://github.com/pytorch/pytorch/pull/156353))
  - Add group_norm support from opset 21 ([#152138](https://github.com/pytorch/pytorch/pull/152138))
  - Implement sym_not ([#152111](https://github.com/pytorch/pytorch/pull/152111))
  - add converters for sym_min, sym_max ([#152196](https://github.com/pytorch/pytorch/pull/152196))

### improvements
- Add asdict method to VerificationInfo class ([#151024](https://github.com/pytorch/pytorch/pull/151024))
- Support running bfloat16 models with ONNX Runtime ([#149646](https://github.com/pytorch/pytorch/pull/149646))
- Update onnx program doc formatting and improve robustness ([#151623](https://github.com/pytorch/pytorch/pull/151623))
- dynamic_shapes uses DYNAMIC ([#153065](https://github.com/pytorch/pytorch/pull/153065))
- Set the name of the producing node using the value name ([#155413](https://github.com/pytorch/pytorch/pull/155413))

### bug fixes
- Fix bfloat16 support in onnx_program callable ([#151121](https://github.com/pytorch/pytorch/pull/151121))
- Produce correct dtypes for bf16/f8 in IR TorchTensor ([#151259](https://github.com/pytorch/pytorch/pull/151259))
- Preserve all legacy exporter params in fallback ([#156659](https://github.com/pytorch/pytorch/pull/156659))

### performance

### docs
- Update types in VerificationInfo ([#149377](https://github.com/pytorch/pytorch/pull/149377))
- Improve docstring of onnx symbolic ops ([#149668](https://github.com/pytorch/pytorch/pull/149668))
- Note on attention op symbolic function ([#156441](https://github.com/pytorch/pytorch/pull/156441))
- Convert to .md: onnx_verification.rst, onnx.rst, package.rst, ([#155556](https://github.com/pytorch/pytorch/pull/155556))
- Add ONNX dynamo metadata documentation ([#155816](https://github.com/pytorch/pytorch/pull/155816))
- [BE] fix typos in docs/ ([#156080](https://github.com/pytorch/pytorch/pull/156080))
- Convert to markdown onnx rst ([#155228](https://github.com/pytorch/pytorch/pull/155228))

### devs

### Untopiced

### not user facing
- Clean up the diagnostics module ([#149864](https://github.com/pytorch/pytorch/pull/149864))
- Add test for decomp_table update ([#153671](https://github.com/pytorch/pytorch/pull/153671))
- Add __main__ guards to tests ([#154716](https://github.com/pytorch/pytorch/pull/154716))
- Delete tools/onnx/update_default_opset_version.py ([#156055](https://github.com/pytorch/pytorch/pull/156055))
- Clean up legacy dynamo export code ([#149745](https://github.com/pytorch/pytorch/pull/149745))
- Add a comment for handling bf16/fp8 tensor to numpy conversion ([#151371](https://github.com/pytorch/pytorch/pull/151371))
- Typo fixes for "overridden" in comments and function names ([#155944](https://github.com/pytorch/pytorch/pull/155944))
### security
