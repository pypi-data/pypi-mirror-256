import io, os, sys, types
from IPython import get_ipython
from nbformat import read
from IPython.core.interactiveshell import InteractiveShell

import pyntload.helper

current_filepath = None
current_levels = None
running_on_databricks = None

#detect if in databricks environment
def detect_environment():
    global running_on_databricks

    print("Detecting environment")
    try:
        print("Databricks check")
        os.environ["DATABRICKS_RUNTIME_VERSION"]
        print("Databricks ok")
        running_on_databricks=1
    except:
        print("Local it is")
        running_on_databricks=0
        print("Yep local")

def find_notebook(fullname, path=None):
    """find a notebook, given its fully qualified name and an optional path

    This turns "foo.bar" into "foo/bar.ipynb"
    and tries turning "Foo_Bar" into "Foo Bar" if Foo_Bar
    does not exist.
    """
    print("find_notebook called with ", fullname)

    if running_on_databricks:

        #extract filename
        name = fullname.split('/')[-1]

        #path is extracted via getcwd
        path= os.getcwd()

        #join path and filename
        nb_path = os.path.join(d, name + ".ipynb")

        return nb_path

    else:

        name = fullname.rsplit('.', 1)[-1]
        print("name = ", name)
        if not path:
            path = ['']
        for d in path:
            
            nb_path = os.path.join(d, name + ".ipynb")
            print("Part of path = ", d, " nb_path = ", nb_path)

            if os.path.isfile(nb_path):
                return nb_path
            # let import Notebook_Name find "Notebook Name.ipynb"
            nb_path = nb_path.replace("_", " ")
            if os.path.isfile(nb_path):
                return nb_path

class NotebookLoader(object):
    """Module Loader for Jupyter Notebooks"""
    def __init__(self, path=None):
        self.shell = InteractiveShell.instance()
        self.path = path

    def load_module(self, fullname):
        # load the notebook object (depending on on databricks or not)
        if running_on_databricks:
            print("on databricks")

            nb = pyntload.helper.read_databricks_notebook(path)
        else:
            """import a notebook as a module"""
            path = find_notebook(fullname, self.path)
            print ("importing Jupyter notebook from %s on local machine" % path)

            with io.open(path, 'r', encoding='utf-8') as f:
                nb = read(f, 4)


        # create the module and add it to sys.modules if name in sys.modules:
        #    return sys.modules[name]
        mod = types.ModuleType(fullname)
        mod.__file__ = path
        mod.__loader__ = self
        mod.__dict__['get_ipython'] = get_ipython
        sys.modules[fullname] = mod

        # extra work to ensure that magics that would affect the user_ns
        # actually affect the notebook module's ns
        save_user_ns = self.shell.user_ns
        self.shell.user_ns = mod.__dict__

        try:
          for cell in nb.cells:
            if cell.cell_type == 'code':
                # transform the input to executable Python
                code = self.shell.input_transformer_manager.transform_cell(cell.source)
                # run the code in themodule
                exec(code, mod.__dict__)
        finally:
            self.shell.user_ns = save_user_ns
        return mod


class NotebookFinder(object):
    """Module finder that locates Jupyter Notebooks"""
    def __init__(self):
        print("Init NotebookFinder called")
        self.loaders = {}

    def find_module(self, fullname, path=None):
        print("find_module called\nfullname = ", fullname, "\npath = ", path)
        nb_path = find_notebook(fullname, path)

        if not nb_path:
            return
        
        else:
        
            if running_on_databricks:
                #create key
                key = os.getcwd()

                #register with self.loaders
                self.loaders[key] = NotebookLoader(nb_path)

                return self.loaders[key]
            
            else:
                key = path
                if path:
                    # lists aren't hashable
                    key = os.path.sep.join(path)

                if key not in self.loaders:
                    self.loaders[key] = NotebookLoader(path)
                return self.loaders[key]


sys.meta_path.append(NotebookFinder())


def set_current_filepath(filepath):
    global current_filepath
    current_filepath = filepath

    global current_levels
    current_levels = [level.lower() for level in filepath.split('/')[1:-1]]