# torch-release-notes

This repo tracks release notes worksheets for each PyTorch release.

## Repo Structure

```
<version>/           # e.g. 2.11.0/
  todo/              # worksheets not yet completed
    result_<area>.md # one file per functional area
  done/              # completed worksheets
    result_<area>.md
  miscategorized.md  # PRs that were put in the wrong area
final_template.md    # template for the merged final release notes
merge.py             # script to merge all done/ files into final notes
```

