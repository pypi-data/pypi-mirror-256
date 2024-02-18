from typing import Optional
import pickle
import logging

logger = logging.getLogger()

class Predictor:
    
    def __init__(
        self,
        local_pickle_path: Optional[str] = None,
    ):
        if local_pickle_path:
            logging.info('Loading model from local pickle file')
            self.model = self._load_pickle(local_pickle_path)
            logging.info('Model loaded successfully')
    
    @classmethod
    def from_local_pickle(cls, model_path):
        return cls(local_pickle_path=model_path)
    
    @classmethod
    def from_model_registry(cls, model_name):
        raise NotImplementedError
        # return cls()

    def _load_pickle(self, local_pickle_path):
        with open(local_pickle_path, 'rb') as f:
            model = pickle.load(f)
        return model
    
    def predict(
        self,
        ts_ms: Optional[int] = None
    ):
        if ts_ms is None:
            raise NotImplementedError
        
        
        # return 0.5
    

if __name__ == '__main__':

    from rtml.logging import initialize_logger
    initialize_logger()

    predictor = Predictor.from_local_pickle('model.pkl')

    