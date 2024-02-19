"""
Utility Functions for parsing input args for export and other customer facing scripts.
"""
from __future__ import annotations

import argparse
import inspect
from pydoc import locate
from typing import Any, List, Mapping, Optional, Type

from qai_hub_models.utils.base_model import (
    BaseModel,
    FromPrecompiledTypeVar,
    FromPretrainedMixin,
    FromPretrainedTypeVar,
    InputSpec,
    TargetRuntime,
)


def parse_target_runtime(path: TargetRuntime | str) -> TargetRuntime:
    return TargetRuntime[path.upper()] if isinstance(path, str) else path


def get_parser() -> argparse.ArgumentParser:
    return argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )


def get_model_cli_parser(
    cls: Type[FromPretrainedTypeVar], parser: argparse.ArgumentParser | None = None
) -> argparse.ArgumentParser:
    """
    Generate the argument parser to create this model from an argparse namespace.
    Default behavior is to assume the CLI args have the same names as from_pretrained method args.
    """
    if not parser:
        parser = get_parser()

    from_pretrained_sig = inspect.signature(cls.from_pretrained)
    for name, param in from_pretrained_sig.parameters.items():
        if name == "cls":
            continue
        # Determining type from param.annotation is non-trivial (it can be a
        # strings like "Optional[str]" or "bool | None").
        if param.default is not None:
            type_ = type(param.default)
        elif param.annotation == "bool":
            type_ = bool
        else:
            type_ = str
        parser.add_argument(
            f"--{name.replace('_', '-')}",
            type=type_,
            default=param.default,
            help=f"For documentation, see {cls.__name__}::from_pretrained.",
        )
    return parser


def get_model_kwargs(
    model_cls: Type[FromPretrainedTypeVar], args_dict: Mapping[str, Any]
) -> Mapping[str, Any]:
    """
    Given a dict with many args, pull out the ones relevant
    to constructing the model via `from_pretrained`.
    """
    from_pretrained_sig = inspect.signature(model_cls.from_pretrained)
    model_kwargs = {}
    for name in from_pretrained_sig.parameters:
        if name == "cls" or name not in args_dict:
            continue
        model_kwargs[name] = args_dict.get(name)
    return model_kwargs


def model_from_cli_args(
    model_cls: Type[FromPretrainedTypeVar], cli_args: argparse.Namespace
) -> FromPretrainedTypeVar:
    """
    Create this model from an argparse namespace.
    Default behavior is to assume the CLI args have the same names as from_pretrained method args.
    """
    return model_cls.from_pretrained(**get_model_kwargs(model_cls, vars(cli_args)))


def get_input_spec_kwargs(
    model: "BaseModel", args_dict: Mapping[str, Any]
) -> Mapping[str, Any]:
    """
    Given a dict with many args, pull out the ones relevant
    to constructing the model's input_spec.
    """
    get_input_spec_args = inspect.signature(model.get_input_spec)
    input_spec_kwargs = {}
    for name in get_input_spec_args.parameters:
        if name == "self" or name not in args_dict:
            continue
        input_spec_kwargs[name] = args_dict[name]
    return input_spec_kwargs


def get_model_input_spec_parser(
    model_cls: Type[BaseModel], parser: argparse.ArgumentParser | None = None
) -> argparse.ArgumentParser:
    """
    Generate the argument parser to get this model's input spec from an argparse namespace.
    Default behavior is to assume the CLI args have the same names as get_input_spec method args.
    """
    if not parser:
        parser = get_parser()

    get_input_spec_sig = inspect.signature(model_cls.get_input_spec)
    for name, param in get_input_spec_sig.parameters.items():
        if name == "self":
            continue
        type_: type | object
        if isinstance(param.annotation, type):
            type_ = param.annotation
        else:
            # locate() converts string type to cls type
            # Any type can be resolved as long as it's accessible in this scope
            type_ = locate(param.annotation)
            assert isinstance(type_, type)
        parser.add_argument(
            f"--{name.replace('_', '-')}",
            type=type_,
            default=param.default,
            help=f"For documentation, see {model_cls.__name__}::get_input_spec.",
        )
    return parser


def input_spec_from_cli_args(
    model: "BaseModel", cli_args: argparse.Namespace
) -> "InputSpec":
    """
    Create this model's input spec from an argparse namespace.
    Default behavior is to assume the CLI args have the same names as get_input_spec method args.
    """
    return model.get_input_spec(**get_input_spec_kwargs(model, vars(cli_args)))


def export_parser(
    model_cls: Type[FromPretrainedTypeVar] | Type[FromPrecompiledTypeVar],
    components: Optional[List[str]] = None,
    supports_qnn=True,
    exporting_compiled_model=False,
) -> argparse.ArgumentParser:
    """
    Arg parser to be used in export scripts.

    Parameters:
        model_cls: Class of the model to be exported. Used to add additional
            args for model instantiation.
        components: Some models have multiple components that need to be
            compiled separately. This represents the list of options for the user to
            select which components they want to compile.
        supports_qnn:
            Whether QNN export is supported.
            Default=True.
        exporting_compiled_model:
            True when exporting compiled model.
            If set, removing skip_profiling flag from export arguments.
            Default = False.

    Returns:
        Arg parser object.
    """
    parser = get_parser()
    parser.add_argument(
        "--device",
        type=str,
        default=None,
        help="Device for which to export.",
    )
    parser.add_argument(
        "--skip-profiling",
        action="store_true",
        help="If set, writes compiled model to local directory without profiling.",
    )
    parser.add_argument(
        "--skip-inferencing",
        action="store_true",
        help="If set, skips verifying on-device output vs local cpu.",
    )
    if not exporting_compiled_model:
        parser.add_argument(
            "--skip-downloading",
            action="store_true",
            help="If set, skips downloading of compiled model.",
        )
    parser.add_argument(
        "--skip-summary",
        action="store_true",
        help="If set, skips printing summary of inference and profiling.",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default=None,
        help="Directory to store generated assets (e.g. compiled model). "
        "Defaults to `<cwd>/build/<model_name>`.",
    )
    if not exporting_compiled_model:
        # Default runtime for compiled model is fixed for given model
        parser.add_argument(
            "--dst-runtime",
            default="TFLITE",
            help="The runtime to export for. Default is TF Lite.",
            choices=TargetRuntime._member_names_
            if supports_qnn
            else [TargetRuntime.TFLITE.name],
        )
        # No compilation for compiled models
        parser.add_argument(
            "--compile-options",
            type=str,
            default="",
            help="Additional options to pass when submitting the compile job.",
        )
    parser.add_argument(
        "--profile-options",
        type=str,
        default="",
        help="Additional options to pass when submitting the profile job.",
    )
    if components is not None:
        parser.add_argument(
            "--components",
            nargs="+",
            type=str,
            default=None,
            choices=components,
            help="Which components of the model to be exported.",
        )

    if issubclass(model_cls, FromPretrainedMixin):
        # Skip adding CLI from model for compiled model
        # TODO: #9408 Refactor BaseModel, BasePrecompiledModel to fetch
        # parameters from compiled model
        parser = get_model_cli_parser(model_cls, parser)

        if issubclass(model_cls, BaseModel):
            parser = get_model_input_spec_parser(model_cls, parser)

    return parser
