import ast
import subprocess
from pathlib import Path

from loguru import logger

from django_translate.services.transformers import ClassDefTransformer


def update_py_file(*, file_path: str, formatted: bool = False) -> None:
    model_file = Path(file_path).with_suffix(".py").absolute()
    tree = ast.parse(model_file.read_text())

    transformer = ClassDefTransformer()
    new_tree = transformer.visit(tree)
    new_tree = transformer.insert_getetxt_import(new_tree)

    code = ast.unparse(new_tree)
    model_file.write_text(code)

    if formatted:
        logger.info("Formatting the code...")
        subprocess.run(["ruff", "format", str(model_file)], check=True)  # noqa: S603, S607
