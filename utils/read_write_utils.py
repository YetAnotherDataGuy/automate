import json
import yaml
import os
from typing import (
    Union,
    List,
    Dict,
    Any
)


def read_and_load_as_dict(file: str, fmt: str, multiline_json=False) -> Union[List[Dict[str, Any]], Dict[str, Any]]:
    """
    Description:
    This utility function reads a  file of a specific format and convert it into
    python dictionary or list of dictionaries.

    :param file: Absolute path to file
    :param fmt: File format. If the specified format is not implemented , it will raise exception.
    :param multiline_json: Boolean value which provides information that if the file contains multi line
    json or not. Only required for JSON file formats. By default it is Fasle.
    :return: Dictionary or List of dictionaries
    """
    implemented_formats = ('yml', 'json', 'yaml')
    if fmt.lower() not in implemented_formats:
        msg = f"Mentioned file format is not implemented yet. Please choose one of the below formats:\n {implemented_formats}"
        raise NotImplementedError(msg)
    elif os.path.exists(file):
        with open(file, 'rt') as f:
            if fmt.lower() in ('yml', 'yaml'):
                out = yaml.safe_load(f.read())
            elif fmt.lower() == 'json' and multiline_json:
                out = []
                for json_obj in f:
                    out.append(json.loads(json_obj))
            elif fmt.lower() == 'json':
                out = json.load(f)

        return out
    else:
        raise FileNotFoundError(f"{file} does not exist. Please provide a valid full qualified"
                                "path for the file if the file is not in current working directory.")
