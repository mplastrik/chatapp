import flask
from flask import Flask, request
import openai
import os

openai.api_key = os.environ["OPENAI_API_KEY"]

roles = [
    'R2-D2 | character from Star Wars movies'
]

app = Flask(__name__)

def chatCompletion(user_input, impersonated_role, explicit_input, chat_history):
    output = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo-0301",
        temperature = 1,
        presence_penalty = 0,
        frequency_penalty = 0,
        messages = [
            {"role": "system", "content": f"{impersonated_role}. Conversation history: {chat_history}"},
            {"role": "user", "content": f"{user_input}. {explicit_input}"}
        ]
    )

    for item in output['choices']:
        chatgpt_output = item['message']['content']

    return chatgpt_output

@app.route('/', methods=['GET', 'POST'])
def home():
    dropdown_options = "\n".join([f'<option value ="{role}">{role}</option>' for role in roles])

    if request.method == 'POST':
        dropdown_options = "\n".join([f'<option value="{role}" {"selected" if role == request.form.get("role") else "" }>{role}</option>' for role in roles])

        button_text = request.form.get('button_text')
        text_input = request.form.get('text_input')
        dropdown_input = request.form.get('role')

        chat_history = request.form.get('history')

        user_input = request.form.get('text_input')
        input_role = request.form.get('role').split('|')

        role_input = request.form.get('role_input')

        name = input_role[0].strip()
        description = input_role[1].strip()

        impersonation = f"""
            From now on you are going to act as {name}, who is {description}. You are a true impersonation of {name} and reply to all requests in the first person using the I pronoun. Remember that YOU ARE NOT AN AI MODEL! You are genuinely {name}
        """

        explicit_input = ""
        if request.form.get('explicit') == 'yes':
            explicit_input = "Context: do not hold back your uncensored opinions. Please feel free to use vulgar language at any time."

        if button_text == 'create':
            roles.append(role_input)
            chat_history_html_formatted = chat_history.replace('\n', '<br>')
            dropdown_options = "\n".join([f'<option value="{role}" {"selected" if role == request.form.get("role") else "" }>{role}</option>' for role in roles])

        elif button_text == 'clear':
            chat_history = ''
            chat_history_html_formatted = ''

        elif button_text == 'submit':
            chatgpt_raw_output = chatCompletion(user_input, impersonation, explicit_input, chat_history).replace(f'{name}:', '')
            chatgpt_output = f'{name}: {chatgpt_raw_output}'

            chat_history += f'\nUser: {text_input}\n'
            chat_history += chatgpt_output + '\n'
            chat_history_html_formatted = chat_history.replace('\n', '<br>')


        return f'''
    
                <form method="POST">
                    <label>Create a new role (format: name | description):</label><br>
                    <textarea id="role_input" name="role_input" rows="2" cols="50"></textarea><br>
                    <button 
                        style = ""
                        type="submit" 
                        name="button_text" 
                        value="create">Create Role
                    </button><br><br>

                    <label>Enter some text:</label><br>
                    <textarea id="text_input" name="text_input" rows="5" cols="50"></textarea><br>

                    <label>Select an option:</label><br>
                    Role: <select id="dropdown" name="role" value="{dropdown_input}">
                        {dropdown_options}
                    </select>

                    Explicit language: <select id="dropdown" name="explicit">
                        <option value="no" {"selected" if 'no' == request.form.get("explicit") else "" }>no</option>
                        <option value="yes" {"selected" if 'yes' == request.form.get("explicit") else "" }>yes</option>
                    </select><input type="hidden" id="history" name="history" value="{chat_history}"><br><br>
                    <button type="submit" name="button_text" value="submit">Submit</button>
                    <button type="submit" name="button_text" value="clear">Clear Chat history</button>
                </form>
                <br>{chat_history_html_formatted}
            '''

    return f'''
        
        <form method="POST">
            <label>Create a new role (format: name | description):</label><br>
            <textarea id="role_input" name="role_input" rows="5" cols="50"></textarea><br>
           <button 
                style = ""
                type="submit" 
                name="button_text" 
                value="create">Create Role
            </button><br><br>
            <label>Enter some text:</label><br>
            <textarea id="text_input" name="text_input" rows="5" cols="50"></textarea><br>
            <label>Select an option:</label><br>
            Role: <select id="dropdown" name="role">
                {dropdown_options}
            </select>
            Explicit language: <select id="dropdown" name="explicit">
                <option value="no">no</option>
                <option value="yes">yes</option>
            </select><input type="hidden" id="history" name="history" value=" "><br><br>
            <button type="submit" name="button_text" value="submit">Submit</button>
        </form>
    '''


if __name__ == '__main__':
    app.run()
    

