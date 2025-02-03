# Persian Alphabet Recognition with MLP

## Overview
This project implements a **Multilayer Perceptron (MLP)** using **PyTorch** to classify Persian alphabet letters. The model is trained on a dataset of Persian letters and demonstrates fundamental neural network concepts, including dataset preparation, model definition, and training.

## Features
- Utilizes **PyTorch** for deep learning.
- Implements a **custom dataset** for Persian alphabets.
- Includes **training and evaluation loops**.
- Uses **data visualization tools** such as confusion matrices and feature visualization.

## Installation
To run this project, install the required dependencies:

```bash
pip install torch torchvision scikit-learn matplotlib
```

## Usage
Clone the repository and run the Jupyter Notebook:

```bash
git clone https://github.com/mjasnaashari/Persian-Alphabet-MLP
cd Persian-Alphabet-MLP
jupyter notebook MLP.ipynb
```

## Project Structure
- `MLP.ipynb`: The main Jupyter Notebook containing model implementation and training steps.
- `dataset/`: Directory containing Persian alphabet images (if applicable).
- `models/`: Folder to save trained models.

## Model Architecture
The implemented MLP consists of:
- Input layer matching the flattened image size.
- Multiple hidden layers with **ReLU activation**.
- Softmax output layer for classification.

## Training Process
1. **Data Loading**: Uses `torch.utils.data.Dataset`.
2. **Model Definition**: A fully connected neural network using `torch.nn`.
3. **Training Loop**: Includes loss computation, backpropagation, and optimization.
4. **Evaluation**: Uses accuracy and confusion matrices for performance analysis.

## Results
The trained model achieves **87% accuracy**. The confusion matrix visualizes misclassifications.

## Future Improvements
- Enhance dataset size and quality.
- Experiment with different optimizers and architectures.
- Extend to real-world applications, such as **OCR systems**.

