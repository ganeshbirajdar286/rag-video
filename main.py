from dotenv import load_dotenv
from utils.audio_processor import process_input
from core.transcription import transcribe_all
from core.summary import summarize, generate_title
from core.extractor import extract_action_items, extract_key_decisions, extract_questions
from core.rag_engine import build_rag_chain, ask_question

from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.rule import Rule
from rich.prompt import Prompt
from rich.live import Live
from rich.spinner import Spinner
from rich.table import Table
from rich.columns import Columns
from rich import box
import time

load_dotenv()

console = Console()


def print_banner():
    banner = Text()
    banner.append("  ██╗   ██╗██╗██████╗ ███████╗ ██████╗      ██████╗  █████╗  ██████╗ \n", style="bold cyan")
    banner.append("  ██║   ██║██║██╔══██╗██╔════╝██╔═══██╗     ██╔══██╗██╔══██╗██╔════╝ \n", style="bold cyan")
    banner.append("  ██║   ██║██║██║  ██║█████╗  ██║   ██║     ██████╔╝███████║██║  ███╗\n", style="bold blue")
    banner.append("  ╚██╗ ██╔╝██║██║  ██║██╔══╝  ██║   ██║     ██╔══██╗██╔══██║██║   ██║\n", style="bold blue")
    banner.append("   ╚████╔╝ ██║██████╔╝███████╗╚██████╔╝     ██║  ██║██║  ██║╚██████╔╝\n", style="bold magenta")
    banner.append("    ╚═══╝  ╚═╝╚═════╝ ╚══════╝ ╚═════╝      ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ \n", style="bold magenta")
    banner.append("\n           🎬  AI-Powered Video Intelligence Assistant  🤖\n", style="bold white")

    console.print(Panel(banner, border_style="cyan", padding=(0, 2)))
    console.print()


def step(label: str, emoji: str = "⚙️"):
    """Show a loading spinner while running a task."""
    return Live(
        Spinner("dots", text=f"  {emoji}  [bold cyan]{label}[/bold cyan]"),
        console=console,
        refresh_per_second=12,
        transient=True,
    )


def print_results(result: dict):
    console.print()
    console.print(Rule("[bold cyan]✦  Analysis Results  ✦[/bold cyan]", style="cyan"))
    console.print()

    # Title
    console.print(Panel(
        f"[bold white]{result['title']}[/bold white]",
        title="[bold cyan]📌 Title[/bold cyan]",
        border_style="cyan",
        padding=(0, 2),
    ))
    console.print()

    # Summary
    console.print(Panel(
        f"[white]{result['summary']}[/white]",
        title="[bold blue]📋 Summary[/bold blue]",
        border_style="blue",
        padding=(1, 2),
    ))
    console.print()

    # Three-column cards: Action Items | Key Decisions | Open Questions
    def make_card(title: str, icon: str, content: str, color: str) -> Panel:
        return Panel(
            f"[white]{content.strip()}[/white]",
            title=f"[bold {color}]{icon} {title}[/bold {color}]",
            border_style=color,
            padding=(1, 1),
            expand=True,
        )

    cards = Columns([
        make_card("Action Items",   "✅", result["action_items"],  "green"),
        make_card("Key Decisions",  "🔑", result["key_decisions"], "yellow"),
        make_card("Open Questions", "❓", result["open_questions"],"magenta"),
    ], equal=True, expand=True)

    console.print(cards)
    console.print()
    console.print(Rule(style="cyan"))


def run_pipeline(source: str, language: str = "english") -> dict:
    with step("Processing input source", "📥"):
        chunks = process_input(source)

    with step(f"Transcribing audio ({len(chunks)} chunk(s))", "🎙️"):
        transcript = transcribe_all(chunks, language)

    console.print(f"  [dim]Transcript preview:[/dim] [italic white]{transcript[:120].strip()}…[/italic white]\n")

    with step("Generating title", "✍️"):
        title = generate_title(transcript)

    with step("Summarising", "📋"):
        summary = summarize(transcript)

    with step("Extracting action items", "✅"):
        action_item = extract_action_items(transcript)

    with step("Extracting key decisions", "🔑"):
        decisions = extract_key_decisions(transcript)

    with step("Extracting open questions", "❓"):
        questions = extract_questions(transcript)

    with step("Building RAG vector store", "🧠"):
        rag_chain = build_rag_chain(transcript)

    return {
        "title": title,
        "transcript": transcript,
        "summary": summary,
        "action_items": action_item,
        "key_decisions": decisions,
        "open_questions": questions,
        "rag_chain": rag_chain,
    }


def chat_loop(rag_chain):
    console.print()
    console.print(Panel(
        "[bold white]Ask anything about the video.[/bold white]\n"
        "[dim]Type [bold]exit[/bold] / [bold]quit[/bold] / [bold]q[/bold] to end the session.[/dim]",
        title="[bold magenta]💬 Chat Mode[/bold magenta]",
        border_style="magenta",
        padding=(0, 2),
    ))
    console.print()

    while True:
        try:
            question = Prompt.ask("[bold cyan]You[/bold cyan]").strip()
        except (KeyboardInterrupt, EOFError):
            break

        if not question:
            continue
        if question.lower() in ["exit", "quit", "q"]:
            console.print("\n[bold cyan]👋  Goodbye![/bold cyan]\n")
            break

        with step("Thinking…", "🤖"):
            answer = ask_question(rag_chain, question)

        console.print(Panel(
            f"[white]{answer}[/white]",
            title="[bold magenta]🤖 Assistant[/bold magenta]",
            border_style="magenta",
            padding=(0, 2),
        ))
        console.print()


if __name__ == "__main__":
    print_banner()

    source   = Prompt.ask("[bold cyan]Enter YouTube URL or local file path[/bold cyan]").strip()
    language = Prompt.ask("[bold cyan]Language[/bold cyan]", default="english").strip()

    console.print()
    result = run_pipeline(source, language)
    print_results(result)
    chat_loop(result["rag_chain"])