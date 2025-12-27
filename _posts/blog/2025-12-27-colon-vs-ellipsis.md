---
layout: post
title: Colon Vs Ellipsis
date: 2025-12-27
categories: machine_learning
---

It turns out there aren't any explanations online on the difference between : and ... for Numpy and PyTorch!

Colon (:): Means 'select all elements along this dimension'. For example, `tensor[:, 0]` selects all rows along the first column.

Ellipsis (...): The ellipsis is a shorthand for 'as many colons as needed to specify a full range of dimensions'. It fills in missing dimensions with full slices (:). This is particularly useful for higher-dimensional tensors.

They are equivalent when the ellipsis can be unambiguously replaced by one or more colons to match the tensor's dimensions. For example, for a 2D tensor, `tensor[..., 0]` is equivalent to `tensor[:, 0]` because the ... expands to a single : to fill the first dimension.

However, they are not always equivalent. Consider a 3D tensor `tensor_3d`. `tensor_3d[..., 0]` would mean `tensor_3d[:, :, 0]` (select all rows and columns for the first element of the last dimension). But `tensor_3d[:, 0]` would mean `tensor_3d[:, 0, :]` (select all elements from the first dimension, the first element from the second dimension, and all elements from the third dimension).

Let me show you with an example:
```python
import torch

tensor_3d = torch.randn(2, 3, 4)
print("Original 3D Tensor shape:", tensor_3d.shape)
print("Original 3D Tensor:\n", tensor_3d)

print("\n--- Using Ellipsis (...) ---")
# tensor_3d[..., 0] means tensor_3d[:, :, 0]
result_ellipsis = tensor_3d[..., 0]
print("Result of tensor_3d[..., 0] shape:", result_ellipsis.shape)
print("Result of tensor_3d[..., 0]:\n", result_ellipsis)

print("\n--- Using Colon (:) ---")
# tensor_3d[:, 0] means tensor_3d[:, 0, :]
result_colon = tensor_3d[:, 0]
print("Result of tensor_3d[:, 0] shape:", result_colon.shape)
print("Result of tensor_3d[:, 0]:\n", result_colon)
```
```text
Original 3D Tensor shape: torch.Size([2, 3, 4])
Original 3D Tensor:
 tensor([[[-0.7922, -0.1005, -0.8469,  0.2109],
         [ 0.4234, -0.0942, -0.7224, -0.0768],
         [ 0.4489, -0.0660, -0.4854, -0.3628]],

        [[ 0.0345, -1.1675,  0.4038, -0.0967],
         [ 0.9421, -1.6283,  0.9903, -1.3062],
         [-0.5849,  2.8879,  0.5213, -0.2349]]])

--- Using Ellipsis (...) ---
Result of tensor_3d[..., 0] shape: torch.Size([2, 3])
Result of tensor_3d[..., 0]:
 tensor([[-0.7922,  0.4234,  0.4489],
        [ 0.0345,  0.9421, -0.5849]])

--- Using Colon (:) ---
Result of tensor_3d[:, 0] shape: torch.Size([2, 4])
Result of tensor_3d[:, 0]:
 tensor([[-0.7922, -0.1005, -0.8469,  0.2109],
        [ 0.0345, -1.1675,  0.4038, -0.0967]])
```