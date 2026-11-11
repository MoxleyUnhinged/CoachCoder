"""Short, side-by-side lessons for the Code Coach desktop app."""

from dataclasses import dataclass


LANGUAGES = {
    "python": "Python",
    "cpp": "C++",
    "csharp": "C#",
}


@dataclass(frozen=True)
class Lesson:
    id: str
    title: str
    explanation: str
    example: str
    challenge: str


_TOPICS = [
    {
        "id": "first-output",
        "title": "Your first output",
        "explanation": "Programs can show messages to a person. Try changing the example message to say something about yourself.",
        "examples": {
            "python": 'print("Hello, world!")',
            "cpp": '#include <iostream>\n\nint main() {\n    std::cout << "Hello, world!\\n";\n    return 0;\n}',
            "csharp": 'using System;\n\nclass Program\n{\n    static void Main()\n    {\n        Console.WriteLine("Hello, world!");\n    }\n}',
        },
        "challenges": {
            "python": "Write a program that prints your name and one thing you want to build.",
            "cpp": "Change the message, then add a second std::cout line that prints one thing you want to build.",
            "csharp": "Change the message, then add a second Console.WriteLine that prints one thing you want to build.",
        },
    },
    {
        "id": "variables",
        "title": "Store information in variables",
        "explanation": "A variable gives a name to information you want to use later. Text is a string; whole numbers are integers. C++ and C# declare a variable's type explicitly.",
        "examples": {
            "python": 'name = "Alex"\nlessons_finished = 1\nprint(name, lessons_finished)',
            "cpp": '#include <iostream>\n#include <string>\n\nint main() {\n    std::string name = "Alex";\n    int lessons_finished = 1;\n    std::cout << name << " " << lessons_finished << "\\n";\n    return 0;\n}',
            "csharp": 'using System;\n\nclass Program\n{\n    static void Main()\n    {\n        string name = "Alex";\n        int lessonsFinished = 1;\n        Console.WriteLine($"{name} {lessonsFinished}");\n    }\n}',
        },
        "challenges": {
            "python": "Create a variable for your favourite subject and another for how many minutes you want to practise. Print both.",
            "cpp": "Create a std::string for your favourite subject and an int for practice minutes. Print both.",
            "csharp": "Create a string for your favourite subject and an int for practice minutes. Print both.",
        },
    },
    {
        "id": "decisions",
        "title": "Make decisions with if",
        "explanation": "An if statement runs code only when a condition is true. An else branch handles the other case. Indentation matters in Python; braces mark blocks in C++ and C#.",
        "examples": {
            "python": 'score = 7\nif score >= 5:\n    print("Nice work!")\nelse:\n    print("Keep practising!")',
            "cpp": '#include <iostream>\n\nint main() {\n    int score = 7;\n    if (score >= 5) {\n        std::cout << "Nice work!\\n";\n    } else {\n        std::cout << "Keep practising!\\n";\n    }\n    return 0;\n}',
            "csharp": 'using System;\n\nclass Program\n{\n    static void Main()\n    {\n        int score = 7;\n        if (score >= 5)\n        {\n            Console.WriteLine("Nice work!");\n        }\n        else\n        {\n            Console.WriteLine("Keep practising!");\n        }\n    }\n}',
        },
        "challenges": {
            "python": "Use an if/else to print a different message depending on whether your practice minutes are at least 15.",
            "cpp": "Use an if/else to print a different message depending on whether your practice minutes are at least 15.",
            "csharp": "Use an if/else to print a different message depending on whether your practice minutes are at least 15.",
        },
    },
    {
        "id": "loops",
        "title": "Repeat work with loops",
        "explanation": "Loops repeat a block of code. A for loop is useful when you know how many times to repeat something. These examples count from 1 to 5.",
        "examples": {
            "python": 'for number in range(1, 6):\n    print(number)',
            "cpp": '#include <iostream>\n\nint main() {\n    for (int number = 1; number <= 5; ++number) {\n        std::cout << number << "\\n";\n    }\n    return 0;\n}',
            "csharp": 'using System;\n\nclass Program\n{\n    static void Main()\n    {\n        for (int number = 1; number <= 5; number++)\n        {\n            Console.WriteLine(number);\n        }\n    }\n}',
        },
        "challenges": {
            "python": "Write a loop that prints the numbers from 1 to 10.",
            "cpp": "Change the loop so it prints the numbers from 1 to 10.",
            "csharp": "Change the loop so it prints the numbers from 1 to 10.",
        },
    },
    {
        "id": "functions",
        "title": "Organise code with functions",
        "explanation": "A function is a named, reusable piece of work. Parameters let you pass information in, and return sends a result back.",
        "examples": {
            "python": "def greet(name):\n    return f\"Hello, {name}!\"\n\nprint(greet(\"Alex\"))",
            "cpp": '#include <iostream>\n#include <string>\n\nstd::string greet(const std::string& name) {\n    return "Hello, " + name + "!";\n}\n\nint main() {\n    std::cout << greet("Alex") << "\\n";\n    return 0;\n}',
            "csharp": 'using System;\n\nclass Program\n{\n    static string Greet(string name)\n    {\n        return $"Hello, {name}!";\n    }\n\n    static void Main()\n    {\n        Console.WriteLine(Greet("Alex"));\n    }\n}',
        },
        "challenges": {
            "python": "Write a function that takes a name and returns a welcome message. Call it with your name.",
            "cpp": "Write a function that takes a name and returns a welcome message. Call it with your name.",
            "csharp": "Write a function that takes a name and returns a welcome message. Call it with your name.",
        },
    },
    {
        "id": "collections",
        "title": "Keep items in a list",
        "explanation": "A collection keeps several values together. The examples create a list, vector, or array of topics and use a loop to visit each one.",
        "examples": {
            "python": 'topics = ["variables", "loops", "functions"]\nfor topic in topics:\n    print(topic)',
            "cpp": '#include <iostream>\n#include <string>\n#include <vector>\n\nint main() {\n    std::vector<std::string> topics = {"variables", "loops", "functions"};\n    for (const std::string& topic : topics) {\n        std::cout << topic << "\\n";\n    }\n    return 0;\n}',
            "csharp": 'using System;\n\nclass Program\n{\n    static void Main()\n    {\n        string[] topics = { "variables", "loops", "functions" };\n        foreach (string topic in topics)\n        {\n            Console.WriteLine(topic);\n        }\n    }\n}',
        },
        "challenges": {
            "python": "Make a list of three things you want to learn, then use a loop to print each one.",
            "cpp": "Make a vector of three things you want to learn, then use a loop to print each one.",
            "csharp": "Make an array of three things you want to learn, then use a loop to print each one.",
        },
    },
]


def lessons_for(language: str) -> list[Lesson]:
    """Return the learning path for one of the supported languages."""
    if language not in LANGUAGES:
        raise ValueError(f"Unknown language: {language}")
    return [
        Lesson(
            id=f"{language}:{topic['id']}",
            title=topic["title"],
            explanation=topic["explanation"],
            example=topic["examples"][language],
            challenge=topic["challenges"][language],
        )
        for topic in _TOPICS
    ]
