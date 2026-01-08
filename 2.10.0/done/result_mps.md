
# Release Notes worksheet mps

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

## mps
### bc breaking
### deprecation
### new features
- MPS sparse backend is functional
([#162349](https://github.com/pytorch/pytorch/pull/162349), [#162349](https://github.com/pytorch/pytorch/pull/162349), [#162007](https://github.com/pytorch/pytorch/pull/162007), [#162910](https://github.com/pytorch/pytorch/pull/162910), [#162885](https://github.com/pytorch/pytorch/pull/162885), [#163011](https://github.com/pytorch/pytorch/pull/163011), [#163694](https://github.com/pytorch/pytorch/pull/163694), [#164961](https://github.com/pytorch/pytorch/pull/164961), [#165102](https://github.com/pytorch/pytorch/pull/165102), [#166708](https://github.com/pytorch/pytorch/pull/166708), [#166711](https://github.com/pytorch/pytorch/pull/166711), [#167013](https://github.com/pytorch/pytorch/pull/167013), [#169125](https://github.com/pytorch/pytorch/pull/169125), [#165232](https://github.com/pytorch/pytorch/pull/165232), [#166708](https://github.com/pytorch/pytorch/pull/166708), [#168154](https://github.com/pytorch/pytorch/pull/168154), [#169368](https://github.com/pytorch/pytorch/pull/169368), [#167908](https://github.com/pytorch/pytorch/pull/167908), [#168112](https://github.com/pytorch/pytorch/pull/168112))
### improvements
- Add `embedding_bag` operator ([#163012](https://github.com/pytorch/pytorch/pull/163012), [#163931](https://github.com/pytorch/pytorch/pull/163931), [#163281](https://github.com/pytorch/pytorch/pull/163281))
- Continue ops migration to Metal and add complex support ( [#169478](https://github.com/pytorch/pytorch/pull/169478), [#166903](https://github.com/pytorch/pytorch/pull/166903), [#167755](https://github.com/pytorch/pytorch/pull/167755), [#167826](https://github.com/pytorch/pytorch/pull/167826)m [#166216](https://github.com/pytorch/pytorch/pull/166216), [#166670](https://github.com/pytorch/pytorch/pull/166670), [#169407](https://github.com/pytorch/pytorch/pull/169407), [#166210](https://github.com/pytorch/pytorch/pull/166210), [#166090](https://github.com/pytorch/pytorch/pull/166090), [#168120](https://github.com/pytorch/pytorch/pull/168120), [#167569](https://github.com/pytorch/pytorch/pull/167569))

- Asynchronously report out-of-bounds access errors for `embedding_bag` and `index_select` ops ([#166615](https://github.com/pytorch/pytorch/pull/166615), [#168930](https://github.com/pytorch/pytorch/pull/168930), [#166468](https://github.com/pytorch/pytorch/pull/166468))
### bug fixes
- Fix empty tensors handling for `median`/`nanmedian`/`mv`, `dot` ([#162846](https://github.com/pytorch/pytorch/pull/162846), [#166561](https://github.com/pytorch/pytorch/pull/166561)), [#165237](https://github.com/pytorch/pytorch/pull/165237))
- Fix dlpack exports/imports of sliced tensors ([#169272](https://github.com/pytorch/pytorch/pull/169272))
- Fix large tensors silent correctness for `fill` and `cat` operation ([#164108](https://github.com/pytorch/pytorch/pull/164108), [#165373](https://github.com/pytorch/pytorch/pull/165373), [#166556](https://github.com/pytorch/pytorch/pull/166556), [#164416](https://github.com/pytorch/pytorch/pull/164416))
- `torch.compile` bugfixes ([#169648](https://github.com/pytorch/pytorch/pull/169648), [#163021](https://github.com/pytorch/pytorch/pull/163021), [#162776](https://github.com/pytorch/pytorch/pull/162776), [#163452](https://github.com/pytorch/pytorch/pull/163452))
- Silent correctness/input validation fixes ([#163036](https://github.com/pytorch/pytorch/pull/163036), ([#165254](https://github.com/pytorch/pytorch/pull/165254), ([#165267](https://github.com/pytorch/pytorch/pull/165267), ([#167777](https://github.com/pytorch/pytorch/pull/167777), ([#165058](https://github.com/pytorch/pytorch/pull/165058), ([#167961](https://github.com/pytorch/pytorch/pull/167961), ([#169261](https://github.com/pytorch/pytorch/pull/169261), ([#165871](https://github.com/pytorch/pytorch/pull/165871), ([#163507](https://github.com/pytorch/pytorch/pull/163507), ([#168332](https://github.com/pytorch/pytorch/pull/168332))
### performance
### docs
### devs
### Untopiced
### not user facing
### security
