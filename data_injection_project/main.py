from app import CreateApp



# Creating the app
app = CreateApp().create_app()


if __name__ == '__main__':


    # Running the app
    app.run(debug=True, port=5050)