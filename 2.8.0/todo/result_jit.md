
# Release Notes worksheet jit

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

## jit
### bc breaking
### deprecation
### new features
### improvements
- Force build to conform C++ standard on windows by adding /permissive- flag ([#149035](https://github.com/pytorch/pytorch/pull/149035))
### bug fixes
### performance
### docs
### devs
### Untopiced
- [pytorch] Fix duplicated Malloc/Free insertation when using IRBuilderBase::CreateMalloc/CreateFree in LLVM 18+ ([#149058](https://github.com/pytorch/pytorch/pull/149058))
- [Torchscript] Add a flag to use mangled names instead of demangled ([#148906](https://github.com/pytorch/pytorch/pull/148906))
- [MTIA] Support loading Tensors on mtia:0 for pytorch code ([#149327](https://github.com/pytorch/pytorch/pull/149327))
- [torch] Fix unsafe concurrent access to autocast_enabled ([#148281](https://github.com/pytorch/pytorch/pull/148281))
- Enable move warnings for torch targets ([#149923](https://github.com/pytorch/pytorch/pull/149923))
- Remove cppcoreguidelines-pro-type-member-init_fix suppression ([#148638](https://github.com/pytorch/pytorch/pull/148638))
- [hop] support base_hop._gen_schema ([#149688](https://github.com/pytorch/pytorch/pull/149688))
- Don't eagerly create AliasInfo in parseAliasDeclaration ([#151630](https://github.com/pytorch/pytorch/pull/151630))
- Fix extra heap allocation in Source constructor ([#151800](https://github.com/pytorch/pytorch/pull/151800))
- Add & use Token::text_view() (which returns a string_view unlike text()) ([#151804](https://github.com/pytorch/pytorch/pull/151804))
- Fix easy missing moves in function_schema_parser ([#151805](https://github.com/pytorch/pytorch/pull/151805))
- Fix a missed c10::TypeFactory::create spot in function_schema_parser ([#151806](https://github.com/pytorch/pytorch/pull/151806))
- Fix missing moves in SchemaTypeParser::parseFakeAndRealType ([#151807](https://github.com/pytorch/pytorch/pull/151807))
- StringCordView: make iterator fast when there is only one piece ([#151810](https://github.com/pytorch/pytorch/pull/151810))
- Fix clang-tidy suppression in torch/csrc/jit ([#152271](https://github.com/pytorch/pytorch/pull/152271))
- Fix StringCoordView::substr after D73379178 / #151810 ([#152304](https://github.com/pytorch/pytorch/pull/152304))
- Forward fix D74196435 ([#152926](https://github.com/pytorch/pytorch/pull/152926))
- Partilally revert https://github.com/pytorch/pytorch/pull/152288 ([#152909](https://github.com/pytorch/pytorch/pull/152909))
- [JIT] add GRAPH_DEBUG for setGraphExecutorOptimize ([#153549](https://github.com/pytorch/pytorch/pull/153549))
- [JIT] Optimize DCE by storing a MemoryLocations for an entire set<Value*> ([#153645](https://github.com/pytorch/pytorch/pull/153645))
- [BE] fix lint errors caused by const SROpFunctor fn ([#154552](https://github.com/pytorch/pytorch/pull/154552))
- [export] inline jit.scripted function in export ([#155180](https://github.com/pytorch/pytorch/pull/155180))
- Make benchmark by op for TS model work with sample inputs ([#155988](https://github.com/pytorch/pytorch/pull/155988))
### not user facing
- Reserve vector in StringCordView ctor ([#151628](https://github.com/pytorch/pytorch/pull/151628))
- [Ez][BE]: Fix click ImportError in torch/csrc/jit ([#153323](https://github.com/pytorch/pytorch/pull/153323))
- [BE] Fix `-Wextra-semi` warning ([#153887](https://github.com/pytorch/pytorch/pull/153887))
- Add /Zc:preprocessor for torch libraries in MSVC builds ([#147825](https://github.com/pytorch/pytorch/pull/147825))
- [Easy][Code Clean] Remove the unused and undefined function in pickler ([#155772](https://github.com/pytorch/pytorch/pull/155772))
- use guard_or_false for expand utils reduction ([#155868](https://github.com/pytorch/pytorch/pull/155868))
### security
