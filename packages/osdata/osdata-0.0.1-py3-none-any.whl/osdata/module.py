class Datasets:
    def __init__(self) -> None:
        pass

    def list(self):
        return print("Listing all your available datasets")

    def get(self, id: str):
        print(f'Retreiving dataset with ID: {id}')
