# import libraries
from groq import Groq

# store api key
client = Groq(api_key="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")

# greeting message
print("Chatbot (Groq Streaming): Type 'quit', 'exit', or 'bye' to stop\n")


while True:
    # wait for input 
    user_input = input("You: ")

    # if user wants to exit the program
    if user_input.lower() in ["quit", "exit", "bye"]:
        print("Chatbot: Goodbye!")
        break

    # chatbot response
    print("Chatbot: ", end="", flush=True)

    # request response
    stream = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You are a helpful chatbot."},
            {"role": "user", "content": user_input}
        ],
        stream=True
    )

    # print response as it is being generated
    for chunk in stream:
        if chunk.choices[0].delta.content:
            print(chunk.choices[0].delta.content, end="", flush=True)
    
    print() # new line after response

