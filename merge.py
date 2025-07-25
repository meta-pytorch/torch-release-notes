import argparse
import glob
import marko
import os

from marko.md_renderer import MarkdownRenderer


def get_arg_parser():
    parser = argparse.ArgumentParser(
        prog='merge',
        description='Merges a directory of results .md files into a single .md file')
    parser.add_argument('-d', '--dir', required=True)
    parser.add_argument('-o', '--output', required=True)
    return parser


# returns a tuple of (module name, dict of category name -> [list of commits])
def parse_result_md(md_text):
    m = marko.Markdown(parser=marko.parser.Parser, renderer=MarkdownRenderer)
    ast = m.parse(md_text)

    # pull out the module name; it should be in a single level 2 heading
    module_name_heading = [c for c in ast.children
                           if isinstance(c, marko.block.Heading) and c.level == 2]
    assert len(module_name_heading) == 1
    module_name = module_name_heading[0].children[0].children

    # get all the level 3 headings that correspond to commit categories
    headings = [(c, i) for (i, c) in enumerate(ast.children)
                if isinstance(c, marko.block.Heading) and c.level == 3]

    # each level 3 heading should have a single RawText child with children as a str
    commit_info = {}
    for h, h_child_idx in headings:
        assert len(h.children) == 1 and isinstance(h.children[0], marko.inline.RawText)
        raw_text = h.children[0]
        assert isinstance(raw_text.children, str)
        commit_category = raw_text.children.lower()

        # commits should be in a list after the heading
        # seeing the next heading before a list implies that there is no list
        commit_list = None
        for i in range(h_child_idx + 1, len(ast.children)):
            if isinstance(ast.children[i], marko.block.List):
                commit_list = ast.children[i]
                break
            elif isinstance(ast.children[i], marko.block.Heading):
                break

        # this category may be empty
        if commit_list is None:
            continue

        # render each child commit line back as markdown
        commits = [m.render(commit) for commit in commit_list.children]
        num_commits = len(commits)
        print(f'found {num_commits} commits for module {module_name} + category {commit_category}')
        commit_info[commit_category] = commits
    return module_name, commit_info


# Sorts commits primarily by category name instead of by module name
# input is per module commits:
#   dict of module_name -> {dict of category name -> [list of commits]}
# returns per category commits:
#   dict of category name -> {dict of module name -> [list of commits]}
def sort_commits_by_category(per_module_commits):
    per_category_commits = {}
    for (module_name, cat_commits) in per_module_commits.items():
        for (cat_name, cat_list) in cat_commits.items():
            if cat_name not in per_category_commits:
                per_category_commits[cat_name] = {}
            per_category_commits[cat_name][module_name] = cat_list
    return per_category_commits


def write_output(per_category_commits, output_filename):
    # defines the order in which these are written in the output file + nicely formatted name
    # note that "not user facing" is intentionally left out
    category_order = [
        ("bc breaking", "Backwards Incompatible Changes"),
        ("deprecation", "Deprecations"),
        ("new features", "New Features"),
        ("improvements", "Improvements"),
        ("bug fixes", "Bug Fixes"),
        ("performance", "Performance"),
        ("docs", "Documentation"),
        ("security", "Security"),
        ("devs", "Developers"),
    ]

    # short name -> nice name
    module_name_mapping = {
        'functorch': 'Functorch',
        'fx': 'FX',
        'autograd_frontend': 'Autograd',
        'foreach_frontend': 'Foreach',
        'mps': 'MPS',
        'onnx': 'ONNX',
        'optim': 'Optimizer',
        'optimizer_frontend': 'Optimizer Frontend',
        'sparse_frontend': 'Sparse Frontend',
        'cpp_frontend': 'C++ Frontend',
        'nn_frontend': 'torch.nn',
        'caffe2': 'Caffe2',
        'complex_frontend': 'Complex Frontend',
        'mobile': 'Mobile',
        'package': 'Package',
        'vulkan': 'Vulkan',
        'python_frontend': 'Python Frontend',
        'distributed (checkpoint)': 'Distributed Checkpointing',
        'dataloader_frontend': 'Dataloader Frontend',
        'jit': 'JIT',
        'linalg_frontend': 'Linear Algebra Frontend',
        'inductor (aoti)': 'Ahead-Of-Time Inductor (AOTI)',
        'cuda': 'CUDA',
        'cudnn': 'cuDNN',
        'cpu (x86)': 'CPU (x86)',
        'cpu (aarch64)': 'CPU (AArch64)',
        'xpu': 'XPU',
        'export': 'Export',
        'quantization': 'Quantization',
        'releng': 'Release Engineering',
        'rocm': 'ROCm',
        'build_frontend': 'Build Frontend',
        'inductor': 'Inductor',
        'composability': 'Composability',
        'distributed': 'Distributed',
        'profiler': 'Profiler',
        'dynamo': 'Dynamo',
        'torch.func': 'torch.func',
        'nested tensor_frontend': 'Nested Tensor (NJT)',
    }

    with open(output_filename, 'w') as f:
        for cat_short_name, cat_nice_name in category_order:
            f.write(f"# {cat_nice_name}\n")
            if cat_short_name not in per_category_commits:
                print(f'Found no commits for category {cat_short_name}; skipping')
                continue
            cat_commits = per_category_commits[cat_short_name]
            module_names = sorted(cat_commits.keys())
            for module_name in module_names:
                assert module_name in module_name_mapping, f"no nice name for {module_name} found; mapping needs to be updated"
                nice_module_name = module_name_mapping[module_name]
                f.write(f"## {nice_module_name}\n")
                module_commits = cat_commits[module_name]
                for commit in module_commits:
                    f.write(f"- {commit}\n")


def main(args):
    md_pattern = os.path.join(args.dir, "result_*.md")
    md_filenames = glob.glob(md_pattern)
    per_module_commits = {}
    for md_filename in md_filenames:
        with open(md_filename, 'r') as f:
            md_text = f.read()
        module_name, commit_info = parse_result_md(md_text)
        per_module_commits[module_name] = commit_info
    per_category_commits = sort_commits_by_category(per_module_commits)
    write_output(per_category_commits, args.output)


if __name__ == "__main__":
    parser = get_arg_parser()
    args = parser.parse_args()
    main(args)
