import pandas as pd
from osdata.data_loaders.module import DataLoader, extract_dir_and_basename_from_url


class Datasets:
    def __init__(self) -> None:
        self.__dl = DataLoader()

    def list(self):
        return print("Listing all your available datasets")

    def load(self, alias: str):
        ds_path, loader = self.__dl.find_by_alias(alias)
        tup = extract_dir_and_basename_from_url(ds_path)
        if ds_path:
            dir, filename = tup[0], tup[1]
            local_path = self.__dl.download_file(
                ds_path, '.osyris/datasets/{dir}/{filename}'.format(dir=dir, filename=filename))

            return self.__run_loader(local_path, loader)

    def __run_loader(self, file_path, loader):
        globals_context = globals()  # You might want to customize this
        context = {'file_path': file_path}
        code = loader.replace("\\n", "\n")
        try:
            exec(code, globals_context, context)
            df = context['df']
            return df
        except Exception as e:
            print(f"Error executing code: {e}")
