from src.AI.client import AIClient

def main():
    ai = AIClient()

    response = ai.ask(
        "Dime tres consejos para una entrevista de Unreal Engine"
    )

    print(response.message.content)
    print(response.generation.model)


if __name__ == "__main__":
    main()