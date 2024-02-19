import argparse
import os
import shutil
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import List

from qai_hub_models.scripts.generate_model_readme import generate_model_readme
from qai_hub_models.scripts.generate_summary_table import (
    generate_table,
    get_global_readme_path,
)
from qai_hub_models.utils.asset_loaders import (
    ASSET_BASES_DEFAULT_PATH,
    ASSET_CONFIG,
    ModelZooAssetConfig,
)
from qai_hub_models.utils.config_loaders import (
    MODEL_IDS,
    MODEL_STATUS,
    QAIHM_PACKAGE_ROOT,
    QAIHMModelInfo,
)
from qai_hub_models.utils.path_helpers import QAIHM_PACKAGE_NAME

QAIHM_ZOO_MODELS: List[QAIHMModelInfo] = [
    QAIHMModelInfo.from_model(id) for id in MODEL_IDS
]
PRIVATE_MODELS = [cfg for cfg in QAIHM_ZOO_MODELS if cfg.status == MODEL_STATUS.PRIVATE]
PUBLIC_MODELS = [cfg for cfg in QAIHM_ZOO_MODELS if cfg.status == MODEL_STATUS.PUBLIC]
FOLDER_NAME = "model-zoo"


def main():
    parser = argparse.ArgumentParser(
        description="Build release QAI Hub Models code.",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "--output_dir",
        type=str,
        help="Path to output directory to dump QAI Hub Models code.",
    )
    args = parser.parse_args()

    # Verify correct environment variables are set.
    ModelZooAssetConfig.load_asset_cfg(
        ASSET_BASES_DEFAULT_PATH, verify_env_has_all_variables=True
    )

    # Output folder
    output_folder = TemporaryDirectory()
    output_dir = Path(args.output_dir)
    output_root = Path(output_folder.name) / FOLDER_NAME

    # Verify output dir is valid
    if os.path.exists(output_dir / FOLDER_NAME):
        raise ValueError(f"{output_dir / FOLDER_NAME} already exists")

    # Copy repo root to tmp
    repo_dir = QAIHM_PACKAGE_ROOT.parent
    shutil.copytree(repo_dir, output_root)
    models_package_path = output_root / QAIHM_PACKAGE_NAME

    # Remove private models
    for model in PRIVATE_MODELS:
        shutil.rmtree(model.get_package_path(output_root))

    # Prepare public models
    for model in PUBLIC_MODELS:
        # If the model is missing a yaml, don't publish it
        if not os.path.exists(model.get_perf_yaml_path(output_root)):
            os.remove(model.get_package_path(output_root))
            continue

        # Write public readmes
        with open(model.get_readme_path(output_root), "w") as README:
            README.write(
                generate_model_readme(model, model.has_model_requirements(output_root))
            )

        # Remove info yaml
        os.remove(model.get_info_yaml_path(output_root))
        if model.get_code_gen_yaml_path(output_root).exists():
            os.remove(model.get_code_gen_yaml_path(output_root))

    # Remove private tests & utils
    os.remove(models_package_path / "utils" / "config_loaders.py")
    os.remove(models_package_path / "utils" / "path_helpers.py")
    os.remove(models_package_path / "test" / "test_utils" / "test_info_specs.py")

    # Remove internal files
    shutil.rmtree(models_package_path / "scripts")
    shutil.rmtree(models_package_path / "models" / "internal")
    shutil.rmtree(models_package_path / "utils" / "internal")

    # Remove repository garbage
    for path in [
        "build",
        "qai_hub_models.egg-info",
        ".pytest_cache",
        ".mypy_cache",
        "qaihm-dev",
        ".coverage",
        ".git",
    ]:
        if os.path.exists(output_root / path):
            if os.path.isdir(output_root / path):
                shutil.rmtree(output_root / path)
            else:
                os.remove(output_root / path)

    # Dump README table
    readme_with_table = generate_table(PUBLIC_MODELS)
    with open(get_global_readme_path(output_root), "a") as global_readme:
        global_readme.write(readme_with_table)

    # Write Global README paths
    readme_with_table.replace("{REPOSITORY_URL}", ASSET_CONFIG.repo_url)
    readme_with_table.replace(
        "{REPOSITORY_ROOT_FILE_NAME}", ASSET_CONFIG.repo_url.split("/")[-1]
    )

    # Copy QAI Hub Models to output dir
    shutil.move(str(output_root), str(output_dir))


if __name__ == "__main__":
    main()
