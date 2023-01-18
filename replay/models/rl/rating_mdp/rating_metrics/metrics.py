import numpy as np
import math
import wandb

def ndcg(k, pred, ground_truth) -> float:
    """
      >>> import pandas as pd
    >>> pred=pd.DataFrame({"user_idx": [1, 1, 2, 2],
    ...                    "item_idx": [4, 5, 6, 7],
    ...                    "relevance": [1, 1, 1, 1]})
    >>> true=pd.DataFrame({"user_idx": [1, 1, 1, 1, 1, 2],
    ...                    "item_idx": [1, 2, 3, 4, 5, 8],
    ...                    "relevance": [0.5, 0.1, 0.25, 0.6, 0.2, 0.3]})
    >>> ndcg = NDCG()
    >>> ndcg(pred, true, 2)
    0.5
    """
    pred_len = min(k, len(pred))
    ground_truth_len = min(k, len(ground_truth))
    denom = [1 / math.log2(i + 2) for i in range(k)]
    dcg = sum(denom[i] for i in range(pred_len) if pred[i] in ground_truth)
    idcg = sum(denom[:ground_truth_len])
    return dcg / idcg


    
def true_ndcg(obs_for_pred, users_full, inv_mapp_items, top_k = 10):
    def item_mapping(item):
        minv = 10000
        decoded = -1
        values = np.asarray([np.asarray(v) for v in inv_mapp_items.keys()])
        original_values = np.asarray([np.asarray(v) for v in inv_mapp_items.values()])
        diff = np.abs(values - item).sum(axis = 1)
        arg = np.argmin(diff)
        original = original_values[arg]      
        return original
            
    def metrics(model = None, episodes = None):
            metrics_ndcg = []
            for episode in episodes:
                current_user = episode.observations[0][:8]
              #  print(users_full)
                values = (users_full - current_user).mean(axis=1) 
                user_observation = obs_for_pred[np.where(values < 0.1)]
                items = [value[8:] for value in user_observation]
                predicted_rating = model.predict(user_observation)
                item_ratings = list(zip(items, predicted_rating))
                predicted_top_items = sorted(item_ratings, key = lambda item_rat:item_rat[1])[::-1]
                predicted_top_items = list(zip(*predicted_top_items))[0]
                
                #find original top items
                true_user_items = [value[8:] for value in episode.observations]
                true_item_ratings = episode.rewards.tolist()
                true_item_ratings = list(zip(true_user_items,true_item_ratings))
                original_top_items = sorted(true_item_ratings, key = lambda item_rat:item_rat[1])[::-1]
                original_top_items = list(zip(*original_top_items))[0]
                
                predicted_to_real = [item_mapping(item) for item in predicted_top_items[:100]]
                original_to_real = [item_mapping(item) for item in original_top_items[:100]]

                ndcg_user = ndcg(top_k, predicted_to_real, original_to_real)
                metrics_ndcg.append(ndcg_user)
            result = np.mean(metrics_ndcg)
            wandb.log({"NDCG": result})
            return np.mean(metrics_ndcg)
    return metrics
