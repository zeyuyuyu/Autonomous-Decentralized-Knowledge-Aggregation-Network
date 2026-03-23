import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from torchvision import datasets, transforms

class FederatedLearningAggregator(nn.Module):
    def __init__(self, model, clients, learning_rate=0.001):
        super(FederatedLearningAggregator, self).__init__()
        self.model = model
        self.clients = clients
        self.learning_rate = learning_rate
        self.optimizer = optim.Adam(self.model.parameters(), lr=self.learning_rate)

    def train(self, num_rounds):
        for round in range(num_rounds):
            client_models = []
            for client in self.clients:
                client_model = client.train(self.model)
                client_models.append(client_model)

            aggregated_model = self.aggregate_models(client_models)
            self.model.load_state_dict(aggregated_model.state_dict())
            self.optimizer.step()

    def aggregate_models(self, client_models):
        aggregated_model = copy.deepcopy(client_models[0])
        for param in aggregated_model.parameters():
            param.data = torch.zeros_like(param.data)

        for client_model in client_models:
            for param, agg_param in zip(client_model.parameters(), aggregated_model.parameters()):
                agg_param.data += param.data / len(client_models)

        return aggregated_model

class FederatedLearningClient(nn.Module):
    def __init__(self, model, dataset, batch_size, learning_rate=0.001):
        super(FederatedLearningClient, self).__init__()
        self.model = copy.deepcopy(model)
        self.dataset = dataset
        self.batch_size = batch_size
        self.learning_rate = learning_rate
        self.optimizer = optim.Adam(self.model.parameters(), lr=self.learning_rate)

    def train(self, global_model):
        self.model.load_state_dict(global_model.state_dict())
        dataloader = DataLoader(self.dataset, batch_size=self.batch_size, shuffle=True)

        for epoch in range(5):
            for data, target in dataloader:
                self.optimizer.zero_grad()
                output = self.model(data)
                loss = nn.functional.cross_entropy(output, target)
                loss.backward()
                self.optimizer.step()

        return self.model
