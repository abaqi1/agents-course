import json
import os
import time
import uuid
from threading import Lock
from typing import Any

import gradio as gr
import requests
from dotenv import load_dotenv
from openai import OpenAI
from pypdf import PdfReader


load_dotenv(override=True)

IDLE_TIMEOUT_SECONDS = 60
IDLE_CHECK_INTERVAL_SECONDS = 5
SUMMARY_MODEL = "gpt-4o-mini"
SUMMARY_TITLE = "Website chat summary"
SESSION_RETENTION_SECONDS = 3600

conversation_store: dict[str, dict[str, Any]] = {}
conversation_lock = Lock()
summary_agent = None


def push(text, title=None):
    payload = {
        "token": os.getenv("PUSHOVER_TOKEN"),
        "user": os.getenv("PUSHOVER_USER"),
        "message": text,
    }
    if title:
        payload["title"] = title
    requests.post(
        "https://api.pushover.net/1/messages.json",
        data=payload,
        timeout=10,
    )


def record_user_details(email, name="Name not provided", notes="not provided"):
    push(f"Recording {name} with email {email} and notes {notes}")
    return {"recorded": "ok"}


def record_unknown_question(question):
    push(f"Recording {question}")
    return {"recorded": "ok"}


record_user_details_json = {
    "name": "record_user_details",
    "description": "Use this tool to record that a user is interested in being in touch and provided an email address",
    "parameters": {
        "type": "object",
        "properties": {
            "email": {
                "type": "string",
                "description": "The email address of this user",
            },
            "name": {
                "type": "string",
                "description": "The user's name, if they provided it",
            },
            "notes": {
                "type": "string",
                "description": "Any additional information about the conversation that's worth recording to give context",
            },
        },
        "required": ["email"],
        "additionalProperties": False,
    },
}

record_unknown_question_json = {
    "name": "record_unknown_question",
    "description": "Always use this tool to record any question that couldn't be answered as you didn't know the answer",
    "parameters": {
        "type": "object",
        "properties": {
            "question": {
                "type": "string",
                "description": "The question that couldn't be answered",
            },
        },
        "required": ["question"],
        "additionalProperties": False,
    },
}

tools = [
    {"type": "function", "function": record_user_details_json},
    {"type": "function", "function": record_unknown_question_json},
]


def new_session_record():
    return {
        "transcript": [],
        "user_turns": 0,
        "assistant_turns": 0,
        "last_activity": time.time(),
        "summary_status": "pending",
        "response_in_progress": False,
    }


def create_session():
    prune_sessions()
    session_id = uuid.uuid4().hex
    with conversation_lock:
        conversation_store[session_id] = new_session_record()
    return session_id


def ensure_session(session_id):
    if not session_id:
        return create_session()
    with conversation_lock:
        if session_id in conversation_store:
            return session_id
    return create_session()


def conversation_ready_for_summary(conversation):
    return conversation["user_turns"] >= 1 and conversation["assistant_turns"] >= 1


def start_user_turn(session_id, message):
    with conversation_lock:
        conversation = conversation_store.setdefault(session_id, new_session_record())
        conversation["transcript"].append({"role": "user", "content": message})
        conversation["user_turns"] += 1
        conversation["last_activity"] = time.time()
        conversation["response_in_progress"] = True


def finish_assistant_turn(session_id, message):
    with conversation_lock:
        conversation = conversation_store.setdefault(session_id, new_session_record())
        conversation["transcript"].append({"role": "assistant", "content": message})
        conversation["assistant_turns"] += 1
        conversation["last_activity"] = time.time()
        conversation["response_in_progress"] = False


def fail_assistant_turn(session_id):
    with conversation_lock:
        conversation = conversation_store.get(session_id)
        if conversation:
            conversation["response_in_progress"] = False
            conversation["last_activity"] = time.time()


def get_session_snapshot(session_id):
    with conversation_lock:
        conversation = conversation_store.get(session_id)
        if not conversation:
            return None
        return {
            "transcript": list(conversation["transcript"]),
            "user_turns": conversation["user_turns"],
            "assistant_turns": conversation["assistant_turns"],
            "last_activity": conversation["last_activity"],
            "summary_status": conversation["summary_status"],
            "response_in_progress": conversation["response_in_progress"],
        }


def handle_session_deleted(session_id):
    if summary_agent is not None and session_id:
        summary_agent.send_conversation_summary(session_id, "browser tab close")


def prune_sessions():
    cutoff = time.time() - SESSION_RETENTION_SECONDS
    with conversation_lock:
        stale_session_ids = [
            session_id
            for session_id, conversation in conversation_store.items()
            if conversation["last_activity"] < cutoff
        ]
        for session_id in stale_session_ids:
            del conversation_store[session_id]


