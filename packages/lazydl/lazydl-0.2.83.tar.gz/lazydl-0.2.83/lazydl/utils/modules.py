import torch


class FFN(torch.nn.Module):
    """
    Feed Forward Network

    """
    def __init__(self, embed_dim, coef=1, dropout=0.1):
        """
        
        Args:
            embed_dim (_type_): 嵌入维度
            coef (_type_): 缩放系数，默认为 1
            dropout (float, optional): 默认为 0.1.
        """
        super().__init__()
        self.layers = torch.nn.Sequential(
            torch.nn.Linear(embed_dim, int(coef*embed_dim)),
            torch.nn.ReLU(),
            torch.nn.Linear(int(coef*embed_dim), embed_dim),
            torch.nn.Dropout(dropout)
        )
    def forward(self, x):
        return self.layers(x)