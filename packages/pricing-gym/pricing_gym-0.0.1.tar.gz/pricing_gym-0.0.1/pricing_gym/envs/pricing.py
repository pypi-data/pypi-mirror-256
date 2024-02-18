import gym
import yaml
import numpy as np
import networkx as nx

from gym import spaces
from scipy import stats
from scipy.special import expit

CAPACITY_STOP = np.array([150], dtype=float)
D0 = 540.0 
P0 = 43.904000000000025

class L2_Kernel:
    def __init__(self, params):
        self.beta = params["d"]
        self.alpha = params["p"]
        self.d0 = D0
        self.p0 = P0

    def predict(self, observation):
        # Normalise
        observation[2] = observation[2] / 100
        observation[3] = observation[3] / 100

        d = self._get_expected_demand(observation)
        p = self._get_prob_of_rejection(observation)

        lam = stats.gamma.rvs(a = p / (1 - p) * d, scale = (1 - p) / p)

        l1 = np.array([observation[1]], dtype = float)
        l2 = np.array([stats.poisson.rvs(lam)], dtype = float)

        if l1 + l2 > CAPACITY_STOP:
            return np.array([np.max(CAPACITY_STOP - l1, 0)], dtype = float)

        return l2

    def _get_expected_demand(self, observation):
        d0_low = 8
        beta_low = np.array([0, 0, 0, 0])
        if stats.bernoulli.rvs(0.5):
            d = self.d0 * np.exp(self.beta @ observation)
        else:
            d = d0_low * np.exp(beta_low @ observation)

        return d

    def _get_prob_of_rejection(self, observation):
        p = 1 / (1 + self.p0 * np.exp(self.alpha @ (observation)))
        return p

class L1_Kernel:
    def __init__(self, params):
        self.beta = params["d"]
        self.alpha = params["p"]
        self.d0 = D0
        self.p0 = P0

    def predict(self, observation):
        # Normalise
        observation[1] = observation[1] / 100
        observation[2] = observation[2] / 100

        d = self._get_expected_demand(observation)
        p = self._get_prob_of_rejection(observation)

        lam = stats.gamma.rvs(a = p / (1 - p) * d, scale = (1 - p) / p)
        l1 = np.array([stats.poisson.rvs(lam)], dtype=float)

        if l1 > CAPACITY_STOP:
            return CAPACITY_STOP

        return l1

    def _get_expected_demand(self, observation):
        d0_low = 8
        beta_low = np.array([0, 0, 0])
        if stats.bernoulli.rvs(0.5):
            d = self.d0 * np.exp(self.beta @ observation)
        else:
            d = d0_low * np.exp(beta_low @ observation)

        return d

    def _get_prob_of_rejection(self, observation):
        p = 1 / (1 + self.p0 * np.exp(self.alpha @ (observation)))
        return p

class A2_Kernel:
    def __init__(self, params):
        self.p = params["p"]

    def predict(self, observation):
        probs = self._get_p(observation)
        return np.array([(stats.binom.rvs(n = 10, p = probs) + 1) * 100], dtype = float)

    def _get_p(self, observation):
        return expit(observation @ self.p)

class X_Kernel:
    def __init__(self, p = None):
        self.p = None

    def predict(self, observation):
        return np.array([stats.norm.rvs(0, 1)], dtype = float)

