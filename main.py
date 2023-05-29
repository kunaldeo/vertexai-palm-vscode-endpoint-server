import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from vertex_generator import GeneratorBase, VertexGenerator
import json

from util import logger, get_parser

app = FastAPI()
app.add_middleware(
    CORSMiddleware
)
generator: GeneratorBase = ...


@app.post("/api/generate/")
async def api(request: Request):
    json_request: dict = await request.json()
    inputs: str = json_request['inputs']
    parameters: dict = json_request['parameters']
    logger.info(f'{request.client.host}:{request.client.port} inputs = {json.dumps(inputs)}')
    generated_text: str = generator.generate(inputs, parameters)
    logger.info(f'{request.client.host}:{request.client.port} generated_text = {json.dumps(generated_text)}')
    return {
        "generated_text": generated_text,
        "status": 200
    }


def main():
    global generator
    args = get_parser().parse_args()
    generator = VertexGenerator(project_id=args.project_id, model_name=args.model_name, location=args.location)
    uvicorn.run(app, host=args.host, port=args.port)


if __name__ == '__main__':
    main()
