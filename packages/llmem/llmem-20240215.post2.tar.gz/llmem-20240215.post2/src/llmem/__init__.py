import contextlib

from starlette.applications import Starlette
from starlette.responses import Response, HTMLResponse
from starlette.routing import Route
from starlette.config import Config
import json
import aiohttp

import logging
import aiosqlite
import uuid
import time
import markdown

from pathlib import Path

from llmem.maketable import ensure_table

# If we're installed, README will be next to us,
# if we're editable, two folders up
try:
    try:
        readme_file = (Path(__file__).parent / 'README.md').resolve()
        with readme_file.open() as f:
            readme_text = f.read()
    except FileNotFoundError:
        readme_file = (Path(__file__).parent / '../../docs/README.md').resolve()
        with readme_file.open() as f:
            readme_text = f.read()
    html = markdown.markdown(readme_text, extensions=['toc', 'pymdownx.tilde', 'markdown.extensions.fenced_code', 'markdown.extensions.codehilite', 'markdown.extensions.footnotes'])
except FileNotFoundError:
    html = "Can't find README.md, oh well"
html = f"<html><head><title>LLMem</title></head><body>{html}</body></html>"

database = None
config = Config()

seconds_per_unit = {"s": 1, "m": 60, "h": 3600, "d": 86400, "w": 604800, "y": 32850000}

def convert_to_seconds(s):
    return int(s[:-1]) * seconds_per_unit[s[-1]]

QUERY = """SELECT response FROM chat WHERE 
                                        messages = :messages AND
                                        -- Special fields
                                        (:max_tokens IS NULL OR max_tokens = :max_tokens) AND 
                                        (:age IS NULL OR (:now - timestamp) <= :age) AND
                                        -- General fields -- null OR equal
                                        (:frequency_penalty IS NULL OR frequency_penalty = :frequency_penalty) AND
                                        (:logit_bias IS NULL OR logit_bias = :logit_bias) AND
                                        (:logprobs IS NULL OR logprobs = :logprobs) AND
                                        (:top_logprobs IS NULL OR top_logprobs = :top_logprobs) AND
                                        (:n IS NULL OR n = :n) AND
                                        (:presence_penalty IS NULL OR presence_penalty = :presence_penalty) AND
                                        (:response_format IS NULL OR response_format = :response_format) AND
                                        (:seed IS NULL OR seed = :seed) AND
                                        (:stop IS NULL OR stop = :stop) AND
                                        (:stream IS NULL OR stream = :stream) AND
                                        (:temperature IS NULL OR temperature = :temperature) AND
                                        (:top_p IS NULL OR top_p = :top_p) AND
                                        (:tools IS NULL OR tools = :tools) AND
                                        (:tool_choice IS NULL OR tool_choice = :tool_choice) AND
                                        (:user IS NULL OR user = :user) AND
                                        (:function_call IS NULL OR function_call = :function_call) AND
                                        (:functions IS NULL OR functions = :functions)
                                    ORDER BY timestamp DESC LIMIT 1"""

@contextlib.asynccontextmanager
async def lifespan(app):
    global database
    db_file = Path(config('LLMEM_DB_FILE', default='llmem.db'))
    if not db_file.exists():
        ensure_table(db_file)
    database = await aiosqlite.connect(db_file)
    yield
    await database.commit()
    await database.close()


def normalize_messages(d):
    return json.dumps(d, sort_keys=True)


async def hit_oai(headers, body):
    body.pop('age', None)
    headers = {
        "Content-Type": "application/json",
        "Authorization": headers['Authorization']
    }
    async with aiohttp.ClientSession() as session:
        async with session.post('https://api.openai.com/v1/chat/completions', headers=headers, json=body) as response:
            return await response.json()

async def chat(request):
    body = await request.json()
    normalized_messages =  normalize_messages(body['messages'])
    now = time.time()
    age = None
    if string_age := body.pop('age', "8w"):
        age = convert_to_seconds(string_age)
    cursor = await database.execute(QUERY,
                                    {
                                        "messages": normalized_messages,
                                        "model": body.get("model"),
                                        "frequency_penalty": body.get("frequency_penalty"),
                                        "logit_bias": body.get("logit_bias"),
                                        "logprobs": body.get("logprobs"),
                                        "top_logprobs": body.get("top_logprobs"),
                                        "max_tokens": body.get("max_tokens"),
                                        "n": body.get("n"),
                                        "presence_penalty": body.get("presence_penalty"),
                                        "response_format": body.get("response_format"),
                                        "seed": body.get("seed"),
                                        "stop": body.get("stop"),
                                        "stream": body.get("stream"),
                                        "temperature": body.get("temperature"),
                                        "top_p": body.get("top_p"),
                                        "tools": body.get("tools"),
                                        "tool_choice": body.get("tool_choice"),
                                        "user": body.get("user"),
                                        "function_call": body.get("function_call"),
                                        "functions": body.get("functions"),
                                        "now": now,
                                        "age": age,
                                    })
    row = await cursor.fetchone()
    await cursor.close()
    if row:
        return Response(content=row[0], media_type='text/json')
    
    result = await hit_oai(request.headers, body)
    await insert(body, normalized_messages, result)
    return Response(content=json.dumps(result), media_type='text/json')

async def insert(body, normalized_messages, response):
    this_uuid = str(uuid.uuid4())
    response = {k:v for k, v in response.items()}
    response['id'] = f'llmem-{this_uuid}'
    await database.execute("""INSERT INTO chat (messages, timestamp, model, frequency_penalty, logit_bias, logprobs, top_logprobs, max_tokens, n, presence_penalty, response_format, seed, stop, stream, temperature, top_p, tools, tool_choice, user, function_call, functions, response, uuid)
                              VALUES(:messages, :timestamp, :model, :frequency_penalty, :logit_bias, :logprobs, :top_logprobs, :max_tokens, :n, :presence_penalty, :response_format, :seed, :stop, :stream, :temperature, :top_p, :tools, :tool_choice, :user, :function_call, :functions, :response, :uuid)""",
                           {
                               'messages': normalized_messages,
                               'timestamp': response['created'],
                                "model": body.get("model"),
                                "frequency_penalty": body.get("frequency_penalty"),
                                "logit_bias": body.get("logit_bias"),
                                "logprobs": body.get("logprobs"),
                                "top_logprobs": body.get("top_logprobs"),
                                "max_tokens": body.get("max_tokens"),
                                "n": body.get("n"),
                                "presence_penalty": body.get("presence_penalty"),
                                "response_format": body.get("response_format"),
                                "seed": body.get("seed"),
                                "stop": body.get("stop"),
                                "stream": body.get("stream"),
                                "temperature": body.get("temperature"),
                                "top_p": body.get("top_p"),
                                "tools": body.get("tools"),
                                "tool_choice": body.get("tool_choice"),
                                "user": body.get("user"),
                                "function_call": body.get("function_call"),
                                "functions": body.get("functions"),
                                'response': json.dumps(response),
                                'uuid': this_uuid
                           }
    )
    await database.commit()

async def website(_):
    return HTMLResponse(html)

app = Starlette(debug=True, routes=[
    Route('/', website),
    Route('/chat', chat, methods=["POST"]),
    Route('/chat/completions', chat, methods=["POST"]),
], lifespan=lifespan)