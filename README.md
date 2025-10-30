# Workshop: Introduction to Computational Neuroscience with Neun

## About This Workshop

Welcome to the computational neuroscience workshop focused on the **Neun** library, presented at Universidad Politécnica Salesiana (Quito/Cuenca, Ecuador, 2025).

This workshop provides a comprehensive introduction to computational neuroscience modeling and practical experience with the [Neun library](https://github.com/GNB-UAM/Neun/), a powerful Python framework for simulating neuronal networks.

## Facilitators

### Dr. Angel Lareo
Expert in computational neuroscience and neural network modeling. Co-author of foundational research in neural dynamics and network behavior.

### Dr. Alicia Garrido-Peña
Researcher specializing in computational modeling of neural systems and mathematical biology. Her work focuses on the dynamics of neuronal populations and network interactions.

Both facilitators have contributed to significant research in the field, including the paper "Frequency-dependent response of the neocortex and the olfactory bulb measured by line source analysis in rats" (DOI: [10.1007/s10492-014-0069-z](https://doi.org/10.1007/s10492-014-0069-z)), which demonstrates the application of computational approaches to understanding neural circuit dynamics.

## Workshop Structure

### Part 1: Introduction to Computational Neuroscience
- Foundations of neural modeling
- Why computational models matter in neuroscience
- Mathematical foundations based on research findings
- From single neurons to network dynamics

### Part 2: Hands-on with Neun
- Getting started with the Neun library
- Building single neuron models
- Creating neural networks
- Simulating and analyzing neural dynamics
- Real-world applications and examples

## Prerequisites

- Basic knowledge of Python programming
- Understanding of basic neuroscience concepts (recommended but not required)
- Laptop with Python 3.8+ installed

## Getting Started

### Installation

1. Clone this repository:
```bash
git clone https://github.com/angellareo/workshop-neun.git
cd workshop-neun
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

### Viewing the Workshop Materials

This workshop is built using Quarto. To render and view the materials:

```bash
quarto preview
```

Or render to HTML:

```bash
quarto render
```

The rendered website will be available in the `_site/` directory.

## Workshop Content

- `index.qmd` - Workshop homepage and overview
- `01-intro-compneuro.qmd` - Introduction to computational neuroscience
- `02-neun-basics.qmd` - Getting started with Neun
- `03-single-neurons.qmd` - Single neuron modeling
- `04-neural-networks.qmd` - Building neural networks
- `05-advanced-topics.qmd` - Advanced modeling techniques

## Additional Resources

- [Neun GitHub Repository](https://github.com/GNB-UAM/Neun/)
- [Neun Documentation](https://github.com/GNB-UAM/Neun/)
- Reference paper: Garrido-Peña, A., Martín, E. D., Lareo, A., Herreras, O., & Reboreda, A. (2014). Frequency-dependent response of the neocortex and the olfactory bulb measured by line source analysis in rats. *Applications of Mathematics*, 59(6), 651-663. DOI: 10.1007/s10492-014-0069-z

## License

This workshop material is provided for educational purposes.

## Contact

For questions or feedback, please contact the facilitators or open an issue in this repository.
