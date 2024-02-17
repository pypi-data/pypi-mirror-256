from dynamiks.utils.test_utils import DefaultDWMFlowSimulation, tfp, npt
from dynamiks.views import XYView, XZView, YZView, EastNorthView, Points
import matplotlib.pyplot as plt
import numpy as np
import matplotlib
from io import BytesIO


def test_views():

    for wd in [270, 300, 0]:
        x_lst = np.linspace(-200, 500, 20)
        y_lst = np.linspace(-200, 500, 20)
        z_lst = np.linspace(0, 200, 20)
        view_lst = [XYView(z=70, x=x_lst, y=y_lst),
                    XZView(y=0, x=x_lst, z=z_lst),
                    YZView(x=100, y=y_lst, z=z_lst),
                    EastNorthView(h=70, east=x_lst, north=y_lst)]
        fs = DefaultDWMFlowSimulation(x=[200, 0], y=[0, 100], wd=wd, site='uniform')
        fs.run(10)

        axes = plt.subplots(2, 2)[1].flatten()
        for view, ax in zip(view_lst, axes):
            view.ax = ax
            fs.visualize(fs.time + 1, dt=1, view=view)
            ax.set_title(view.__class__.__name__)

        plt.suptitle(f'{wd}deg')

        if 0:
            # check result (installation dependent, fails on test machine)
            # save ref fig
            # plt.savefig(tfp + f"ref_figs/test_views_{wd}deg.png")
            bio = BytesIO()
            plt.savefig(bio, format='png')
            bio.seek(0)
            img = plt.imread(bio)

            ref = plt.imread(tfp + f"ref_figs/test_views_{wd}deg.png")
            try:
                npt.assert_array_equal(img, ref)

            except BaseException:
                plt.figure()
                plt.imshow(ref)
                plt.title('ref')
                plt.figure()
                plt.imshow((ref - img)[:, :, :3])
                plt.title('diff')
                # plt.show()
                raise

    if 0:
        plt.show()
    plt.close('all')


# def test_points_shape():
#     p = Points(x=[1, 2, 3], y=[0, 0, 0], z=[70, 70, 70])
#     assert p.shape == (3,)
