
import sys

class EarlyStoppingMonitor:

    def __init__(self, min_delta=0.001, patience=5, restore_best_weights:bool= False, verbose=True):
        self._min_delta = min_delta
        self._patience = patience
        self._n_rounds_with_no_improvement = 0
        self._best_loss_to_date = sys.float_info.max
        self._current_loss = sys.float_info.max
        self._restore_best_weights = restore_best_weights
        self._verbose = verbose
        self._best_weights = None
        self._rounds = 0
        self._epoch = 0

    def should_stop(self, average_loss, weights, epoch) -> bool:
        """

        :param average_loss: the average loss for the latest round
        :param weights:
        :return: True if there has been no improvement for more than patience rounds
        """
        self._current_loss = average_loss
        self._rounds += 1
        self._epoch = epoch
        if self._best_loss_to_date - average_loss > self._min_delta:
            # there has been an improvement better than min Delta
            self._best_loss_to_date = average_loss
            self._best_weights = weights
            self._n_rounds_with_no_improvement = 0
        else:
            self._n_rounds_with_no_improvement += 1
        return self._n_rounds_with_no_improvement > self._patience

    @property
    def n_rounds_with_no_improvement(self):
        return self._n_rounds_with_no_improvement\

    @property
    def patience(self):
        return self._patience

    @property
    def best_loss_to_date(self):
        return self._best_loss_to_date

    @property
    def current_loss(self):
        return self._current_loss

    def get_best_weights(self):
        return self._best_weights

    def display(self):
        return f"loss: {self._current_loss:.4f} (best loss to date: {self._best_loss_to_date:.4f}) \
        [round {self._rounds}/epoch {self._epoch}; rounds without improvement {self._n_rounds_with_no_improvement}/ patience: {self._patience}]"