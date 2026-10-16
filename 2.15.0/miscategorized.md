# Miscategorized PRs

PRs that ended up in the wrong worksheet, organized by which area they belong to.

- Improve the error when a symbolic size reaches an op expecting concrete ints: report the offending index and value, and suggest common dynamic-shape causes ([#186082](https://github.com/pytorch/pytorch/pull/186082))
- Speed up `FunctionalTensor` creation with dynamic shapes by reusing the inner tensor's storage size (about 1s less compile time on one model) ([#193416](https://github.com/pytorch/pytorch/pull/193416))
