
# Release Notes worksheet distributed (checkpoint)

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

## distributed (checkpoint)
### bc breaking
### deprecation
### new features
### improvements
### bug fixes
### performance
### docs
### devs
### Untopiced
### not user facing
- Fix test consolidate hf safetensors ([#157386](https://github.com/pytorch/pytorch/pull/157386))
- HF loads dcp - don't do a full deserialize on every file ([#157715](https://github.com/pytorch/pytorch/pull/157715))
- [BE][1/16] fix typos in torch/ ([#156311](https://github.com/pytorch/pytorch/pull/156311))
- [BE][6/6] fix typos in test/ (test/distributed/) ([#157640](https://github.com/pytorch/pytorch/pull/157640))
- [BE] add noqa for flake8 rule B036: found `except BaseException` without re-raising ([#159043](https://github.com/pytorch/pytorch/pull/159043))
- Fix test_fsdp_ep.py due to _MeshEnv API change ([#158695](https://github.com/pytorch/pytorch/pull/158695))
- port distributed pipeline test files for Intel GPU ([#159033](https://github.com/pytorch/pytorch/pull/159033))
- [dcp_poc] add async checkpointing tests ([#161034](https://github.com/pytorch/pytorch/pull/161034))
- port distributed pipeline test files for Intel GPU ([#159033](https://github.com/pytorch/pytorch/pull/159033))
- [dcp_poc] Introduce a new simple rank local checkpointer ([#156142](https://github.com/pytorch/pytorch/pull/156142))
- Create a base Checkpointer and SyncCheckpointer and add dist barrier impl and  ([#156926](https://github.com/pytorch/pytorch/pull/156926))
- [DCP] OSS Zero Overhead Checkpointing Implementation ([#156207](https://github.com/pytorch/pytorch/pull/156207))
- HF - consolidate shards of safetensors files to full tensors in finish step ([#156705](https://github.com/pytorch/pytorch/pull/156705))
- Add async checkpointing impl to experimental checkpointer and add a builder API ([#156927](https://github.com/pytorch/pytorch/pull/156927))
- [oss] Add version to metadata ([#155343](https://github.com/pytorch/pytorch/pull/155343))
- [HF][DCP] Upload local consolidated files to remote storage if needed ([#157371](https://github.com/pytorch/pytorch/pull/157371))
- [oss][hf][bug fix] Remove buggy consolidation logic ([#158380](https://github.com/pytorch/pytorch/pull/158380))
- Script for consolidation of sharded safetensor files ([#154743](https://github.com/pytorch/pytorch/pull/154743))
- Updates to safetensors checkpoint consolidation script to be faster ([#157936](https://github.com/pytorch/pytorch/pull/157936))
- DCP safetensors test fix ([#158685](https://github.com/pytorch/pytorch/pull/158685))
- [DCP] Add support for ShardedTensor to PgTransport ([#158573](https://github.com/pytorch/pytorch/pull/158573))
- Device agnostic for DCP ([#158337](https://github.com/pytorch/pytorch/pull/158337))
- [DCP] Improve error handling for process based async checkpointing ([#159374](https://github.com/pytorch/pytorch/pull/159374))
- HF component update to not use fsspec components ([#159405](https://github.com/pytorch/pytorch/pull/159405))
- DCP HF reader: use safe_open instead of reading the bytes ([#159406](https://github.com/pytorch/pytorch/pull/159406))
- Use only safetensors APIs in HFStorageReader ([#159681](https://github.com/pytorch/pytorch/pull/159681))
- [dcp][hf] Improve HF consolidation algorithm ([#158648](https://github.com/pytorch/pytorch/pull/158648))
- Fix requires_cuda to requires_cuda_and_triton ([#160222](https://github.com/pytorch/pytorch/pull/160222))
- [DCP][Prototype] Checkpoint replication via PGTransport (#157963) ([#159801](https://github.com/pytorch/pytorch/pull/159801))
- [dcp_poc] Fix parameter order in distributed checkpoint API to use path-first for consistency ([#160986](https://github.com/pytorch/pytorch/pull/160986))
- [dcp][hf] Fix multi-rank consolidation for no files to process case ([#160660](https://github.com/pytorch/pytorch/pull/160660))
- [DCP][HF] Add option to parallelize reads in HF Storage Reader ([#160205](https://github.com/pytorch/pytorch/pull/160205))
- [DCP][HuggingFace] Add Support for dequantization of SafeTensors checkpoints ([#160682](https://github.com/pytorch/pytorch/pull/160682))
- Remove usage of fsspec in HF consolidation script ([#159392](https://github.com/pytorch/pytorch/pull/159392))
- Add new function consolidate_safetensors_files_on_every_rank for HF consolidation ([#159393](https://github.com/pytorch/pytorch/pull/159393))
- Write full tensors out at once in HF consolidation script ([#159394](https://github.com/pytorch/pytorch/pull/159394))
- [DCP][OSS] Rank local checkpointing in DCP without collectives ([#147758](https://github.com/pytorch/pytorch/pull/147758))
- Add pg argument to consolidate_safetensors_files_on_every_rank ([#161421](https://github.com/pytorch/pytorch/pull/161421))
- Fix for FP8 multiplication during dequantization ([#162202](https://github.com/pytorch/pytorch/pull/162202))
- Fix the issue when scale vector is in a different SafeTensors file ([#162214](https://github.com/pytorch/pytorch/pull/162214))
- Bug fix for losing shape on wrapper tensor for DTensor ([#156774](https://github.com/pytorch/pytorch/pull/156774))
- Add device generalization support for distributed tests ([#156796](https://github.com/pytorch/pytorch/pull/156796))
- Call `pin_memory_utils.unpin_memory` with `data_ptr` instead of tensor ([#160992](https://github.com/pytorch/pytorch/pull/160992))
- Fix forced loglevel in checkpointing code ([#158820](https://github.com/pytorch/pytorch/pull/158820))
### security
