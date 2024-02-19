# llmem

A read through cache for OpenAI chat completions.

Why:

* Avoid running up bills when developing/testing by sending the same request multiple times/forgetting to mock things.
* ~~Fine-tune an open source model on data I've paid for~~ Adhere to all terms of use.
* Evaluate future models.
* Track model changes over time.

## use

It currently only supports the chat completion API. 

There is one additional (optional) field in the request, `age`. You can give it a number + characters like `10w` it will only return from cache if the entry is younger than that (in this case 10 weeks). Acceptable characters are s(econds), m(inute), h(hours), d(ays), w(eeks), y(ears).

### requests

**NOTE**: These examples run against my public server `llmem.com`. You [might want to run your own server instead](#public-server).

```python
import requests

headers = {
  "Content-Type": "application/json",
  "Authorization": f"Bearer {api_key}"
}

payload = {
  "model": "gpt-3.5-turbo",
  "messages": [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "Hi."
        },
      ]
    }
  ],
  "max_tokens": 10
}

response = requests.post("https://llmem.com/chat/completions", headers=headers, json=payload)

print(response.json())
```

If you run that twice, you'll see that first it gives an ID starting with `chatcmpl`, then IDs starting with `llmem`.

You can also use the OpenAI client, although it will currently only work for `/chat` requests:

```python
from openai import OpenAI

client = OpenAI(
    api_key=api_key,
    base_url="https://llmem.com"
)

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "Say this is a test",
        }
    ],
    model="gpt-3.5-turbo",
)
```

## private server

### docker

Makes it available on port `8000`, and keeps its cache in `~/.llmem`.

```bash
docker run --rm -p 8000:8000  -v ~/.llmem:/workspace ghcr.io/c0g/llmem:latest
```

### python

```bash
pip install llmem
uvicorn llmem:app
```

By default it will make a `llmem.db` file in the working directory, you can override this location by setting the `LLMEM_DB_FILE` environment variable.

You can get the code [on GitHub](https://github.com/c0g/llmem).

## public server

I host a public server at [llmem.com](https://llmem.com). If you point your API client to `https://llmem.com/chat`, you'll hit my cache and share the wealth (and get to share other people's wealth).

* **NOTE**: I could look at your OpenAI key if I wanted to. I don't, but I could. You can probably trust me[^criminal].
* **NOTE**: I can look at your queries. I probably will (see 'Why' bullets above). Please don't submit anything you wouldn't want your mother seeing, since I might well be your mother.
* **NOTE**: If any of the above **NOTE**s worry you it's probably best not to point your API client to `https://llmem.com`.

[^criminal]: That's exactly what a criminal would say.
