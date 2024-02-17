import os
import pickle
import pathlib
import random
import shutil
import networkx as nx
import numpy as np
from tqdm import tqdm
from data4co.solver.mis import KaMIS


class MISDataGenerator:
    def __init__(
        self,
        nodes_num_min: int=700,
        nodes_num_max: int=800,
        data_type: str="er",
        solver_type: str="kamis",
        train_samples_num: int=128000,
        val_samples_num: int=1280,
        test_samples_num: int=1280,
        save_path: pathlib.Path="data/mis/er",
        filename: str=None,
        # args for generate
        er_prob: float=0.5,
        ba_conn_degree: int=10,
        hk_prob: float=0.5,
        hk_conn_degree: int=10,
        ws_prob: float=0.5,
        ws_ring_neighbors: int=2,
        # args for solve
        kamis_recompile: bool=False,
        mis_weighted: bool=False,
        solve_limit_time: float=600.0,
    ):
        # record variable data
        self.nodes_num_min = nodes_num_min
        self.nodes_num_max = nodes_num_max
        self.data_type = data_type
        self.solver_type = solver_type
        self.train_samples_num = train_samples_num
        self.val_samples_num = val_samples_num
        self.test_samples_num = test_samples_num
        self.save_path = save_path
        self.filename = filename
        # args for generate
        self.er_prob = er_prob
        self.ba_conn_degree = ba_conn_degree
        self.hk_prob = hk_prob
        self.hk_conn_degree = hk_conn_degree
        self.ws_prob = ws_prob
        self.ws_ring_neighbors = ws_ring_neighbors
        # args for solve
        self.kamis_recompile = kamis_recompile
        self.mis_weighted = mis_weighted
        self.solve_limit_time = solve_limit_time
        
        # check the input variables
        self.sample_types = ['train', 'val', 'test']
        self.check_data_type()
        self.check_solver_type()
        self.check_save_path()
        self.get_filename()
        
    def check_data_type(self):
        generate_func_dict = {
            "erdos_renyi": self.generate_erdos_renyi,
            "er": self.generate_erdos_renyi,
            "barabasi_albert": self.generate_barabasi_albert,
            "ba": self.generate_barabasi_albert,
            "holme_kim": self.generate_holme_kim,
            "hk": self.generate_holme_kim,
            "watts_strogatz": self.generate_watts_strogatz,
            "ws": self.generate_watts_strogatz,
        }
        supported_data_type = generate_func_dict.keys()
        if self.data_type not in supported_data_type:
            message = f"The input data_type({self.data_type}) is not a valid type, "
            message += f"and the generator only supports {supported_data_type}"
            raise ValueError(message)
        self.generate_func = generate_func_dict[self.data_type]    
    
    def check_save_path(self):
        if not os.path.exists(self.save_path):
            os.makedirs(self.save_path)
        for sample_type in self.sample_types:
            path = os.path.join(self.save_path, sample_type)
            setattr(self, f"{sample_type}_save_path", path)
            if not os.path.exists(path):
                os.mkdir(path)

    def get_filename(self):
        if self.filename is None:
            self.filename = f"mis_{self.data_type}_{self.nodes_num_min}_{self.nodes_num_max}"
        
    def check_solver_type(self):
        supported_solver_dict = {
            "kamis": self.solve_by_kamis, 
            "gurobi": self.solve_by_gurobi
        }
        supported_solver_type = supported_solver_dict.keys()
        if self.solver_type not in supported_solver_type:
            message = f"The input solver_type({self.solver_type}) is not a valid type, "
            message += f"and the generator only supports {supported_solver_type}"
            raise ValueError(message)
        self.solver = supported_solver_dict[self.solver_type]
        if self.solver_type == "kamis" and self.kamis_recompile:
            self.recompile_kamis()
    
    def recompile_kamis(self):
        if os.path.exists('solver/mis/KaMIS/deploy/'):
            shutil.rmtree('solver/mis/KaMIS/deploy/')
        shutil.copytree('solver/mis/kamis-source/', 
                        'solver/mis/KaMIS/tmp_build/')
        ori_dir = os.getcwd()
        os.chdir('solver/mis/KaMIS/tmp_build/')
        os.system("bash cleanup.sh")
        os.system("bash compile_withcmake.sh")
        os.chdir(ori_dir)
        shutil.copytree('solver/mis/KaMIS/tmp_build/deploy/', 
                        'solver/mis/KaMIS/deploy/')
        shutil.rmtree('solver/mis/KaMIS/tmp_build/')
    
    def random_weight(self, n, mu = 1, sigma = 0.1):
        return np.around(np.random.normal(mu, sigma, n)).astype(int).clip(min=0)

    def generate(self):
        for sample_type in self.sample_types:
            samples_num = getattr(self, f"{sample_type}_samples_num")
            for idx in tqdm(range(samples_num), 
                            desc=f"Generate MIS({self.data_type}) {sample_type}_dataset"):
                filename = f"{self.filename}_{idx}"
                graph = self.generate_func()
                if self.mis_weighted:
                    weight_mapping = { 
                        vertex: int(weight) for vertex, 
                        weight in zip(
                            graph.nodes, 
                            self.random_weight(
                                graph.number_of_nodes(), 
                                sigma=30, 
                                mu=100
                            )
                        ) 
                    }
                    nx.set_node_attributes(graph, values=weight_mapping, name='weight')
                output_file = os.path.join(
                    getattr(self, f"{sample_type}_save_path"), f"{filename}.gpickle"
                )
                with open(output_file, "wb") as f:
                    pickle.dump(graph, f, pickle.HIGHEST_PROTOCOL)
                    
    def solve(self):
        for sample_type in self.sample_types:
            folder = getattr(self, f"{sample_type}_save_path")
            self.solver(folder)

    def generate_erdos_renyi(self) -> nx.Graph:
        num_nodes = random.randint(self.nodes_num_min, self.nodes_num_max)
        return nx.erdos_renyi_graph(num_nodes, self.er_prob)

    def generate_barabasi_albert(self) -> nx.Graph:
        num_nodes = random.randint(self.nodes_num_min, self.nodes_num_max)
        return nx.barabasi_albert_graph(num_nodes, min(self.ba_conn_degree, num_nodes))

    def generate_holme_kim(self) -> nx.Graph:
        num_nodes = random.randint(self.nodes_num_min, self.nodes_num_max)
        return nx.powerlaw_cluster_graph(num_nodes, min(self.hk_conn_degree, num_nodes), self.hk_prob)   

    def generate_watts_strogatz(self) -> nx.Graph:
        num_nodes = random.randint(self.nodes_num_min, self.nodes_num_max)
        return nx.watts_strogatz_graph(num_nodes, self.ws_ring_neighbors, self.ws_prob)

    def solve_by_kamis(self, folder: pathlib.Path):
        solver = KaMIS(self.mis_weighted, self.solve_limit_time)
        try:
            solver.solve(folder, folder)
        except TypeError:
            message = "expected str, bytes or os.PathLike object, not float. "
            message += "This may be the reason for KaMIS compilation, "
            message += "you can try 'self.recompile_kamis()'"
            raise TypeError(message)
        
    def solve_by_gurobi(self):
        pass
