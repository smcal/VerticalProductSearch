from flask import Flask
from flask import render_template
from flask import request
import os
from queryProcessing_and_Ranking import QueryProcessing
import pdb

app = Flask(__name__)

@app.route("/")
@app.route("/<query>")
def index():
    query = request.args.get("query")

    try:
        #pdb.set_trace()
        Processing = QueryProcessing()
        ranked_list = Processing.getDataFromQuery( query )
        return render_template( "index.html", ranked_list = ranked_list, user_input = query )

    except Exception:
        return render_template( "error_page.html", user_input = query )

if __name__ == '__main__':
    port = int( os.environ.get('PORT', 5000 ) )
    #app.run( host='0.0.0.0', port=port, debug=True)
    app.run( host='0.0.0.0')
