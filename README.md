# Comics Generator

This program use Generative AI to create an entire comic strip from a short scenario.

The scenario must mention the characters with a physical description.

## How it works

First, a LLM (OpenAI API) is used to split the scenario into 6 panels with their description and associated text.

Then for each panel:
 - an image is generated with Stable Diffusion (Stability API).
 - the panel text is added to the image

The 6 generated images with their texts are then merged into a final strip !

## Usage

Export `OPENAI_API_KEY` and `STABILITY_KEY`.

Install dependencies:
pip install -r requirements.txt

## Run
Run the script: `streamlit run main.py`
