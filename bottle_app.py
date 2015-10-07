from bottle import default_app, route, static_file, request
import linear_algebra_project.plotting as plotting
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
fignames = plotting.figurenames 

@route('/')
def hello_world():
    #return 'Hello from Bottle!'
    return static_file('index.html', root='/home/strangesast/mysite/')

@route('/recalculate/<which>', method='POST')
def recalcuate(which):
    if which in fignames:
        by_var = {}
        values = request.json['values']
        for keyval in values:
            by_var[str(keyval['name'])] = float(keyval['value'])

        testfig = plt.figure()
        ax = testfig.add_subplot(111)

        label = ""
        name = ""
        s = 2.0
        deg = 30
        k = 0.5

        if which == 'scale':
            prime = plotting.scale(by_var['s'], ax)
            name = 'scale'

        elif which == 'rotate':
            prime = plotting.rotate(by_var['deg'], ax)
            name = 'rotate'

        elif which == 'shear':
            prime = plotting.shear(by_var['k'], ax)
            name = 'shear'

        elif which == "shearrotate":
            prime = plotting.shear(by_var['k'], ax)
            ax.cla()
            new_label = "shear: {}, rotate: {}".format(by_var['k'], by_var['deg'])
            prime = plotting.rotate(by_var['deg'], ax, prime, label=new_label)
            name = 'shearrotate'

        elif which == "rotateshear":
            prime = plotting.rotate(by_var['deg'], ax)
            ax.cla()
            new_label = "rotate: {}, shear: {}".format(by_var['deg'], by_var['k'])
            prime = plotting.shear(by_var['k'], ax, prime, label=new_label)
            name = 'rotateshear'

        plotting.set_axis_and_save(testfig, ax, name)

        return "updated"

    else:
        return "method not available"


@route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='/home/strangesast/mysite')


application = default_app()
