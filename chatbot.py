import openai, config

def openAIRequest(question = "", apiKey = "", userId = ""):
    openai.api_type = os.environ['api_type']
    openai.api_version = os.environ['api_version']
    openai.api_base = os.environ['api_endpoint']
    openai.api_key = apiKey
    response = openai.ChatCompletion.create(
        engine=os.environ['engine'], # The deployment name you chose when you deployed the ChatGPT or GPT-4 model.
        messages=[
            # {"role": "system", "content": "Assistant is a large language model trained by OpenAI."},
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": question},
        ],
        user = userId
    )
    
    print(response)
    return response['choices'][0]['message']['content']

def openAIRequestWithPastMessages(pastMsg = [], question = "", apiKey = "", userId = ""):
    openai.api_type = os.environ['api_type']
    openai.api_version = os.environ['api_version']
    openai.api_base = os.environ['api_endpoint']
    openai.api_key = apiKey
    msg = [{'role': 'system', 'content': 'You are a helpful AI assistant.'}]
    # print(type(pastMsg))
    # print(pastMsg[0])
    for m in pastMsg:
        msg.append(m)
    msg.append({'role': 'user', 'content': question})
    # print(msg)

    try:
        response = openai.ChatCompletion.create(
            engine=os.environ['engine'], # The deployment name you chose when you deployed the ChatGPT or GPT-4 model.
            messages=msg,
            user = userId
        )
        
        print(response)
        answer = response['choices'][0]['message']['content']
    except Exception as e:
        answer = "Sorry, I can not answer your question. Please try again."
        print(e)
    
    pastMsg.append({'role': 'user', 'content': question})
    pastMsg.append({'role': 'assistant', 'content': answer})
    print(pastMsg)
    savePastMessages(userId, pastMsg)

    return answer

def loadPastMessages(uid):
    try:
        pastMessages = r.get(f'{uid}_msg')
    except Exception as e:
        print(f"No past messages for {uid}")
        print(e)
        pastMessages = []
        return pastMessages
    # print(pastMessages)
    if pastMessages is None:
        pastMessages = []
        return pastMessages
    return ast.literal_eval(pastMessages)

def savePastMessages(uid, msg):
    global r
    #Clean first message
    if len(msg) > int(config.environ['past_message_included'])*2:
        msg = msg[2:]
    # r.set(f'{uid}_msg', str(msg))
    try:
        r.set(f'{uid}_msg', str(msg))
    except Exception as e:
        print(f"No past messages for {uid}")
        print(e)
        return False

    return True
