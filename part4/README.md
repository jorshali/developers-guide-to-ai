# Part 4 : Fine-tuning

All the code and examples used in **Part 4: Fine-tuning** of the book are available here.


# Folders and Files
- `01-dataset.ipynb`: Notebook for exploring and preparing datasets.
- `02.zeroShot.ipynb`: Baselining zero-shot performance before fine-tuning.
- `03-finetune-classificationModel.ipynb`: Fine-tuning a classification model.
- `04-chat-examples.ipynb`: Exploring chat-formats.
- `05-finetune-dataset.ipynb`: Preparing datasets for fine-tuning.
- `06-finetune-llm.ipynb`: Fine-tuning a large language model.
- `07-test-ft-llm.ipynb`: Testing the fine-tuned LLM.
- `data/`: Contains processed datasets
    - `llm_mail_dataset/`: Mail dataset for fine-tuning LLM.
    - `mail_data/`: Combined mail dataset with 3 files - train.csv, val.csv, test.csv.
    - `mail_dataset/`: Mail dataset unlabeled.
    - `mail_dataset_labeled/`: Labeled mail dataset.
- `rawData/`: Contains raw CSV data files for experiments.
    - `in_bank.csv`: Raw bank-related data (India).
    - `in_school.csv`: Raw school-related data (India).
    - `us_bank.csv`: Raw bank-related data (US).
    - `us_school.csv`: Raw school-related data (US).

# Setting up the environment

To set up the environment, you can use `pyenv` and `pyenv-virtualenv` to create a virtual environment for the project. After setting up the virtual environment, you can install the required packages using `pip`.

Once you have set up the virtual environment and installed the required packages, you can activate the virtual environment and start a Jupyter notebook server. The notebooks can then be accessed through a web browser.

For example, to set up the virtual environment and start the Jupyter notebook server, you can use the following commands:

```bash
pyenv virtualenv 3.12.0 developers-guide-to-ai-part4
pyenv activate developers-guide-to-ai-part4
```

