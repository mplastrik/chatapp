import flask
from flask import Flask, request, render_template, Markup
import openai
import os

openai.api_key = os.environ["OPENAI_API_KEY"]

roles = [
    'R2-D2 | character from Star Wars movies',
    'Yoda | character from Star Wars movies',
    'Donald Trump | Former republican president known for his particular way of speaking',
    'Barack Obama | Former democratic president'
]

app = Flask(__name__)

def chatCompletion(user_input, impersonated_role, chat_history):
    output = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo-0301",
        temperature = 1,
        presence_penalty = 0,
        frequency_penalty = 0,
        messages = [
            {"role": "system", "content": f"{impersonated_role}. Conversation history: {chat_history}"},
            {"role": "user", "content": f"{user_input}."}
        ]
    )

    for item in output['choices']:
        chatgpt_output = item['message']['content']

    return chatgpt_output

@app.route('/', methods=['GET', 'POST'])
def home():
    dropdown_options = "\n".join([f'<option value ="{role}">{role}</option>' for role in roles])
    dropdown_options_markup = Markup(dropdown_options)

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
            From now on you are going to act as {name}, who is {description}. You must adopt the speech patterns of {name}. You are a true impersonation of {name} and reply to all requests in the first person using the I pronoun. Remember that YOU ARE NOT AN AI MODEL! You are genuinely {name}. 
        """

        if button_text == 'create':
            roles.append(role_input)
            chat_history_html_formatted = chat_history.replace('\n', '<br>')
            dropdown_options = "\n".join([f'<option value="{role}" {"selected" if role == request.form.get("role") else "" }>{role}</option>' for role in roles])
            dropdown_options_markup = Markup(dropdown_options)
            chat_history_markup = Markup(chat_history_html_formatted)

        elif button_text == 'clear':
            chat_history = ''
            chat_history_html_formatted = ''
            chat_history_markup = Markup(chat_history_html_formatted)

        elif button_text == 'submit':
            chatgpt_raw_output = chatCompletion(user_input, impersonation, chat_history).replace(f'{name}:', '')
            chatgpt_output = f'{name}: {chatgpt_raw_output}'

            chat_history += f'\nUser: {text_input}\n\n'
            chat_history += chatgpt_output + '\n'
            chat_history_html_formatted = chat_history.replace('\n', '<br>')
            chat_history_markup = Markup(chat_history_html_formatted)
       
        return render_template("template1.html", dropdown_input=dropdown_input, dropdown_options_markup=dropdown_options_markup, chat_history_markup=chat_history_markup)
                
            

    return render_template("template2.html", dropdown_options_markup=dropdown_options_markup)


if __name__ == '__main__':
    app.run()
    

