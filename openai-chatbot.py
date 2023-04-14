import openai, config, os, ast, sys

# Author vietjovi@gmail.com

def openAIRequest(question = "", userId = ""):
    openai.api_key = config.api_key
    openai.api_base = config.api_endpoint
    openai.api_type = config.api_type
    openai.api_version = config.api_version

    response = openai.ChatCompletion.create(
        engine = config.engine,
        messages = [
            # {"role": "system", "content": "Assistant is a large language model trained by OpenAI."},
            {"role": "system", "content": "You are a helpful AI assistant."},
            {"role": "user", "content": question},
        ],
        user = userId
    )
    
    # print(response)
    return response['choices'][0]['message']['content']

def openAIRequestWithPastMessages(pastMsg = [], question = "", userId = ""):
    openai.api_key = config.api_key
    openai.api_base = config.api_endpoint
    openai.api_type = config.api_type
    openai.api_version = config.api_version
    
    msg = [{'role': 'system', 'content': 'You are a helpful AI assistant.'}]
    # print(type(pastMsg))
    # print(pastMsg)
    for m in pastMsg:
        msg.append(m)
    msg.append({'role': 'user', 'content': question})
    # print(msg)

    try:
        response = openai.ChatCompletion.create(
        engine = config.engine,
        messages = msg,
        user = userId
    )
        
        # print(response)
        answer = response['choices'][0]['message']['content']
    except Exception as e:
        answer = "Sorry, I can not answer your question. Please try again."
        print(e)
    
    pastMsg.append({'role': 'user', 'content': question})
    pastMsg.append({'role': 'assistant', 'content': answer})
    # print(pastMsg)
    savePastMessages(userId, pastMsg)

    return answer

def loadPastMessages(uid):
    pastMessages = []
    dataPath = config.data_dir + "/" +  uid
    if os.path.exists(dataPath):
        try:
            with open(dataPath, "r") as f:
                pastMessages = f.read()
        except:
            pastMessages = []
            return pastMessages
    else:
        return pastMessages

    if pastMessages is None:
        pastMessages = []
        return pastMessages
    # try:
    # print(pastMessages)
    return ast.literal_eval(pastMessages)
    # except:
    #     return []

def savePastMessages(uid, msg):
    dataPath = config.data_dir + "/"+  uid
    #Clean first message
    if len(msg) > int(config.past_message_included*2):
        msg = msg[2:]

    try:
        with open(dataPath, "w") as f:
            pastMessages = f.write(str(msg))
        return True
    except Exception as e:
        return False

def main():
    userInput = ''
    userId = "user_123"
    print(f'OPENAI CHATBOT {config.version} - Engine: {config.engine}')
    print("Enter 'bye' or 'exit' to quit")
    while ((userInput.lower() != 'exit') and (userInput.lower() != 'bye')):
        userInput = input("You: ")
        if ((userInput.lower() == 'exit') or (userInput.lower() == 'bye')):
            print('Goodbye. See you!')
            sys.exit(0)
        # print(userInput)
        print("OpenAI-Bot: " + openAIRequestWithPastMessages(loadPastMessages(userId), userInput, userId))
    print('Goodbye. See you!')
    return True

if __name__ == "__main__":
    main()