
# transformation (rotation, shift) of pixels
class Transformer:

    ROT_0 = 0
    ROT_90 = 1
    ROT_180 = 2
    ROT_270 = 3

    # rotation matrix (rotate passiv - is against the clock)
    MX_ROT = {

        ROT_0: [[1, 0], [0, 1]],  # Ausgangsposition
        ROT_90: [[0, -1], [1, 0]],
        ROT_180: [[-1, 0], [0, -1]],
        ROT_270: [[0, 1], [-1, 0]]
    }

    # shift vectors for each rotation angle
    XYC = {
        ROT_0: [0, 0],
        ROT_90: [0, 1],
        ROT_180: [1, 1],
        ROT_270: [1, 0],
    }

    # rotation
    @staticmethod
    def rotate(xy, rot, boxsize) -> object:

        x = xy[0]
        y = xy[1]

        # process rotation
        mx_rot = Transformer.MX_ROT[rot]
        xtr = mx_rot[0][0] * x + mx_rot[1][0] * y
        ytr = mx_rot[0][1] * x + mx_rot[1][1] * y

        # process shift
        sh_rot = Transformer.XYC[rot]
        xtr += sh_rot[0] * boxsize
        ytr += sh_rot[1] * boxsize

        return [xtr, ytr]
