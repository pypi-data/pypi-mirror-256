import sqlite3

def ensure_table(file):
    con = sqlite3.connect(file)
    cur = con.cursor()
    cur.execute(
        """CREATE TABLE chat (
            id INTEGER PRIMARY KEY,
            messages TEXT NOT NULL,
            model TEXT NOT NULL,
            frequency_penalty REAL,
            logit_bias TEXT,
            logprobs INTEGER,
            top_logprobs INTEGER,
            max_tokens INTEGER,
            n INTEGER,
            presence_penalty REAL,
            response_format TEXT,
            seed INTEGER,
            stop TEXT,
            stream INTEGER,
            temperature REAL,
            top_p REAL,
            tools TEXT,
            tool_choice TEXT,
            user TEXT,
            function_call TEXT,
            functions TEXT,
            timestamp REAL,
            response TEXT,
            uuid TEXT
        )"""
    )
    cur.execute(
        """CREATE INDEX messages_ix ON chat(messages)"""
    )

if __name__ == "__main__":
    ensure_table('llmem.db')