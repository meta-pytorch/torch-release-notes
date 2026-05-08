
# Release Notes worksheet fx

## fx
### bc breaking
### deprecation
### new features
- Add `tuple_return` option to `split_module` that wraps submodule outputs in a tuple ([#179007](https://github.com/pytorch/pytorch/pull/179007))
- Add `ignore_raw_node` option to `GraphPickler` ([#176939](https://github.com/pytorch/pytorch/pull/176939))
- Add `_merge_overlapping_fusions()` method to `FxNetSplitter` which detects and merges overlapping fusion groups ([#177099](https://github.com/pytorch/pytorch/pull/177099))
### improvements
- Update `get_source_partitioner` to parse `nn_module_stack` metadata for improved source-based graph partitioning ([#175788](https://github.com/pytorch/pytorch/pull/175788))
- `split_module` now uses `_make_graph_module` to support lazy recompile ([#177907](https://github.com/pytorch/pytorch/pull/177907))
- Fix `fuser_utils.topo_sort` to produce a stable ordering ([#175378](https://github.com/pytorch/pytorch/pull/175378))
- Fix GraphPickler to support nodes with slice() arguments ([#175996](https://github.com/pytorch/pytorch/pull/175996))
### bug fixes
- Fix edge case in `get_source_partitioner` ([#175935](https://github.com/pytorch/pytorch/pull/175935))
- Fix `make_fx` handling of value types for opaque objects so values are inlined into the graph consistently with dynamo behavior ([#178036](https://github.com/pytorch/pytorch/pull/178036))
- Fix `meta["val"]` not being populated for reconstructed opaque nodes, resolving partitioner classification issues ([#179660](https://github.com/pytorch/pytorch/pull/179660))
- Fix `repeat_interleave` fx graph to be runnable ([#177909](https://github.com/pytorch/pytorch/pull/177909))
- Fix fuse_by_partitions crash when partition has no external outputs ([#175203](https://github.com/pytorch/pytorch/pull/175203))
- Fix set_stack_trace ([#177332](https://github.com/pytorch/pytorch/pull/177332))
- Handle weakref objects during graph serialization in GraphPickler ([#178190](https://github.com/pytorch/pytorch/pull/178190))
- Fix horizontal fusion bug and add partition tests for regional inductor ([#178421](https://github.com/pytorch/pytorch/pull/178421))
### performance
- Fix quadratic name generation in `_NamespaceBase.create_name`, significantly improving performance for graphs with many nodes ([#176515](https://github.com/pytorch/pytorch/pull/176515), [#177217](https://github.com/pytorch/pytorch/pull/177217))
- Propagate custom annotations to runtime asserts ([#170796](https://github.com/pytorch/pytorch/pull/170796))
### docs
- Update and correct the documentation for Cond operator ([#175419](https://github.com/pytorch/pytorch/pull/175419))
### devs
- Add type annotations to core torch/fx types ([#179590](https://github.com/pytorch/pytorch/pull/179590))
- Add type annotations to torch/fx `operator_schemas` and `subgraph_rewriter` ([#179761](https://github.com/pytorch/pytorch/pull/179761))
- Add type annotations to `torch/fx/experimental/migrate_gradual_types` ([#180070](https://github.com/pytorch/pytorch/pull/180070))
- Add type annotations to torch/fx proxy, interpreter, symbol ([#179718](https://github.com/pytorch/pytorch/pull/179718))
- Add type annotations to torch/fx/experimental proxy_tensor ([#179864](https://github.com/pytorch/pytorch/pull/179864))
- Improve consistency between variable name and typing annotation ([#176291](https://github.com/pytorch/pytorch/pull/176291))
- Add timing to GraphPickler.loads method ([#175440](https://github.com/pytorch/pytorch/pull/175440))
- Apply up007 and up045 to torch/fx ([#176308](https://github.com/pytorch/pytorch/pull/176308))
- Remove more undocumented functions ([#175663](https://github.com/pytorch/pytorch/pull/175663))
### not user facing
- Windows specific test fixes ([#176024](https://github.com/pytorch/pytorch/pull/176024))
- Refactor proxy tensor to deduplicate and improve free-thread support ([#179199](https://github.com/pytorch/pytorch/pull/179199))
### security
