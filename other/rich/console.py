from rich.console import Console
console = Console()

print(f"console.size = {console.size}")
print(f"console.encoding = {console.encoding}")
print(f"console.is_terminal = {console.is_terminal}")
print(f"console.color_system = {console.color_system}")

console.print([1, 2, 3])
console.print("[blue underline]Looks like a link")
console.print(locals())
console.print("Lorem ipsum dolor sit amet", style="white on blue")
console.print("[white underline on blue]Lorem ipsum dolor sit amet")
console.log("Hello, World!")
console.rule("Linia")
console.rule("[red]Separator")
console.rule("[bold red]Separator")
console.rule("[yellow on blue]Separator")