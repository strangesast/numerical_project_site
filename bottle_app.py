from bottle import default_app, route, static_file
import linear_algebra_project.plotting as plotting
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
fignames = plotting.figurenames 

@route('/')
def hello_world():
    #return 'Hello from Bottle!'
    return static_file('index.html', root='/home/strangesast/mysite/')

@route('/recalculate/<which>')
def recalcuate(which):
    if which in fignames:
        testfig = plt.figure()
        ax = testfig.add_subplot(111)

        label = ""
        name = ""
        s = 2.0
        deg = 30
        k = 0.5

        if which == 'scale':
            prime = plotting.scale(s, ax)
            name = 'scale'

        elif which == 'rotate':
            prime = plotting.rotate(deg, ax)
            name = 'rotate'

        elif which == 'shear':
            prime = plotting.shear(k, ax)
            name = 'shear'

        elif which == "shearrotate":
            prime = plotting.shear(k, ax)
            ax.cla()
            new_label = "shear: {}, rotate: {}".format(k, deg)
            prime = plotting.rotate(deg, ax, prime, label=new_label)
            name = 'shearrotate'

        elif which == "rotateshear":
            prime = plotting.rotate(deg, ax)
            ax.cla()
            new_label = "rotate: {}, shear: {}".format(deg, k)
            prime = plotting.shear(k, ax, prime, label=new_label)
            name = 'rotateshear'

        plotting.set_axis_and_save(testfig, ax, name)

        return "updated"

    else:
        return "method not available"


@route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='/home/strangesast/mysite')


application = default_app()
