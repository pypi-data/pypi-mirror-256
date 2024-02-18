"""Class that benchmarks Scandinavian language models."""

import importlib.metadata
import json
import logging
import re
import sys
from pathlib import Path
from shutil import rmtree
from time import sleep

from pydantic import BaseModel

from .benchmark_config_factory import build_benchmark_config
from .config import DatasetConfig, Language
from .dataset_configs import get_all_dataset_configs
from .dataset_factory import DatasetFactory
from .enums import Device, Framework
from .exceptions import InvalidBenchmark, InvalidModel
from .types import ScoreDict
from .utils import get_huggingface_model_lists

logger = logging.getLogger(__package__)


class BenchmarkResult(BaseModel):
    """A benchmark result."""

    dataset: str
    task: str
    dataset_languages: list[str]
    model: str
    results: ScoreDict
    num_model_parameters: int
    max_sequence_length: int
    vocabulary_size: int
    generative: bool
    few_shot: bool
    validation_split: bool
    scandeval_version: str = importlib.metadata.version(__package__)

    @classmethod
    def from_dict(cls, config: dict) -> "BenchmarkResult":
        """Create a benchmark result from a dictionary.

        Args:
            config:
                The configuration dictionary.

        Returns:
            The benchmark result.
        """
        # To be backwards compatible, we accept old results which changed the model
        # name with parameters rather than adding them as explicit parameters
        val_matches = re.search(r"\(.*val.*\)$", config["model"])
        few_shot_matches = re.search(r"\(.*few-shot.*\)$", config["model"])
        config["model"] = re.sub(
            r"\(.*(few-shot|val).*\)$", "", config["model"]
        ).strip()

        # The default value for `few_shot` is True. It won't do anything if the model
        # is not generative, so this is fine
        if "generative" not in config:
            config["generative"] = few_shot_matches is not None
        if "few_shot" not in config:
            config["few_shot"] = True

        if "validation_split" not in config:
            config["validation_split"] = val_matches is not None

        return cls(**config)

    def append_to_results(self, results_path: Path) -> None:
        """Append the benchmark result to the results file.

        Args:
            results_path:
                The path to the results file.
        """
        json_str = json.dumps(self.dict())
        with results_path.open("a") as f:
            f.write("\n" + json_str)


