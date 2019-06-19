from flask import Flask, render_template, request
from database import *
from excel_to_sql import ExcelOperations
from cloud import CloudOperations
from simulator import Simulator

app = Flask(__name__)
app.config.from_object('settings')

@app.route('/',  methods=['GET', 'POST'])
def search_page():
    if request.method == "GET":
        return render_template("cloud_search.html")
    else:
        cloud = CloudOperations()
        diskEnd= request.form['DiskCapacity']
        ramEnd= request.form['RAM']
        diskStart = cloud.Get_Disk_Capacity(diskEnd)
        ramStart = cloud.Get_Ram_Capacity(ramEnd)
        searchList = cloud.Search_Cloud(region=request.form['Region'], os=request.form['OS'], core=request.form['Core'],
                                        diskType=request.form['DiskType'], diskCapStart=diskStart, diskCapEnd=int(diskEnd),
                                        ramStart=ramStart, ramEnd=int(ramEnd))
        return result_page(searchList)


@app.route('/result',  methods=['GET', 'POST'])
def result_page(searchList):
    print("Search List =>")
    print(searchList)
    return render_template("cloud_search.html", searchList=searchList)


@app.route('/initdb')
def init_page():
    db = DatabaseOperations()
    db.create_tables()
    db.db_init_parameters()
    print("Database initialized and parameters added!")
    return "Database initialized and parameters added!"


@app.route('/excel')
def excel_page():
    excel = ExcelOperations()
    excel.transfer_cloud()
    excel.transfer_storage()
    print("Data was transferred to the database!")
    return "Data was transferred to the database!"


@app.route('/sim')
def simulator_page():
    sim = Simulator()
    sim.sim()
    return "Simulator ended!"

if __name__ == '__main__':
    port = app.config.get("PORT", 5000)
    debug = True
    app.run(host='0.0.0.0', port=port, debug=debug)