try:
    import collections.abc as collections
except ImportError:
    import collections as collections
from mcpi.timer import t
def flatten(l):
    for e in l:
        if isinstance(e, collections.Iterable) and not isinstance(e, str):
            for ee in flatten(e): yield ee
        else: yield e

def flatten_parameters_to_string(l):
    p=flatten(l)
    #t.print("flatten(l)")
    d=",".join(map(str, p))
    #t.print("joined")
    return d

# def _misc_to_bytes(m):
#     """
#     Convert an arbitrary object into a string encoded as a UTF-8 series of bytes. 

#     See `Connection.send` for more details.
#     """

#     return str(m).encode("UTF-8")
