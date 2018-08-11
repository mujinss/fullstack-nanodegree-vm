from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Restaurant, Base, MenuItem
import cgi
## create session and connect to DB ##
## Better to make this global, and outside the class webserverHandler##
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
Session = sessionmaker(bind=engine)
session = Session()
names = session.query(MenuItem.name).all()
#session.commit()

class webserverHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		try: 
			if self.path.endswith("/restaurants"):
				restaurants = session.query(Restaurant).all()
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()

				output = ""
				output += "<html><body>"
				output += "<h1>Hello! Welcome to the restaurant!</h1>"
				output += "<a href='./restaurants/new'>Add a new restaurant here.</a>"
				output += "<ul>Menu Items"
				
				
				for restaurant in restaurants:
					output +="<li>" + restaurant.name + "</li>"
					output +="<a href='#'>Edit</a><br>"
					output +="<a href='#'>Delete</a>"
					#output +="<form method='POST' multipart/form-data action='/restaurants'><input type='submit' value='Delete'></form>"
					output +="<br><br><br>"
				output += "</ul></body><html>"
				self.wfile.write(output)
				print (output)
				return
			elif self.path.endswith("restaurants/new"):
				print("hello")
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()
				output = ""
				output += "<html><body>"
				output += "<h1>Hello! Add a new restaurant!</h1>"
				output += "<form method='POST' enctype='multipart/form-data' action='/restaurants'>"
				output += "<h2>New restaurant</h2><input name ='message' type = 'text'>"
				output += "<input type = 'submit' value = 'Submit'></form>"
				output += "</ul></body><html>"
				self.wfile.write(output)
				print (output)
				return
				
		except IOError:
			self.send_error(404, "File Not Found %s" % self.path)

	def do_POST(self):
		try:
			self.send_response(301)
			self.end_headers()

			ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
			if ctype == 'multipart/form-data':
				fields = cgi.parse_multipart(self.rfile, pdict)
				new_r_name = fields.get('message')[0]
				new_r = Restaurant(name = new_r_name)
				session.add(new_r)
				session.commit()
				restaurants = session.query(Restaurant).all()

			output = ""
			output += "<html><body>"
			output += "<h1>Hello! Welcome to the restaurant!</h1>"
			output += "<a href='./restaurants/new'>Add a new restaurant here.</a>"
			output += "<ul>Menu Items"
			for restaurant in restaurants:
				output +="<li>" + restaurant.name + "</li>"
				output +="<a href='./new'>Edit</a><br>"
				output +="<a href='#'>Delete</a>"
				#output +="<form method='POST' multipart/form-data action='/restaurants'><input type='submit' value='Delete'></form>"
				output +="<br><br><br>"
			output += "</ul></body><html>"
			self.wfile.write(output)
			print (output)
			return
		except:
			pass

def main():
	try:
		port = 8080
		server = HTTPServer(('', port), webserverHandler)
		print ("Web server running on port %s" % port)
		server.serve_forever()
	except KeyboardInterrupt:
		print ("^C entered, stopping web server...")
		server.socket.close()


if __name__ == '__main__':
	main()


	

