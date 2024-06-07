## In this work, I compare different types of machine-learning algorithms.
1. Linear Regression
2. Decision Tree
3. Random Forest
4. Polynomial Features
## Streamlit web application using vscode for windows :

### Follow the below steps:

1. Open your vscode and click the new terminal. Use the `` Ctrl+Shift+` `` keyboard shortcut to create a new terminal.

2. Create a new set up virtual environment. A virtual environment is a named, isolated, working copy of Python that that maintains its own files, 
directories, and paths so that you can work with specific versions of libraries or Python itself without affecting other Python projects. Run this code :
`` python -m venv private ``

3. Activating the virtual environment : `` private\Scripts\activate ``

4. Installation of required packages to the virtual environment.

- A. Install Streamlit :	`` pip install streamlit ``
	
- B. Install Sklearn : `` pip install scikit-learn ``

5. Generate a Requirements File. This file is a checklist for the Python application in question. It lists all libraries and associated versions used in the app. 
To generate a requirements.txt file, navigate to the terminal and run this code : `` pip freeze > requirements.txt ``
  
6. Run Streamlit as a Python module : `` streamlit run app.py ``

7. Fianal deploy in streamlit website create account or sign in streamlit.io and deploy final web app.