class Benchmarker:
    """Benchmarking all the Scandinavian language models.

    Attributes:
        benchmark_config:
            The benchmark configuration.
        force:
            Whether to force evaluations of models, even if they have been benchmarked
            already.
        dataset_factory:
            The factory for creating datasets.
        results_path:
            The path to the results file.
        benchmark_results:
            The benchmark results.
    """

    def __init__(
        self,
        progress_bar: bool = True,
        save_results: bool = False,
        language: str | list[str] = ["da", "sv", "no"],
        model_language: str | list[str] | None = None,
        framework: Framework | str | None = None,
        dataset_language: str | list[str] | None = None,
        task: str | list[str] | None = None,
        batch_size: int = 32,
        evaluate_train: bool = False,
        raise_errors: bool = False,
        cache_dir: str = ".scandeval_cache",
        token: bool | str = False,
        openai_api_key: str | None = None,
        force: bool = False,
        device: Device | None = None,
        verbose: bool = False,
        trust_remote_code: bool = False,
        load_in_4bit: bool | None = None,
        use_flash_attention: bool = False,
        clear_model_cache: bool = False,
        only_validation_split: bool = False,
        few_shot: bool = True,
    ) -> None:
        """Initialise the benchmarker.

        Args:
            progress_bar:
                Whether progress bars should be shown. Defaults to True.
            save_results:
                Whether to save the benchmark results to
                'scandeval_benchmark_results.jsonl'. Defaults to False.
            language:
                The language codes of the languages to include, both for models and
                datasets. Here 'no' means both Bokmål (nb) and Nynorsk (nn). Set this
                to 'all' if all languages (also non-Scandinavian) should be considered.
                Defaults to ['da', 'sv', 'no'].
            model_language:
                The language codes of the languages to include for models. If specified
                then this overrides the `language` parameter for model languages.
                Defaults to None.
            framework:
                The model framework to use. Only relevant if `model-id` refers to a
                local path. Otherwise, the framework will be set automatically.
                Defaults to None.
            dataset_language:
                The language codes of the languages to include for datasets. If
                specified then this overrides the `language` parameter for dataset
                languages. Defaults to None.
            task:
                The tasks benchmark the model(s) on. If "all" then datasets will not be
                filtered based on their task. Defaults to "all".
            batch_size:
                The batch size to use. Defaults to 32.
            evaluate_train:
                Whether to evaluate the training set as well. Defaults to False.
            raise_errors:
                Whether to raise errors instead of skipping the model evaluation.
                Defaults to False.
            cache_dir:
                Directory to store cached models. Defaults to '.scandeval_cache'.
            token:
                The authentication token for the Hugging Face Hub. If a boolean value
                is specified then the token will be fetched from the Hugging Face CLI,
                where the user has logged in through `huggingface-cli login`. If a
                string is specified then it will be used as the token. Defaults to
                False.
            openai_api_key:
                The OpenAI API key to use for authentication. If None, then no OpenAI
                models will be evaluated. Defaults to None.
            force:
                Whether to force evaluations of models, even if they have been
                benchmarked already. Defaults to False.
            device:
                The device to use for benchmarking. Defaults to None.
            verbose:
                Whether to output additional output. Defaults to False.
            trust_remote_code:
                Whether to trust remote code when loading models. Defaults to False.
            load_in_4bit:
                Whether to load models in 4-bit precision. If None then this will be
                done if CUDA is available and the model is a decoder model. Defaults to
                None.
            use_flash_attention:
                Whether to use Flash Attention. Defaults to False.
            clear_model_cache:
                Whether to clear the model cache after benchmarking each model.
                Defaults to False.
            only_validation_split:
                Whether to only evaluate the validation split of the datasets. Defaults
                to False.
            few_shot:
                Whether to only evaluate the model using few-shot evaluation. Only
                relevant if the model is generative. Defaults to True.
        """
        self.benchmark_config = build_benchmark_config(
            language=language,
            model_language=model_language,
            dataset_language=dataset_language,
            dataset_task=task,
            batch_size=batch_size,
            raise_errors=raise_errors,
            cache_dir=cache_dir,
            evaluate_train=evaluate_train,
            token=token,
            openai_api_key=openai_api_key,
            progress_bar=progress_bar,
            save_results=save_results,
            verbose=verbose,
            framework=framework,
            device=device,
            trust_remote_code=trust_remote_code,
            load_in_4bit=load_in_4bit,
            use_flash_attention=use_flash_attention,
            clear_model_cache=clear_model_cache,
            only_validation_split=only_validation_split,
            few_shot=few_shot,
        )

        # Set attributes from arguments
        self.force = force

        # Initialise variable storing model lists, so we only have to fetch it once
        self._model_lists: dict[str, list[str]] | None = None

        # Set up the results path
        self.results_path = Path.cwd() / "scandeval_benchmark_results.jsonl"

        # Set up the benchmark results variable, which will be populated with the
        # contents of the results file if it exists. If not, then it will be an empty
        # list
        self.benchmark_results: list[BenchmarkResult] = list()
        if self.results_path.exists():
            with self.results_path.open() as f:
                self.benchmark_results = [
                    BenchmarkResult.from_dict(json.loads(line))
                    for line in f
                    if line.strip()
                ]
        else:
            self.benchmark_results = list()

        # Set logging level based on verbosity
        if hasattr(sys, "_called_from_test"):
            logging_level = logging.CRITICAL
        elif self.benchmark_config.verbose:
            logging_level = logging.DEBUG
        else:
            logging_level = logging.INFO
        logger.setLevel(logging_level)

        # Initialise a dataset factory
        self.dataset_factory = DatasetFactory(benchmark_config=self.benchmark_config)

    def benchmark(
        self,
        model: list[str] | str | None = None,
        dataset: list[str] | str | None = None,
    ) -> list[BenchmarkResult]:
        """Benchmarks models on datasets.

        Args:
            model:
                The full Hugging Face Hub path(s) to the pretrained transformer model.
                The specific model version to use can be added after the suffix '@':
                "model@v1.0.0". It can be a branch name, a tag name, or a commit id,
                and defaults to the latest version if not specified. If None then all
                relevant model IDs will be benchmarked. Defaults to None.
            dataset:
                The datasets to benchmark on. If None then all datasets will be
                benchmarked. Defaults to None.

        Returns:
            A list of benchmark results.
        """
        if self.benchmark_config.clear_model_cache:
            self.clear_model_cache()

        # Prepare the model IDs
        model_ids = self._prepare_model_ids(model=model)

        # Get all the relevant dataset configurations
        dataset_configs = self._prepare_dataset_configs(dataset)

        # Iterate over all the models and datasets
        for m_id in model_ids:
            m_id = m_id.rstrip(" /")

            for dataset_config in dataset_configs:
                # Skip if we have already benchmarked this model on this dataset and
                # we are not forcing the benchmark
                if not self.force and model_has_been_benchmarked(
                    model_id=m_id,
                    dataset=dataset_config.name,
                    few_shot=self.benchmark_config.few_shot,
                    validation_split=self.benchmark_config.only_validation_split,
                    benchmark_results=self.benchmark_results,
                ):
                    logger.debug(
                        f"Skipping benchmarking {m_id} on {dataset_config.pretty_name},"
                        " as it has already been benchmarked."
                    )
                    continue

                # Benchmark a single model on a single dataset
                try:
                    record = self._benchmark_single(
                        dataset_config=dataset_config, model_id=m_id
                    )
                except InvalidModel as e:
                    if self.benchmark_config.raise_errors:
                        raise e
                    logger.info(e)
                    break

                # If the benchmark was unsuccessful then skip
                if isinstance(record, dict) and "error" in record:
                    error_msg = record["error"]
                    logger.info(
                        f"{m_id} could not be benchmarked on "
                        f"{dataset_config.pretty_name}. Skipping. The error message "
                        f"raised was {error_msg!r}."
                    )
                    continue

                # Add the record to the benchmark results
                assert isinstance(record, BenchmarkResult)
                self.benchmark_results.append(record)

                # Save the benchmark results
                if self.benchmark_config.save_results:
                    record.append_to_results(results_path=self.results_path)

            if self.benchmark_config.clear_model_cache:
                self.clear_model_cache()

        return self.benchmark_results

    def clear_model_cache(self) -> None:
        """Clear the model cache.

        Note that this will not remove the stored completions, and it will only clear
        the cache if `clear_model_cache` is set to True.
        """
        model_cache_path = Path(self.benchmark_config.cache_dir) / "model_cache"
        model_cache_path.mkdir(parents=True, exist_ok=True)
        for model_dir in model_cache_path.iterdir():
            if model_dir.is_dir():
                for sub_model_dir in model_dir.iterdir():
                    if sub_model_dir.is_dir():
                        rmtree(sub_model_dir)

    def _prepare_model_ids(self, model: list[str] | str | None) -> list[str]:
        """Prepare the model ID(s) to be benchmarked.

        Args:
            model:
                The model ID(s) of the models to benchmark. If None then all model IDs
                will be retrieved.

        Returns:
            The prepared list of model IDs.
        """
        model_ids: list[str]

        # If `model_id` is not specified, then fetch all the relevant model IDs
        if model is None:
            model_ids = self._get_model_ids(
                languages=self.benchmark_config.model_languages
            )

        # Otherwise, if `model_id` is a string, ensure that it is a list
        elif isinstance(model, str):
            model_ids = [model]

        # Otherwise `model_id` is already a list, so we do nothing
        else:
            model_ids = model

        # Reorder the `model_ids` list to include the ones present in the benchmark
        # results first
        benchmarked_model_ids = [
            re.sub(r"\(.+\)", "", record.model).strip()
            for record in self.benchmark_results
        ]
        model_ids_sorted = [m_id for m_id in model_ids if m_id in benchmarked_model_ids]
        model_ids_sorted += [
            m_id for m_id in model_ids if m_id not in benchmarked_model_ids
        ]

        return model_ids_sorted

    def _prepare_dataset_configs(
        self, dataset: list[str] | str | None
    ) -> list[DatasetConfig]:
        """Prepare the dataset configuration(s) to be benchmarked.

        Args:
            dataset:
                The datasets to benchmark on. If None then all datasets will be
                benchmarked. Defaults to None.

        Returns:
            The prepared list of model IDs.
        """
        if dataset is None:
            dataset_configs = [
                cfg
                for cfg in get_all_dataset_configs().values()
                if any(
                    lang in self.benchmark_config.dataset_languages
                    for lang in cfg.languages
                )
                and cfg.task in self.benchmark_config.dataset_tasks
            ]
        elif isinstance(dataset, str):
            dataset_configs = [
                cfg for cfg in get_all_dataset_configs().values() if cfg.name == dataset
            ]
        else:
            dataset_configs = [
                cfg for cfg in get_all_dataset_configs().values() if cfg.name in dataset
            ]

        return dataset_configs

    def _benchmark_single(
        self, dataset_config: DatasetConfig, model_id: str
    ) -> BenchmarkResult | dict[str, str]:
        """Benchmark a single model on a single dataset.

        Args:
            dataset_config:
                The dataset configuration to use.
            model_id:
                The model ID to use.

        Returns:
            The benchmark result, or a dictionary containing an error message.
        """
        logger.info(f"Benchmarking {model_id} on {dataset_config.pretty_name}")
        while True:
            try:
                dataset = self.dataset_factory.build_dataset(dataset_config)
                results, metadata_dict = dataset(model_id)
                record = BenchmarkResult(
                    dataset=dataset_config.name,
                    task=dataset_config.task.name,
                    dataset_languages=[
                        language.code for language in dataset_config.languages
                    ],
                    model=model_id,
                    results=results,
                    **metadata_dict,
                )
                logger.debug(f"Results:\n{results}")
                return record

            except InvalidBenchmark as e:
                # If the model ID is not valid then raise an error, if specified
                model_err_msg = "does not exist on the Hugging Face Hub"
                if self.benchmark_config.raise_errors and model_err_msg in str(e):
                    raise e

                # Otherwise, if the error is due to Hugging Face Hub being down, then
                # wait a bit and try again
                if "The Hugging Face Hub seems to be down." in str(e):
                    wait_time = 30
                    logger.debug(
                        "The Hugging Face Hub seems to be down. Retrying in "
                        f"{wait_time} seconds."
                    )
                    sleep(wait_time)
                    continue

                # Otherwise, if the error is due to the MPS fallback not being enabled,
                # then raise an error asking the user to enable it
                elif "PYTORCH_ENABLE_MPS_FALLBACK" in str(e):
                    raise RuntimeError(
                        "The benchmark failed because the environment variable "
                        "`PYTORCH_ENABLE_MPS_FALLBACK` is not set. Please set this "
                        "environment variable to `1` and try again."
                    )

                # Otherwise, raise the error or return the error message
                else:
                    if self.benchmark_config.raise_errors:
                        raise e
                    return dict(error=str(e))

    def __call__(self, *args, **kwargs) -> list[BenchmarkResult]:
        """Call the benchmarker. See `Benchmarker.benchmark`."""
        return self.benchmark(*args, **kwargs)

    def _get_model_ids(self, languages: list[Language]) -> list[str]:
        """Get list of model IDs from the Hugging Face Hub.

        Args:
            languages:
                The languages of the models to fetch.

        Returns:
            List of model IDs.
        """
        # Specify boolean variables determining whether the input variables are new
        new_languages = self._model_lists is not None and any(
            lang.code not in self._model_lists for lang in languages
        )

        # If the model lists have not been fetched already, then do it
        if self._model_lists is None or new_languages:
            self._model_lists = get_huggingface_model_lists(
                languages=languages, token=self.benchmark_config.token
            )

        # Extract all the model IDs from the model lists, for the chosen languages
        model_ids: list[str] = list()
        for language in languages:
            model_ids.extend(self._model_lists[language.code])

        # Add the multilingual models
        model_ids.extend(self._model_lists["multilingual"])

        # Add the fresh models
        model_ids.extend(self._model_lists["fresh"])

        # Remove duplicate model IDs
        model_ids = list(set(model_ids))

        return model_ids


def model_has_been_benchmarked(
    model_id: str,
    dataset: str,
    few_shot: bool,
    validation_split: bool,
    benchmark_results: list[BenchmarkResult],
) -> bool:
    """Checks whether a model has already been benchmarked on a dataset.

    Args:
        model_id:
            The model ID.
        dataset:
            The dataset.
        few_shot:
            Whether the model was evaluated using few-shot evaluation.
        validation_split:
            Whether the model was evaluated on the validation split.
        benchmark_results:
            The benchmark results.

    Returns:
        Whether the model has already been evaluated on the dataset.
    """
    for record in benchmark_results:
        same_evaluation = record.model == model_id and record.dataset == dataset
        same_validation_split_setting = record.validation_split == validation_split
        same_few_shot_setting = record.few_shot == few_shot or not record.generative
        if same_evaluation and same_validation_split_setting and same_few_shot_setting:
            return True
    return False
