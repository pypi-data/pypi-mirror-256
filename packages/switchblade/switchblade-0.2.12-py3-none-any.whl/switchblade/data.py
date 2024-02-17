from concurrent.futures import ThreadPoolExecutor
from math import ceil
import random
import torch


class ParallelDataLoader:
    def __init__(
            self, 
            dataset, 
            batch_size: int, 
            num_workers: int, 
            shuffle: bool = False,
            subset_indices: list = None
    ):
        self.dataset = dataset
        self.batch_size = batch_size
        self.num_workers = num_workers
        self.shuffle = shuffle
        self.subset_indices = subset_indices
        self.indices = list(range(len(self.dataset)))


    def _fetch_data(self, index):
        return self.dataset.__getitem__(index)


    def __iter__(self):
        # Shuffle data indices if required
        if self.shuffle:
            random.shuffle(self.indices)

        # If subset indices were passed in, ensure every batch_size indices
        # come from the same subset_indices subset:
        if self.subset_indices:
            subsets = []
            for start, end in self.subset_indices:
                subsets.append([
                    i for i in self.indices 
                    if i in range(start, end)
                ])
                
            indices = []
            # now randomly pick a subset and append self.batch_size of its
            # indices to indices. if there is anything left over, then just
            # append at the end of indices
            while any([len(s) >= self.batch_size for s in subsets]):
                subset = random.choice([s for s in subsets if len(s) >= self.batch_size])
                indices.extend([subset.pop() for _ in range(self.batch_size)])

            for s in subsets:
                indices.extend(s)

        # This function yields batches of data
        self.executor = ThreadPoolExecutor(max_workers=self.num_workers)
        self.iterable_data = iter(self.indices)
        return self


    def __next__(self):
        # Fetch the next batch
        indices_batch = [next(self.iterable_data) for _ in range(self.batch_size)]
        futures = [self.executor.submit(self._fetch_data, index) for index in indices_batch]

        # results is a list of tuples, each containing multiple items
        results = [future.result() for future in futures]

        # Initialize lists to hold batches of each item
        batches = [[] for _ in range(len(results[0]))]

        # Iterate over the results and separate each item, stacking them if they are torch tensors
        for result in results:
            for i, item in enumerate(result):
                if isinstance(item, torch.Tensor):
                    batches[i].append(item)
                else:
                    batches[i].append(torch.tensor(item))

        # Stack the batches into tensors
        batches = [torch.stack(batch) for batch in batches]

        return batches


    def __len__(self):
        return ceil(len(self.dataset) / self.batch_size)