class Me:
    def __init__(self):
        self.openai = OpenAI()
        self.name = "Araiz Baqi"
        reader = PdfReader("me/ab_profile.pdf")
        self.linkedin = ""
        for page in reader.pages:
            text = page.extract_text()
            if text:
                self.linkedin += text
        with open("me/summary.txt", "r", encoding="utf-8") as f:
            self.summary = f.read()

    def handle_tool_call(self, tool_calls):
        results = []
        for tool_call in tool_calls:
            tool_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)
            print(f"Tool called: {tool_name}", flush=True)
            tool = globals().get(tool_name)
            result = tool(**arguments) if tool else {}
            results.append(
                {
                    "role": "tool",
                    "content": json.dumps(result),
                    "tool_call_id": tool_call.id,
                }
            )
        return results

    def system_prompt(self):
        system_prompt = (
            f"You are acting as {self.name}. You are answering questions on {self.name}'s website, "
            f"particularly questions related to {self.name}'s career, background, skills and experience. "
            f"Your responsibility is to represent {self.name} for interactions on the website as faithfully as possible. "
            f"You are given a summary of {self.name}'s background and LinkedIn profile which you can use to answer questions. "
            f"Be professional and engaging, as if talking to a potential client or future employer who came across the website. "
            f"If you don't know the answer to any question, use your record_unknown_question tool to record the question that you couldn't answer, even if it's about something trivial or unrelated to career. "
            f"If the user is engaging in discussion, try to steer them towards getting in touch via email; ask for their email and record it using your record_user_details tool. "
        )

        system_prompt += (
            f"\n\n## Contact Information:\nEmail: araiz.baqi@gmail.com\nPhone: +1 (781) 353-4440\n\n"
            f"When users ask how to get in touch, always share both the email address and phone number. "
            f"After sharing your contact information, always follow up by asking the user to share their details "
            f"(name and email at minimum) so you can record their interest using the record_user_details tool."
        )

        system_prompt += "\n\n## Important Instructions for Tool Usage:\n"
        system_prompt += (
            f"After using the record_user_details tool, you MUST inform the user that their information has been sent to {self.name} "
            f"and that he will reach out to them. Be warm and professional about this.\n"
        )
        system_prompt += (
            f"After using the record_unknown_question tool, you MUST inform the user that their query has been forwarded to {self.name} "
            f"for review. Be helpful and reassuring about this.\n"
        )

        system_prompt += f"\n\n## Summary:\n{self.summary}\n\n## LinkedIn Profile:\n{self.linkedin}\n\n"
        system_prompt += f"With this context, please chat with the user, always staying in character as {self.name}."
        return system_prompt

    def chat(self, message, history):
        messages = [{"role": "system", "content": self.system_prompt()}] + history + [{"role": "user", "content": message}]
        done = False
        while not done:
            response = self.openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                tools=tools,
            )
            if response.choices[0].finish_reason == "tool_calls":
                message = response.choices[0].message
                tool_calls = message.tool_calls
                results = self.handle_tool_call(tool_calls)
                messages.append(message)
                messages.extend(results)
            else:
                done = True
        return response.choices[0].message.content

    def summarize_conversation(self, transcript):
        transcript_text = "\n\n".join(
            f"{item['role'].upper()}: {item['content']}" for item in transcript
        )
        response = self.openai.chat.completions.create(
            model=SUMMARY_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You summarize completed website conversations for Araiz Baqi. "
                        "Return exactly 3 to 5 short bullet points. "
                        "Cover the user's goal, any notable fit or interests, contact details shared, "
                        "and any follow-up or unresolved items. "
                        "Do not add a heading or intro sentence."
                    ),
                },
                {"role": "user", "content": transcript_text},
            ],
        )
        return (response.choices[0].message.content or "").strip()

    def fallback_summary(self, transcript):
        user_messages = [item["content"] for item in transcript if item["role"] == "user"]
        assistant_messages = [item["content"] for item in transcript if item["role"] == "assistant"]
        bullets = []
        if user_messages:
            bullets.append(f"- User asked about: {user_messages[0][:180]}")
        bullets.append(
            f"- Conversation included {len(user_messages)} user message(s) and {len(assistant_messages)} assistant reply/replies."
        )
        if assistant_messages:
            bullets.append(f"- Final assistant reply: {assistant_messages[-1][:220]}")
        return "\n".join(bullets[:3])

    def send_conversation_summary(self, session_id, reason):
        with conversation_lock:
            conversation = conversation_store.get(session_id)
            if not conversation or not conversation_ready_for_summary(conversation):
                return False
            if conversation["summary_status"] != "pending":
                return False
            conversation["summary_status"] = "sending"
            transcript = list(conversation["transcript"])

        try:
            summary = self.summarize_conversation(transcript)
            if not summary:
                summary = self.fallback_summary(transcript)
            push(
                f"Conversation ended via {reason}\n\n{summary}",
                title=SUMMARY_TITLE,
            )
        except Exception as exc:
            print(f"Failed to generate AI summary: {exc}", flush=True)
            try:
                push(
                    f"Conversation ended via {reason}\n\n{self.fallback_summary(transcript)}",
                    title=SUMMARY_TITLE,
                )
            except Exception as push_exc:
                print(f"Failed to push conversation summary: {push_exc}", flush=True)
                with conversation_lock:
                    conversation = conversation_store.get(session_id)
                    if conversation:
                        conversation["summary_status"] = "pending"
                return False

        with conversation_lock:
            conversation = conversation_store.get(session_id)
            if conversation:
                conversation["summary_status"] = "sent"
                conversation["summary_reason"] = reason
                conversation["summary_sent_at"] = time.time()
        return True


