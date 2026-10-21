import platform
import torch

def get_environment():
    return {
        "python": platform.python_version(),
        "pytorch": torch.__version__,
        "cuda_available": torch.cuda.is_available(),
        "gpu": (
            torch.cuda.get_device_name(0)
            if torch.cuda.is_available()
            else None
        ),
    }

if __name__ == "__main__":
    for key, value in get_environment().items():
        print(f"{key}: {value}")
