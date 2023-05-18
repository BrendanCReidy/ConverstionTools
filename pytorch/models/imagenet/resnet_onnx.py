import torch
import os
import torchvision.datasets as datasets
from torch.utils.data import DataLoader, TensorDataset
import torchvision.transforms as transforms
from torchvision.models import resnet18, ResNet18_Weights
import torch.onnx
os.environ["CUDA_VISIBLE_DEVICES"]="1"

model = resnet18(weights=ResNet18_Weights.IMAGENET1K_V1)
model.eval()

# move the input and model to GPU for speed if available
if torch.cuda.is_available():
    model.to('cuda')

x = torch.randn(1, 3, 224, 224, requires_grad=True).to('cuda')
torch_out = model(x)

# Export the model
torch.onnx.export(model,               # model being run
                  x,                         # model input (or a tuple for multiple inputs)
                  "resnet18.onnx",   # where to save the model (can be a file or file-like object)
                  export_params=True,
                  opset_version=10,
                  do_constant_folding=True,
                  input_names = ['input'],
                  output_names = ['output'],
                  dynamic_axes={'input' : {0 : 'batch_size'},
                                'output' : {0 : 'batch_size'}})