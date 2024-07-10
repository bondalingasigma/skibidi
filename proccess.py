import os
import json
from openai import OpenAI
import threading
import funcs
import imagerec
from say import say

api_key = "sk-proj-jBrtG6TRqETlklbXFoLST3BlbkFJwUhu1DuoYJjEabQ20yNy"
assistant_id = "asst_4JKKzrWYvEl8HoiTAIsJHkaq"
client = OpenAI(api_key=api_key)

THREAD_ID_FILE = "thread_id.json"

def save_thread_id(thread_id):
    with open(THREAD_ID_FILE, 'w') as file:
        json.dump({"thread_id": thread_id}, file)

def load_thread_id():
    if os.path.exists(THREAD_ID_FILE):
        with open(THREAD_ID_FILE, 'r') as file:
            data = json.load(file)
            return data.get("thread_id")
    return None

# Load the existing thread ID
thread_id = load_thread_id()

if thread_id:
    thread = client.beta.threads.retrieve(thread_id=thread_id)
else:
    thread = client.beta.threads.create()
    save_thread_id(thread.id)  # Use thread.id instead of thread['id']

def run_script_in_thread(filename, directory=""):
    thread = threading.Thread(target=funcs.run_script, args=(filename, directory))
    thread.start()
    return "Successfully started running the script"

def process(input_text):
    try:

        # User input for the assistant
        user_input = input_text

        # Send user input message
        client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=[
                {
                    "type": "text",
                    "text": user_input
                }
            ]
        )

        # Start a run to interact with the assistant
        run = client.beta.threads.runs.create_and_poll(
            thread_id=thread.id,
            assistant_id=assistant_id,
        )

        # Define the list to store tool outputs
        tool_outputs = []

        # Check if tool outputs are required
        if run.required_action is not None:
            for tool in run.required_action.submit_tool_outputs.tool_calls:
                # Cool Stuff
                if tool.function.name == "my_ip":
                    tool_outputs.append({
                        "tool_call_id": tool.id,
                        "output": funcs.my_ip()
                    })
                elif tool.function.name == "current_time":
                    tool_outputs.append({
                        "tool_call_id": tool.id,
                        "output": funcs.current_time()
                    })
                elif tool.function.name == "internet_speed":
                    tool_outputs.append({
                        "tool_call_id": tool.id,
                        "output": funcs.internet_speed()
                    })
                elif tool.function.name == "random_advice":
                    tool_outputs.append({
                        "tool_call_id": tool.id,
                        "output": funcs.randomadvice()
                    })
                elif tool.function.name == "search_youtube":
                    arguments = json.loads(tool.function.arguments)
                    prompt = arguments["prompt"]
                    tool_outputs.append({
                        "tool_call_id": tool.id,
                        "output": funcs.search_yt(prompt)
                    })

                # Image Stuff
                elif tool.function.name == "analyse_image":
                    arguments = json.loads(tool.function.arguments)
                    tool_outputs.append({
                        "tool_call_id": tool.id,
                        "output": imagerec.main()
                    })

                # File Stuff
                elif tool.function.name == "new_file":
                    arguments = json.loads(tool.function.arguments)
                    file_name = arguments["filename"]
                    file_type = arguments["filetype"]
                    directory = arguments.get("dir", "")
                    tool_outputs.append({
                        "tool_call_id": tool.id,
                        "output": funcs.newfile(file_name, file_type, directory)
                    })
                elif tool.function.name == "write_file":
                    arguments = json.loads(tool.function.arguments)
                    file_name = arguments["filename"]
                    file_content = arguments["content"]
                    directory = arguments.get("dir", "")
                    tool_outputs.append({
                        "tool_call_id": tool.id,
                        "output": funcs.writefile(file_name, file_content, directory)
                    })
                elif tool.function.name == "new_folder":
                    arguments = json.loads(tool.function.arguments)
                    dir_name = arguments["foldername"]
                    directory = arguments.get("dir", "")
                    tool_outputs.append({
                        "tool_call_id": tool.id,
                        "output": funcs.newdir(dir_name, directory)
                    })
                elif tool.function.name == "run_script":
                    arguments = json.loads(tool.function.arguments)
                    file_name = arguments["filename"]
                    directory = arguments.get("dir", "")
                    # Call run_script_in_thread to run the script asynchronously
                    tool_outputs.append({
                        "tool_call_id": tool.id,
                        "output": run_script_in_thread(file_name, directory)
                    })

        # Submit tool outputs if necessary
        if tool_outputs:
            run = client.beta.threads.runs.submit_tool_outputs_and_poll(
                thread_id=thread.id,
                run_id=run.id,
                tool_outputs=tool_outputs
            )

        if run.status == 'completed':
            # Retrieve messages from the thread
            messages = client.beta.threads.messages.list(
                thread_id=thread.id
            )
            if messages.data:
                response_message = messages.data[0]  # Assuming there is only one message
                if response_message.content:
                    response_text = response_message.content[0].text.value
                    return response_text
        else:
            return run.status  # Return the status if not completed

    except Exception as e:
        return str(e)  # Return any exceptions as string

    return None  # Default return if no response

if __name__ == "__main__":
    while True:
        prompt = input("User: ")
        output = process(prompt)
        print(f"Jarvis: {output}")