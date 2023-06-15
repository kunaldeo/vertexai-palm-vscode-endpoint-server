# Vertex AI Palm VSCode Endpoint Server

Vertex AI Palm VSCode server for [huggingface-vscdoe](https://github.com/huggingface/huggingface-vscode) custom endpoint.

## Usage

```shell
pip install -r requirements.txt
python main.py --project_id <gcp project name>
```

Fill `http://localhost:8000/api/generate/` into `Hugging Face Code > Model ID or Endpoint` in VSCode.

If you are using Palm api you may want to change the following settings as well:
```
"HuggingFaceCode.endToken": "",
"HuggingFaceCode.middleToken": "",
"HuggingFaceCode.stopToken": "",
"HuggingFaceCode.startToken": "",
```

## API

```shell
curl -X POST http://localhost:8000/api/generate/ -d '{"inputs": "", "parameters": {"maxOutputTokens": 64}}'
# response = {"generated_text": ""}
```
