# Indice

- [Presents Notebook](./Presents.ipynb) - Notebook de Jupyter con el código fuente y la lógica del proyecto.
- [Documentación del Proyecto](./Documentation%20of%20the%20Gift%20Idea%20Generation%20Project.pdf) - Documento PDF con la descripción detallada del proyecto y su funcionamiento.
- [Código Fuente](./Wizeline_christmas_project.py) - Script en Python del proyecto para la generación de ideas de regalos.
- [Licencia](./LICENSE.txt) - Texto de la licencia MIT que cubre el uso y distribución del software.

# Project Name

Brief description of your project: an automated tool that generates personalized gift ideas using personal interest data extracted from Instagram and the OpenAI API.

## Getting Started

To start using this tool, follow the steps below.

### Prerequisites

To use this project, you need to have the Chrome extension "IG Follower Export Tool" installed. You can download it from here: [IG Follower Export Tool](https://ig-follower-extractor.gmapsscraper.com/)

### Installation

Install the necessary project dependencies using pip:

\`\`\`bash
pip install openai
\`\`\`

## Usage

1. Use the "IG Follower Export Tool" extension to extract follower data from an Instagram account and save it in a CSV file.
2. Run the provided Python script. You will be prompted to enter:
   - The name of the CSV file.
   - The column that contains the followed accounts.
   - Information about the person who will receive the gift (name, gender, age).
3. The program will generate gift recommendations based on this data and will provide Amazon links for each gift, as well as personalized explanations.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Authors

- **Germán Andrés Magallón Corona** - *Wizeline project*
