# final.md Proofreading TODOs

## Content/Accuracy Issues

1. [fixed] **Line 110**: Title says "Add `sliding_window` support" but the actual parameter added is `window_size`, not `sliding_window`. The description and code example correctly use `window_size`.

2. [do not fix] **Line 112**: The description says "Previously, optional arguments like `is_causal`, `return_aux`, and `scale` could be passed positionally" — but the entry just above (line 98) says `is_causal` was *removed*. This is confusing because both changes landed in the same release. The "Before (2.10)" example passes `True` as a positional `is_causal`, which is consistent, but a reader might wonder why a removed parameter is being referenced.

3. [fixed] **Line 222**: "which returns same graph" — missing "the" → "which returns **the** same graph"

4. [fixed] **Line 403**: "Attention operator support on gfx1151/1152/1153 via AOTriton 0.11.2b." — no PR link, unlike every other entry in the document.

5. [fixed] **Line 690**: "Grouped gemm 2d2d has uninitalized data." — typo "uninitalized" → "uninitialized". Also reads as a bug description, not a fix. Should be more like "Fixed uninitialized data in grouped gemm 2d2d."

6. [fixed] **Line 819**: "MIOpen channels last support remains opt-in using the environment variables..." — this reads more like a status note than a performance improvement. Unclear what changed.

7. [fixed] **Line 574**: "Hint_int -> size_hint, support size_hint in user code." — unclear for an end-user. Doesn't explain what `hint_int` was or what the practical impact is.

8. [fixed] **Line 74**: Title mentions `torch.hub.get_dir()` but `get_dir()` doesn't take a `trust_repo` parameter. Seems like it shouldn't be listed here.

## Formatting Issues

9. [fixed] **Line 410**: Malformed URL — `https://github.com/pytorch/pytorch/issues/162143]` has a trailing `]` inside the link text.

10. [fixed] **Line 594**: "better error message for mixed device tensors" — not capitalized, unlike every other bullet point.

11. [fixed] **Line 176-177**: Missing blank line between the end of the `DTensor.to_local()` BC entry and the start of the `_PhiloxState` BC entry.

12. [fixed] **Line 836**: Two PR links with no comma: `([#171671](...)) ([#172527](...))` — should be `([#171671](...), [#172527](...))` to match the pattern used everywhere else.

13. [skip] **Lines 412, 419, 480, 534, 543, etc.**: `####` subheadings (Dynamo, Inductor, DTensor, etc.) appear under `##` parents, skipping `###`. This is consistent throughout the doc so it's a style choice, but it means these render at h4 size which is quite small.

14. [fixed] **Line 395**: `x=torch.rand(10, 1, 10, device='mps')` — missing spaces around `=` in code example.

15. [fixed] **Lines 128-137**: The DebugInfoWriter examples use ` ```python ` but contain only comments, not executable Python. Plain ` ``` ` would be more appropriate.

16. [fixed] **Line 203**: Trailing whitespace after "behavior." (double-space before end of line).

## Minor Wording

17. [fixed] **Line 875**: "Update previous version 2.10 installation in get start xpu" — awkward phrasing, likely should be "Get Started" guide.

18. [fixed] **Line 596**: "Change cpp_kernel_name to public API to match AOTI shim gen; add mm_type_out to AOTI fallback kernel" — trailing double space, and the description is quite terse/internal-facing for release notes.

19. [fixed] **Line 401**: Device property names (`clock_rate`, `memory_clock_rate`, etc.) should use backticks for consistency with the rest of the doc.
