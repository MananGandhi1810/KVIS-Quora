from initial import *
app=create_app()
# with app.app_context():    
    # db.create_all()
app.run(debug=True)