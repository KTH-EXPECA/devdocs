# #!/bin/env python3
# import jsonschema2md
# import json
# import glob
# from pathlib import Path

# def build_schemas(*args, **kwargs) -> None:
#     parser = jsonschema2md.Parser()
    
#     for fname in glob.glob('docs/technical_documents/workload_definitions/schema/*.json'):
#         fpath = Path(fname).resolve()
#         with fpath.open('r') as fp:
#             md_lines = parser.parse_schema(json.load(fp))
            
#         md_path = Path('docs/technical_documents/workload_definitions/reference') / f'{fpath.stem}.md'
#         with md_path.open('w') as fp:
#             fp.writelines(md_lines)
    
