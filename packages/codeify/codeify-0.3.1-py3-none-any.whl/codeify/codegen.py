from .types import CodeGeneration, DirectoryContext, FileGeneration
from .modules import import_file
from .conversions import get_pascal_name

from csv import DictReader
from io import StringIO
from jinja2 import Template
from typing import Any, Dict, Iterable, List, IO, Optional
from pathlib import Path
import json
import shutil
import yaml

def _load_yaml_file(filename: str) -> Any:
    with open(filename, 'r') as fd:
        return yaml.safe_load(fd)

def _load_json_file(filename: str) -> Any:
    with open(filename, 'r') as fd:
        return json.load(fd)

def _load_csv_file(filename: str, header: Optional[List[str]] = None) -> Any:
    with open(filename, 'r') as fd:
        return list( DictReader(fd, fieldnames=header) )


class CodeGenerator:
    def __init__(self):
        self._vars : Dict[str, Any] = {}
        self._funcs : Dict[str, Any] = {}

    def load_module(self, py_file: str) -> None:
        module = import_file(py_file)
        for name in dir(module):
            if hasattr(getattr(module, name), '__call__'):
                self._funcs[name] = getattr(module, name)

    def clear_vars(self) -> None:
        self._vars.clear()

    def set_var(self, name: str, value: Any) -> None:
        self._vars[name] = value

    def _init_template_env(self, tpl: Template) -> None:
        tpl.environment.globals['pascal_name'] = get_pascal_name
        tpl.environment.globals['yaml'] = _load_yaml_file
        tpl.environment.globals['json'] = _load_json_file
        tpl.environment.globals['csv'] = _load_csv_file
        for name, func in self._funcs.items():
            tpl.environment.globals[name] = func

    def generate_string(self, input_template_file: str) -> str:
        tpl = Template( Path(input_template_file).read_text() )
        self._init_template_env(tpl)
        return tpl.render(**self._vars)

    def generate(self, input_template_file: str, output_file: str) -> None:
        Path(output_file).write_text( self.generate_string(input_template_file) )


class FileProcessor:
    def __init__(self, input_dir: str, output_dir: str, generator: CodeGenerator):
        self._input_dir = Path(input_dir)
        self._output_dir = Path(output_dir)
        self._processors = {".j2": self._process_jinja}
        self._code_gen = generator
    
    def _process_jinja(self, input_file: Path, output_file: Path) -> None:
        # Drop last extension from file
        self._code_gen.generate(str(input_file), str(output_file.with_suffix("")))

    def _copy_file(self, input_file: Path, output_file: Path) -> None:
        if input_file.is_dir():
            output_file.mkdir(exist_ok=True)
        else:
            shutil.copyfile(str(input_file), str(output_file), follow_symlinks=False)

    def _process_files(self, input_dir: Path, output_dir: Path) -> None:
        output_dir.mkdir(parents=True, exist_ok=True)
        ctx = DirectoryContext()
        
        # Check for ".codeify" file first
        codeify_template = input_dir / ".codeify"
        if codeify_template.is_file():
            ctx = load_directory_context_yaml(self._code_gen, str(codeify_template))

        for item in input_dir.iterdir():
            if ctx.ignore_file(item.name):
                continue
            proc = self._processors.get(item.suffix, self._copy_file)
            proc(item, output_dir / item.name)

        # Post-generation instructions
        generator = CodeGenerator()
        for file_gen in ctx.file_generators:
            generator.clear_vars()
            for key, value in file_gen.data.items():
                generator.set_var(key, value)
            
            inp, outp = input_dir / Path(file_gen.input_file), output_dir / Path(file_gen.output_file)
            generator.generate(str(inp), str(outp))

    def process(self) -> None:
        self._process_files(self._input_dir, self._output_dir)


def load_code_generator_yaml(yaml_file: str) -> CodeGenerator:
    code_gen = CodeGenerator()
    data = yaml.safe_load(Path(yaml_file).read_text())
    for name, value in data.items():
        code_gen.set_var(name, value)
    return code_gen


def load_directory_context_yaml(code_gen: CodeGenerator, yaml_j2_file: str) -> DirectoryContext:
    file_gen : List[FileGeneration] = []

    ctx_data = yaml.safe_load( code_gen.generate_string(yaml_j2_file) )
    ignore = ctx_data.get('ignore', []) + ['.codeify']
    for output_file, input_data in ctx_data.get('generate', {}).items():
        file_gen.append( FileGeneration(input_data['input'], output_file, input_data.get('data', {})) )

    return DirectoryContext(ignore_files=ignore, file_generators=file_gen)


def run_generation(info: CodeGeneration) -> None:
    code_gen = load_code_generator_yaml(info.spec_file)

    for module_file in info.modules:
        code_gen.load_module(module_file)

    file_proc = FileProcessor(info.input_dir, info.output_dir, code_gen)
    file_proc.process()


def generate_output(template_file: str, template_args: Iterable[str], spec_file: Optional[str], output: IO, modules: Iterable[str]) -> None:
    code_gen = CodeGenerator()

    if spec_file:
        with open(spec_file, 'r') as fd:
            yaml_data = yaml.safe_load(fd)
        # Apply first to code generator
        for key, value in yaml_data.items():
            code_gen.set_var(key, value)
    
    if template_args:
        with StringIO() as yaml_buf:
            for arg in template_args:
                name, value = arg.split('=', 1)
                yaml_buf.write(f"{name.strip()}: {value.strip()}\n")
            yaml_buf.seek(0)
            yaml_data = yaml.safe_load(yaml_buf)
        
        for key, value in yaml_data.items():
            code_gen.set_var(key, value)
    
    for module_file in modules:
        code_gen.load_module(module_file)

    output.write( code_gen.generate_string(template_file) )
