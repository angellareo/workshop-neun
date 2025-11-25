# Workshop: Introduction to Computational Neuroscience with Neun

## About This Workshop

Materials for the **Neun** library workshop presented at Universidad Politécnica Salesiana (Quito/Cuenca, Ecuador, 2025).

This workshop provides a comprehensive introduction to computational neuroscience modeling and practical experience with the [Neun library](https://github.com/GNB-UAM/Neun/), a powerful C++ framework for simulating neuronal networks.

* **Facilitators**: [Angel Lareo](github.com/angellareo) and [Alicia Garrido-Peña]().

## Workshop Structure
* Part 1: Introduction to Computational Neuroscience
* Part 2: Hands-on with Neun to simulate neural dynamics
* Part 3: Analyzing neural dynamics from Neun's simulations

## Prerequisites

- Basic knowledge of programming
- Computer with Python 3.8+ installed
- Understanding of basic neuroscience concepts (recommended but not required)

## Getting Started

### Building this 

1. Clone this repository:
```bash
git clone https://github.com/angellareo/workshop-neun.git
cd workshop-neun
```

2. Create a virtual environment (recommended):
```bash
python -m venv quarto-neun-workshop
source quarto-neun-workshop/bin/activate  # On Windows: quarto-neun-workshop\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

### Viewing the Workshop Materials

This workshop is built using Quarto. 

To install Quarto CLI:
```bash
# Debian/Ubuntu
wget https://quarto.org/download/latest/quarto-linux-amd64.deb && sudo dpkg -i quarto-linux-amd64.deb
# Conda
conda install -c conda-forge quarto
```

To render and view the materials:
```bash
quarto preview
```

Or render to HTML:

```bash
quarto render
```

The rendered website will be available in the `_site/` directory.

## Additional Resources

- [Neun GitHub Repository](https://github.com/GNB-UAM/Neun/)
- [Neun Documentation](XXX)
- Reference paper: XXX

## License

This workshop material is provided under a [CC BY-NC-SA License](https://creativecommons.org/licenses/by-nc-sa/4.0/). That means you can share and adapt the material non-commercially, as long as you credit the creator and license your changes under the same terms.

## Contact

For questions or feedback, please [contact the facilitators](mailto:angel.lareo@uam.es,alicia.garrido@uam.es?subject=[UPS2025%20Neun%20Workshop]) or open an issue in this repository.
