from initial import *
print("Running....")
app=create_app()
# with app.app_context():    
		# db.create_all()
app.run(debug=False, host="0.0.0.0", port=3000)
