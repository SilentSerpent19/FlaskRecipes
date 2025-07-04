from flask import Flask
from flask import render_template, session, flash, redirect, request
app= Flask(__name__)
app.secret_key="hsuiqw"