class Pricing(gym.Env):
    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 4}

    def __init__(self):
        self.capacity_stop = 150
        self.d0 = 540
        self.p0 = 43.904
        self.time_step = 0

        # Set config
        with open('config/dag_specs.yaml', 'r') as file:
            self.dag_specs = yaml.safe_load(file)

        # Variables
        self.action_variables = ["A_1"]
        self.non_action_variables = self._get_non_action_variables() # TODO: get these automatically
        self.state_variables = ["X", "L_1", "A_1", "A_2"]

        # Spaces
        self.observation_space = spaces.Box(-np.inf, np.inf, shape=(4,), dtype=float)
        self.action_space = spaces.Box(-np.inf, np.inf, shape=(1,), dtype=float)

        # Inject functional relationships (TODO: Avoid hard-coding)
        self.kernels = {
            "X": X_Kernel(self._get_dependency_params("X")),
            "L_1": L1_Kernel(self._get_dependency_params("L_1")),
            "L_2": L2_Kernel(self._get_dependency_params("L_2")),
            "A_2": A2_Kernel(self._get_dependency_params("A_2"))
        }
    
    # TODO: We need to specify kernels of a type to do this.
    # def _setup_kernels(self):
    #     self.kernels = {}
    #     for var_name in self.dag_specs.keys():
    #         params = self._get_dependency_params(var_name)
    #         self.kernels[var_name] = 


    def _get_non_action_variables(self):
        return [i for i in self.dag_specs.keys() if i not in self.action_variables]

    def _get_dependency_params(self, var_name):
        if self.dag_specs[var_name]["dependencies"] is None:
            return None

        params = {}
        for lag in self.dag_specs[var_name]["dependencies"]["lag"].keys():
            for var in self.dag_specs[var_name]["dependencies"]["lag"][lag].keys():
                for param, val in self.dag_specs[var_name]["dependencies"]["lag"][lag][var].items():
                    if param not in params.keys():
                        params[param] = np.array([])
                    params[param] = np.append(params[param], val)

        return params

    def _extend_graph(self):
        for var_name in self.topological_order:
            node_name = f"{var_name}_{self.time_step + 1}"
            self._add_variable(var_name, self.time_step + 1)
            self.G.add_edges_from([(parent_node, node_name) for parent_node in self._get_parent_nodes(var_name, self.time_step + 1)])

    def get_parent_values(self, child_node: str):
        var_name = self.G.nodes[child_node]["var_name"]
        if self.dag_specs[var_name]["dependencies"] is None:
            return np.array([])

        # Make dict with vals
        parent_values = {}
        for graph_parent in self.G.predecessors(child_node):
            parent_var_name = self.G.nodes[graph_parent]["var_name"]
            parent_values[parent_var_name] = self.G.nodes[graph_parent]["value"].item()

        return np.array(list(parent_values.values()), dtype = float)

    def _add_variable(self, var_name, time_step):
        node_name = var_name + f"_{time_step}"
        node_offset = self.dag_specs[var_name]["level_offset"]

        self.G.add_node(node_name, level = time_step + node_offset, var_name = var_name, time = time_step)

    def _get_parent_nodes(self, var_name, time_step):
        if self.dag_specs[var_name]["dependencies"] is None:
            return []

        parent_nodes = []
        for lag in self.dag_specs[var_name]["dependencies"]["lag"].keys():
            for parent_var_name in self.dag_specs[var_name]["dependencies"]["lag"][lag].keys():
                t_append = time_step - int(lag)
                parent_name = parent_var_name + f"_{str(t_append)}"
                if parent_name in self.G.nodes:
                    parent_nodes.append(parent_name)

        return parent_nodes

    def _current_observation(self):
        observation = []
        for var_name in self.state_variables:
            if var_name in self.action_variables:
                node_name = f"{var_name}_{self.time_step - 1}"
            else:
                node_name = f"{var_name}_{self.time_step}"
            observation.append(self.G.nodes[node_name]["value"].item())

        return np.array(observation, dtype=float)

    def _get_reward(self):
        return \
            float(self.G.nodes[f"A_2_{self.time_step - 1}"]["value"] * self.G.nodes[f"L_2_{self.time_step}"]["value"] + \
                  self.G.nodes[f"A_1_{self.time_step - 1}"]["value"] * self.G.nodes[f"L_1_{self.time_step}"]["value"])

    def _set_action_values(self, action):
        # - Action Variables
        for var_name, value in zip(self.action_variables, action):
            node_name = f"{var_name}_{self.time_step}"
            self.G.nodes[node_name]['value'] = value

    def _set_non_action_values(self):
        # 2. Set values
        for var_name in self.non_action_variables:
            node_name = f"{var_name}_{self.time_step + 1}"
            parent_values = self.get_parent_values(node_name)
            self.G.nodes[node_name]['value'] = self.kernels[var_name].predict(parent_values)

    def step(self, action):
        """will use TimeLimit wrapper for truncation..."""
        # Set action node value at current time-step
        self._set_action_values(action)

        # Extend Graph (build all next time-step variables)
        self._extend_graph()

        # Set non-action node values at next time-step
        self._set_non_action_values()

        # Move one time-step
        self.time_step += 1

        reward = self._get_reward()
        next_observation = self._current_observation()

        info = self._get_info()

        return next_observation, reward, False, False, info
            
    def _get_info(self):
        return {
            "observation": self._current_observation(),
            "time_step": self.time_step}

    def _init_graph(self):
        # Init values
        for time_step in range(2):
            for var_name in self.non_action_variables + self.action_variables:
                node_name = f"{var_name}_{time_step}"
                self._add_variable(var_name, time_step)
                self.G.nodes[node_name]["value"] = np.array([0], dtype = float)

        # Init edges
        for time_step in range(2):
            for var_name in self.non_action_variables + self.action_variables:
                node_name = f"{var_name}_{time_step}"            
                self.G.add_edges_from([(parent_node, node_name) for parent_node in self._get_parent_nodes(var_name, 0)])

        self.time_step = 1

    def _get_topological_order(self):
        topological_order = [i.split("_")[0] + "_" + i.split("_")[1] for i in list(nx.topological_sort(self.G)) if i.split("_")[-1] == "1"]
        for i, var in enumerate(topological_order):
            if var[0] == "X":
                topological_order[i] = "X"

        return topological_order

    def reset(self, seed=None):
        # We need the following line to seed self.np_random
        super().reset(seed=seed)

        self.G = nx.DiGraph()

        # Set init values
        self._init_graph()

        # Set topological order among variables
        self.topological_order = self._get_topological_order()

        observation = self._current_observation()

        info = self._get_info()

        return observation, info

    def render(self):
        pass

    def _render_frame(self):
        pass

    def close(self):
        pass