import flet as ft
import datetime
import random

knowledge_base = {
    "velocity": "v = u + at (Final velocity equation)",
    "displacement": "s = ut + 1/2 at^2 (Displacement equation)",
    "force": "F = ma (Newton's Second Law)",
    "density": "Density (d) = Mass / Volume",
    "work": "Work Done (W) = F * d * cos(theta)",
    "power": "Power (P) = Work / Time",
    "mole": "Moles (n) = Mass / Molar Mass",
    "ideal gas": "PV = nRT (Ideal Gas Law)",
    "ph formula": "pH = -log10[H+]",
    "avogadro": "Avogadro constant = 6.022 x 10^23 mol^-1",
    "quadratic": "Roots of ax^2 + bx + c = 0: x = (-b ± √(b^2 - 4ac)) / (2a)",
    "g": "Acceleration due to Gravity = 9.81 m/s^2"
}

quotes = [
    "Believe in yourself! You are capable of amazing things.",
    "Success is the sum of small efforts repeated day in and day out.",
    "Push yourself, because no one else is going to do it for you.",
    "Hard work beats talent when talent doesn't work hard."
]

def main(page: ft.Page):
    page.title = "PyBot - Study & AI Assistant"
    page.padding = 15

    chat_history = ft.ListView(
        expand=True,
        spacing=10,
        auto_scroll=True
    )

    def add_message(text, is_user=False):
        bubble = ft.Container(
            content=ft.Text(text, size=14, color="white"),
            bgcolor="#1565C0" if is_user else "#37474F",
            padding=12,
            border_radius=10
        )
        row = ft.Row(
            controls=[bubble],
            alignment=ft.MainAxisAlignment.END if is_user else ft.MainAxisAlignment.START
        )
        chat_history.controls.append(row)
        page.update()

    def process_bot_response(user_input):
        clean_input = user_input.lower().strip()
        if not clean_input:
            return ""

        if clean_input in ["hello", "hi", "hey"]:
            return "Hi there! How can I help with your studies today?"
        elif "time" in clean_input:
            return f"Current time is {datetime.datetime.now().strftime('%I:%M %p')}"
        elif "quote" in clean_input:
            return random.choice(quotes)
        
        # Math calculation
        expr = clean_input.replace("math:", "").replace("^", "**").strip()
        allowed_chars = set("0123456789+-*/%. ()")
        if expr and set(expr).issubset(allowed_chars) and any(c.isdigit() for c in expr):
            try:
                result = eval(expr, {"__builtins__": None}, {})
                return f"🧮 Math Result: {expr} = {result}"
            except Exception:
                pass

        for key in knowledge_base:
            if key in clean_input:
                return f"{key.upper()}: {knowledge_base[key]}"

        return "I don't know that yet. Try typing a math problem like 25*4 or 'force'."

    def send_click(e):
        if not input_field.value or not input_field.value.strip():
            return
        user_text = input_field.value
        add_message(user_text, is_user=True)
        input_field.value = ""
        page.update()
        response = process_bot_response(user_text)
        add_message(response, is_user=False)

    add_message("Hello! I am PyBot 👋\nYour personal study & AI assistant.")

    input_field = ft.TextField(
        hint_text="Ask something (e.g. 2+2, force, quote)...",
        expand=True,
        on_submit=send_click
    )
    send_button = ft.ElevatedButton(
        content=ft.Text("Send"),
        on_click=send_click
    )

    input_row = ft.Row(controls=[input_field, send_button])
    header = ft.Container(content=ft.Text("🤖 PyBot Companion", size=22, weight="bold"), padding=10)

    page.add(header, ft.Divider(), chat_history, input_row)

if __name__ == "__main__":
    ft.app(target=main)