import os
import glob
import numpy as np
import torch
import torch.nn.functional as F

cuda = True if torch.cuda.is_available() else False

def check_adj_param_size(adj_parameter, data_tr_list):
    # adj param is a tuneable hyperparameter, but it has to be < number of sample in train data block
    sample_sizes = [block.shape[0] for block in data_tr_list]
    common_size = all(x==sample_size[0] for x in sample_sizes)
    if not common_size:
        raise Exception('Samples have no common size, check')
    return adj_parameter

def getViewList(data_folder):
    exclude = "labels"
    pattern = "_tr"
    # First list all files of data folder
    files = glob.glob(os.path.join(data_folder, f"*{pattern}*"))
    vlist = []
    for file in files:
        if exclude not in file:
            base = os.path.splitext(os.path.basename(file))[0]
            name = base.replace(pattern, "")
            vlist.append(name)
    view_list = sorted(vlist)
    return view_list

def cal_sample_weight(labels, num_class, use_sample_weight=True):
    if not use_sample_weight:
        return np.ones(len(labels)) / len(labels)
    count = np.zeros(num_class)
    for i in range(num_class):
        count[i] = np.sum(labels==i)
    sample_weight = np.zeros(labels.shape)
    for i in range(num_class):
        sample_weight[np.where(labels==i)[0]] = count[i]/np.sum(count)
    
    return sample_weight


def one_hot_tensor(y, num_dim):
    y_onehot = torch.zeros(y.shape[0], num_dim)
    y_onehot.scatter_(1, y.view(-1,1), 1)
    
    return y_onehot


def cosine_distance_torch(x1, x2=None, eps=1e-8):
    """
    Calculates the cosine distance tensor x1 vs tensor x2
    
    Parameters
    ----------
        x1: torch.Tensor
          The data tensor
        x2: torch.Tensor
          Default is the same data tensor of x1, otherwise extra data tensor input
        eps: float, optional
          The epsilon (error) of each entry 
    """
    x2 = x1 if x2 is None else x2
    # calculates norm for x1 in frobenius form of dimension 1
    w1 = x1.norm(p=2, dim=1, keepdim=True)
    # calculates norm for x2 in frobenius form of dimension 1
    w2 = w1 if x2 is x1 else x2.norm(p=2, dim=1, keepdim=True)
    return 1 - torch.mm(x1, x2.t()) / (w1 * w2.t()).clamp(min=eps)

def to_sparse(x):
    x_typename = torch.typename(x).split('.')[-1]
    sparse_tensortype = getattr(torch.sparse, x_typename)
    indices = torch.nonzero(x)
    if len(indices.shape) == 0:  # if all elements are zeros
        return sparse_tensortype(*x.shape)
    indices = indices.t()
    values = x[tuple(indices[i] for i in range(indices.shape[0]))]
    return sparse_tensortype(indices, values, x.size())


def cal_adj_mat_parameter(edge_per_node, data, metric="cosine"):
    assert metric == "cosine", "Only cosine distance implemented"
    dist = cosine_distance_torch(data, data)
    parameter = torch.sort(dist.reshape(-1,)).values[edge_per_node*data.shape[0]]
    #return np.asscalar(parameter.data.cpu().numpy())
    return np.ndarray.item(parameter.data.cpu().numpy())



def graph_from_dist_tensor(dist, parameter, self_dist=True):
    
    """
    Returns a graph with diagonals 0, with all other entries
    equals 1 if distance <= parameters, 0s otherwise
    
    Parameters
    ----------
    dist: torch.Tensor
        The cosine distance matrix of the data
    
    parameter: int
        Number of adjacent parameters
    
    self_dict= bool, optional
        EDIT here
    """
    if self_dist:
        assert dist.shape[0]==dist.shape[1], "Input is not pairwise dist matrix"
    g = (dist <= parameter).float()
    if self_dist:
        diag_idx = np.diag_indices(g.shape[0])
        g[diag_idx[0], diag_idx[1]] = 0
        
    return g


def gen_adj_mat_tensor(data, parameter, metric="cosine"):
    assert metric == "cosine", "Only cosine distance implemented"
    dist = cosine_distance_torch(data, data)
    g = graph_from_dist_tensor(dist, parameter, self_dist=True)
    if metric == "cosine":
        adj = 1-dist
    else:
        raise NotImplementedError
    adj = adj*g 
    adj_T = adj.transpose(0,1)
    I = torch.eye(adj.shape[0])
    if cuda:
        I = I.cuda()
    adj = adj + adj_T*(adj_T > adj).float() - adj*(adj_T > adj).float()
    adj = F.normalize(adj + I, p=1)
    adj = to_sparse(adj)
    
    return adj


def gen_test_adj_mat_tensor(data, trte_idx, parameter, metric="cosine"):
    assert metric == "cosine", "Only cosine distance implemented"
    adj = torch.zeros((data.shape[0], data.shape[0]))
    if cuda:
        adj = adj.cuda()
    num_tr = len(trte_idx["tr"])
    
    dist_tr2te = cosine_distance_torch(data[trte_idx["tr"]], data[trte_idx["te"]])
    g_tr2te = graph_from_dist_tensor(dist_tr2te, parameter, self_dist=False)
    if metric == "cosine":
        adj[:num_tr,num_tr:] = 1-dist_tr2te
    else:
        raise NotImplementedError
    adj[:num_tr,num_tr:] = adj[:num_tr,num_tr:]*g_tr2te
    
    dist_te2tr = cosine_distance_torch(data[trte_idx["te"]], data[trte_idx["tr"]])
    g_te2tr = graph_from_dist_tensor(dist_te2tr, parameter, self_dist=False)
    if metric == "cosine":
        adj[num_tr:,:num_tr] = 1-dist_te2tr
    else:
        raise NotImplementedError
    adj[num_tr:,:num_tr] = adj[num_tr:,:num_tr]*g_te2tr # retain selected edges
    
    adj_T = adj.transpose(0,1)
    I = torch.eye(adj.shape[0])
    if cuda:
        I = I.cuda()
    adj = adj + adj_T*(adj_T > adj).float() - adj*(adj_T > adj).float()
    adj = F.normalize(adj + I, p=1)
    adj = to_sparse(adj)
    
    return adj


def save_model_dict(model_dict, output_name):
    # if not os.path.exists(folder):
    #     os.makedirs(folder)
    # Use a different way to just dump everything into local path
        #for module in model_dict:
    #    torch.save(model_dict[module].state_dict(), os.path.join(folder, module+".pth"))
    path = f"{output_name}.pt"
    print(f"Saving model to {path}")
    torch.save(model_dict, path)
    return None

def load_model_dict(path):
    print(f"Loading model from {path}")
    model_dict = torch.load(path)
    for m in model_dict.values():
        m.eval()
    return model_dict
    
# def load_model_dict(folder, model_dict):
#     for module in model_dict:
#         if os.path.exists(os.path.join(folder, module+".pth")):
# #            print("Module {:} loaded!".format(module))
#             model_dict[module].load_state_dict(torch.load(os.path.join(folder, module+".pth"), map_location="cuda:{:}".format(torch.cuda.current_device())))
#         else:
#             print("WARNING: Module {:} from model_dict is not loaded!".format(module))
#         if cuda:
#             model_dict[module].cuda()    
#     return model_dict