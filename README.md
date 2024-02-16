# GelaToD: A Very Small ToD Dataset for Gelato

A very small and LLM generated task oriented dialogue dataset for gelato. 🍨

![An image of Gelato](./ice_cream.png)


## Overview

GelaToD offers arguably the first dataset for one of the most important businesses, gelato shops! This dataset contains hypothetical and simplified dialogues between a customer and an assistant in Jack's Gelato, one of the most important shops for Cambridge students! This dataset provides resources for state tracking models and response generation models.

## Project Structure

- `dialogue_data.json`: Dialogue dataset generated with LLM.
- `dst_data.json`, `rg_data.json`: Processed datasets for dialogue state tracking and response generation.
- `dst_models.py`, `rg_models.py`: Example model implementations for DST and RG tasks.
- `gelatoAPI.py`: Simulated API for interacting with a gelato ordering system. It could give you a picture as the one above!
- `generate_data.py`, `process_data.py`: Utilities for data generation with GPT4 and preprocessing for DST and RG.
- `train_dst.py`, `train_rg.py`: Scripts for training DST and RG models.
- `environment.yml`: Conda environment file for setting up a development environment.
- `prompt.txt`: Sample prompts used for LLM dialogue generation.
- `ice_cream.png`: The ice cream you will get from gelatoAPI.

