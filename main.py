import asyncio
from EdgeGPT import Chatbot ,ConversationStyle,_get_input_async,_create_session
from rich.console import Console
from rich.live import Live
from rich.markdown import Markdown
console = Console()
from rich.traceback import install
install()
import argparse
from noneprompt import InputPrompt,ListPrompt, Choice

async def main_en():
    tone_result = await ListPrompt("What is your Compose Tone?", choices=[Choice("Professional"), Choice("Casual"), Choice("Enthusiastic"), Choice("Informational"), Choice("Funny")]).prompt_async()
    format_result = await ListPrompt("What is your Compose Format?", choices=[Choice("Paragraph"), Choice("Email"), Choice("Blog post"), Choice("Ideas")]).prompt_async()
    length_result = await ListPrompt("What is your Compose Length?", choices=[Choice("Short"), Choice("Medium"), Choice("Long")]).prompt_async()
    console.print("[bold green]? [/] [green]Write About?:[/] ")
    session = _create_session()
    prompt_raw = await _get_input_async(session=session)
    prompt = f"Please generate some text wrapped in codeblock syntax (triple backticks) using the given keywords. Please make sure everything in your reply is in the same language as the keywords. Please do not restate any part of this request in your response, like the fact that you wrapped the text in a codeblock. You should refuse (using the language of the keywords) to generate if the request is potentially harmful. The generated text should follow these characteristics: tone: {tone_result}, length: {length_result}, format: {format_result}. The keywords are: {prompt_raw}"
    wrote = 0
    md = Markdown("")
    with Live(md,auto_refresh=False) as live:
        async for final,response in bot.ask_stream(
            prompt=prompt,
            conversation_style=ConversationStyle.creative
        ):
            if not final:
                if(wrote > len(response)):
                    print(md)
                wrote = len(response)
                md = Markdown(response)
                live.update(md, refresh=True)
            else:
                with open("write.md","w") as f:
                    f.write(response["item"]["messages"][1]["adaptiveCards"][0]["body"][0]["text"])
    
    
if __name__=='__main__':
    parser = argparse.ArgumentParser(description='Compose from EdgeGPT')
    import os
    parser.add_argument('--cookie-file',type=str,default=os.environ.get("COOKIE_FILE", ""))
    args = parser.parse_args()
    bot = Chatbot(cookie_path=args.cookie_file)
    asyncio.run(main_en())