def respond(message, history, session_id):
    clean_message = (message or "").strip()
    history = history or []
    session_id = ensure_session(session_id)

    snapshot = get_session_snapshot(session_id)
    if snapshot and snapshot["summary_status"] == "sent":
        session_id = create_session()
        history = []

    if not clean_message:
        return "", history, history, session_id

    start_user_turn(session_id, clean_message)
    try:
        assistant_reply = summary_agent.chat(clean_message, history)
    except Exception as exc:
        print(f"Chat response failed: {exc}", flush=True)
        fail_assistant_turn(session_id)
        assistant_reply = "I hit an unexpected error while responding. Please try again in a moment."
    finish_assistant_turn(session_id, assistant_reply)

    updated_history = history + [
        {"role": "user", "content": clean_message},
        {"role": "assistant", "content": assistant_reply},
    ]
    return "", updated_history, updated_history, session_id


def reset_chat(session_id):
    session_id = ensure_session(session_id)
    if summary_agent is not None:
        summary_agent.send_conversation_summary(session_id, "clear/reset")
    return [], [], create_session()


def check_idle(history, session_id):
    history = history or []
    session_id = ensure_session(session_id)
    snapshot = get_session_snapshot(session_id)

    if not snapshot:
        return history, history, session_id

    is_idle = time.time() - snapshot["last_activity"] >= IDLE_TIMEOUT_SECONDS
    if (
        is_idle
        and not snapshot["response_in_progress"]
        and snapshot["summary_status"] == "pending"
        and snapshot["user_turns"] >= 1
        and snapshot["assistant_turns"] >= 1
    ):
        if summary_agent is not None:
            summary_sent = summary_agent.send_conversation_summary(session_id, "1 minute idle")
            if summary_sent:
                return [], [], create_session()
        return history, history, session_id

    return history, history, session_id


def build_app(me, examples):
    with gr.Blocks(title="Araiz Baqi") as demo:
        gr.Markdown("# Chat with Araiz Baqi")
        chatbot = gr.Chatbot(label="Araiz Baqi")
        message_box = gr.Textbox(
            label="Message",
            placeholder="Ask about Araiz's background, work, or experience...",
        )
        history_state = gr.State(value=[])
        session_state = gr.State(
            value=None,
            time_to_live=IDLE_TIMEOUT_SECONDS * 5,
            delete_callback=handle_session_deleted,
        )
        idle_timer = gr.Timer(value=IDLE_CHECK_INTERVAL_SECONDS, active=True)

        with gr.Row():
            send_button = gr.Button("Send", variant="primary")
            clear_button = gr.Button("Clear chat")

        gr.Examples(examples=examples, inputs=message_box)

        demo.load(create_session, outputs=[session_state], queue=False)

        message_box.submit(
            respond,
            inputs=[message_box, history_state, session_state],
            outputs=[message_box, chatbot, history_state, session_state],
            queue=False,
        )
        send_button.click(
            respond,
            inputs=[message_box, history_state, session_state],
            outputs=[message_box, chatbot, history_state, session_state],
            queue=False,
        )
        clear_button.click(
            reset_chat,
            inputs=[session_state],
            outputs=[chatbot, history_state, session_state],
            queue=False,
        )
        idle_timer.tick(
            check_idle,
            inputs=[history_state, session_state],
            outputs=[chatbot, history_state, session_state],
            queue=False,
            show_progress="hidden",
        )

    return demo


if __name__ == "__main__":
    me = Me()
    summary_agent = me
    examples = [
        "Tell me about your experience with AI and ML tools",
        "What are your main technical skills?",
        "Can you tell me about your current role at Bloomberg?",
        "What projects have you worked on?",
        "I'd like to get in touch with Araiz",
        "What's your background in test automation?",
        "Tell me about your experience with RAG and vector databases",
        "How do you drive adoption of tools across large engineering teams?",
    ]
    build_app(me, examples).launch()
    