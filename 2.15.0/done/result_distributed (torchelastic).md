
# Release Notes worksheet distributed (torchelastic)

You should:

1. ensure commit categorization is correct
2. write up major features, bc-breaking changes, deprecations in detail
3. summarize the other sections

## 1. Ensure commit categorization is correct

* Please sort commits into the following categories (you should not rename the categories!), I tried to pre-sort these to ease your work, feel free to move commits around if the current categorization is not good.
* Anything that is not public facing needs to be removed.
* If anything is miscategorized/belongs to another domain, move it to `miscategorized.md`.
* Please scan through `miscategorized.md` and handle any commits that belong within your domain according to these instructions.

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

## 2. Major features, BC-breaking changes, deprecations

The main goal of this process is to rephrase all the commit messages below to make them **clear and easy to read** by the end user. You should follow the following instructions to do so:

* **Please clean up and format commit titles to be readable by the general PyTorch user.** Make sure you're [following the guidance here](https://docs.google.com/document/d/14OmgGBr1w6gl1VO47GGGdwrIaUNr92DFhQbY_NEk8mQ/edit)! Your resulting notes must be consistent and easy to read.
* We place a lot of emphasis on the “BC-breaking” and “deprecation” sections. Those should be where the most effort goes in. The “improvements” and “bug fixes” for Python API should be nice as well.

## 3. Summarize the other sections

For the other sections (improvements, bug fixes, performance, documentation, developers, not user facing) - use your
judgement to summarize the key PRs. You do not need to make every commit description perfect
(changed in v2.10 to simplify the process).

Once you are finished, move this very file from `todo/` to `done/` and submit a pull request.

Feel free to use https://github.com/pytorch/pytorch/releases/tag/v2.10.0 as an example.

## distributed (torchelastic)
### bc breaking
### deprecation
### new features
### improvements
- Add a `cas_backoff_max_seconds` rendezvous option that adds a random delay after a failed rendezvous state write, which reduces repeated write conflicts at large scale. It defaults to `0.0` (off) ([#185930](https://github.com/pytorch/pytorch/pull/185930))
- Pass the `@record` entrypoint's qualified name to `ErrorHandler` through `set_entrypoint_fn_name()`, and add a `record_success()` hook that runs when the entrypoint returns normally, so custom error handlers can attribute failures and observe successful completion ([#194269](https://github.com/pytorch/pytorch/pull/194269), [#194746](https://github.com/pytorch/pytorch/pull/194746), [#195034](https://github.com/pytorch/pytorch/pull/195034))
- Report socket-creation failures in the etcd server's `find_free_port()` through the module logger instead of `print` ([#197711](https://github.com/pytorch/pytorch/pull/197711))
### bug fixes
- Fix the etcd server's `find_free_port()` raising `UnboundLocalError` and skipping the remaining addresses when socket creation fails ([#191451](https://github.com/pytorch/pytorch/pull/191451))
- Fix `EtcdServer` never registering its exit handler, which left the etcd subprocess and its data directory behind when the process exited ([#197744](https://github.com/pytorch/pytorch/pull/197744))
- Fix `get_socket_with_port()` returning ports already in use on other addresses, which made the TCPStore server fail with `EADDRINUSE` ([#199015](https://github.com/pytorch/pytorch/pull/199015))
- Fix races that truncated or dropped tailed worker log output when a worker finished while its log was being read ([#195211](https://github.com/pytorch/pytorch/pull/195211))
- Fix a file descriptor leak on every file-store rendezvous created without an endpoint, which could exhaust the process file descriptor limit ([#191425](https://github.com/pytorch/pytorch/pull/191425))
- Fix an exception raised while shutting down the rendezvous in `launch_agent` replacing the worker's `ChildFailedError`; the shutdown error is now logged instead ([#195316](https://github.com/pytorch/pytorch/pull/195316))
### performance
### docs
- Fix the outdated `EtcdServer` usage example and arguments, and remove a nonexistent `id` argument from the `Worker` docstring ([#198238](https://github.com/pytorch/pytorch/pull/198238), [#199255](https://github.com/pytorch/pytorch/pull/199255))
### devs
### Untopiced
### not user facing
### security
