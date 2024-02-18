<div align='center'>
<img src="https://raw.githubusercontent.com/ScandEval/ScandEval/main/gfx/scandeval.png" width="517" height="217">
</div>

### Evaluation of pretrained language models on mono- or multilingual language tasks.

______________________________________________________________________
[![PyPI Status](https://badge.fury.io/py/scandeval.svg)](https://pypi.org/project/scandeval/)
[![Paper](https://img.shields.io/badge/arXiv-2304.00906-b31b1b.svg)](https://arxiv.org/abs/2304.00906)
[![License](https://img.shields.io/github/license/ScandEval/ScandEval)](https://github.com/ScandEval/ScandEval/blob/main/LICENSE)
[![LastCommit](https://img.shields.io/github/last-commit/ScandEval/ScandEval)](https://github.com/ScandEval/ScandEval/commits/main)
[![Code Coverage](https://img.shields.io/badge/Coverage-76%25-yellowgreen.svg)](https://github.com/ScandEval/ScandEval/tree/main/tests)
[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-2.0-4baaaa.svg)](https://github.com/ScandEval/ScandEval/blob/main/CODE_OF_CONDUCT.md)


## Maintainers

- Dan Saattrup Nielsen (@saattrupdan, dan.nielsen@alexandra.dk)
- Kenneth Enevoldsen (@KennethEnevoldsen, kenneth.enevoldsen@cas.au.dk)


## Installation
To install the package simply write the following command in your favorite terminal:
```
$ pip install scandeval
```

## Quickstart
### Benchmarking from the Command Line
The easiest way to benchmark pretrained models is via the command line interface. After
having installed the package, you can benchmark your favorite model like so:
```
$ scandeval --model-id <model-id>
```

Here `model_id` is the HuggingFace model ID, which can be found on the [HuggingFace
Hub](https://huggingface.co/models). By default this will benchmark the model on all
the datasets eligible. If you want to benchmark on a specific dataset, this can be done
via the `--dataset` flag. This will for instance evaluate the model on the
`AngryTweets` dataset:
```
$ scandeval --model-id <model-id> --dataset angry-tweets
```

We can also separate by language. To benchmark all Danish models on all Danish
datasets, say, this can be done using the `language` tag, like so:
```
$ scandeval --language da
```

Multiple models, datasets and/or languages can be specified by just attaching multiple
arguments. Here is an example with two models:
```
$ scandeval --model-id <model-id1> --model-id <model-id2> --dataset angry-tweets
```

The specific model version to use can also be added after the suffix '@':
```
$ scandeval --model-id <model-id>@<commit>
```

It can be a branch name, a tag name, or a commit id. It defaults to 'main' for latest.

See all the arguments and options available for the `scandeval` command by typing
```
$ scandeval --help
```

### Benchmarking from a Script
In a script, the syntax is similar to the command line interface. You simply initialise
an object of the `Benchmarker` class, and call this benchmark object with your favorite
models and/or datasets:
```
>>> from scandeval import Benchmarker
>>> benchmark = Benchmarker()
>>> benchmark('<model-id>')
```

To benchmark on a specific dataset, you simply specify the second argument, shown here
with the `AngryTweets` dataset again:
```
>>> benchmark('<model_id>', 'angry-tweets')
```

If you want to benchmark a subset of all the models on the Hugging Face Hub, you can
specify several parameters in the `Benchmarker` initializer to narrow down the list of
models to the ones you care about. As a simple example, the following would benchmark
all the Nynorsk models on Nynorsk datasets:
```
>>> benchmark = Benchmarker(language='nn')
>>> benchmark()
```


## Citing ScandEval
If you want to cite the framework then feel free to use this:

```
@inproceedings{nielsen2023scandeval,
  title={ScandEval: A Benchmark for Scandinavian Natural Language Processing},
  author={Nielsen, Dan Saattrup},
  booktitle={The 24rd Nordic Conference on Computational Linguistics},
  year={2023}
}
```


## Remarks
The image used in the logo has been created by the amazing [Scandinavia and the
World](https://satwcomic.com/) team. Go check them out!
