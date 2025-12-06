We are building an MVP web app that helps users tailor their resumes and apply for jobs. It needs to be light weight. It is called ResumeBuilder01. I want to use FastAPI and templates with html files to render the pages in the same application.
I would like to keep the code base in the src directory. This application needs to be modular so please keep the code in the routes short but use functions in separate files that execute the heavier functionality.

This will be a website geared to helping users apply to jobs. They will be able to upload their resume and the job description they are applying for. Then the web app will send this information to an LLM, there will be two models to choose from the OpenAI’s gpt-4o-mini and a Ollama which runs on my personal server. I have a .env file with the URL_BASE_OPENAI variable that is the base url to the open ai https://api.openai.com/v1. Then I have the key stored in KEY_OPENAI. Also For Ollama I have URL_BASE_OLLAMA which is the base url and KEY_OLLAMA, which is the api key. Please create functions to use each. The home page will have a radio button that will say “mistral:instruct” and “gpt-4o-mini”. Depending on the selected option the user will send the resume and job descripton using a prompt to the corresponding model. See the docs/OLLAMA_REFERENCE.md for connecting to the Ollama app which is running “mistral:instruct”. For chatGPT please use the Open AI documentation for connecting to the OpenAI API.

I have started the project folder with an src/templates/markdown/prompt01.md file that will be the template for the prompt sent to the LLM. The endpoint of the first page will take the resume word document and read and place replace the “< Resume of user>”. Then it will replace the “< Job Requirements >” with the job requirements pasted into the textarea for the job requirements.

Once the user hits submit there should be a custom spinner that indicates to the user the web app is working. When the LLM sends a response the user will be advanced to the second page of the web app.

The second page of the web app will have many sections and could be quite long: at the top it will have a score based on a feature-extraction model’s vector rating. So we’ll call this the “Resume qualifier match %”. This section will take up 15% of the view port. This functionality should just be a placeholder.

The next section just below the “Resume qualifier match %”,will be the new resume. In this same section but above the resume there will be a “Resume qualifier match REVISED %”. Which will be the new score based on the LLM’s tailored resume. The “Resume qualifier match REVISED %” will also just be a placeholder.

The next section below will present the user with a tailored cover letter.

The final section in the bottom will be a section that presents the user with a list of suggestions or gaps in their resume that could improve their resume.

I have docs/STYLE_GUIDE.md file which shows the style that should be followed. Each section should have a black border with rounded corners.

For now let’s just store the uploaded resumes in a directory in the project.
