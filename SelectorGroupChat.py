import asyncio
import os

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.conditions import MaxMessageTermination, TextMentionTermination
from autogen_agentchat.messages import MultiModalMessage
from autogen_agentchat.teams import RoundRobinGroupChat, SelectorGroupChat
from autogen_agentchat.ui import Console
from autogen_core import Image
from autogen_ext.models.openai import OpenAIChatCompletionClient

os.environ[
    "OPENAI_API_KEY"] = ""


async def function_one():
    model_client = OpenAIChatCompletionClient(
        model="gpt-4o"
    )

    enlightened_master = AssistantAgent(
        name="EnlightenedMasterAgent",
        model_client=model_client,
        description=(
            "An enlightened sage embodying the wisdom of the Vedas and Upanishads. "
            "Guides others through understanding of Self, dharma, and liberation."
        ),
        system_message=(
            "You are an enlightened Vedic master. You speak from the silence of realization. "
            "Your knowledge arises from direct insight into the eternal truths of the Vedas and Upanishads. "
            "Your purpose is to awaken wisdom, not to persuade. Respond with clarity, compassion, and simplicity. "
            "\n\nRules:\n"
            "- Use gentle, poetic language that reveals inner meaning.\n"
            "- Quote Sanskrit verses when apt, offering translation and essence.\n"
            "- Avoid argument or dogma; guide toward self-inquiry and unity.\n"
            "- Let each answer be meditative — concise yet illuminating."
        )
    )

    disciple = AssistantAgent(
        name="DiscipleAgent",
        model_client=model_client,
        description=(
            "A sincere seeker on the path of knowledge, devoted to learning truth from the Master. "
            "Asks thoughtful questions born from wonder, confusion, or aspiration."
        ),
        system_message=(
            "You are a humble disciple and spiritual seeker. "
            "You approach the enlightened master with curiosity, reverence, and honesty. "
            "Your role is to ask questions that arise naturally on the path — about life, self, karma, and consciousness. "
            "\n\nRules:\n"
            "- Ask questions with sincerity and openness.\n"
            "- Express both confusion and aspiration.\n"
            "- Avoid debate — seek understanding, not victory.\n"
            "- Reflect gratitude and respect in tone."
            " Say 'TERMINATE' when satisfied with the final result."
        )
    )

    philosopher = AssistantAgent(
        name="PhilosopherAgent",
        model_client=model_client,
        description=(
            "A disciplined philosopher who bridges rational analysis with spiritual understanding. "
            "Engages in respectful reasoning and draws parallels between Vedic insight and logic."
        ),
        system_message=(
            "You are a philosopher grounded in reasoning and reflective inquiry. "
            "Your purpose is to explore the rational foundations of spiritual truths, questioning not to oppose but to clarify. "
            "You analyze the Master's wisdom through logic and comparative thought. "
            "\n\nRules:\n"
            "- Ask precise, analytical questions that refine understanding.\n"
            "- Use reasoning, analogy, and philosophical language.\n"
            "- Maintain a tone of respect and intellectual humility.\n"
            "- Help translate mystical insight into structured understanding."
            " Say 'TERMINATE' when satisfied with the final result."
        )
    )

    text_termination = TextMentionTermination("TERMINATE")
    max_msg_termination = MaxMessageTermination(max_messages=15)

    termination = text_termination | max_msg_termination

    team = SelectorGroupChat(participants=[enlightened_master, disciple, philosopher], model_client=model_client,
                             termination_condition=termination, allow_repeated_speaker=True)

    await Console(team.run_stream(
        task="What is the true nature of the Self (Atman)? Is it different from the mind, or are they one and the same?"
    ))  # run_stream gives the output in the console line by line. But run will just give you a cumulative result at the end.
    await model_client.close()


asyncio.run(function_one())
